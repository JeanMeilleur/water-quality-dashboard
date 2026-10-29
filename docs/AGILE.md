# AGILE Process – Water Quality Dashboard

**Framework:** Scrum (solo developer, 3 sprints of 1 week)
**Board:** GitHub Projects (Backlog → In Progress → In Review → Done)
**Tracking:** GitHub Issues, one issue per user story, closed by commit message

---

## Roles

| Role | Who |
|---|---|
| Product Owner | Prof. Gregory Reis (assignment requirements) |
| Scrum Master / Developer | [Your name] |
| End user | A researcher or student who needs to read a water quality CSV without writing code |

---

## Product Backlog

| ID | User Story | Priority | Points | Sprint | Status |
|---|---|---|---|---|---|
| US-01 | As a user, I want the app to load a water quality dataset so I can see data immediately | High | 2 | 1 | Done |
| US-02 | As a user, I want to upload my own CSV so I can analyze my own readings | High | 3 | 1 | Done |
| US-03 | As a user, I want to see the raw table and summary stats so I can verify the data | High | 2 | 1 | Done |
| US-04 | As a user, I want to pick which columns appear so the table isn't overwhelming | Medium | 2 | 1 | Done |
| US-05 | As a user, I want to plot any parameter over time so I can spot trends | High | 3 | 2 | Done |
| US-06 | As a user, I want to compare two parameters on a scatter plot so I can see relationships | High | 3 | 2 | Done |
| US-07 | As a user, I want to see the readings on a map so I know where they were taken | High | 3 | 2 | Done |
| US-08 | As a user, I want to filter the range of readings so I can focus on part of the run | Medium | 2 | 2 | Done |
| US-09 | As a user, I want plain-English insights so I don't have to interpret stats myself | Medium | 3 | 3 | Done |
| US-10 | As a user, I want clear sections and explanations so I know what I'm looking at | Medium | 2 | 3 | Done |
| US-11 | As a developer, I need the app deployed publicly so anyone can use it | High | 3 | 3 | Done |
| US-12 | As a developer, I need a README so others can run and understand the project | High | 2 | 3 | Done |

**Total: 30 story points across 3 sprints.**

---

## Sprint 1 — Data foundation (Oct 13 – Oct 19, 2026)

**Sprint goal:** The app loads data, displays it, and lets the user swap in their own file.
**Committed:** US-01, US-02, US-03, US-04 (9 points)

| Day | Standup: done / next / blockers |
|---|---|
| Mon | Repo and venv created / build base Streamlit layout / none |
| Wed | CSV loads, title and headers in place / add file uploader / hardcoded Windows path won't survive deploy |
| Fri | Uploader works, fallback moved to relative `data/` path / add multiselect for columns / none |
| Sun | Data tab complete with stats toggle / close sprint / none |

**Sprint review:** All 4 stories accepted. Data tab usable end to end.
**Retrospective:**
- *Went well:* caching with `@st.cache_data` made reloads instant.
- *Went wrong:* the absolute Windows path would have crashed the deployed app. Fixed with `pathlib`.
- *Action:* never hardcode a local path again — anything the app reads ships inside the repo.

---

## Sprint 2 — Visualization (Oct 20 – Oct 26, 2026)

**Sprint goal:** The user can plot any parameter and see the readings geographically.
**Committed:** US-05, US-06, US-07, US-08 (11 points)

| Day | Standup: done / next / blockers |
|---|---|
| Mon | Line chart with parameter dropdown / wire the Y axis dynamically / selectbox was listing non-numeric columns |
| Wed | Numeric-only column helper written / build scatter with X, Y, color pickers / none |
| Fri | Scatter and 3D plots done / build the map / `px.scatter_map` needs Plotly 6 |
| Sun | Map done, centered on data mean; row slider added / close sprint / none |

**Sprint review:** All 4 stories accepted. Every chart now reacts to user input.
**Retrospective:**
- *Went well:* filtering the selectbox to numeric columns killed a whole class of crashes.
- *Went wrong:* Plotly version mismatch broke the map locally.
- *Action:* pin minimum versions in `requirements.txt` before deploying.

---

## Sprint 3 — Insights, documentation, deployment (Oct 27 – Nov 2, 2026)

**Sprint goal:** The app explains itself and is publicly reachable.
**Committed:** US-09, US-10, US-11, US-12 (10 points)

| Day | Standup: done / next / blockers |
|---|---|
| Mon | Overview tab and captions written / build insights metrics / none |
| Wed | Summary stats and correlation matrix done / write README / none |
| Fri | README and requirements.txt finished / deploy to Streamlit Cloud / none |
| Sun | App live, URL verified in a fresh browser / submit / none |

**Sprint review:** All stories accepted. Public URL confirmed working.
**Retrospective:**
- *Went well:* writing captions under every chart exposed two charts that had no real purpose.
- *Went wrong:* first deploy failed because `requirements.txt` was missing Plotly.
- *Action:* test a clean `pip install -r requirements.txt` in a fresh venv before every deploy.

---

## Definition of Done

A story is Done when:
1. The feature works with the default dataset **and** an uploaded CSV
2. It does not crash when a column is missing or a value is null
3. Every chart has a title, axis labels, and a legend
4. There is explanatory text for the end user
5. The code is committed and pushed, and the issue is closed