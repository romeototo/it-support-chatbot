#!/usr/bin/env python3
"""
IT Support Chatbot - Enhanced Web App
Backend with SQLite ticket persistence, admin auth, and conversation memory
"""

import os
import json
import sqlite3
import hashlib
import hmac
import secrets
import time
import logging
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import wraps
from flask import (
    Flask, request, jsonify, send_file,
    session, redirect, url_for, abort
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from chatbot import load_kb, get_response, conversation_history

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# ============================================================
# APP CONFIG
# ============================================================
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)

# Session cookie security
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'

# Rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per minute"],
    storage_uri="memory://"
)

# Admin credentials: read from config.json or ENV vars
_config_path = os.path.join(os.path.dirname(__file__), "config.json")
_config = {}
if os.path.exists(_config_path):
    with open(_config_path, "r") as _f:
        _config = json.load(_f)

ADMIN_USER = os.getenv("ADMIN_USER") or _config.get("admin_user", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS") or _config.get("admin_pass", "changeme")

if ADMIN_PASS == "changeme":
    logger.warning("Using default password! Set ADMIN_PASS env var or update config.json")

DB_PATH = os.path.join(os.path.dirname(__file__), "tickets.db")

# Load Knowledge Base
kb = load_kb()

# ============================================================
# DATABASE SETUP
# ============================================================
@contextmanager
def get_db():
    """Get database connection with row_factory as context manager."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database tables."""
    with get_db() as conn:
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
@limiter.limit("10 per minute")
def admin_login():
    """Admin login endpoint."""
    data = request.json or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if hmac.compare_digest(username, ADMIN_USER) and hmac.compare_digest(password, ADMIN_PASS):
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
@limiter.limit("30 per minute")
def chat():
    """RAG Chat API with session tracking."""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    user_input = data.get("message", "").strip()
    session_id = data.get("session_id", request.remote_addr)

    if not user_input:
        return jsonify({"response": "กรุณาพิมพ์คำถาม"})

    if len(user_input) > 2000:
        return jsonify({"error": "Message too long"}), 400

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
    try:
        limit = int(request.args.get("limit", 50))
        offset = int(request.args.get("offset", 0))
    except (ValueError, TypeError):
        limit, offset = 50, 0

    with get_db() as conn:
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

    tickets = [dict(row) for row in rows]
    return jsonify({"tickets": tickets, "total": total})

@app.route("/api/tickets/new", methods=["POST"])
@limiter.limit("20 per minute")
def new_ticket():
    """Create a new support ticket."""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    if len(data.get("message", "")) > 5000:
        return jsonify({"error": "Message too long"}), 400

    ticket_id = generate_ticket_id()

    with get_db() as conn:
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

    return jsonify({
        "status": "success",
        "ticket_id": ticket_id,
        "message": f"สร้าง ticket {ticket_id} เรียบร้อยแล้ว"
    })

@app.route("/api/tickets/<ticket_id>", methods=["GET"])
@admin_required
def get_ticket(ticket_id):
    """Get single ticket with messages."""
    with get_db() as conn:
        ticket = conn.execute(
            "SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)
        ).fetchone()

        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404

        messages = conn.execute(
            "SELECT * FROM ticket_messages WHERE ticket_id = ? ORDER BY created_at",
            (ticket_id,)
        ).fetchall()

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

    with get_db() as conn:
        ticket = conn.execute("SELECT 1 FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404

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

    return jsonify({"status": "success", "message": "ตอบกลับเรียบร้อยแล้ว"})

@app.route("/api/tickets/<ticket_id>/close", methods=["POST"])
@admin_required
def close_ticket(ticket_id):
    """Close a ticket."""
    with get_db() as conn:
        ticket = conn.execute("SELECT 1 FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404

        conn.execute("""
            UPDATE tickets
            SET status = 'closed', closed_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE ticket_id = ?
        """, (ticket_id,))
        conn.commit()
    return jsonify({"status": "success"})

@app.route("/api/tickets/<ticket_id>/reopen", methods=["POST"])
@admin_required
def reopen_ticket(ticket_id):
    """Reopen a closed ticket."""
    with get_db() as conn:
        ticket = conn.execute("SELECT 1 FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404

        conn.execute("""
            UPDATE tickets
            SET status = 'open', closed_at = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE ticket_id = ?
        """, (ticket_id,))
        conn.commit()
    return jsonify({"status": "success"})

# ============================================================
# ANALYTICS API
# ============================================================
@app.route("/api/analytics")
@admin_required
def analytics():
    """Get ticket analytics for dashboard charts."""
    with get_db() as conn:
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
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    rating = data.get("rating")
    if rating is not None:
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({"error": "Rating must be 1-5"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid rating"}), 400

    with get_db() as conn:
        conn.execute("""
            INSERT INTO feedback (ticket_id, rating, comment)
            VALUES (?, ?, ?)
        """, (data.get("ticket_id"), rating, data.get("comment")))
        conn.commit()
    return jsonify({"status": "success"})

# ============================================================
# HEALTH CHECK
# ============================================================
@app.route("/api/health")
def health():
    """System health check."""
    with get_db() as conn:
        ticket_count = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    faq_count = sum(len(c["faqs"]) for c in kb["categories"])

    return jsonify({
        "status": "ok",
        "faqs_count": faq_count,
        "categories_count": len(kb["categories"]),
        "tickets_counts": ticket_count,
        "db_available": os.path.exists(DB_PATH),
        "llm_enabled": bool(os.getenv("GOOGLE_API_KEY")),
        "version": "2.1.0"
    })

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    logger.info("------------------------------------------")
    logger.info("  IT Support Chatbot - Enhanced Edition")
    logger.info("  URL: http://localhost:5000")
    logger.info("  Admin: http://localhost:5000/dashboard")
    logger.info("  DB: %s", DB_PATH)
    logger.info("------------------------------------------")
    app.run(host="0.0.0.0", port=5000, debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
