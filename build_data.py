#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game of Thrones — The Last Claimant (משחקי הכס — הטוען האחרון לכתר)
Data Engineering, Algorithmic Matrix Validation & Injection Pipeline
Author: Senior Technical Architect & AI Pipeline Engineer
Working Directory: C:\BIU01\HW\1
"""

import sys
import json
import re
from pathlib import Path

# ==============================================================================
# CANONICAL GAME DATA (PRD Section 7, 8, 12)
# ==============================================================================

GAME_DATA = {
    "metadata": {
        "title": "משחקי הכס — הטוען האחרון לכתר",
        "titleEn": "Game of Thrones — The Last Claimant",
        "version": "1.2.0",
        "slideCount": 10
    },
    "houses": {
        "targaryen": {
            "nameHe": "בית טארגאריין",
            "nameEn": "House Targaryen",
            "mottoHe": "אש ודם",
            "mottoEn": "Fire and Blood",
            "color": "#FF5722",
            "theme": "dragonfire"
        },
        "stark": {
            "nameHe": "בית סטארק",
            "nameEn": "House Stark",
            "mottoHe": "החורף מתקרב",
            "mottoEn": "Winter Is Coming",
            "color": "#00E5FF",
            "theme": "ice"
        },
        "lannister": {
            "nameHe": "בית לאניסטר",
            "nameEn": "House Lannister",
            "mottoHe": "שמעו את שאגתי!",
            "mottoEn": "Hear Me Roar!",
            "color": "#D4AF37",
            "theme": "gold"
        },
        "watch": {
            "nameHe": "מסדר משמר הלילה",
            "nameEn": "The Order of the Night's Watch",
            "mottoHe": "המגן על ממלכות האדם",
            "mottoEn": "The Shield that Guards the Realms of Men",
            "color": "#9E9E9E",
            "theme": "shadow"
        }
    },
    "nineHouses": {
        "stark": {
            "nameHe": "בית סטארק",
            "seatHe": "ווינטרפל",
            "mottoHe": "החורף מתקרב",
            "descHe": "כבוד, חוסן נפשי ונאמנות לשבועות הצפון.",
            "color": "#00E5FF"
        },
        "targaryen": {
            "nameHe": "בית טארגאריין",
            "seatHe": "דרגונסטון",
            "mottoHe": "אש ודם",
            "descHe": "עוצמה דרקונית מוחלטת ומורשת ואליריאנית.",
            "color": "#FF5722"
        },
        "lannister": {
            "nameHe": "בית לאניסטר",
            "seatHe": "צוק קאסטרלי",
            "mottoHe": "שמעו את שאגתי!",
            "descHe": "עושר בלתי נדלה, עורמה פוליטית ותחכום.",
            "color": "#D4AF37"
        },
        "baratheon": {
            "nameHe": "בית באראתיאון",
            "seatHe": "קץ-סופה",
            "mottoHe": "שלנו הוא הזעם",
            "descHe": "עוצמת שדה קרב סוחפת וזעם לוחמים.",
            "color": "#FBC02D"
        },
        "greyjoy": {
            "nameHe": "בית גרייג'וי",
            "seatHe": "פייק",
            "mottoHe": "איננו זורעים",
            "descHe": "שליטי איי הברזל ועוצמה ימית פראית.",
            "color": "#FFB300"
        },
        "tyrell": {
            "nameHe": "בית טיירל",
            "seatHe": "רמות גן",
            "mottoHe": "גדלים בעוצמה",
            "descHe": "אבירות מפוארת, שפע חקלאי ודיפלומטיה.",
            "color": "#4CAF50"
        },
        "martell": {
            "nameHe": "בית מארטל",
            "seatHe": "סאנספיר",
            "mottoHe": "בלתי מורכן, בלתי מנוצח",
            "descHe": "גאוות מדבר עקשנית ולוחמת גרילה.",
            "color": "#E64A19"
        },
        "tully": {
            "nameHe": "בית טאלי",
            "seatHe": "נהרן",
            "mottoHe": "משפחה, חובה, כבוד",
            "descHe": "ביצורי מים ואסטרטגיית נהרות חכמה.",
            "color": "#0288D1"
        },
        "arryn": {
            "nameHe": "בית ארין",
            "seatHe": "קן הנשרים",
            "mottoHe": "גבוה ככבוד",
            "descHe": "מבצר קן הנשרים הבלתי חדיר בין העננים.",
            "color": "#81D4FA"
        },
        "watch": {
            "nameHe": "משמר הלילה",
            "seatHe": "טירת שחור",
            "mottoHe": "המגן על ממלכות האדם",
            "descHe": "שבועת נצח עצמאית על חומת הקרח.",
            "color": "#9E9E9E"
        }
    },
    "regions": [
        {
            "id": "north",
            "nameHe": "הצפון הגדול — ווינטרפל",
            "badge": "חבל ארץ // הצפון",
            "lore": "המרחב הגדול ביותר בווסטרוז, עטוף בכפור עתיק ויערות סודיים. אנשי הצפון זוכרים שבועות.",
            "army": "45,000 חרבות",
            "pct": 70,
            "color": "#00E5FF"
        },
        {
            "id": "riverlands",
            "nameHe": "ארצות הנהר — נהרן",
            "badge": "חבל ארץ // המרכז האסטרטגי",
            "lore": "צומת הדרכים המבוצר של הממלכה, מרושת בנהרות אדירים וטירות מים.",
            "army": "35,000 חרבות",
            "pct": 55,
            "color": "#29B6F6"
        },
        {
            "id": "reach",
            "nameHe": "מישור המשגב — רמות גן",
            "badge": "חבל ארץ // הדרום-מערב הפורה",
            "lore": "אסם התבואה של וסטרוז, עושר חקלאי וצי פרשים מפואר.",
            "army": "70,000 פרשים",
            "pct": 95,
            "color": "#66BB6A"
        },
        {
            "id": "dorne",
            "nameHe": "דורן — סאנספיר",
            "badge": "חבל ארץ // הדרום הלוהט",
            "lore": "מדבריות חמים ותרבות גאה שלא נכבשה מעולם בחרב.",
            "army": "30,000 לוחמים",
            "pct": 50,
            "color": "#FFA726"
        },
        {
            "id": "kings_landing",
            "nameHe": "מעלה המלך — המבצר האדום",
            "badge": "חבל ארץ // בירת הממלכה",
            "lore": "לב הכוח הפוליטי וכס הברזל. כאן נקבעים גורלות שבע הממלכות.",
            "army": "משמר העיר (6,000)",
            "pct": 40,
            "color": "#D4AF37"
        }
    ],
    "quizQuestions": [
        {
            "id": "q1",
            "title": "שאלה 1 מתוך 3: משבר המצור",
            "prompt": "האויב צר על חומותיך ואנשיך רעבים. כיצד תפעל?",
            "options": [
                { "text": "שורף את קווי האספקה שלו באש דרקון חסרת רחמים.", "faction": "targaryen" },
                { "text": "מוביל פשיטת לילה אמיצה ומגן על החלשים בגופי.", "faction": "stark" },
                { "text": "משלם לשכירי חרב שיתקפו את עורף האויב בזהב.", "faction": "lannister" },
                { "text": "מחזיק מעמד בחומות ומקריב הכול למען המשמר.", "faction": "watch" }
            ]
        },
        {
            "id": "q2",
            "title": "שאלה 2 מתוך 3: צדק מול תועלת",
            "prompt": "לורד בעל צבא בגד בשבועה, אך חייליו נחוצים לקרב. מה דינו?",
            "options": [
                { "text": "כורת את ראשו מיד; הכבוד והדין קודמים לכל תועלת.", "faction": "stark" },
                { "text": "מאיים עליו בדרקונים ומאלץ אותו להישבע מחדש בדם.", "faction": "targaryen" },
                { "text": "מוחל לו תמורת מס זהב כבד ובני ערובה להבטחת ציות.", "faction": "lannister" },
                { "text": "שולח אותו לגלות נצחית אל החומה, ללא תואר ואדמה.", "faction": "watch" }
            ]
        },
        {
            "id": "q3",
            "title": "שאלה 3 מתוך 3: ההקרבה העליונה",
            "prompt": "אימה עתיקה מתעוררת בצפון הקפוא. במה תשקיע את כוחותיך?",
            "options": [
                { "text": "מגייס את כל מסדרי הממלכה לביצור החומה; האיום קודם לכתר.", "faction": "watch" },
                { "text": "רותם את אש הדרקונים להשמדת האויב העל-טבעי.", "faction": "targaryen" },
                { "text": "מאחד את צבאות הצפון במסדר כבוד ומגן בחרב פלדה.", "faction": "stark" },
                { "text": "מממן קווי אספקה ומבצרי אבן עורפיים בעזרת אוצר הממלכה.", "faction": "lannister" }
            ]
        }
    ],
    "doctrines": {
        "iron_fist": {
            "titleHe": "אש וברזל",
            "titleEn": "Iron Fist & Absolute Order",
            "descHe": "שלטון ריכוזי, דיכוי מרידות ומשמעת ברזל כערובה לשלום."
        },
        "just_law": {
            "titleHe": "צדק ורפורמה",
            "titleEn": "Just Law & Realm Reform",
            "descHe": "פירוק מוקדי כוח ישנים ומשפט הוגן לכל אזרח בממלכה."
        },
        "guard": {
            "titleHe": "מגן הגבולות",
            "titleEn": "Vigilant Guardian & Border Shield",
            "descHe": "הפניית כלל משאבי הממלכה לביצור החומה מפני איומי חורף."
        },
        "commerce": {
            "titleHe": "שגשוג ומסחר",
            "titleEn": "Pragmatic Commerce & Diplomacy",
            "descHe": "פתיחת נתיבי סחר עם אסוס ויצירת שלום דרך תלות כלכלית."
        }
    },
    "decisionMatrix": {
        "targaryen": { "iron_fist": "ARC-01", "just_law": "ARC-08", "guard": "ARC-07", "commerce": "ARC-08" },
        "stark":     { "iron_fist": "ARC-06", "just_law": "ARC-02", "guard": "ARC-04", "commerce": "ARC-05" },
        "lannister": { "iron_fist": "ARC-06", "just_law": "ARC-05", "guard": "ARC-08", "commerce": "ARC-03" },
        "watch":     { "iron_fist": "ARC-06", "just_law": "ARC-04", "guard": "ARC-04", "commerce": "ARC-08" }
    },
    "archetypes": {
        "ARC-01": {
            "titleHe": "שליט הדרקונים הנצחי",
            "titleEn": "The Eternal Dragon Sovereign",
            "summary": "שלום של מורא מוחלט. שבע הממלכות מאוחדות תחת צל כנפי הדרקונים.",
            "chronicle": "שליטה מוחלטת בכוח האש. הממלכה מאוחדת תחת מורא כבד, מרידות מדוכאות באיבן, ושבע הממלכות חוות שלום של צייתנות מוחלטת. צללי הדרקונים בשמי מעלה המלך מהווים תזכורת תמידית לכך ששום התקוממות לא תעבור ללא עונש צורב."
        },
        "ARC-02": {
            "titleHe": "המלך החוקק של הצפון",
            "titleEn": "The Lawgiver of the North",
            "summary": "עידן של צדק ויושרה שבו החוק שווה מאיכר ועד אחרון הלורדים.",
            "chronicle": "עידן של צדק, יושרה וסדר חוקתי חדש. חוקי הממלכה שווים לכל נפש, השחיתות נעקרת ממוסדות השלטון, ושמך נזכר לדורות כמגן החלשים וההוגן במלכי וסטרוז. תחת שלטונך, הכבוד והאמת הפכו לעמודי התווך של החברה."
        },
        "ARC-03": {
            "titleHe": "אדון הצללים והזהב",
            "titleEn": "The Lord of Shadows and Gold",
            "summary": "כס הברזל הופך למרכז הפיננסי של העולם הידוע.",
            "chronicle": "כס הברזל הופך למרכז הפיננסי והמסחרי של העולם הידוע. בריתות נרכשות בזהב, אויבים מנוטרלים בחשאי עוד לפני שהניפו חרב, ושגשוג כלכלי חסר תקדים שוטף את ערי הנמל. הוכחת כי כוחו של המטבע גדול מכל חרב."
        },
        "ARC-04": {
            "titleHe": "מגן האנושות הנשגב",
            "titleEn": "The Sovereign Shield of the Living",
            "summary": "כל עוצמת הממלכה מופנית לביצור החומה והדפת החשכה לתמיד.",
            "chronicle": "כל עוצמת הממלכה מופנית להגנת החיים מפני החשכה. החומה מבוצרת במבצרי גרניט חדשים, משמר הלילה הופך לצבא העילית של הממלכה, והחשכה שמעבר לגבול נהדפת לתמיד. שלטונך ייזכר כעידן שבו האנושות ניצחה את הכליה."
        },
        "ARC-05": {
            "titleHe": "הבורר הצודק של שבע הממלכות",
            "titleEn": "The Just Arbitrator",
            "summary": "מועצה עליונה משותפת המאזנת בין אצולה לזכויות העם.",
            "chronicle": "הקמת מועצה עליונה משותפת לכל בתי האב הגדולים. שלטון מאוזן הפורק מתיחויות מעמדיות, מעגן זכויות אזרחיות לכל שכבות העם, ומבטיח כי שום בית יחיד לא יוכל שוב לרדות בממלכה כולה."
        },
        "ARC-06": {
            "titleHe": "רודן הברזל והאפר",
            "titleEn": "The Ashen Tyrant / Lord of the Bastion",
            "summary": "סדר נוקשה הנאכף בחומות ברזל ובגרדומים בכיכרות.",
            "chronicle": "סדר נוקשה ואכזרי המושג בחומות ברזל ובגרדומים בכיכרות העיר. הפחד שזרעת מגן על וסטרוז מפני כאוס ואיומים חיצוניים, אך המחיר ששולם הוא שממה תרבותית ושתיקה רועמת בצללים."
        },
        "ARC-07": {
            "titleHe": "שומר הסודות והכשף",
            "titleEn": "The Mystic Warden",
            "summary": "תחיית הקסם הואליריאני ולחשי מגן קדומים להגנת הממלכה.",
            "chronicle": "תחיית הקסם העתיק והידע הואליריאני ברחבי הממלכה. לחשי מגן, פלדה ואליריאנית ונבואות קדומות חוברים יחד לשמירה על שלום וסטרוז מפני כוחות קוסמיים ואיומים שמעבר להבנת בני התמותה."
        },
        "ARC-08": {
            "titleHe": "משקם ההריסות הפרגמטי",
            "titleEn": "The Pragmatic Restorer",
            "summary": "בנייה מחדש סבלנית של הערים החרבות ופיוס בין הבתים.",
            "chronicle": "בנייה מחדש סבלנית של הערים החרבות, חידוש קווי הסחר העולמיים עם הערים החופשיות באסוס, ופיוס הדרגתי ועקבי בין כל הבתים המסוכסכים. שלטונך הניח את היסודות לריפוי פצעי המלחמה."
        }
    }
}

# ==============================================================================
# ALGORITHMIC METRICS ENGINE & VALIDATION SUITE (PRD Section 7 & 9)
# ==============================================================================

def calculate_metrics(faction: str, doctrine: str):
    """
    Computes Political Stability, People's Prosperity, and Defense Readiness
    strictly adhering to PRD mathematical formulas.
    """
    # 1. Political Stability
    base_stab = {"targaryen": 65, "stark": 85, "lannister": 80, "watch": 75}[faction]
    stab_mods = {
        "iron_fist": {"targaryen": 15, "lannister": 10, "stark": -15, "watch": -10},
        "just_law":  {"stark": 15, "watch": 10, "lannister": 5, "targaryen": -10},
        "guard":     {"watch": 15, "stark": 10, "lannister": -5, "targaryen": 0},
        "commerce":  {"lannister": 15, "stark": 5, "targaryen": 0, "watch": -15}
    }
    stab = max(30, min(98, base_stab + stab_mods[doctrine][faction]))

    # 2. People's Prosperity
    base_prosp = {"lannister": 75, "stark": 70, "watch": 50, "targaryen": 45}[faction]
    prosp_bonus = {"commerce": 25, "just_law": 20, "guard": 5, "iron_fist": -20}[doctrine]
    prosp = max(20, min(95, base_prosp + prosp_bonus))

    # 3. Defense Readiness
    base_def = {"watch": 95, "targaryen": 90, "stark": 85, "lannister": 65}[faction]
    def_bonus = {"guard": 25, "iron_fist": 15, "just_law": 5, "commerce": -15}[doctrine]
    defe = max(40, min(99, base_def + def_bonus))

    return {"stability": stab, "prosperity": prosp, "defense": defe}


def simulate_tie_breaker(q1_idx: int, q2_idx: int, q3_idx: int) -> str:
    """
    Simulates the deterministic tie-breaking logic specified in PRD 7 & 8:
    1. Highest score
    2. Tie-break: Question 3 choice
    3. Secondary: Question 2 choice
    4. Canonical fallback: Targaryen > Stark > Lannister > Night's Watch
    """
    questions = GAME_DATA["quizQuestions"]
    factions = ["targaryen", "stark", "lannister", "watch"]
    scores = {f: 0 for f in factions}

    picks = [
        questions[0]["options"][q1_idx]["faction"],
        questions[1]["options"][q2_idx]["faction"],
        questions[2]["options"][q3_idx]["faction"]
    ]

    for p in picks:
        scores[p] += 3

    max_score = max(scores.values())
    tied = [f for f, s in scores.items() if s == max_score]

    if len(tied) == 1:
        return tied[0]

    # Rule 1: Question 3 priority
    if picks[2] in tied:
        return picks[2]
    # Rule 2: Question 2 priority
    if picks[1] in tied:
        return picks[1]
    # Rule 3: Canonical hierarchy
    canonical_order = ["targaryen", "stark", "lannister", "watch"]
    for c in canonical_order:
        if c in tied:
            return c

    return tied[0]


def run_validation_suite() -> bool:
    """
    Executes automated testing across all matrix combinations and quiz permutations.
    """
    print("=" * 70)
    print("RUNNING GOVERNANCE & METRIC MATHEMATICAL VALIDATION SUITE")
    print("=" * 70)

    factions = list(GAME_DATA["houses"].keys())
    doctrines = list(GAME_DATA["doctrines"].keys())
    matrix = GAME_DATA["decisionMatrix"]
    expected_archetypes = set(GAME_DATA["archetypes"].keys())
    reachable_archetypes = set()

    tested_combinations = 0
    for f in factions:
        for d in doctrines:
            tested_combinations += 1
            arc_id = matrix[f][d]
            reachable_archetypes.add(arc_id)
            metrics = calculate_metrics(f, d)

            # Mathematical clamp assertions
            assert 30 <= metrics["stability"] <= 98, f"Stability out of bounds: {metrics['stability']}"
            assert 20 <= metrics["prosperity"] <= 95, f"Prosperity out of bounds: {metrics['prosperity']}"
            assert 40 <= metrics["defense"] <= 99, f"Defense out of bounds: {metrics['defense']}"

    print(f"  [PASS] 16/16 Faction x Doctrine combinations evaluated.")
    print(f"  [PASS] All stability, prosperity, and defense metrics within PRD clamp ranges.")

    # Archetype Reachability Test
    assert reachable_archetypes == expected_archetypes, (
        f"Mismatch in reachable archetypes: Expected {expected_archetypes}, got {reachable_archetypes}"
    )
    print(f"  [PASS] All 8 canonical ruling archetypes (ARC-01 to ARC-08) are fully reachable!")

    # Quiz Permutations Test (4^3 = 64 permutations)
    quiz_tested = 0
    resolved_counts = {f: 0 for f in factions}
    for q1 in range(4):
        for q2 in range(4):
            for q3 in range(4):
                winner = simulate_tie_breaker(q1, q2, q3)
                assert winner in factions, f"Invalid winner: {winner}"
                resolved_counts[winner] += 1
                quiz_tested += 1

    print(f"  [PASS] 64/64 Quiz answer permutations resolved deterministically.")
    for f, count in resolved_counts.items():
        print(f"         - {f.capitalize():12}: {count:2} resolutions ({count/64*100:.1f}%)")

    print("-" * 70)
    print("ALL 16 COMBINATORIAL OUTCOMES AND 64 QUIZ PATHS PASSED WITH 100% COVERAGE.")
    print("=" * 70)
    return True


# ==============================================================================
# HTML INJECTION PIPELINE
# ==============================================================================

def inject_data_into_html(html_path: Path) -> bool:
    """
    Safely injects validated GAME_DATA between comment delimiters in index.html.
    Preserves all markup, CSS styles, and application logic intact.
    """
    if not html_path.exists():
        print(f"[ERROR] Target file does not exist: {html_path}", file=sys.stderr)
        return False

    content = html_path.read_text(encoding="utf-8")

    start_delim = "/* --- PYTHON_DATA_START --- */"
    end_delim = "/* --- PYTHON_DATA_END --- */"

    if start_delim not in content or end_delim not in content:
        print(f"[ERROR] Delimiters '{start_delim}' or '{end_delim}' not found in {html_path}", file=sys.stderr)
        return False

    json_payload = json.dumps(GAME_DATA, ensure_ascii=False, indent=2)
    js_snippet = f"{start_delim}\n    const GAME_DATA = {json_payload};\n    {end_delim}"

    pattern = re.compile(
        rf"{re.escape(start_delim)}[\s\S]*?{re.escape(end_delim)}",
        re.MULTILINE
    )

    new_content, count = pattern.subn(js_snippet, content)
    if count == 0:
        print("[ERROR] Failed to replace payload inside target file.", file=sys.stderr)
        return False

    html_path.write_text(new_content, encoding="utf-8")
    print(f"[SUCCESS] Safely injected canonical GAME_DATA into {html_path.name}")
    return True


# ==============================================================================
# CLI ENTRY POINT
# ==============================================================================

def main():
    root_dir = Path(__file__).resolve().parent
    html_target = root_dir / "index.html"

    # 1. Always execute validation suite first
    validation_passed = run_validation_suite()
    if not validation_passed:
        print("[FAIL] Validation suite failed. Aborting injection.", file=sys.stderr)
        sys.exit(1)

    # 2. Check for verify-only flag
    if "--verify-only" in sys.argv:
        print("\n[INFO] --verify-only flag detected. Target index.html was NOT modified.")
        sys.exit(0)

    # 3. Perform safe injection
    success = inject_data_into_html(html_target)
    if not success:
        sys.exit(1)

    print("\nPipeline execution complete. Presentation data is verified and synchronized.")


if __name__ == "__main__":
    main()
