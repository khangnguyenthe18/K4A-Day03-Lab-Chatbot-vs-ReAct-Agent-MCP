"""
🌐 WEB DEMO UI - DAY 03: GYM WORKOUT REACT AGENT (MCP ENHANCED)
Giao diện chuyên nghiệp phong cách Thể hình / Muscle & Strength, tích hợp bộ phân giải Markdown
loại bỏ các ký tự thô (###, ***) và hiển thị Trace Log ReAct trực quan.
"""

import os
import sys
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_server import MCPAcademicServer
from providers import get_llm_provider
from app import run_react_agent, load_test_cases

PORT = 8080
mcp_server = MCPAcademicServer()
provider = get_llm_provider()

HTML_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VinLAB Fitness - Gym Workout ReAct Agent</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <!-- Markdown parser library -->
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    :root {
      --primary-blue: #0d529b;
      --primary-blue-dark: #083c74;
      --primary-blue-light: #1e6ec2;
      --accent-orange: #f97316;
      --accent-orange-hover: #ea580c;
      --accent-cyan: #06b6d4;
      --accent-green: #10b981;
      --accent-purple: #a855f7;
      --dark-bg: #090d16;
      --card-bg: #111726;
      --card-inner: #161e31;
      --card-border: #1e293b;
      --text-main: #f8fafc;
      --text-sub: #94a3b8;
      --text-muted: #64748b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--dark-bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* TOP ANNOUNCEMENT BAR (STYLE MUSCLE & STRENGTH) */
    .announcement-bar {
      background: #000;
      color: #fff;
      padding: 0.45rem 1.5rem;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #222;
    }
    .announcement-tag {
      background: var(--accent-orange);
      color: #000;
      padding: 0.15rem 0.6rem;
      border-radius: 4px;
      font-weight: 900;
      margin-right: 0.6rem;
      text-transform: uppercase;
      font-size: 0.7rem;
    }
    .announcement-btn {
      background: var(--accent-orange);
      color: #fff;
      padding: 0.25rem 0.85rem;
      border-radius: 4px;
      text-decoration: none;
      font-weight: 800;
      font-size: 0.72rem;
      transition: background 0.2s;
    }
    .announcement-btn:hover { background: var(--accent-orange-hover); }

    /* ATHLETIC MAIN NAVIGATION */
    header {
      background: linear-gradient(180deg, var(--primary-blue), var(--primary-blue-dark));
      border-bottom: 2px solid #06315e;
      box-shadow: 0 4px 20px rgba(0,0,0,0.4);
      position: sticky;
      top: 0;
      z-index: 50;
    }
    .header-content {
      max-width: 1500px;
      margin: 0 auto;
      padding: 0.85rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 0.85rem;
      text-decoration: none;
      color: inherit;
    }
    .brand-badge {
      background: #fff;
      color: var(--primary-blue);
      font-size: 1.5rem;
      font-weight: 900;
      font-style: italic;
      padding: 0.2rem 0.6rem;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .brand-text h1 {
      font-size: 1.25rem;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: -0.5px;
      color: #fff;
      line-height: 1.1;
    }
    .brand-text p {
      font-size: 0.72rem;
      color: #cbd5e1;
      font-weight: 500;
    }

    .nav-tabs {
      display: flex;
      gap: 0.4rem;
      background: rgba(0,0,0,0.25);
      padding: 0.3rem;
      border-radius: 8px;
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: #cbd5e1;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.82rem;
      cursor: pointer;
      transition: all 0.2s;
    }
    .tab-btn.active, .tab-btn:hover {
      background: #fff;
      color: var(--primary-blue-dark);
      box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    }
    .tab-btn.active { font-weight: 800; }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .toggle-trace-btn {
      background: rgba(0,0,0,0.3);
      border: 1px solid rgba(255,255,255,0.25);
      color: #fff;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
    }
    .toggle-trace-btn:hover {
      background: #fff;
      color: var(--primary-blue-dark);
      border-color: #fff;
    }

    /* HERO STATS BAR (LIKE REFERENCE IMAGE) */
    .stats-bar {
      background: #0f1523;
      border-bottom: 1px solid var(--card-border);
      padding: 0.75rem 1.5rem;
    }
    .stats-container {
      max-width: 1500px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      text-align: center;
    }
    .stat-item {
      padding: 0.3rem 0;
      border-right: 1px solid rgba(255,255,255,0.06);
    }
    .stat-item:last-child { border-right: none; }
    .stat-num {
      font-size: 1.35rem;
      font-weight: 900;
      color: #fff;
      letter-spacing: -0.5px;
    }
    .stat-label {
      font-size: 0.72rem;
      color: var(--text-sub);
      text-transform: uppercase;
      font-weight: 600;
      margin-top: 0.15rem;
    }

    /* MAIN CONTAINER */
    .container {
      max-width: 1500px;
      margin: 0 auto;
      padding: 1.25rem 1.5rem;
      flex: 1;
      width: 100%;
    }
    .tab-content { display: none; }
    .tab-content.active { display: block; }

    /* WORKOUT PRE-MADE CHIPS (CATEGORY BUTTONS) */
    .quick-prompts-bar {
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      overflow-x: auto;
      padding-bottom: 0.3rem;
    }
    .quick-title {
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      white-space: nowrap;
      margin-right: 0.3rem;
    }
    .quick-chip {
      background: var(--card-inner);
      border: 1px solid var(--card-border);
      color: #cbd5e1;
      padding: 0.4rem 0.85rem;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s;
    }
    .quick-chip:hover {
      background: var(--primary-blue);
      color: #fff;
      border-color: var(--primary-blue-light);
      transform: translateY(-1px);
    }

    /* SPLIT GRID LAYOUT */
    .demo-grid {
      display: grid;
      grid-template-columns: 1fr 1.05fr;
      gap: 1.25rem;
      height: calc(100vh - 250px);
      transition: all 0.3s ease;
    }
    .demo-grid.hide-trace {
      grid-template-columns: 1fr;
    }
    .demo-grid.hide-trace #trace-panel {
      display: none !important;
    }

    /* CARDS */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    .card-header {
      padding: 0.85rem 1.25rem;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(255,255,255,0.02);
    }
    .card-title {
      font-size: 0.92rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      letter-spacing: -0.3px;
    }
    .status-badge {
      font-size: 0.72rem;
      padding: 0.25rem 0.65rem;
      border-radius: 20px;
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent-green);
      font-weight: 700;
      border: 1px solid rgba(16, 185, 129, 0.3);
      display: flex;
      align-items: center;
      gap: 0.3rem;
    }

    /* CHAT BOX */
    .chat-messages {
      flex: 1;
      padding: 1.25rem;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
    }
    .msg {
      max-width: 90%;
      padding: 1rem 1.25rem;
      border-radius: 12px;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .msg-user {
      align-self: flex-end;
      background: linear-gradient(135deg, var(--primary-blue), var(--primary-blue-light));
      color: #fff;
      border-bottom-right-radius: 2px;
      box-shadow: 0 4px 15px rgba(13, 82, 155, 0.3);
    }
    .msg-agent {
      align-self: flex-start;
      background: var(--card-inner);
      border: 1px solid #283548;
      color: #e2e8f0;
      border-bottom-left-radius: 2px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }
    .msg-author {
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      letter-spacing: 0.5px;
    }
    .msg-user .msg-author { color: #bae6fd; }
    .msg-agent .msg-author { color: var(--accent-cyan); }

    /* CLEAN FORMATTED MARKDOWN IN AGENT CHAT */
    .md-content h2, .md-content h3, .md-content h4 {
      color: #fff;
      font-weight: 800;
      margin: 0.8rem 0 0.4rem 0;
      line-height: 1.3;
    }
    .md-content h2 { font-size: 1.1rem; border-bottom: 1px solid #2d3b52; padding-bottom: 0.3rem; }
    .md-content h3 { font-size: 1rem; color: #38bdf8; }
    .md-content h4 { font-size: 0.92rem; color: #bae6fd; }
    .md-content strong { color: #fff; font-weight: 700; }
    .md-content em { color: #fcd34d; }
    .md-content ul, .md-content ol {
      margin: 0.5rem 0 0.5rem 1.4rem;
    }
    .md-content li {
      margin-bottom: 0.35rem;
      line-height: 1.5;
    }
    .md-content p {
      margin-bottom: 0.5rem;
    }
    .md-content hr {
      border: 0;
      height: 1px;
      background: #2d3b52;
      margin: 0.8rem 0;
    }

    /* MARKDOWN TABLES (FORMATTED CRISP & BEAUTIFUL) */
    .md-content table {
      width: 100%;
      border-collapse: collapse;
      margin: 0.75rem 0;
      font-size: 0.82rem;
      background: #090e18;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid #223049;
    }
    .md-content th {
      background: #152033;
      color: #38bdf8;
      font-weight: 700;
      padding: 0.55rem 0.85rem;
      text-align: left;
      border-bottom: 1px solid #223049;
    }
    .md-content td {
      padding: 0.55rem 0.85rem;
      border-bottom: 1px solid #1a263a;
      color: #cbd5e1;
    }
    .md-content tr:last-child td { border-bottom: none; }
    .md-content tr:hover { background: rgba(255,255,255,0.02); }

    /* CHAT INPUT */
    .chat-input-area {
      padding: 1rem 1.25rem;
      border-top: 1px solid var(--card-border);
      background: rgba(0,0,0,0.3);
      display: flex;
      gap: 0.75rem;
    }
    .chat-input {
      flex: 1;
      background: #090e18;
      border: 1px solid #283548;
      color: #fff;
      padding: 0.85rem 1.25rem;
      border-radius: 10px;
      font-family: inherit;
      font-size: 0.9rem;
      outline: none;
      transition: all 0.2s;
    }
    .chat-input:focus {
      border-color: var(--primary-blue-light);
      box-shadow: 0 0 0 3px rgba(30, 110, 194, 0.2);
    }
    .send-btn {
      background: linear-gradient(135deg, var(--accent-orange), var(--accent-orange-hover));
      color: white;
      border: none;
      padding: 0 1.6rem;
      border-radius: 10px;
      font-weight: 800;
      font-size: 0.88rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: transform 0.15s, box-shadow 0.15s;
    }
    .send-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 15px rgba(249, 115, 22, 0.4);
    }
    .send-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

    /* WATERFALL TRACE LOG VIEW */
    .trace-container {
      flex: 1;
      padding: 1.25rem;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      background: #090d16;
      font-family: 'JetBrains Mono', monospace;
    }
    .trace-card {
      background: #111827;
      border-left: 4px solid #4b5563;
      border-radius: 8px;
      padding: 0.85rem;
      font-size: 0.8rem;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .trace-card.thought { border-left-color: var(--accent-purple); }
    .trace-card.action { border-left-color: var(--accent-cyan); }
    .trace-card.observation { border-left-color: var(--accent-orange); }
    .trace-card.final { border-left-color: var(--accent-green); }

    .trace-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.45rem;
    }
    .trace-tag {
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .trace-card.thought .trace-tag { color: var(--accent-purple); }
    .trace-card.action .trace-tag { color: var(--accent-cyan); }
    .trace-card.observation .trace-tag { color: var(--accent-orange); }
    .trace-card.final .trace-tag { color: var(--accent-green); }

    .trace-latency { font-size: 0.72rem; color: var(--text-muted); font-weight: 600; }
    .trace-body { color: #cbd5e1; line-height: 1.45; word-break: break-word; }
    .trace-json {
      background: #060911;
      border: 1px solid #1c2738;
      padding: 0.6rem;
      border-radius: 6px;
      margin-top: 0.45rem;
      color: #38bdf8;
      font-size: 0.75rem;
      overflow-x: auto;
    }

    /* SLIDE PRESENTATION STYLES */
    .slide-section {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 2rem;
      margin-bottom: 1.5rem;
    }
    .slide-header {
      display: flex;
      align-items: center;
      gap: 0.85rem;
      margin-bottom: 1.25rem;
    }
    .slide-num {
      background: var(--primary-blue);
      color: #fff;
      font-weight: 900;
      width: 36px;
      height: 36px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
    }
    .slide-title { font-size: 1.35rem; font-weight: 800; color: #fff; }
    .slide-text { color: var(--text-sub); line-height: 1.7; margin-bottom: 1rem; font-size: 0.95rem; }

    /* MATRIX TABLE */
    .matrix-table {
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-size: 0.9rem;
    }
    .matrix-table th, .matrix-table td {
      padding: 0.9rem 1.1rem;
      text-align: left;
      border-bottom: 1px solid var(--card-border);
    }
    .matrix-table th { background: #152033; color: #fff; font-weight: 800; }
    .matrix-table tr:hover { background: rgba(255,255,255,0.02); }
    .score-badge {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      background: rgba(6, 182, 212, 0.15);
      color: var(--accent-cyan);
      border-radius: 6px;
      font-weight: 800;
    }

    /* ARCHITECTURE DIAGRAM BOX */
    .diagram-box {
      background: #060911;
      border: 1px solid #1c2738;
      border-radius: 12px;
      padding: 1.75rem;
      margin: 1.25rem 0;
    }
    .arch-flow {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .arch-node {
      background: #141b2a;
      border: 1px solid #283548;
      padding: 1.1rem;
      border-radius: 10px;
      text-align: center;
      flex: 1;
      min-width: 180px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .arch-node.agent { border-color: var(--primary-blue-light); background: rgba(13, 82, 155, 0.15); }
    .arch-node.mcp { border-color: var(--accent-orange); background: rgba(249, 115, 22, 0.12); }
    .arch-arrow { color: var(--accent-cyan); font-size: 1.3rem; font-weight: 900; }
  </style>
</head>
<body>

  <!-- TOP BANNER -->
  <div class="announcement-bar">
    <div>
      <span class="announcement-tag">HOT DEMO</span>
      VINUNI AI COURSE • DAY 03: REACTION AGENT + MODEL CONTEXT PROTOCOL (MCP)
    </div>
    <div>
      <span style="color:#94a3b8; margin-right:1rem;">Học viên: <b>Nguyễn Thế Khang</b> (2A202602964)</span>
      <a href="#slides" class="announcement-btn" onclick="switchTab('slides')">XEM BÁO CÁO 18/20</a>
    </div>
  </div>

  <!-- ATHLETIC HEADER -->
  <header>
    <div class="header-content">
      <a href="#" class="brand" onclick="switchTab('demo')">
        <div class="brand-badge">M&amp;S</div>
        <div class="brand-text">
          <h1>VINLAB FITNESS</h1>
          <p>ReAct Agent Workout Routine &amp; Training Planner</p>
        </div>
      </a>

      <div class="nav-tabs">
        <button class="tab-btn active" id="btn-tab-demo" onclick="switchTab('demo')">🏋️ Live Workout AI</button>
        <button class="tab-btn" id="btn-tab-slides" onclick="switchTab('slides')">📊 5 Câu Hỏi Trình Bày</button>
        <button class="tab-btn" id="btn-tab-architecture" onclick="switchTab('architecture')">🏛️ Workflow Kiến Trúc</button>
      </div>

      <div class="header-actions">
        <button id="toggle-trace-btn" class="toggle-trace-btn" onclick="toggleTracePanel()" title="Thu gọn / Mở rộng bảng Trace Log">
          <span>📊 Ẩn Trace Log</span>
        </button>
      </div>
    </div>
  </header>

  <!-- METRIC STATS BAR (LIKE REFERENCE IMAGE) -->
  <div class="stats-bar">
    <div class="stats-container">
      <div class="stat-item">
        <div class="stat-num">1000+</div>
        <div class="stat-label">Bài Tập Đa Dạng</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">100%</div>
        <div class="stat-label">Native Tool Calling</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">JSON-RPC 2.0</div>
        <div class="stat-label">Giao Thức MCP Server</div>
      </div>
      <div class="stat-item">
        <div class="stat-num" style="color: var(--accent-cyan);">18 / 20</div>
        <div class="stat-label">Agentic Fit Score</div>
      </div>
    </div>
  </div>

  <!-- MAIN VIEW -->
  <div class="container">
    
    <!-- TAB 1: WORKOUT AGENT CHAT & TRACE -->
    <div id="tab-demo" class="tab-content active">
      
      <!-- QUICK WORKOUT CATEGORY CHIPS -->
      <div class="quick-prompts-bar">
        <span class="quick-title">Gợi ý nhanh:</span>
        <button class="quick-chip" onclick="sendQuickPrompt('Chào bạn, giải thích giúp mình bài tập Compound khác gì Isolation?')">
          🏋️ TC01: Compound vs Isolation
        </button>
        <button class="quick-chip" onclick="sendQuickPrompt('Hãy tra cứu hồ sơ thể trạng và mục tiêu tập luyện của hội viên GYM001.')">
          🔍 TC02: Hồ sơ GYM001
        </button>
        <button class="quick-chip" onclick="sendQuickPrompt('Hãy tạo lịch tập 4 buổi/tuần theo phương pháp Push-Pull-Legs cho hội viên GYM001 với mục tiêu tăng cơ.')">
          📅 TC03: Lịch Push-Pull-Legs
        </button>
        <button class="quick-chip" onclick="sendQuickPrompt('Hội viên GYM002 muốn lên lịch tập phù hợp với thể trạng hiện tại và chấn thương nếu có. Bạn hãy kiểm tra hồ sơ trước rồi tạo chương trình tập luyện an toàn nhất.')">
          ⚠️ TC04: Chấn thương GYM002 (An toàn)
        </button>
        <button class="quick-chip" onclick="sendQuickPrompt('Hãy tra cứu thông tin hồ sơ thể trạng của hội viên có mã GYM999.')">
          🚫 TC05: Mã hội viên không tồn tại
        </button>
      </div>

      <!-- SPLIT DEMO GRID -->
      <div class="demo-grid">
        
        <!-- CỘT TRÁI: KHUNG CHAT TƯƠNG TÁC -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">
              <span>🤖 Trợ Lý Lên Lịch Tập ReAct Agent</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span class="status-badge" id="agent-provider">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--accent-green);"></span>
                Gemini 3.6 Flash Active
              </span>
            </div>
          </div>

          <div class="chat-messages" id="chat-box">
            <div class="msg msg-agent">
              <div class="msg-author">🤖 VINLAB GYM ASSISTANT</div>
              <div class="md-content">
                <p>Chào mừng bạn đến với <strong>VinLAB Fitness Agent</strong>! Tôi là trợ lý AI được tích hợp công cụ qua chuẩn <strong>Model Context Protocol (MCP)</strong>.</p>
                <p>Tôi có thể:</p>
                <ul>
                  <li>Tra cứu hồ sơ thể hình, kinh nghiệm và tiền sử chấn thương của hội viên.</li>
                  <li>Tự động điều chỉnh bài tập an toàn (loại bỏ bài tập rủi ro khi có đau khớp, chấn thương).</li>
                  <li>Thiết lập và lưu chương trình tập luyện cá nhân hóa (Push-Pull-Legs, Upper-Lower, Fullbody) trực tiếp vào hệ thống.</li>
                </ul>
                <p><em>Hãy bấm vào các nút gợi ý nhanh ở trên hoặc nhập yêu cầu của bạn bên dưới!</em></p>
              </div>
            </div>
          </div>

          <div class="chat-input-area">
            <input type="text" id="user-input" class="chat-input" placeholder="Nhập yêu cầu: Ví dụ 'Lên lịch tập an toàn cho GYM002'..." onkeydown="if(event.key==='Enter') sendMessage()">
            <button class="send-btn" id="send-btn" onclick="sendMessage()">
              <span>Gửi Ngay</span> ➔
            </button>
          </div>
        </div>

        <!-- CỘT PHẢI: TRACE LOG WATERFALL (CÓ NÚT THU GỌN) -->
        <div class="card" id="trace-panel">
          <div class="card-header">
            <div class="card-title">
              <span>📊 Real-time Waterfall Trace Log (MCP Protocol)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <span class="status-badge" style="background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan); border-color: rgba(6, 182, 212, 0.3);" id="trace-count">0 sự kiện</span>
              <button class="toggle-trace-btn" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;" onclick="toggleTracePanel()" title="Thu gọn bảng Trace">✕ Thu gọn</button>
            </div>
          </div>
          <div class="trace-container" id="trace-box">
            <div style="color: var(--text-muted); text-align: center; margin-top: 30%; font-size: 0.85rem; line-height: 1.6;">
              <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔌</div>
              <b>Chưa có sự kiện thực thi ReAct</b><br>
              Hãy gửi một câu hỏi để theo dõi chuỗi suy luận từng bước<br>
              <span style="color: var(--accent-purple);">Thought</span> ➔ 
              <span style="color: var(--accent-cyan);">Action</span> ➔ 
              <span style="color: var(--accent-orange);">Observation</span> ➔ 
              <span style="color: var(--accent-green);">Final Answer</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- TAB 2: 5 CÂU HỎI TRÌNH BÀY DAY 3 -->
    <div id="tab-slides" class="tab-content">
      
      <!-- CÂU 1 -->
      <div class="slide-section">
        <div class="slide-header">
          <div class="slide-num">1</div>
          <div class="slide-title">Đề tài lựa chọn là gì? Tại sao chọn đề tài đó?</div>
        </div>
        <p class="slide-text">
          <b>Tên đề tài:</b> <span style="color: var(--accent-cyan); font-weight: 800;">Gym Workout Assistant (Trợ lý Lên lịch tập &amp; Gợi ý lộ trình Gym cá nhân hóa)</span> — Thuộc nhóm <b>Đề tài Mở (Open Choice)</b> tại Mục 5 của <code>DANH_SACH_DE_TAI.md</code>.
        </p>
        <p class="slide-text">
          <b>Lý do chọn đề tài:</b><br>
          • <b>Bài toán thực tế:</b> Người tập gym (đặc biệt là người mới) rất dễ tập sai lịch, phân bổ cơ bắp không cân đối hoặc <i>nguy hiểm nhất là tập phải bài xung đột với chấn thương sẵn có</i> (đau khớp gối, thoái hóa cột sống, đau vai).<br>
          • <b>Hạn chế của Chatbot thông thường (Level 2):</b> Chatbot thuần LLM chỉ trả lời văn mẫu chung chung, hoàn toàn không có quyền truy cập hồ sơ thể trạng người dùng, không biết người dùng có tiền sử chấn thương gì và không thể ghi nhận lịch tập vào cơ sở dữ liệu phòng gym.<br>
          • <b>Vai trò của ReAct Agent (Level 3):</b> Agent có khả năng tự động tra cứu hồ sơ người tập, phân tích tình trạng thể lực, tự động loại trừ bài tập rủi ro và gọi công cụ lưu lịch tập tối ưu vào hệ thống qua giao thức MCP.
        </p>
      </div>

      <!-- CÂU 2 -->
      <div class="slide-section">
        <div class="slide-header">
          <div class="slide-num">2</div>
          <div class="slide-title">Tại sao ReAct Agent lại phù hợp? (Bảng 4 Tiêu chí Agentic Fit)</div>
        </div>
        <p class="slide-text">Đánh giá theo khung chuẩn <b>Agentic Fit Scoring Matrix</b> đạt <b>18 / 20 điểm</b> (Vượt xa ngưỡng > 12/20):</p>
        
        <table class="matrix-table">
          <thead>
            <tr>
              <th>Tiêu chí Đánh giá</th>
              <th>Mức độ</th>
              <th>Giải trình thực tế cho đề tài Gym Assistant</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>1. Multi-step Reasoning</b></td>
              <td><span class="score-badge">5 / 5</span></td>
              <td>Không thể giải quyết bằng 1 lần sinh text: Cần 5 bước tuần tự: Nhận diện hội viên ➔ Tra cứu thể trạng &amp; chấn thương ➔ Xác định tần suất buổi/tuần ➔ Chọn bài an toàn thay thế ➔ Thiết lập &amp; lưu lịch tập vào DB.</td>
            </tr>
            <tr>
              <td><b>2. Tool Interaction</b></td>
              <td><span class="score-badge">5 / 5</span></td>
              <td>Bắt buộc kết nối với Database hồ sơ hội viên và hệ thống lưu trữ lịch tập độc lập qua <b>MCP Server</b> theo chuẩn JSON-RPC 2.0.</td>
            </tr>
            <tr>
              <td><b>3. Dynamic Decision</b></td>
              <td><span class="score-badge">4 / 5</span></td>
              <td>Quyết định bước sau phụ thuộc vào kết quả quan sát (Observation) bước trước: Nếu hội viên GYM002 bị đau gối ➔ Agent chủ động rẽ nhánh: loại bỏ Squat nặng / nhảy cao, thay bằng Leg Press nhẹ.</td>
            </tr>
            <tr>
              <td><b>4. Long Horizon Goal</b></td>
              <td><span class="score-badge">4 / 5</span></td>
              <td>Duy trì mục tiêu thể hình tổng thể (tăng cơ / giảm mỡ an toàn) xuyên suốt toàn bộ lộ trình tập luyện nhiều tuần của hội viên.</td>
            </tr>
            <tr style="background: rgba(6, 182, 212, 0.08);">
              <td><b>TỔNG ĐIỂM AGENTIC FIT</b></td>
              <td><span class="score-badge" style="background: var(--accent-cyan); color: #0b0f19;">18 / 20</span></td>
              <td><b>Khẳng định: Bài toán cực kỳ phù hợp để xây dựng ReAct Agent System!</b></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- CÂU 3 -->
      <div class="slide-section">
        <div class="slide-header">
          <div class="slide-num">3</div>
          <div class="slide-title">Kiến trúc Agent &amp; Workflow Suy luận (ReAct Loop)</div>
        </div>
        <p class="slide-text">Mô hình hoạt động theo chu trình khép kín: <b>User Query ➔ LLM Thought ➔ Tool Action ➔ MCP Server Execution ➔ Observation ➔ Final Answer</b>.</p>
        <div class="diagram-box">
          <div class="arch-flow">
            <div class="arch-node">
              <div style="font-size: 1.6rem; margin-bottom: 0.3rem;">🏋️</div>
              <b>User / Member</b>
              <div style="font-size: 0.75rem; color: var(--text-sub); margin-top: 0.2rem;">Yêu cầu tạo lịch tập an toàn</div>
            </div>
            <div class="arch-arrow">➔</div>
            <div class="arch-node agent">
              <div style="font-size: 1.6rem; margin-bottom: 0.3rem;">🧠</div>
              <b>ReAct Agent (LLM)</b>
              <div style="font-size: 0.75rem; color: var(--accent-cyan); margin-top: 0.2rem;">Thought &amp; Native Tool Call</div>
            </div>
            <div class="arch-arrow">➔</div>
            <div class="arch-node mcp">
              <div style="font-size: 1.6rem; margin-bottom: 0.3rem;">🔌</div>
              <b>MCP Server (Port 8000)</b>
              <div style="font-size: 0.75rem; color: var(--accent-orange); margin-top: 0.2rem;">JSON-RPC 2.0 Dispatcher</div>
            </div>
            <div class="arch-arrow">➔</div>
            <div class="arch-node">
              <div style="font-size: 1.6rem; margin-bottom: 0.3rem;">🗄️</div>
              <b>Fitness Database</b>
              <div style="font-size: 0.75rem; color: var(--text-sub); margin-top: 0.2rem;">Hồ sơ thể trạng &amp; Lịch tập</div>
            </div>
          </div>
        </div>
      </div>

      <!-- CÂU 4 -->
      <div class="slide-section">
        <div class="slide-header">
          <div class="slide-num">4</div>
          <div class="slide-title">Các Tool đã xây dựng &amp; Công dụng</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem;">
          <div style="background: var(--card-inner); padding: 1.4rem; border-radius: 10px; border-left: 4px solid var(--accent-cyan);">
            <h3 style="color: var(--accent-cyan); font-size: 1.05rem; margin-bottom: 0.5rem; font-weight: 800;">🔍 Tool 1: fitness_profile_query</h3>
            <p style="font-size: 0.88rem; color: var(--text-sub); margin-bottom: 0.6rem; line-height: 1.5;">
              <b>Công dụng:</b> Tra cứu hồ sơ thể trạng của hội viên gym theo mã định danh (chiều cao, cân nặng, cấp độ kinh nghiệm, tiền sử chấn thương, mục tiêu).
            </p>
            <div style="background: #060911; border: 1px solid #1c2738; padding: 0.6rem; border-radius: 6px; font-family: monospace; font-size: 0.78rem; color: #38bdf8;">
              Input: {"member_id": "GYM001"}<br>
              Output: {status: "SUCCESS", data: {weight: 70, height: 175, injuries: "None", ...}}
            </div>
          </div>

          <div style="background: var(--card-inner); padding: 1.4rem; border-radius: 10px; border-left: 4px solid var(--accent-green);">
            <h3 style="color: var(--accent-green); font-size: 1.05rem; margin-bottom: 0.5rem; font-weight: 800;">📅 Tool 2: create_workout_plan</h3>
            <p style="font-size: 0.88rem; color: var(--text-sub); margin-bottom: 0.6rem; line-height: 1.5;">
              <b>Công dụng:</b> Thiết lập và lưu chương trình tập luyện cá nhân hóa vào hệ thống (phương pháp chia lịch, số buổi, mục tiêu và lưu ý an toàn chấn thương).
            </p>
            <div style="background: #060911; border: 1px solid #1c2738; padding: 0.6rem; border-radius: 6px; font-family: monospace; font-size: 0.78rem; color: #34d399;">
              Input: {"member_id": "GYM002", "split_type": "Upper-Lower", "days_per_week": 3, "safety_notes": "..."}<br>
              Output: {status: "SUCCESS", plan_id: "PLAN-GYM002-2026"}
            </div>
          </div>
        </div>
      </div>

      <!-- CÂU 5 -->
      <div class="slide-section">
        <div class="slide-header">
          <div class="slide-num">5</div>
          <div class="slide-title">Kịch bản Demo trực tiếp &amp; Waterfall Trace Logs</div>
        </div>
        <p class="slide-text">Hệ thống hỗ trợ 5 Test Cases nghiệm thu đầy đủ: từ câu hỏi thuần kiến thức (không gọi tool), tra cứu đơn bước, suy luận đa bước xử lý chấn thương, cho đến trường hợp xử lý ngoại lệ hội viên không tồn tại (Anti-hallucination).</p>
        <p class="slide-text">👉 <i>Hãy chuyển sang Tab <b>"🏋️ Live Workout AI"</b> để trực tiếp bấm thử và xem log trích xuất thời gian thực!</i></p>
      </div>

    </div>

    <!-- TAB 3: WORKFLOW ARCHITECTURE DETAILS -->
    <div id="tab-architecture" class="tab-content">
      <div class="slide-section">
        <div class="slide-header">
          <div class="slide-num">🏛️</div>
          <div class="slide-title">Chu trình ReAct Loop Chi Tiết (Thought - Action - Observation)</div>
        </div>
        <p class="slide-text">Dưới đây là chu trình chi tiết khi xử lý câu hỏi phức tạp (Test Case TC04):</p>
        
        <div style="background: #060911; border: 1px solid #1c2738; border-radius: 12px; padding: 1.5rem; font-family: monospace; font-size: 0.85rem; line-height: 1.8;">
          <div style="color: #94a3af;">// 1. Nhận yêu cầu từ người dùng</div>
          <div style="color: #f3f4f6;">👤 User: "Hội viên GYM002 đau gối, hãy kiểm tra hồ sơ rồi lên lịch tập an toàn."</div><br>

          <div style="color: var(--accent-purple);">🧠 [Thought Step 1]: "Cần tra cứu hồ sơ GYM002 trước để xem tiền sử chấn thương và kinh nghiệm."</div>
          <div style="color: var(--accent-cyan);">🛠️ [Action Step 1]: fitness_profile_query(member_id='GYM002')</div>
          <div style="color: var(--accent-orange);">👁️ [Observation Step 1]: {"injuries": "Chấn thương khớp gối nhẹ", "level": "Beginner"}</div><br>

          <div style="color: var(--accent-purple);">🧠 [Thought Step 2]: "Thấy GYM002 bị đau gối, loại bỏ Squat nặng và bài tập nhảy, tạo lịch Upper-Lower 3 buổi an toàn."</div>
          <div style="color: var(--accent-cyan);">🛠️ [Action Step 2]: create_workout_plan(member_id='GYM002', split='Upper-Lower an toàn', days=3, safety_notes='Tránh Squat sâu...')</div>
          <div style="color: var(--accent-orange);">👁️ [Observation Step 2]: {"status": "SUCCESS", "plan_id": "PLAN-GYM002-2026"}</div><br>

          <div style="color: var(--accent-green);">🏁 [Final Answer]: "Đã thiết lập thành công lịch tập an toàn cho hội viên Trần Thị Bình. Tránh bài tập gây áp lực lên khớp gối."</div>
        </div>
      </div>
    </div>

  </div>

  <script>
    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById('tab-' + tabId).classList.add('active');
      document.getElementById('btn-tab-' + tabId).classList.add('active');
    }

    function toggleTracePanel() {
      const grid = document.querySelector('.demo-grid');
      const btn = document.getElementById('toggle-trace-btn');
      grid.classList.toggle('hide-trace');
      if (grid.classList.contains('hide-trace')) {
        btn.innerHTML = '<span>📊 Mở Trace Log</span>';
        btn.style.background = 'var(--accent-orange)';
        btn.style.color = '#fff';
      } else {
        btn.innerHTML = '<span>📊 Ẩn Trace Log</span>';
        btn.style.background = 'rgba(0,0,0,0.3)';
        btn.style.color = '#fff';
      }
    }

    function sendQuickPrompt(text) {
      document.getElementById('user-input').value = text;
      sendMessage();
    }

    // ROBUST MARKDOWN PARSER: LOẠI BỎ TRIỆT ĐỂ DẤU ###, *** VÀ RENDER THÀNH HTML ĐẸP
    function cleanMarkdown(text) {
      if (!text) return '';
      
      // Nếu có thư viện marked.js
      if (window.marked && typeof window.marked.parse === 'function') {
        try {
          return window.marked.parse(text);
        } catch (e) {
          console.warn('Marked parse fallback:', e);
        }
      }

      // Fallback parser thuần JS (hoạt động kể cả offline không có internet)
      let html = text;

      // 1. Headers: ### Title -> <h4>, ## -> <h3>, # -> <h2>
      html = html.replace(/^### (.*$)/gim, '<h4 style="color:#38bdf8; margin:0.6rem 0 0.3rem;">$1</h4>');
      html = html.replace(/^## (.*$)/gim, '<h3 style="color:#fff; margin:0.8rem 0 0.4rem; font-weight:800;">$1</h3>');
      html = html.replace(/^# (.*$)/gim, '<h2 style="color:#fff; margin:1rem 0 0.5rem; font-weight:900;">$1</h2>');

      // 2. Bold & Italic: Clean ***, **, *
      html = html.replace(/\\*\\*\\*(.*?)\\*\\*\\*/g, '<strong style="color:#fcd34d;"><em>$1</em></strong>');
      html = html.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color:#fff;">$1</strong>');
      html = html.replace(/\\*(.*?)\\*/g, '<em style="color:#cbd5e1;">$1</em>');

      // 3. Horizontal rules ---
      html = html.replace(/^---$/gim, '<hr style="border:0; height:1px; background:#2d3b52; margin:0.75rem 0;">');

      // 4. Bullet lists
      html = html.replace(/^\\s*[\\-\\*]\\s+(.*$)/gim, '<li style="margin-bottom:0.3rem;">$1</li>');
      html = html.replace(/((?:<li[^>]*>.*?<\\/li>\\s*)+)/gis, '<ul style="margin:0.4rem 0 0.6rem 1.25rem;">$1</ul>');

      // 5. Tables
      const lines = html.split('\\n');
      let inTable = false;
      let tableHtml = '';
      let processed = [];

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('|') && line.endsWith('|')) {
          if (!inTable) {
            inTable = true;
            tableHtml = '<table style="width:100%; border-collapse:collapse; margin:0.7rem 0; font-size:0.82rem; background:#090e18; border:1px solid #223049; border-radius:8px;">';
          }
          if (line.includes('---')) continue;
          const cols = line.split('|').slice(1, -1);
          const isHeader = !tableHtml.includes('<tbody>');
          if (isHeader) {
            tableHtml += '<thead><tr style="background:#152033; color:#38bdf8;">' + cols.map(c => `<th style="padding:0.5rem 0.8rem; text-align:left;">${c.trim()}</th>`).join('') + '</tr></thead><tbody>';
          } else {
            tableHtml += '<tr style="border-bottom:1px solid #1a263a;">' + cols.map(c => `<td style="padding:0.5rem 0.8rem;">${c.trim()}</td>`).join('') + '</tr>';
          }
        } else {
          if (inTable) {
            tableHtml += '</tbody></table>';
            processed.push(tableHtml);
            inTable = false;
            tableHtml = '';
          }
          processed.push(lines[i]);
        }
      }
      if (inTable) {
        tableHtml += '</tbody></table>';
        processed.push(tableHtml);
      }
      html = processed.join('\\n');

      // 6. Dọn dẹp dòng trống và xuống dòng
      html = html.replace(/\\n\\n/g, '<div style="height:0.5rem;"></div>');
      html = html.replace(/\\n/g, '<br>');
      html = html.replace(/<br><(h[234]|ul|table|hr)/g, '<$1');
      html = html.replace(/<\\/(h[234]|ul|table|hr)><br>/g, '</$1>');

      return html;
    }

    async function sendMessage() {
      const input = document.getElementById('user-input');
      const text = input.value.trim();
      if (!text) return;

      const chatBox = document.getElementById('chat-box');
      const sendBtn = document.getElementById('send-btn');
      
      // Thêm message của user
      const userMsgDiv = document.createElement('div');
      userMsgDiv.className = 'msg msg-user';
      userMsgDiv.innerHTML = '<div class="msg-author">👤 HỘI VIÊN</div>' + escapeHtml(text);
      chatBox.appendChild(userMsgDiv);
      input.value = '';
      input.disabled = true;
      sendBtn.disabled = true;

      // Loading message
      const loadingDiv = document.createElement('div');
      loadingDiv.className = 'msg msg-agent';
      loadingDiv.id = 'loading-msg';
      loadingDiv.innerHTML = '<div class="msg-author">🤖 AGENT SUY LUẬN...</div>Đang thực thi vòng lặp ReAct và kết nối MCP Server...';
      chatBox.appendChild(loadingDiv);
      chatBox.scrollTop = chatBox.scrollHeight;

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: text })
        });
        const data = await response.json();
        
        // Remove loading
        const loadingEl = document.getElementById('loading-msg');
        if (loadingEl) loadingEl.remove();

        // Render Agent Response với Markdown sạch sẽ
        const agentMsgDiv = document.createElement('div');
        agentMsgDiv.className = 'msg msg-agent';
        agentMsgDiv.innerHTML = '<div class="msg-author">🤖 VINLAB GYM ASSISTANT</div><div class="md-content">' + cleanMarkdown(data.answer) + '</div>';
        chatBox.appendChild(agentMsgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Render Traces
        renderTraces(data.traces);

      } catch (err) {
        const loadingEl = document.getElementById('loading-msg');
        if (loadingEl) loadingEl.remove();
        alert('Lỗi kết nối: ' + err.message);
      } finally {
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
      }
    }

    function renderTraces(traces) {
      const traceBox = document.getElementById('trace-box');
      traceBox.innerHTML = '';
      document.getElementById('trace-count').innerText = traces.length + ' sự kiện';

      traces.forEach(t => {
        const card = document.createElement('div');
        let cardType = 'thought';
        let icon = '🧠';
        let typeTitle = 'Thought (Suy luận)';

        if (t.action_type === 'TOOL_EXECUTION') {
          cardType = 'action';
          icon = '🛠️';
          typeTitle = 'Action & Observation (' + t.tool_name + ')';
        } else if (t.action_type === 'FINAL_ANSWER') {
          cardType = 'final';
          icon = '🏁';
          typeTitle = 'Final Answer';
        }

        card.className = 'trace-card ' + cardType;
        
        let contentHtml = '';
        if (t.thought) {
          contentHtml += '<div style="margin-bottom: 0.35rem;"><b style="color:var(--accent-purple);">Thought:</b> ' + escapeHtml(t.thought) + '</div>';
        }
        if (t.arguments) {
          contentHtml += '<div style="margin-bottom: 0.35rem;"><b style="color:var(--accent-cyan);">Arguments:</b> <div class="trace-json">' + escapeHtml(JSON.stringify(t.arguments, null, 2)) + '</div></div>';
        }
        if (t.observation) {
          contentHtml += '<div><b style="color:var(--accent-orange);">Observation (MCP):</b> <div class="trace-json">' + escapeHtml(JSON.stringify(t.observation, null, 2)) + '</div></div>';
        }
        if (t.output) {
          contentHtml += '<div><b style="color:var(--accent-green);">Output:</b> ' + escapeHtml(t.output) + '</div>';
        }

        card.innerHTML = `
          <div class="trace-header">
            <span class="trace-tag">${icon} Step ${t.step} • ${typeTitle}</span>
            <span class="trace-latency">⏱️ ${t.latency_ms} ms</span>
          </div>
          <div class="trace-body">${contentHtml}</div>
        `;
        traceBox.appendChild(card);
      });
      traceBox.scrollTop = traceBox.scrollHeight;
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>
"""


class WebDemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif parsed.path == "/api/test_cases":
            cases = load_test_cases()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(cases, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            query = data.get("query", "")

            # Chạy ReAct Agent
            traces = run_react_agent(query, provider, mcp_server)
            
            # Lấy final answer
            final_answer = ""
            for t in reversed(traces):
                if t.get("action_type") == "FINAL_ANSWER":
                    final_answer = t.get("output", "")
                    break
                elif t.get("observation"):
                    obs = t.get("observation", {})
                    if obs.get("status") == "SUCCESS" and "message" in obs:
                        final_answer = obs["message"]
                        break

            if not final_answer and traces:
                final_answer = "Đã hoàn thành phiên xử lý qua MCP Server."

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            response_payload = {
                "query": query,
                "answer": final_answer,
                "traces": traces
            }
            self.wfile.write(json.dumps(response_payload, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Giảm ồn console log
        return


def run_web_server():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, WebDemoHandler)
    print("==========================================================")
    print(f"🚀 VINLAB FITNESS WEB UI ĐANG CHẠY: http://localhost:{PORT}")
    print("==========================================================")
    print(f"👉 Mở trình duyệt truy cập: http://localhost:{PORT}")
    print("👉 Giao diện phong cách Muscle & Strength, hiển thị Markdown sạch đẹp.")
    print("👉 Nhấn Ctrl+C để dừng server khi hoàn thành.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Đã tắt Web Demo Server.")


if __name__ == "__main__":
    run_web_server()
