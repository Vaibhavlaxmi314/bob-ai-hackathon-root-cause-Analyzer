# Document Refinement Plan
## Supply Chain Disruption Assistant & Fleet Utilisation Optimizer

### Top-Level Overview

**Goal:** Replace every template placeholder and generic boilerplate across all submission documents with accurate, specific content that reflects the Supply Chain Disruption Assistant & Fleet Utilisation Optimizer problem statement discussed and agreed upon.

**Scope:** Eight files require content rewrites or completion. The `docs/template-guide.md`, `CONTRIBUTING.md`, and configuration files are reference/infra files and are excluded from scope.

**Approach:** Each sub-task targets one file. Sub-tasks are ordered by dependency — `problem-statement.md` and `solution-overview.md` first (they define the narrative), then `architecture.md`, then `README.md` and `submission.yaml` (which summarise the above), and finally `setup-guide.md` (which depends on final tech stack decisions).

**Problem statement pillars driving all content:**
1. Disruption-to-Shipment Mapping — identify which active shipments are affected by a live event
2. Re-routing & Carrier Recommendation — surface alternative routes / carriers per affected shipment
3. Idle Fleet Asset Identification — detect idle trucks, containers, vessels for redeployment
4. Cold Chain IoT Monitoring & Severity Classification — detect temperature excursions and classify regulatory severity before delivery

---

### Sub-Task 1 — Rewrite `docs/problem-statement.md`

**Status:** [x] done

**Intent:**
The file currently contains the correct structure (Background, The Problem, Who is Affected, Why It Matters, Why Existing Solutions Fall Short) but every section is wrapped in `[brackets]` indicating placeholder status. This sub-task removes the brackets and rewrites each section as polished, submission-ready prose grounded in the four problem pillars.

**Expected Outcomes:**
- No `[` or `]` characters remain in the file
- Background section explains the global logistics and cold chain context (reefers, vaccines, perishables, tight schedules)
- The Problem section names all four pain points: disruption blindness, fleet idle waste, cold chain excursion detection lag, and inability to re-route in time
- Who is Affected names specific personas: Logistics Operations Managers, Fleet Dispatchers, Cold Chain Compliance Officers at mid-to-large enterprise shippers, pharma companies, food distributors
- Why It Matters calls out the $500K+ cargo loss risk, 2x–3x emergency freight costs, and production line shutdown costs
- Why Existing Solutions Fall Short names fragmented data silos (TMS, FMS, weather feeds), manual operator workflows, and lack of predictive re-routing

**Todo List:**
1. Read the current `docs/problem-statement.md` content
2. Remove all `[` bracket wrappers from every section
3. Expand Background to include cold chain specifics (vaccines, biologics, perishables, reefer containers) and disruption types (storms, port strikes, geopolitical crises)
4. Rewrite The Problem to explicitly name all four pain areas in fluent prose
5. Expand Who is Affected to include Cold Chain Compliance Officers and the pharma / food & beverage verticals
6. Rewrite Why It Matters with the three financial impact points written as clear numbered paragraphs (not bracketed)
7. Rewrite Why Existing Solutions Fall Short with the three named root causes (fragmented data, manual workflows, no predictive re-routing)
8. Verify no placeholder text remains

**Relevant Context:**
- File: `docs/problem-statement.md`
- Problem pillars: Disruption Mapping, Re-routing, Fleet Utilisation, Cold Chain IoT
- Key statistics to include: $500K+ cargo loss, 2x–3x emergency freight premium, hundreds of simultaneous active shipments

---

### Sub-Task 2 — Rewrite `docs/solution-overview.md`

**Status:** [x] done

**Intent:**
This file is completely blank (template only). It needs to be written from scratch to explain what the Bob-powered solution does across all four pillars, how it works step by step, which IBM technologies are used and how, and the key design decisions made.

**Expected Outcomes:**
- What We Built: 2–3 paragraph plain-language description of the Bob solution covering all four capabilities
- How It Works: Numbered 5-step flow covering — disruption event ingestion → shipment impact analysis → re-routing recommendation → fleet idle asset scan → cold chain IoT excursion classification
- Architecture Diagram: A simple Mermaid diagram (see note below) showing the data flow at a glance
- Key Design Decisions: Table with at least 4 rows explaining why Bob agents were used, why watsonx.ai was chosen for classification, why simulated data sources were used vs. live APIs, and why generic regulatory severity thresholds are referenced rather than a specific standard
- IBM Technologies Used: Explains IBM Bob (agents, skills, MCP tools), watsonx.ai (Granite model for NLP classification), and how each was used specifically

**Note on diagrams:** Do not include Mermaid in the plan file itself — diagrams go in the actual document files.

**Todo List:**
1. Draft "What We Built" section describing the four-pillar Bob solution in plain language
2. Write "How It Works" as a numbered 5-step flow without brackets
3. Add a simple ASCII flow as a quick-reference diagram (no Mermaid in this file — reference architecture.md)
4. Populate the Key Design Decisions table with 4 specific rows
5. Write the IBM Technologies Used section explaining Bob and watsonx.ai usage concretely
6. Verify no placeholder or bracket text remains

**Relevant Context:**
- File: `docs/solution-overview.md`
- IBM Bob is the core runtime — agents, skills, MCP servers are the delivery mechanism
- watsonx.ai Granite model is used for text classification (severity, carrier recommendation reasoning)
- Simulated IoT sensor data and disruption event feeds are used as data sources (no live API keys needed for demo)

---

### Sub-Task 3 — Rewrite `docs/architecture.md`

**Status:** [x] done

**Intent:**
The file has a generic template Mermaid diagram (User → React → FastAPI → watsonx.ai → PostgreSQL → Slack) that bears no relation to the actual solution. This sub-task replaces the diagram and all component/data-flow content with the real architecture of the Supply Chain Disruption Assistant.

**Expected Outcomes:**
- System Architecture section has a Mermaid diagram representing the actual solution components: Disruption Feed → Bob Agent Orchestrator → Shipment Matcher, Re-routing Advisor, Fleet Scanner, Cold Chain Monitor → watsonx.ai → Output Dashboard
- Components table has 5–6 real rows: Bob Orchestration Agent, Disruption Ingestion Tool (MCP), Shipment Impact Analyzer, Re-routing Advisor, Fleet Asset Scanner, Cold Chain IoT Classifier
- Data Flow section has 5 numbered steps specific to the solution flow
- Security Considerations notes env-var-based API key storage and watsonx.ai credential handling
- Scalability Notes addresses how the Bob agent pattern scales across more shipment records

**Todo List:**
1. Replace the generic Mermaid diagram with a solution-specific architecture diagram
2. Rewrite the Components table with actual component names, technologies, and responsibilities
3. Rewrite the Data Flow section with the five real steps of the solution
4. Update Security Considerations to name actual secrets (WATSONX_API_KEY, WATSONX_PROJECT_ID)
5. Rewrite Scalability Notes for the Bob agent model
6. Verify no placeholder or bracket text remains

**Relevant Context:**
- File: `docs/architecture.md`
- Core components: Bob Agent, MCP Disruption Tool, Shipment Impact Engine, Re-routing Advisor, Fleet Scanner, Cold Chain IoT Classifier, watsonx.ai (Granite)
- Data sources: Simulated JSON disruption events, shipment manifest CSVs, fleet telemetry JSON, IoT temperature sensor logs

---

### Sub-Task 4 — Rewrite `README.md`

**Status:** [x] done

**Intent:**
The README is the first thing judges see. It currently has partial team info filled in but every section after that is a template placeholder. This sub-task rewrites every bracketed section with real, specific content consistent with the solution described in sub-tasks 1–3.

**Expected Outcomes:**
- Team table has no brackets — track is set to "AI", lead and members filled correctly
- Problem Statement section is 2–3 crisp sentences with no brackets
- Solution section is 2–3 sentences explaining the Bob-powered four-pillar system
- Key Features lists 4–5 specific features (e.g., "Disruption-to-Shipment Impact Mapping", "AI-powered Re-routing Recommendations via watsonx.ai Granite", "Cold Chain Excursion Severity Classification against WHO/GDP thresholds", "Idle Fleet Asset Redeployment Suggestions")
- Tech Stack table is filled with real values: Python, FastAPI / Bob SDK, IBM Bob, watsonx.ai, simulated JSON data sources
- How to Run block has real clone/install/run commands (copied from setup-guide.md)
- Known Limitations lists honest hackathon constraints: simulated data, no live carrier API, no production auth
- What We're Most Proud Of is written

**Todo List:**
1. Update Team table — remove brackets, set track to "AI"
2. Rewrite Problem Statement row (2–3 sentences, no brackets)
3. Rewrite Solution section (2–3 sentences, no brackets)
4. Rewrite Key Features with 4–5 specific feature bullets
5. Fill Tech Stack table with real technologies
6. Update How to Run block with real commands from setup-guide.md
7. Update demo links to reflect actual state (point to demo-video-link.txt, etc.)
8. Write Known Limitations (3 honest items)
9. Write What We're Most Proud Of
10. Verify no `[` or `]` characters remain in the file

**Relevant Context:**
- File: `README.md`
- Team name: root-cause-Analyzer, Lead: Vaibhavlaxmi (26mca113@gmail.com), Members: Kevina, Aayush, Abhishek
- The GitHub Actions validator explicitly checks that no `[` characters appear in README.md

---

### Sub-Task 5 — Fill `submission.yaml`

**Status:** [x] done

**Intent:**
This is the most critical file for automated evaluation. The GitHub Actions validator reads it directly and fails the submission if any required field is empty. Every required field must be populated with real values derived from the problem statement and solution.

**Expected Outcomes:**
- `team.name` = "root-cause-Analyzer"
- `team.track` = "AI"
- `team.lead.name` = "Vaibhavlaxmi", `team.lead.email` = "26mca113@gmail.com"
- `team.members` filled with Kevina, Aayush, Abhishek (emails to be confirmed or set to placeholder contact format)
- `submission.title` = "Supply Chain Disruption Assistant & Fleet Utilisation Optimizer"
- `problem_statement` = 2–3 sentence summary matching README
- `solution_summary` = 2–3 sentence summary of the Bob solution
- `key_features` = 4–5 specific feature strings, no empty strings
- `tech_stack.languages` = ["Python"]
- `tech_stack.frameworks` = ["FastAPI", "IBM Bob SDK"]
- `tech_stack.ibm_technologies` = ["IBM Bob", "watsonx.ai"]
- `tech_stack.databases` = ["SQLite"]
- `tech_stack.other` = ["GitHub Actions", "React", "SQLite"]
- `what_we_are_most_proud_of` and `known_limitations` filled with real text

**Todo List:**
1. Fill `team` block with real values
2. Fill `submission.title`
3. Write `problem_statement` (1–3 sentences, no template text)
4. Write `solution_summary` (1–3 sentences)
5. Fill `key_features` list with 4 non-empty strings
6. Fill `tech_stack` all four arrays
7. Write `what_we_are_most_proud_of`
8. Write `known_limitations`
9. Run YAML syntax check (validate indentation, no orphan template strings)

**Relevant Context:**
- File: `submission.yaml`
- The GitHub Actions workflow at `.github/workflows/validate.yml` checks: team.name, team.track, team.lead.name, team.lead.email, submission.title, problem_statement, solution_summary, key_features length >= 1
- Track must be exactly one of: AI | DevOps | Sustainability | Open

---

### Sub-Task 6 — Rewrite `docs/setup-guide.md`

**Status:** [x] done

**Intent:**
The setup guide is what judges use to run the project locally. It currently has zero real commands. This sub-task replaces all placeholders with real instructions once the tech stack is finalised by sub-tasks 1–5.

**Expected Outcomes:**
- Prerequisites list is accurate and specific (Python version, IBM Bob CLI or SDK, watsonx.ai account)
- Environment Variables table lists only the variables actually used
- Installation block has real, runnable commands
- Running the Application block has real commands with the real port number
- Running Tests section has a real test command
- Quick Demo section shows how to seed simulated disruption/shipment data and run a sample query
- Troubleshooting table has 3 real rows specific to this project

**Todo List:**
1. Update Prerequisites with real requirements (Python 3.11+, IBM Bob CLI, watsonx.ai API key)
2. Update Environment Variables table to match final `.env.example` variables
3. Replace installation code block with real commands
4. Replace running commands with real commands and real port
5. Write Quick Demo block showing a sample disruption scenario
6. Write 3 real troubleshooting rows specific to watsonx.ai and Bob
7. Verify no `[` or `]` placeholder text remains

**Relevant Context:**
- File: `docs/setup-guide.md`
- Depends on final tech stack confirmed in sub-tasks 2–5
- Should be done last, after implementation decisions are locked

---

### Sub-Task 7 — Update `demo/demo-video-link.txt` and `demo/live-demo-url.txt`

**Status:** [x] done

**Intent:**
Both demo files currently contain placeholder URLs that will cause the GitHub Actions validator to fail. They must be updated to reflect the actual demo state — either a real hosted video URL, or a clear "NOT DEPLOYED" / "VIDEO PENDING" declaration that does not trip the placeholder string check.

**Expected Outcomes:**
- `demo/demo-video-link.txt` contains either a real YouTube/Loom/Box URL or the explicit text `VIDEO PENDING — will be added before final submission` (no `your-demo-video-link-here` string)
- `demo/live-demo-url.txt` contains either a real deployed URL or the explicit text `NOT DEPLOYED — run locally using docs/setup-guide.md`
- Neither file contains the original placeholder hostname strings that trigger the validator failure

**Todo List:**
1. Read `demo/demo-video-link.txt` current content
2. Replace placeholder URL with real video URL if available, otherwise use `VIDEO PENDING — will be added before final submission`
3. Read `demo/live-demo-url.txt` current content
4. Replace placeholder URL with `NOT DEPLOYED — run locally using docs/setup-guide.md`
5. Verify neither file contains `your-demo-video-link-here` or `your-live-demo-url-here`

**Relevant Context:**
- Files: `demo/demo-video-link.txt`, `demo/live-demo-url.txt`
- The GitHub Actions validator at `.github/workflows/validate.yml` checks that `demo-video-link.txt` does NOT contain the string `your-demo-video-link-here`
- The live demo URL file is optional — writing "NOT DEPLOYED" is a valid and accepted response

---

### Confirmed Design Decisions

| Decision | Value |
|---|---|
| Backend language | Python |
| AI framework | IBM Bob SDK + watsonx.ai (Granite) |
| Frontend | React dashboard |
| Database | SQLite (local dev, seeded on startup) |
| Data sources | Simulated JSON flat files seeded at startup |
| Severity classification | Generic regulatory thresholds (no specific standard cited) |
| Cold chain standards reference | Generic — "applicable cold chain regulatory thresholds" |

---

### Execution Order

```
Sub-Task 1  →  Sub-Task 2  →  Sub-Task 3
                                    ↓
         Sub-Task 4  ←  Sub-Task 5  ←  Sub-Task 7
                                    ↓
                              Sub-Task 6
```

Sub-tasks 1, 2, and 3 can inform each other and should be done in sequence.
Sub-tasks 4, 5, and 7 all draw from the outputs of 1–3 and can be done in parallel.
Sub-task 6 must come last as it depends on tech stack confirmed in 4 and 5.
