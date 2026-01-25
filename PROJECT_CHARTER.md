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
* **Location:** `/data` directory.
* **`work_log_2026.md`:** The primary ledger for tasks, projects, and logs. Strict formatting required.
* **`inbox.md`:** The "Dump" zone for raw, unprocessed thoughts.
* **`/meetings/`:** Folder for unstructured meeting notes.

### B. The Satellite (Input Layer)
* **Tool:** `tools/quick_capture.py`
* **Tech Stack:** Python 3.12
* **Behavior:** A global hotkey (`Ctrl+Alt+Space`) triggers a borderless, modern HTML popup. It appends text to `inbox.md`.

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
* **Python Version:** **Python 3.12** ONLY. (Do not use 3.14/Preview versions).
* **Permissions:** All `pip` installs must be user-scoped. No system-level changes.
* **Paths:** Use relative paths (`os.path.join`). Never hardcode `C:\Users\...`.
* **OS:** Windows 11 (Corporate Environment).
