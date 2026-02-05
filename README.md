🚀 Personal AI Employee – Hackathon 0

Building Autonomous Digital FTEs (Full-Time Equivalents)

Tagline:

Your life and business on autopilot — local-first, agent-driven, human-in-the-loop.

📌 Overview

This project implements a Personal AI Employee (Digital FTE) — an autonomous, local-first AI system that proactively manages personal and business workflows such as:

Emails & messages

Social media drafts & approvals

Task planning

Accounting & audits

CEO-style weekly briefings

Unlike chatbots, this AI does not wait for prompts.
It continuously monitors events, reasons about them, and requests human approval before executing sensitive actions.

This project was built as part of Hackathon 0: Building Autonomous FTEs (2026).

🧠 Core Idea: Digital FTE

A Digital FTE is an AI agent treated like a real employee:

Feature	Human FTE	Digital FTE
Availability	40 hrs/week	24/7 (168 hrs/week)
Cost	$4k–$8k/month	$500–$2k/month
Consistency	Variable	Predictable
Scaling	Linear	Instant duplication

💡 9,000 AI working hours per year vs 2,000 human hours

🏗️ System Architecture

This system follows a Perception → Reasoning → Action model.

1️⃣ Perception (Watchers)

Python scripts continuously monitor:

Gmail

WhatsApp

Local file drops

Accounting files

They create structured .md files inside the Obsidian vault.

2️⃣ Reasoning (Claude Code)

Claude Code acts as the brain:

Reads vault files

Creates plans

Generates drafts

Requests approvals

Updates dashboard

Uses the Ralph Wiggum Loop to keep working until tasks are complete.

3️⃣ Action (MCP + HITL)

Actions are executed only after human approval:

Email sending

Social posting

Payments

External system updates

📁 Obsidian Vault Structure
AI_Employee_Vault/
│
├── Dashboard.md
├── Company_Handbook.md
├── Business_Goals.md
│
├── Needs_Action/
│   ├── EMAIL_*.md
│   ├── WHATSAPP_*.md
│   └── FILE_*.md
│
├── Pending_Approval/
├── Approved/
├── Rejected/
├── Done/
│
├── social/
│   ├── Draft/
│   ├── Posted/
│
├── Logs/
├── Invoices/
└── Updates/


📌 Vault = Database + Memory + UI State

🖥️ Frontend (Human Control Panel)

A local web UI built with Flask + HTML/CSS:

Features

📊 Dashboard (renders Dashboard.md)

⏳ Pending approvals (Approve / Reject buttons)

📥 Needs Action viewer

📝 Social media draft preview

📜 Audit logs viewer

⚠️ UI never executes actions — it only moves files (HITL safety).

🔐 Human-in-the-Loop (HITL)

For sensitive actions, the AI creates approval files:

/Pending_Approval/PAYMENT_ClientA_2026_01_07.md


Human decision:

✅ Move to /Approved

❌ Move to /Rejected

The orchestrator then executes the action safely.

🔄 Ralph Wiggum Loop (Autonomy Engine)

Claude is prevented from exiting until the task is complete.

Completion strategies:

File moved to /Done

Explicit completion promise

This solves the “lazy agent” problem.

🔧 Tech Stack
Layer	Technology
Reasoning	Claude Code
Memory / UI	Obsidian (Markdown)
Watchers	Python
Orchestration	Python
External Actions	MCP Servers
UI	Flask + HTML/CSS
Automation	PM2 / Task Scheduler
🛡️ Security & Privacy

🔒 Local-first (no cloud dependency)

❌ Secrets never stored in vault

✅ .env for credentials (git-ignored)

🧾 Full audit logging

🛑 No auto-payments or auto-posts

🏆 Hackathon Tier

Target Tier:
🥇 Gold → Platinum Ready

Implemented:

Watchers

Approval workflow

Claude reasoning

Vault-driven UI

Audit logs

Autonomous planning

▶️ How to Run (Local)
# Clone repo
git clone https://github.com/rabia758/Hackthone-0.git
cd Hackthone-0

# Setup environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run UI
python app.py


Open browser:

http://127.0.0.1:5000

📅 Research & Learning Sessions


👩‍💻 Author

Rabia Rizwan
AI Engineer | Agent Architect | Digital FTE Builder

🌟 Final Note

This project is not a chatbot.
It is a thinking, planning, auditing, approval-aware AI employee.

Software runs tasks.
Digital FTEs run businesses.