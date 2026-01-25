# 📜 J-OS Project Charter & Technical Standards

**Project Name:** J-OS (Joseph's Operating System)
**Owner:** Joseph
**Version:** 1.0

## 1. 🎯 Mission
To build a **future-proof, text-file-based Operating System** for executive management. The system decouples **Storage** (Markdown files) from **Processing** (AI/IDE) and **Input** (Python Scripts), creating a workflow that is flexible, portable, and independent of proprietary SaaS apps.

---

## 2. 🧠 Core Philosophy
1.  **Text is King:** All data lives in `.md` files. If the tools break, the data remains readable.
2.  **IDE as the Engine:** We do not build a monolithic app. We use the IDE (VS Code / Antigravity) as the main interface.
3.  **Local & Private:** Tools run on `localhost`. Data syncs via Git. No reliance on cloud APIs for basic functionality.
4.  **Admin-Free:** All tools must function within "User Scope" permissions. No Admin rights required.

---

## 3. 🏗️ Architecture

### A. The Database (Storage Layer)
* **Location:** `/log` directory.
* **`log/CH/work_log_2026.md`:** The primary ledger for corporate tasks.
* **`log/CH/inbox.md`:** The "Dump" zone for raw, unprocessed corporate thoughts.
* **`log/Personal/personal_log_2026.md`:** The primary ledger for personal tasks.
* **`/log/CH/meetings/`:** Folder for unstructured meeting notes.

### B. The Satellite (Input Layer)
* **Tool:** `src/quick_capture/quick_capture.py`
* **Tech Stack:** Python 3.12
* **Behavior:** A global hotkey (`Ctrl+Shift+Space`) triggers a borderless, modern HTML popup. It appends text to `log/CH/inbox.md`.

### C. The Dashboard (Visualization Layer)
* **Tool:** `tools/dashboard_server.py`
* **Tech Stack:** Python 3.12, `Flask`, HTML/CSS.
* **Behavior:** A local web server (`localhost:5000`) that parses Markdown files and renders them as a Kanban board.

### D. The Brain (Processing Layer)
* **Engine:** Google Antigravity / VS Code.
* **Intelligence:** AI Agent (Gemini Pro/Flash).
* **Role:** Refactoring, sorting, planning, and code generation.

---

## 4. 🛑 Technical Constraints (Strict Rules)
* **Python Version:** **Python 3.12** is the default. Other tools/languages (e.g., Node.js, Rust) are permitted if they offer superior capability and are approved by the User.
* **Permissions:** All `pip` installs must be user-scoped. No system-level changes.
* **Paths:** Use relative paths (`os.path.join`). Never hardcode `C:\Users\...`.
* **OS:** Windows 11 (Corporate Environment).

ALWAYS check for a local AI_rules.md in the subfolder you are working in (e.g., src/quick_capture/AI_rules.md) for tool-specific rules.
