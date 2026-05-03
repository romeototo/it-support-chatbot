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

