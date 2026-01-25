---
description: Process items from the central inbox and distribute them to domain logs.
---

1.  **Read Inbox**: Read `log/inbox.md` to capture all pending items.
2.  **Scan for Projects**:
    *   Traverse `log/` and its subdirectories to find active log files (e.g., `work_log_2026.md`, `personal_log_2026.md`, `quick_capture_log.md`).
    *   **CRITICAL exclusion**: Flag and IGNORE any file containing "archive" in its name (e.g., `work_log_archive_2026.md`).
3.  **Load Rules & Prefixes**:
    *   For each active log file found, read the local `AI_rules.md` in its directory.
    *   Extract:
        *   **Known Projects** (for sorting items).
        *   **ID Prefix** (e.g., `w`, `p`, `q`) defined in the "Global Sequential Numbering" section.
4.  **Propose Transfer Plan**:
    *   Match inbox items to projects/files based on keywords or tags.
    *   If a match is found, assign the item to that file.
    *   If no match is found, ask the user or leave in Inbox.
5.  **Assign Smart IDs**:
    *   For each item moving to a destination file, generate a new **Smart ID**: `(Prefix + NextNumber)`.
    *   *Example*: If moving to Work Log and highest ID is `(w52)`, assign `(w53)`.
6.  **Execute (On Approval)**:
    *   Append items to their destination files (under correct headers).
    *   Clear `log/inbox.md`.
