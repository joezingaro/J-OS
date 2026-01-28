# Innovation Exercise
Date: 2026-01-26

## Innovation Pearls: AI Strategy

### 1. Recursive Prompting (The "Meta-Prompt" Approach)
One of the most effective ways to use AI is to use it to **design its own instructions**.

*   **Problem:** "Prompt Engineering" often feels like memorizing spells or lengthy guides (prompt generators, etc.), which isn't necessary.
*   **Philosophy:** Focus on intent over mechanics. You don't need to memorize prompt libraries; you can use the AI itself to translate your goals into the optimal instructions.
*   **Technique:** Start a chat by providing the raw context and background of what you want, and then explicitly ask:
    > "Let's discuss what I'm looking for, and then please provide me with a detailed prompt I can use with AI to generate my document."
*   **Refinement Loop:** This allows you to go back and forth—critiquing the AI's proposed prompt to ensure it truly captures your intent.
*   **Execution:** Once the prompt is perfect, take it to a **fresh chat window**. This gives you a clean context with highly optimized instructions.
*   **Benefit:** This offloads the structural complexity to the AI, allowing you to focus purely on the creative intent.

### 2. The Adversarial Thought Partner (Risk Management & Brainstorming)
AI isn't just a solution generator; it can be a powerful tool to **stress-test your logic and act as a brainstorming partner**.

*   **The Trap:** Many AI models are trained to be agreeable; they often prioritize "helpfulness," which can manifest as agreeing with flawed ideas.
*   **The Pivot:** Explicitly invite the AI to challenge you. Don't just ask for a plan; provide your draft (e.g., a new Excel time-tracking process) and ask for a "Pre-Mortem."
*   **Key Prompts for Risk Assessment:**
    *   "Where do you think this process might break?"
    *   "What edge cases, bugs, or user friction points am I sensitive to here?"
    *   "What alternative technologies or approaches should I have considered but missed?"
*   **Value:** This helps transform the AI from a 'yes-man' into an objective risk management tool, helping you harden your plans before execution.

### 3. Executive Brief: Innovation Team Huddle Strategy

**Goal:** Define concrete Innovation Goals for 2026 PEPs (ranging from Quick Wins to Strategic Bets).
**Format:** 30-Minute "Sprint" (Virtual/Miro)

#### 1. The Elevator Pitch (Summary)
#### 1. The Elevator Pitch (Summary)
> *   **Part 1 (The Context):** We define "Little i" (Process) vs "Big I" (Strategy) innovation.
> *   **Part 2 (The Tools):** We learn **Rose, Thorn, Bud** and **15% Solutions** via a live whiteboarding exercise.
> *   **Part 3 (The Toolkit):** You get a "Meeting-in-a-Box" to run this exact session with your own staff.
>
> **The Goal:** Empower leads to identify their own innovation ideas, and give them a way to do the same with their teams.

#### 2. The Core Strategy: "Full Spectrum" Innovation
We are looking for a balanced portfolio of innovation. The session will educate leads on the difference between:
*   **"Little i" Innovation:** Removal of friction, process improvements (Quick Wins).
*   **"Big I" Innovation:** Major structural changes or new initiatives (Strategic Bets).

**The Goal:** Ensure 2026 PEPs aren't just one or the other, but a conscious choice between the two.

#### 3. The Frameworks: Methodology Deep Dive

**A. The Diagnostic Tool: "Rose, Thorn, Bud"**
*   **Origin:** Design Thinking (IDEO) / Boy Scouts of America
*   **Purpose:** To quickly map current reality. It stops people from just complaining and forces them to see the whole picture.
    *   🌹 **Rose (Successes):** What is working well? (e.g., "Team energy is great.")
    *   🌵 **Thorn (Pain Points):** What is broken? (e.g., "Updating Excel takes 4 hours.") -> *Becomes "Little i" Innovation.*
    *   🌱 **Bud (Opportunities):** What is a "baby idea" with potential? (e.g., "We have Teams but no file structure.") -> *Becomes "Big I" Innovation.*
*   **Why use it?** It acts as the **Brainstorming Engine**. Instead of asking for "innovation ideas" (brain freeze), you simply ask for 2 Thorns and 1 Bud.

**B. The Action Tool: "15% Solutions"**
*   **Origin:** Liberating Structures (Lipmanowicz & McCandless)
*   **Purpose:** To overcome "Analysis Paralysis" and helplessness.
*   **The Concept:** Most people focus on the 85% they cannot control (Budget, IT, CEO). This asks: *Where do you have discretion to act right now?*
*   **Why use it?** It acts as the **Reality Check**. When a Lead suggests a "High Effort" Money Pit (e.g., "New $50k CRM"), challenge them:
    > "That's a great Big I goal. But what is the 15% Solution you can start tomorrow? Researching vendors? Cleaning data?"
*   **Result:** Ensures the PEP goal is actionable, not just a wish list.

#### 4. The Exercise: The "Impact vs. Effort" Matrix
*   **Why this tool:** It is the only framework that allows us to visualize and sort both "Big" and "Little" ideas simultaneously.
*   **The Workflow:**
    1.  **Brain Dump:** Leads dump ALL ideas (Thorns/Pain points and Blue Sky opportunities).
    2.  **Map:** They map them on the matrix to separate them:
        *   *Top Left:* Quick Wins (Do it now).
        *   *Top Right:* Major Projects (Big I / Strategic Goals).
    3.  **Selection:** Leads choose the goal that fits their capacity for 2026.

#### 5. The Deliverables
*   **Part A: The "Innovation Menu":** A curated list of work practices to inspire the team.
*   **Part B: The "Meeting-in-a-Box":** A facilitation guide so leads can run this exact matrix exercise with their teams to surface their own high-impact projects.

#### 6. Expected Outcomes
By the end of 30 minutes, every lead will have a drafted Innovation Goal—whether it's a tactical fix or a major 2026 initiative.

### 4. Behind the Scenes: The AI Prompt Used
This session itself was designed using the "Cross-Model Prompting" strategy. I initially used **Gemini Pro** to brainstorm the structure, then refined the prompt and fed it into **Co-Pilot** to generate the final agenda. You can view the full [AI Workflow Summary](file:///c:/Users/joezi/Desktop/J-OS/log/CH/notes/2026-01-26_Innovation_Exercise_AI_Workflow_Summary.html).

> *Note: Playing with different models (when no sensitive organizational data is involved) is a great way to understand their unique strengths.*

**The Prompt Used:**

```text
Act as a Lead Innovation Strategist and Facilitator.

I am running a strictly time-boxed 30-minute Team Huddle for organizational Leads. The teams are siloed, so the exercise utilizes individual work on a shared digital whiteboard.

Goals:
1. Education: Briefly introduce two innovation frameworks.
2. Action: Have every Lead define a set of "Innovation Goals" for their 2026 PEP using an Impact vs. Effort Matrix.
3. Enablement: Provide a "Menu" of ideas they can take back to their teams (per my manager's request).

Please design a 30-minute Agenda and a Leave-Behind Resource.

Part 1: The "Lightning" Intro (5 Minutes)
Provide a script for a rapid introduction that contrasts two techniques:
- Technique 1: "Rose, Thorn, Bud" (Design Thinking): Explain how to use this to diagnose issues (Rose = Success, Thorn = Pain Point, Bud = Potential).
- Technique 2: "15% Solutions" (Liberating Structures): Explain how to use this to act (focusing only on what you can change without extra budget/permission).

Part 2: The Miro Workflow (20 Minutes)
Design a specific board layout and workflow:
- Min 0-7 (The Brain Dump): What specific prompt do they answer on their sticky notes? (Please use the "Thorn" concept—pain points—as the trigger).
- Min 7-15 (The Matrix Ranking): Describe how to set up an "Impact vs. Effort" Matrix on the board. Provide specific definitions for the 4 quadrants to help leads categorize their ideas:
    * High Impact / Low Effort: "Quick Wins" (Do these immediately).
    * High Impact / High Effort: "Major Projects" (Strategic bets for the year).
    * Low Impact / Low Effort: "Fillers" (Nice to have, but not a priority).
    * Low Impact / High Effort: "Money Pits" (Avoid/Delete these).
- Min 15-20 (The Selection Strategy): Instruct them on how to select a "Balanced Portfolio" for their PEP. (e.g., "Choose 2 Quick Wins to build momentum, and 1 Major Project for career growth").

Part 3: The Leave-Behind One-Pager (Diana's Request)
Create the text for a 1-page PDF resource I can email immediately after the call.
- Section A: The "Innovation Menu." List 5 specific, low-effort "Micro-Habits" they can adopt to inspire innovation in their teams (e.g., "The Friday Fail Share," "The No-Meeting Afternoon," "Video Updates").
- Section B: The Facilitation Guide. A simple bulleted list on how to run this exact "Rose, Thorn, Bud" + "Impact Matrix" exercise with their own staff.

Tone: High-energy, efficient, and practical.
```

### 5. The Outcome: Generated Huddle Plan (Co-Pilot Output)
*Refined output generated from the prompt above.*

#### PART 1 — “Lightning” Intro (5 Minutes)
**Script (You can read this verbatim)**
> "Welcome everyone — today is a fast, practical innovation sprint. We’re going to use two proven techniques to help you sharpen your 2026 PEP innovation goals."

**1. Rose, Thorn, Bud (Design Thinking)**
> "First, a quick diagnosis tool: Rose, Thorn, Bud.
>
> *   **A Rose** is what’s working — successes we can build on.
> *   **A Thorn** is a pain point — something frustrating, slow, inefficient, or holding your team back.
> *   **A Bud** is an opportunity that’s emerging — something promising that isn’t fully developed yet.
>
> We’ll use the **Thorn** piece today as the spark — because pain points are where innovation starts."

**2. 15% Solutions (Liberating Structures)**
> "Next, once we identify issues, we don’t wait for permission or extra budget. We look for our **15% Solutions** — the actions we can take right now with the authority, resources, and influence we already have.
>
> Why 15%? Because most innovation isn’t a moonshot — it’s small, doable shifts that accumulate into big change.
>
> Today, you’ll identify your Thorns, then use an Impact vs. Effort Matrix to choose the innovation moves that belong in your 2026 PEP."

#### PART 2 — Miro Workflow (20 Minutes)
**Board Layout Overview**
Your Miro board has 3 zones:
1.  **Brain Dump Area:** Blank sticky space
2.  **Impact vs. Effort Matrix:** 4 labelled quadrants
3.  **Selection Box:** Where final PEP picks go

**Min 0–7 — The Brain Dump (Thorn-Prompt Activity)**
*   **Prompt for sticky notes:** "What are the top Thorns (pain points, barriers, inefficiencies, friction points) that slowed you or your team down in 2025? Create 1 sticky per Thorn."
*   **Encourage:** Performance barriers, Process bottlenecks, Customer complaints, Workarounds, Tech gaps.
*   **Instruction Script:** "Individually add as many Thorn stickies as you can — 1 idea per sticky. Don’t overthink it. This is about surfacing the raw data."

**Min 7–15 — Impact vs. Effort Matrix Ranking**
*   **X-axis:** Effort (Low → High)
*   **Y-axis:** Impact (Low → High)
*   **Quadrant Definitions:**
    1.  **High Impact / Low Effort — QUICK WINS:** Immediate actions. Clear value. Great for momentum.
    2.  **High Impact / High Effort — MAJOR PROJECTS:** Strategic initiatives. Require planning or cross-team alignment.
    3.  **Low Impact / Low Effort — FILLERS:** Nice-to-have improvements. Save for capacity gaps.
    4.  **Low Impact / High Effort — MONEY PITS:** Minimal payoff. Avoid or delete from consideration.
*   **Instructions:** "Drag each of your Thorn stickies into the quadrant that best fits the effort to fix it vs. the impact of solving it. Go with your instinct."

**Min 15–20 — The Selection Strategy (Choosing Your PEP Portfolio)**
*   **Script:** "Now that your ideas are placed, we’re going to build a balanced innovation portfolio for your 2026 PEP."
*   **Selection Criteria:**
    *   2 Quick Wins (early momentum)
    *   1 Major Project (strategic growth)
    *   0–1 Filler (optional)
    *   0 Money Pits (eliminate)
*   **Final Action:** Drag chosen stickies into the ‘2026 PEP Innovation Picks’ box on the board.

#### PART 3 — Leave-Behind One-Pager (Text for PDF)

**📄 INNOVATION MICRO‑PLAYBOOK FOR LEADS (2026 EDITION)**

**SECTION A — The “Innovation Menu”: 5 Micro-Habits for Your Team**
1.  **The Friday Fail Share (5 minutes):** Normalize smart risk-taking. Each Friday, one person shares a small experiment that didn’t work — and what they learned.
2.  **The No-Meeting Afternoon:** Protect thought-time. Choose one afternoon each week where the team has protected focus time.
3.  **The 10-Minute Weekly Demo:** End-of-week micro‑demos where team members quickly show something they built, fixed, or improved.
4.  **The 3-Question Retro:** Once a month ask: *What should we start? What should we stop? What should we continue?*
5.  **Video Updates Over Email:** Use short Loom/Teams recordings to explain a process, change, or decision. Faster, clearer, and more human.

**SECTION B — Facilitation Guide: How to Run This Exercise With Your Team**
1.  **Rose, Thorn, Bud (10 minutes):** Ask team to list Roses, Thorns, Buds. Focus on Thorns for innovation.
2.  **Impact vs. Effort Sorting (10 minutes):** Place Thorns in Matrix (Quick Wins, Major Projects, Fillers, Money Pits).
3.  **Choose Your Portfolio (5 minutes):** Pick 1–2 Quick Wins, 1 Major Project. Delete Money Pits.
4.  **Convert into Actions (5 minutes):** Turn each selected sticky into: Single Owner, Success Indicator, 30/60/90‑day checkpoint.