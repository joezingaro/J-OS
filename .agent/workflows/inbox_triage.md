---
description: Process items from the central inbox and distribute them to domain logs.
---

1. Read `log/inbox.md` to capture all pending items.
2. Read `log/CH/AI_rules.md` and `log/Personal/AI_rules.md` to load the current list of known projects.
3. Propose a "Transfer Plan" to the user, sorting each inbox item into:
    - **Personal** (`log/Personal/personal_log_2026.md`)
    - **Work** (`log/CH/work_log_2026.md`)
    - **Quick Capture Log** (`log/quick_capture/quick_capture_log.md`) (For meta-items about the tool itself)
4. Assign a **Global Sequential ID** to each item (continuing from the highest number found in the destination files).
5. Upon user approval:
    - Append the items to their respective destination files.
    - clear the contents of `log/inbox.md`.
