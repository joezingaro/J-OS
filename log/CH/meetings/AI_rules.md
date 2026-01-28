# CONFIGURATION: MEETINGS PROTOCOL

**⚠️ INHERITANCE REQUIRED:**
Read `../AI_rules.md` (Parent) for global definitions.

## 🔄 The Sync Protocol (Bi-Directional Linking)
All action items identified in meeting notes must be synced to the master Work Log (`../work_log_2026.md`).

### 1. Extracting to Work Log
When moving a task from a meeting note to the Work Log, append the source using a relative link (`meetings/Filename.md`):
> `- [ ] [TASK] Task Description... (Source: [Meeting Name > Context](meetings/Diana.md#header-slug))`
> *Example Anchor: `#2026-01-26-team-huddle`*

### 2. Tracking in Meeting Note
When a task has been extracted, update the meeting note line to indicate it is being tracked:
> `*   Task Description... (-> [Tracked](file:///path/to/work_log_2026.md))`

### 3. AI Summary Section
Every meeting note should start with an **AI Summary** block that aggregates key decisions and actions, ensuring they are not lost in the detailed bullet points.
