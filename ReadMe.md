# Game of Thrones: The Last Claimant

משחקי הכס: הטוען האחרון לכתר

A Hebrew-first, right-to-left interactive presentation that places the player in the role of a claimant to the Iron Throne. Its goal is to combine visual storytelling with consequential choices: explore Westeros, establish an allegiance, choose a governing doctrine, and discover the realm and ruler those decisions produce.

The experience contains **10 interactive slides, two major player decisions, and 16 faction/doctrine combinations leading to 8 unique endings**. The presentation runs in the browser; Python maintains the canonical game data and validates the finite decision paths during development.

[GitHub repository](https://github.com/sspirogan/game-of-thrones)

<!-- Screenshot placeholder: Opening slide with the Iron Throne and the start button. Future GitHub-hosted attachment URL: SLIDE_01_GITHUB_ATTACHMENT_URL. -->

Slide 01: The Iron Throne introduces the player's claim.

## Getting Started

Download the repository and open `index.html` in a modern browser with JavaScript enabled. The HTML already includes its game data; no Python execution, package installation, build step, or backend is required to view the presentation.

The full visual experience depends on external Three.js and Google Fonts requests unless those resources are cached. CSS graphics and system-font fallbacks are implemented, but local-file loading, offline behavior, and fallback operation remain unverified in the browser.

## Repository Contents

| Path | Purpose |
| :--- | :--- |
| `index.html` | Browser presentation containing ten slides, inline CSS, SVG artwork, embedded `GAME_DATA`, application logic, and Three.js scene code. |
| `build_data.py` | Standard-library Python tool that defines canonical data, validates decision paths and metrics, and optionally replaces the embedded data block in `index.html`. |
| `PRD.md` | Product requirements, slide specifications, implementation notes, and outstanding verification work. |
| `README.md` | Root-level project overview, opening instructions, architecture, validation evidence, and media. |

## Experience Overview

| Slide | Experience | Interaction |
| :--- | :--- | :--- |
| 01 | The Throne Awaits | Begin the journey and optionally expand the opening lore. |
| 02 | Map of the Seven Kingdoms | Select among five represented regions to update the information panel. |
| 03 | The Great Houses and the Order | Explore nine noble houses and a separate Night's Watch profile. |
| 04 | Fire and Blood | Adjust dragonfire intensity with a slider or preset buttons. |
| 05 | Winter Is Coming | Toggle the frost-themed reveal to read the hidden prophecy. |
| 06 | Choose Your Allegiance | Answer a three-question quiz to determine the first major decision: faction allegiance. |
| 07 | The Great War | View the faction-specific battle banner and highlight a front card; this does not simulate combat or affect the ending. |
| 08 | The Governing Doctrine | Make the second major decision by selecting one of four doctrines. |
| 09 | The Fate of the Realm | View calculated stability, prosperity, and defense gauges. |
| 10 | The Coronation | Reveal the resulting ruler archetype and chronicle, or restart the journey. |

The house gallery is not a ten-faction selection screen. Its nine noble houses and separate Night's Watch entry provide lore; the decision system has only four playable affiliations.

### Navigation and Replay

| Control | Action |
| :--- | :--- |
| Next / Previous buttons | Move between slides, subject to decision prerequisites. |
| Left Arrow, Space, or Page Down | Request the next slide, subject to decision prerequisites and keyboard-handling rules. |
| Right Arrow or Page Up | Go back. |
| `1` to `9`, and `0` | Request slides 01 to 09, and slide 10 respectively. |
| Jump dots | Request a particular slide using the same prerequisite checks. |
| Horizontal swipe | Swipe left to advance or right to go back when horizontal displacement exceeds 55 pixels and is more than 1.5 times vertical displacement; gestures starting on inputs, buttons, custom button-role controls, or lore drawers are ignored. |
| Restart on slide 10 | Clear answers and choices, restore the initial interface, relock decision gates, and return to slide 01. |

Slides 07 and 08 require a resolved faction, while slides 09 and 10 require both faction and doctrine. The header brand returns to slide 01 without clearing the current choices; a full restart or page reload clears the in-memory journey.

Global slide shortcuts ignore editable fields, already-handled events, and Alt/Ctrl/Meta combinations. Space does not also advance when focus is on a button, custom button-role control, or link; Enter and Space activate custom button-role controls.

## Decisions and Endings

- **Allegiance, slide 06:** Three questions each offer four answers. Each answer awards three points to Targaryen, Stark, Lannister, or the Night's Watch.
- **Doctrine, slide 08:** Choose Iron Fist & Absolute Order (`iron_fist`), Just Law & Realm Reform (`just_law`), Vigilant Guardian & Border Shield (`guard`), or Pragmatic Commerce & Diplomacy (`commerce`).

The highest quiz score determines allegiance. Ties favor the third answer's faction if it is among the tied leaders, then apply the same check to the second answer; the final fallback selects the first tied faction in the order Targaryen, Stark, Lannister, Night's Watch.

The first two answers immediately advance the quiz, and the third resolves allegiance. The final question remains selectable and can change the result, and the doctrine can also be changed; there is no interface for editing the first two answers.

The resulting faction and doctrine are looked up in the following matrix. Multiple combinations deliberately share an ending, so the 16 combinations are not 16 distinct endings.

| Faction | Iron Fist | Just Law | Border Shield | Commerce |
| :--- | :--- | :--- | :--- | :--- |
| Targaryen | ARC-01 | ARC-08 | ARC-07 | ARC-08 |
| Stark | ARC-06 | ARC-02 | ARC-04 | ARC-05 |
| Lannister | ARC-06 | ARC-05 | ARC-08 | ARC-03 |
| Night's Watch | ARC-06 | ARC-04 | ARC-04 | ARC-08 |

| Ending | Ruler archetype |
| :--- | :--- |
| ARC-01 | The Eternal Dragon Sovereign |
| ARC-02 | The Lawgiver of the North |
| ARC-03 | The Lord of Shadows and Gold |
| ARC-04 | The Sovereign Shield of the Living |
| ARC-05 | The Just Arbitrator |
| ARC-06 | The Ashen Tyrant / Lord of the Bastion |
| ARC-07 | The Mystic Warden |
| ARC-08 | The Pragmatic Restorer |

Slide 09 calculates fictional realm metrics from faction base values and doctrine modifiers: stability is clamped to 30–98%, prosperity to 20–95%, and defense to 40–99%. These gauges are game mechanics, not real-world measurements; slide 10 uses the decision matrix to select the narrative ending.

## Browser Architecture and Dependencies

The application is packaged as one HTML document containing vanilla JavaScript, inline styles, SVG illustrations, and procedural Three.js geometry and textures. Its source implements navigation, quiz scoring, doctrine selection, metrics, ending selection, and replay entirely on the client.

- **`GAME_DATA`:** Embedded data supplies faction profiles, gallery lore, regions, quiz questions, doctrines, the decision matrix, and eight ending records.
- **`AppState`:** Holds the current slide, answers, decisions, visual settings, and results in memory. There is no saved-game persistence, database, or runtime Python process.
- **`PresentationEngine`:** Controls navigation, decision gates, interactive panels, scoring, results, focus updates, and restart.
- **`ThreeSceneManager`:** When graphics initialization succeeds, builds ten slide-specific groups in one shared Three.js scene. Only the active slide's group is visible, animated systems skip updates for inactive groups, and hidden groups remain allocated rather than being unloaded.

The HTML requests Three.js r128 from cdnjs and Google Fonts for Frank Ruhl Libre, Heebo, Cinzel, Cinzel Decorative, and Courier Prime. These are external dependencies, not bundled resources; missing Three.js, graphics-initialization failure, rendering exceptions, and WebGL context loss route to a CSS fallback, with a separate context-restoration handler.

The source includes Hebrew RTL markup, keyboard activation for custom controls, focus styling, and inactive-slide `inert`/`aria-hidden` handling. Reduced-motion handling disables CSS animation and transitions, replaces continuous Three.js animation with static redraws, and makes restart immediate rather than using the normal two 400 ms replay phases.

## Python Data Generation and Validation

`build_data.py` uses only Python 3's standard library: `sys`, `json`, `re`, and `pathlib`. Its canonical dictionary contains metadata, four playable factions, ten gallery records representing nine houses plus the Watch, five regions, three quiz questions, four doctrines, the decision matrix, and eight archetypes.

### Validate Without Changing HTML

From the repository root, run:

```bash
python3 build_data.py --verify-only
```

This command evaluates all 16 faction/doctrine combinations, asserts that the Python metric results stay within their clamp ranges, and checks that every declared archetype is reachable. It also enumerates all 64 three-answer quiz paths, asserts a valid faction winner for each, and reports the resolution counts.

The flag exits before HTML injection and does not write `index.html`, compare embedded data with the Python dictionary, check injection delimiters, or execute JavaScript. Quiz results are checked for valid factions rather than independently specified expected winners, and per-faction counts are reported rather than separately asserted.

### Regenerate the Embedded Data

After intentionally changing canonical data, run:

```bash
python3 build_data.py
```

**A successful generation run rewrites `index.html`.** After validation, the script serializes `GAME_DATA` with `json.dumps(..., ensure_ascii=False, indent=2)` and uses a regular expression to replace the marked data block in the `index.html` beside the script, regardless of the current working directory:

```javascript
/* --- PYTHON_DATA_START --- */
const GAME_DATA = { /* generated data */ };
/* --- PYTHON_DATA_END --- */
```

Python generates the embedded data payload, not the entire presentation, its artwork, or its interaction code. Gallery structure and doctrine-card markup remain authored in HTML, while metric and quiz algorithms have separate Python and JavaScript implementations; data generation alone does not synchronize every part of the interface.

### Actual Validation Results

A verification run against the supplied files completed with exit status `0`. The verify-only command reported that `index.html` was not modified; the data-generation write path was not run.

The following is an excerpt of the actual standard output:

```text
  [PASS] 16/16 Faction x Doctrine combinations evaluated.
  [PASS] All stability, prosperity, and defense metrics within PRD clamp ranges.
  [PASS] All 8 canonical ruling archetypes (ARC-01 to ARC-08) are fully reachable!
  [PASS] 64/64 Quiz answer permutations resolved deterministically.
         - Targaryen   : 16 resolutions (25.0%)
         - Stark       : 16 resolutions (25.0%)
         - Lannister   : 16 resolutions (25.0%)
         - Watch       : 16 resolutions (25.0%)

ALL 16 COMBINATORIAL OUTCOMES AND 64 QUIZ PATHS PASSED WITH 100% COVERAGE.

[INFO] --verify-only flag detected. Target index.html was NOT modified.
```

The script's “100% coverage” message refers only to the enumerated Python combinations and quiz paths. It is not measured application code coverage and does not establish JavaScript parity, browser behavior, accessibility, visual quality, or performance.

The interpreter also emitted a `SyntaxWarning` for an invalid `\B` escape in the script's historical Windows-path docstring. The warning is visible in the supplied terminal screenshot and did not prevent the successful validation run.

<!-- Screenshot placeholder: Actual terminal screenshot showing Python verify-only validation results. Future GitHub-hosted attachment URL: PYTHON_VALIDATION_GITHUB_ATTACHMENT_URL. -->

Python validation: the supplied terminal capture shows passing combination, metric-range, archetype-reachability, and quiz-path checks.

The terminal screenshot contains local account and filesystem details outside the validation results. Before making it public, consider cropping that surrounding context while preserving the command, warning, and actual results.

## AI-Assisted Development Process

AI supported requirements drafting, critical review, front-end implementation, Python tooling, and documentation refinement. Development proceeded through focused iterations, with the developer defining the scope, evaluating outputs, and directing corrections rather than relying on a single generated solution.

### Development Stages and Iterations

- **Requirements and critical review:** The initial PRD established the narrative, Hebrew RTL presentation, single-file architecture, and two-decision model. Repeated Red Team reviews challenged navigation consistency, quiz tie-breaking, decision gates, metric formulas, and the Python integration contract before implementation progressed.
- **Working foundation:** The first implementation established the ten-slide presentation, navigation, styling, state management, and interactive decision flow. More advanced graphics and the separate Python pipeline were reserved for subsequent work.
- **Visual storytelling:** Feedback redirected the presentation away from lengthy text toward concise Hebrew messages, interactive exploration, visual decision cards, and optional lore drawers. The house gallery was expanded while keeping the Night's Watch separate.
- **Graphics and data engineering:** AI helped implement slide-specific Three.js scene code and `build_data.py` for offline data preparation and validation, while JavaScript retained browser interactions. Existing scoring rules, formulas, and ending mappings were explicit preservation constraints.
- **Targeted repairs:** Further prompts addressed oversized artwork, unclear silhouettes, square-looking particles, overlapping scene groups, incomplete restart behavior, keyboard interaction, synchronized flame controls, reduced motion, and graphics-failure handling.
- **Documentation alignment:** Subsequent reviews reconciled the PRD and README with the source, preserving observed Python results while distinguishing implemented features from behavior still requiring browser verification.

### Representative Prompts and Technical Decisions

- **Specification-led implementation:** “Before writing any code, read the existing `PRD.md` file carefully.” The PRD served as the starting specification, with discrepancies flagged for review.
- **Visual clarity:** “Show, don't tell.” Later feedback emphasized recognizable subjects and purposeful interaction rather than technical complexity or decorative effects alone.
- **Preservation of working behavior:** “Do not rebuild the project or change its working game logic.” Visual and technical revisions were constrained to retain the established presentation and decision system.
- **Evidence-aware validation:** “Clearly distinguish code inspection, mock tests and browser tests.” Review instructions required unavailable checks to be reported rather than presented as completed verification.

### Human-AI Collaboration

The developer supplied the creative direction, identified shortcomings, requested independent reviews, and controlled file-change and Git permissions. AI proposed and implemented revisions within those instructions; later reviews also challenged earlier AI descriptions and corrected unsupported claims.

The process combined generation, critique, targeted repair, and documentation review. AI completion reports were not treated as a substitute for source inspection, recorded validation output, or browser testing.

Full conversation record: [AI_Interaction_Log(1_6).docx](./AI_Interaction_Log%281_6%29.docx), containing the prompts, review exchanges, and recorded development reports.

## Presentation Screenshots

The opening-slide caption appears at the top of this README. The captions below identify the supplied captures of the lore gallery, winter interaction, allegiance result, realm gauges, and final coronation.

<!-- Screenshot placeholder: Slide 03 showing nine noble-house shields and a separate Night's Watch panel. Future GitHub-hosted attachment URL: SLIDE_03_GITHUB_ATTACHMENT_URL. -->

Slide 03: Nine noble houses appear above the independent Night's Watch entry.

<!-- Screenshot placeholder: Slide 05 showing the Wall and the frost-reveal button. Future GitHub-hosted attachment URL: SLIDE_05_GITHUB_ATTACHMENT_URL. -->

Slide 05: The winter scene offers a button to reveal the hidden prophecy.

<!-- Screenshot placeholder: Slide 06 showing the third quiz question and a resolved Targaryen allegiance. Future GitHub-hosted attachment URL: SLIDE_06_GITHUB_ATTACHMENT_URL. -->

Slide 06: The three-question allegiance quiz resolves to House Targaryen in this captured playthrough.

<!-- Screenshot placeholder: Slide 09 showing 65 percent stability, 70 percent prosperity, and 75 percent defense. Future GitHub-hosted attachment URL: SLIDE_09_GITHUB_ATTACHMENT_URL. -->

Slide 09: This captured result displays 65% stability, 70% prosperity, and 75% defense.

<!-- Screenshot placeholder: Slide 10 showing The Pragmatic Restorer ending and the restart button. Future GitHub-hosted attachment URL: SLIDE_10_GITHUB_ATTACHMENT_URL. -->

Slide 10: The coronation reveals The Pragmatic Restorer and offers a new journey.

## Demo Video

<!-- Video placeholder: DEMO_VIDEO_GITHUB_URL. Add the future GitHub-hosted video URL here when available; no video URL has been supplied, so no live video preview is embedded. -->

Suggested caption: “Project demo: a journey from the Iron Throne through allegiance and doctrine to the final coronation.”

## Known Limitations and Verification Status

Python validation results above are observed terminal results; browser behavior is documented from the supplied source and screenshots, not a runtime acceptance test. Browser/device compatibility, offline fallback, WebGL recovery, accessibility, and performance remain unverified, and WCAG AA compliance is not claimed.

See `PRD.md`, sections 12, 13, 15, and 17, for detailed validation boundaries, injection limitations, accessibility and touch-scrolling gaps, and the acceptance-test plan. No live deployment is claimed.
