# GLOBAL SYSTEM INSTRUCTIONS

You are an intelligent OS Agent. Your behavior is defined dynamically by local context files.

## NAVIGATION PROTOCOL (CRITICAL)
Before writing code or generating text, you MUST load the correct "Instruction Stack" based on your active directory.

* **IF working in `/src`:**
    * Read `src/AI_rules.md`.

* **IF working in `/log` (Any subfolder):**
    * **Step 1 (Context):** Read the local `AI_rules.md` in your specific subfolder (e.g., `log/CH/AI_rules.md`) to get Project Lists and File Names.
    * **Step 2 (Logic):** Read the parent `log/AI_rules.md` to get the Formatting Protocols and Execution Logic.
    * *You must combine both files to function.*