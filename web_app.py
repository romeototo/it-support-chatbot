#!/usr/bin/env python3
"""
IT Support Chatbot - Modern Web UI
Backend for RAG-based IT Support Chatbot
"""

import os
from flask import Flask, request, jsonify, send_file
from chatbot import load_kb, get_response

app = Flask(__name__)

# Load Knowledge Base
kb = load_kb()

@app.route("/")
def index():
    """Serve the main UI page."""
    try:
        return send_file("index.html")
    except Exception as e:
        return f"Error loading index.html: {str(e)}", 500

@app.route("/dashboard")
def dashboard():
    """Serve the Admin Dashboard page."""
    try:
        return send_file("dashboard.html")
    except Exception as e:
        return f"Error loading dashboard.html: {str(e)}", 500

@app.route("/static/kb.js")
def serve_kb():
    """Serve the KB data as a JS file."""
    try:
        return send_file("kb.js", mimetype='application/javascript')
    except Exception as e:
        return f"Error loading kb.js: {str(e)}", 404

@app.route("/api/chat", methods=["POST"])
def chat():
    """RAG Chat API."""
    data = request.json
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "กรุณาพิมพ์คำถาม"})
    
    # Process with RAG logic from chatbot.py
    response, engine_name = get_response(user_input, kb)
    return jsonify({"response": response, "engine": engine_name})

# -------------------------------------------------------------
# Admin Ticket Management API (For Full-Stack Production Mode)
# -------------------------------------------------------------
tickets_db = []

@app.route("/api/tickets", methods=["GET"])
def get_tickets():
    """Fetch all tickets for dashboard."""
    return jsonify(tickets_db)

@app.route("/api/tickets/new", methods=["POST"])
def new_ticket():
    """Create a new ticket from user UI."""
    data = request.json
    # Logic to save to tickets_db / SQLite goes here
    return jsonify({"status": "success", "ticket": data})

@app.route("/api/tickets/reply", methods=["POST"])
def reply_ticket():
    """Admin replies to a ticket."""
    data = request.json
    # Logic to update ticket and notify user goes here
    return jsonify({"status": "success"})

@app.route("/api/health")
def health():
    """Check system status."""
    return jsonify({
        "status": "ok", 
        "faqs_count": sum(len(c["faqs"]) for c in kb["categories"]),
        "categories_count": len(kb["categories"])
    })

if __name__ == "__main__":
    print("------------------------------------------")
    print("Starting IT Support Chatbot Premium UI...")
    print("URL: http://localhost:5000")
    print("------------------------------------------")
    app.run(host="0.0.0.0", port=5000, debug=True)

