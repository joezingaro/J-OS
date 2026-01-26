---
description: Generates a summary of activity (file changes and log entries) for a specific period. Use to end a day or week.
---
# Workflow: Debrief (Activity Pulse)

Follow these steps to generate an activity report for the user.

1. **Clarify Scope**
   - If the user didn't specify a time period (e.g., "today", "last 3 days", "this week"), ASK: "What time period should I cover?"
   - If the user didn't specify which logs (e.g., "all", "work", "personal"), ASK: "Which log domains should I include? (J-OS, Personal, Work, or All?)"

2. **Scan for Modified Files**
   - Use `find_by_name` to search for files in the user's active context (e.g., `c:\Users\joezi\Desktop\J-OS`).
   - **Filter**: Only include files modified within the requested Time Period.
   - **Exclusions**: Ignore system files, `node_modules`, `.git`, `__pycache__`, and the log files themselves (we handle logs separately).
   - **Note**: Gather the filename, path, and modification time.

3. **Scan Log Files (Recursive)**
   - Use `find_by_name` to search for **all** markdown files in the `log/` directory recursively.
   - **Pattern**: `*.md`
   - **Exclusions**: `archive`, `reports`, `README.md`, `AI_rules.md`.
   - **Action**: Use `view_file` (NOT `read_url_content`) to read each found log file.
   - **Parse**: Look for lines with timestamps `[YYYY-MM-DD]` within scope.

4. **Generate Report**
   - **Target**: `log/reports/Debrief/debrief_[YYYY-MM-DD].md`
   - **Structure**:
     ```markdown
     # Debrief Report: [Period Description]
     **Generated:** [Current Date]
     **Scope:** [Start Date] to [End Date]

     ## 📂 Modified Documents
     - [Filename](absolute/path/to/file) (Modified: YYYY-MM-DD)
       - *Brief 1-line summary of file content/header*

     ## 📝 Logged Activity
     
     ## 📝 Logged Activity
     
     ### [[filename_without_extension]]
     - (ID) **[TAG]** Content...
     ```
   - **Critical**: Use **Standard Relative Markdown Links** (`[Label](../path/to/file)`).
     - Wiki-Links (`[[ ]]`) are extension-dependent and less reliable.
     - Calculate the relative path from the report file to the log file.
     - Example: `[Inbox](../../inbox.md)` (from `log/reports/Debrief/` to `log/`)

   > [!TIP]
   > **Date Filtering**: The `find_by_name` tool returns all files. To efficiently filter by modification date on Windows, pro-actively use `run_command` with PowerShell:
   > `Get-ChildItem -Path "C:\Path\To\Search" -Recurse -File | Where-Object { $_.LastWriteTime -ge (Get-Date "YYYY-MM-DD") } | Select-Object FullName`

5. **Notify User**
   - Present a brief summary to the user.
   - Provide the ABSOLUTE path to the generated artifact in `PathsToReview`.
   - Ask if they want to review specific items in detail.
