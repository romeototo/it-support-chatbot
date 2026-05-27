#!/usr/bin/env python3
"""
IT Support Chatbot - Enhanced Web App
Backend with SQLite ticket persistence, admin auth, and conversation memory
"""

import os
import json
import sqlite3
import hashlib
import secrets
import time
from datetime import datetime, timezone
from functools import wraps
from flask import (
    Flask, request, jsonify, send_file,
    session, redirect, url_for, abort
)
from chatbot import load_kb, get_response, conversation_history

# ============================================================
# APP CONFIG
# ============================================================
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)

# Admin credentials: read from config.json or ENV vars
import json as _json
_config_path = os.path.join(os.path.dirname(__file__), "config.json")
_config = {}
if os.path.exists(_config_path):
    with open(_config_path, "r") as _f:
        _config = _json.load(_f)

ADMIN_USER = os.getenv("ADMIN_USER") or _config.get("admin_user", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS") or _config.get("admin_pass", "changeme")

if ADMIN_PASS == "changeme":
    print("[WARNING] Using default password! Set ADMIN_PASS env var or update config.json")

DB_PATH = os.path.join(os.path.dirname(__file__), "tickets.db")

# Load Knowledge Base
kb = load_kb()

# ============================================================
# DATABASE SETUP
# ============================================================
def get_db():
    """Get database connection with row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    """Initialize database tables."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            user_name TEXT DEFAULT 'Anonymous',
            user_message TEXT NOT NULL,
            bot_response TEXT,
            category TEXT DEFAULT 'General',
            status TEXT DEFAULT 'open',
            priority TEXT DEFAULT 'normal',
            admin_reply TEXT,
            admin_user TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            closed_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS ticket_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT,
            rating INTEGER,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
        CREATE INDEX IF NOT EXISTS idx_tickets_created ON tickets(created_at);
        CREATE INDEX IF NOT EXISTS idx_messages_ticket ON ticket_messages(ticket_id);
    """)
    conn.commit()
    conn.close()

def generate_ticket_id():
    """Generate unique ticket ID like TKT-20260527-A1B2."""
    now = datetime.now()
    rand = secrets.token_hex(2).upper()
    return f"TKT-{now.strftime('%Y%m%d')}-{rand}"

# Initialize DB on startup
init_db()

# ============================================================
# AUTH MIDDLEWARE
# ============================================================
def admin_required(f):
    """Decorator to require admin login."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            if request.is_json:
                return jsonify({"error": "Unauthorized"}), 401
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

# ============================================================
# PUBLIC ROUTES
# ============================================================
@app.route("/")
def index():
    """Serve the main chatbot UI."""
    return send_file("index.html")

@app.route("/dashboard")
@admin_required
def dashboard():
    """Serve admin dashboard (requires login)."""
    return send_file("dashboard.html")

@app.route("/static/kb.js")
def serve_kb():
    """Serve the KB data as a JS file."""
    return send_file("kb.js", mimetype="application/javascript")

@app.route("/sw.js")
def serve_sw():
    """Service worker must be at root."""
    return send_file("sw.js", mimetype="application/javascript")

# ============================================================
# ADMIN AUTH ROUTES
# ============================================================
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    """Admin login endpoint."""
    data = request.json or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if username == ADMIN_USER and password == ADMIN_PASS:
        session["admin_logged_in"] = True
        session["admin_user"] = username
        return jsonify({"status": "ok", "message": "เข้าสู่ระบบสำเร็จ"})
    return jsonify({"status": "error", "message": "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"}), 401

@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    """Admin logout."""
    session.clear()
    return jsonify({"status": "ok"})

@app.route("/api/admin/status")
def admin_status():
    """Check if admin is logged in."""
    return jsonify({"logged_in": session.get("admin_logged_in", False)})

# ============================================================
# CHAT API
# ============================================================
@app.route("/api/chat", methods=["POST"])
def chat():
    """RAG Chat API with session tracking."""
    data = request.json
    user_input = data.get("message", "").strip()
    session_id = data.get("session_id", request.remote_addr)

    if not user_input:
        return jsonify({"response": "กรุณาพิมพ์คำถาม"})

    response, engine_name = get_response(user_input, kb, session_id)
    return jsonify({
        "response": response,
        "engine": engine_name,
        "session_id": session_id
    })

# ============================================================
# TICKET API (SQLite-backed)
# ============================================================
@app.route("/api/tickets", methods=["GET"])
@admin_required
def get_tickets():
    """Fetch all tickets with optional filters."""
    status = request.args.get("status")
    search = request.args.get("search", "").strip()
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))

    conn = get_db()
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if status and status != "all":
        query += " AND status = ?"
        params.append(status)

    if search:
        query += " AND (ticket_id LIKE ? OR user_message LIKE ? OR user_name LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term, search_term])

    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(query, params).fetchall()
    total = conn.execute(
        "SELECT COUNT(*) FROM tickets WHERE 1=1" +
        (" AND status = ?" if status and status != "all" else "") +
        (" AND (ticket_id LIKE ? OR user_message LIKE ? OR user_name LIKE ?)" if search else ""),
        [p for p in params if p not in [limit, offset]]
    ).fetchone()[0]

    conn.close()

    tickets = [dict(row) for row in rows]
    return jsonify({"tickets": tickets, "total": total})

@app.route("/api/tickets/new", methods=["POST"])
def new_ticket():
    """Create a new support ticket."""
    data = request.json
    ticket_id = generate_ticket_id()

    conn = get_db()
    conn.execute("""
        INSERT INTO tickets (ticket_id, user_name, user_message, bot_response, category, status)
        VALUES (?, ?, ?, ?, ?, 'open')
    """, (
        ticket_id,
        data.get("user_name", "Anonymous"),
        data.get("message", ""),
        data.get("bot_response", ""),
        data.get("category", "General")
    ))

    # Also add first message to thread
    conn.execute("""
        INSERT INTO ticket_messages (ticket_id, sender, message)
        VALUES (?, 'user', ?)
    """, (ticket_id, data.get("message", "")))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "ticket_id": ticket_id,
        "message": f"สร้าง ticket {ticket_id} เรียบร้อยแล้ว"
    })

@app.route("/api/tickets/<ticket_id>", methods=["GET"])
@admin_required
def get_ticket(ticket_id):
    """Get single ticket with messages."""
    conn = get_db()
    ticket = conn.execute(
        "SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)
    ).fetchone()

    if not ticket:
        conn.close()
        return jsonify({"error": "Ticket not found"}), 404

    messages = conn.execute(
        "SELECT * FROM ticket_messages WHERE ticket_id = ? ORDER BY created_at",
        (ticket_id,)
    ).fetchall()

    conn.close()

    return jsonify({
        "ticket": dict(ticket),
        "messages": [dict(m) for m in messages]
    })

@app.route("/api/tickets/<ticket_id>/reply", methods=["POST"])
@admin_required
def reply_ticket(ticket_id):
    """Admin replies to a ticket."""
    data = request.json
    reply_text = data.get("reply", "").strip()
    admin_user = session.get("admin_user", "admin")

    if not reply_text:
        return jsonify({"error": "Reply cannot be empty"}), 400

    conn = get_db()

    # Update ticket
    conn.execute("""
        UPDATE tickets
        SET admin_reply = ?, admin_user = ?, status = 'replied',
            updated_at = CURRENT_TIMESTAMP
        WHERE ticket_id = ?
    """, (reply_text, admin_user, ticket_id))

    # Add message to thread
    conn.execute("""
        INSERT INTO ticket_messages (ticket_id, sender, message)
        VALUES (?, 'admin', ?)
    """, (ticket_id, reply_text))

    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "ตอบกลับเรียบร้อยแล้ว"})

@app.route("/api/tickets/<ticket_id>/close", methods=["POST"])
@admin_required
def close_ticket(ticket_id):
    """Close a ticket."""
    conn = get_db()
    conn.execute("""
        UPDATE tickets
        SET status = 'closed', closed_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE ticket_id = ?
    """, (ticket_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/api/tickets/<ticket_id>/reopen", methods=["POST"])
@admin_required
def reopen_ticket(ticket_id):
    """Reopen a closed ticket."""
    conn = get_db()
    conn.execute("""
        UPDATE tickets
        SET status = 'open', closed_at = NULL,
            updated_at = CURRENT_TIMESTAMP
        WHERE ticket_id = ?
    """, (ticket_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# ============================================================
# ANALYTICS API
# ============================================================
@app.route("/api/analytics")
@admin_required
def analytics():
    """Get ticket analytics for dashboard charts."""
    conn = get_db()

    # Status counts
    status_counts = {}
    for row in conn.execute("SELECT status, COUNT(*) as cnt FROM tickets GROUP BY status"):
        status_counts[row["status"]] = row["cnt"]

    # Category distribution
    category_counts = {}
    for row in conn.execute("SELECT category, COUNT(*) as cnt FROM tickets GROUP BY category ORDER BY cnt DESC"):
        category_counts[row["category"]] = row["cnt"]

    # Daily ticket count (last 7 days)
    daily = conn.execute("""
        SELECT DATE(created_at) as day, COUNT(*) as cnt
        FROM tickets
        WHERE created_at >= datetime('now', '-7 days')
        GROUP BY DATE(created_at)
        ORDER BY day
    """).fetchall()

    # Response rate
    total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    replied = conn.execute("SELECT COUNT(*) FROM tickets WHERE admin_reply IS NOT NULL").fetchone()[0]
    response_rate = (replied / total * 100) if total > 0 else 0

    conn.close()

    return jsonify({
        "status_counts": status_counts,
        "category_counts": category_counts,
        "daily_tickets": [dict(d) for d in daily],
        "response_rate": round(response_rate, 1),
        "total_tickets": total
    })

@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    """Submit user feedback."""
    data = request.json
    conn = get_db()
    conn.execute("""
        INSERT INTO feedback (ticket_id, rating, comment)
        VALUES (?, ?, ?)
    """, (data.get("ticket_id"), data.get("rating"), data.get("comment")))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# ============================================================
# HEALTH CHECK
# ============================================================
@app.route("/api/health")
def health():
    """System health check."""
    conn = get_db()
    ticket_count = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    faq_count = sum(len(c["faqs"]) for c in kb["categories"])
    conn.close()

    return jsonify({
        "status": "ok",
        "faqs_count": faq_count,
        "categories_count": len(kb["categories"]),
        "tickets_count": ticket_count,
        "db_path": DB_PATH,
        "llm_enabled": bool(os.getenv("GOOGLE_API_KEY")),
        "version": "2.0.0"
    })

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("------------------------------------------")
    print("  IT Support Chatbot - Enhanced Edition")
    print("  URL: http://localhost:5000")
    print("  Admin: http://localhost:5000/dashboard")
    print(f"  DB: {DB_PATH}")
    print("------------------------------------------")
    app.run(host="0.0.0.0", port=5000, debug=True)
