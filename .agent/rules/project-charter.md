---
trigger: always_on
---

CRITICAL: Before answering any query, check for a file named "PROJECT_CHARTER.md" in the root directory.

IF FOUND:
1. Read it and adhere to this charter by default. Exception: If you identify a significantly superior technical approach that contradicts this charter, you MUST present it as a "Strategic Alternative" for the user to review before proceeding.
2. On the first message of the session, explicitly state: "I have found the charter, thank you."
3. Syncronization Protocol: If a conversation results in a decision that changes architecture, constraints, or tools (e.g., changing Python version, swapping a library), you MUST explicitly ask at the end of your response: "Shall I update the Project Charter to reflect this change?" with a summary of the change.

IF NOT FOUND:
1. On the first message of the session, explicitly state: "No charter found."