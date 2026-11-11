"""
What your test runs. ← UNIT 8, MILESTONE 3

One scenario (or a pair) per criterion in criteria.md. `run_eval.py` runs
everything here three times.

A scenario carries exactly one of these:

    "texts"    a list of strings. Each is sent as {"text": ..., "creator_id": ...}
               with a creator_id made up for you. Used for criteria 1, 2 and 3.

    "bodies"   a list of whole request bodies, sent exactly as written. Used for
               criterion 5, where the malformed request IS the point. An optional
               parallel "expect" list says which status/error code the Milestone 1
               contract promises for each body, so the report shows them side by side.

    "appeals"  {"texts": [...], "reasoning": "..."}. Criterion 4 can't be tested by
               sending text alone: each text is submitted, then appealed with the
               content_id that came back, then checked against GET /log. I extended
               run_eval.py (`run_appeals`) to do this, rather than test it by hand.

Creator ids: run_eval.py builds `eval_<first 12 chars of name>_<n>`, so every
scenario name below differs in its first 12 characters. Each creator sends one
request per trial, which keeps every scenario well under the 5/minute limit.
"""

# ── Writing I did not write: unedited chatbot output on ordinary prompts ──────
# Generated with Claude (see "How I Used AI" in the README) and pasted in
# without edits. Criterion 2 uses the first five; criterion 4 uses all ten
# simply as valid submissions to appeal.
CLEARLY_AI = [
    # Prompt: "Write a paragraph about the benefits of regular exercise."
    "Regular exercise offers a wide range of benefits for both physical and mental health. "
    "Engaging in physical activity strengthens the heart, improves circulation, and helps "
    "maintain a healthy body weight. In addition, exercise releases endorphins, which can "
    "reduce stress and improve overall mood. Studies have shown that people who exercise "
    "regularly tend to sleep better and have more energy throughout the day. By making "
    "exercise a consistent part of your routine, you can enjoy a healthier and more "
    "fulfilling life.",
    # Prompt: "Write a paragraph about why time management is important for students."
    "Time management is an essential skill for students who want to succeed academically. "
    "By planning their schedules carefully, students can balance coursework, extracurricular "
    "activities, and personal responsibilities more effectively. Good time management helps "
    "reduce stress and prevents the last-minute rush that often leads to lower-quality work. "
    "It also allows students to set clear priorities and focus on what matters most. "
    "Ultimately, developing strong time management habits early can lead to long-term "
    "success in both school and future careers.",
    # Prompt: "Write a paragraph about the importance of recycling."
    "Recycling plays a crucial role in protecting the environment and conserving natural "
    "resources. When materials such as paper, plastic, and glass are recycled, they can be "
    "turned into new products instead of ending up in landfills. This process reduces "
    "pollution and lowers the amount of energy needed to manufacture goods from raw "
    "materials. Recycling also helps create jobs in the collection and processing "
    "industries. By recycling consistently, individuals can make a meaningful contribution "
    "to a cleaner and more sustainable future.",
    # Prompt: "Write a paragraph about the advantages of reading books."
    "Reading books provides numerous advantages that extend far beyond entertainment. "
    "Books expand vocabulary, improve writing skills, and enhance critical thinking "
    "abilities. They also allow readers to explore different cultures, perspectives, and "
    "time periods without leaving their homes. Furthermore, reading has been shown to "
    "reduce stress and improve concentration. Whether it is fiction or nonfiction, making "
    "reading a regular habit can enrich a person's knowledge and contribute to lifelong "
    "learning and personal growth.",
    # Prompt: "Write a paragraph about how technology has changed communication."
    "Technology has dramatically transformed the way people communicate with one another. "
    "In the past, communication often relied on letters and landline telephones, which "
    "could be slow and limited. Today, smartphones, email, and social media platforms allow "
    "people to connect instantly with others around the world. These tools have made it "
    "easier to maintain relationships, collaborate on projects, and share information. "
    "However, it is also important to use technology responsibly to ensure that digital "
    "communication remains meaningful and respectful.",
    # Prompt: "Write a paragraph about the benefits of learning a second language."
    "Learning a second language offers many cognitive, social, and professional benefits. "
    "Studies suggest that bilingual individuals often have stronger memory and "
    "problem-solving skills. Knowing another language also makes it easier to connect with "
    "people from different backgrounds and to appreciate other cultures. In today's "
    "globalized economy, language skills can open doors to new career opportunities. "
    "Overall, learning a second language is a valuable investment that can enrich many "
    "aspects of a person's life.",
    # Prompt: "Write a paragraph about why sleep matters."
    "Getting enough sleep is essential for maintaining good health and well-being. During "
    "sleep, the body repairs tissues, strengthens the immune system, and consolidates "
    "memories. A lack of sleep can lead to difficulty concentrating, irritability, and an "
    "increased risk of chronic health problems. Experts generally recommend that adults get "
    "seven to nine hours of sleep each night. By prioritizing healthy sleep habits, people "
    "can improve their mood, productivity, and overall quality of life.",
    # Prompt: "Write a paragraph about the value of teamwork."
    "Teamwork is a fundamental component of success in many areas of life. When people work "
    "together toward a common goal, they can combine their unique skills and perspectives "
    "to achieve results that would be difficult to accomplish alone. Effective teamwork "
    "encourages open communication, mutual respect, and shared responsibility. It also "
    "helps build trust and strengthens relationships among team members. By fostering a "
    "collaborative environment, organizations can increase productivity and drive "
    "innovation.",
    # Prompt: "Write a paragraph about the importance of healthy eating."
    "Healthy eating is one of the most important factors in maintaining overall wellness. A "
    "balanced diet that includes fruits, vegetables, whole grains, and lean proteins "
    "provides the nutrients the body needs to function properly. Eating well can help "
    "prevent chronic diseases such as heart disease and diabetes. It also supports energy "
    "levels, mental clarity, and a strong immune system. By making mindful food choices "
    "each day, individuals can improve their health and enjoy a better quality of life.",
    # Prompt: "Write a paragraph about the benefits of volunteering."
    "Volunteering is a rewarding activity that benefits both individuals and communities. By "
    "giving their time and skills, volunteers help support important causes such as "
    "education, health care, and environmental protection. Volunteering also provides "
    "opportunities to meet new people, develop valuable skills, and gain a sense of purpose. "
    "Research has shown that people who volunteer often experience lower stress levels and "
    "greater life satisfaction. Ultimately, volunteering creates positive change while "
    "enriching the lives of those who participate.",
]

# ── My own writing ─────────────────────────────────────────────────────────────
# ⚠️ Every string in this section must be something I actually wrote.
# Anything still starting with "REPLACE ME" stops run_eval.py before it sends.

# Every piece below is copied word for word (markdown and link URLs stripped)
# from writing I already had before this unit. Nothing was written for the test.
# Sources are noted on each one.
#
# ⚠️ GAPS against criteria.md, recorded rather than filled with made-up text:
#   - Only 2 casual pieces exist as text (criterion 2 asks for 5 clearly-human).
#   - No "paragraph in short, even sentences" (one of criterion 1's four named
#     formal types).
#   - No lightly-edited AI (criterion 3(b) asks for 2).
# To close a gap later: add the piece to the right list and re-run run_eval.py.

# Casual, personal, uneven rhythm. Criterion 2's "clearly human" set.
MY_CASUAL = [
    # Unit 7 calibration + reachability check (README).
    "My grandmother kept a jar of buttons on the windowsill, and every Sunday I would tip it "
    "out onto the rug and sort them by color while she yelled at the Padres on the radio. "
    "There was one brass button shaped like an anchor. Nobody knew where it came from.",
    # Unit 7 Sample Run (README).
    "The 7 bus was late again — twenty minutes, in the rain, with no shelter. A guy next to "
    "me was eating sunflower seeds and spitting the shells into a Big Gulp cup. I asked him "
    "how long he'd been waiting. \"Since Tuesday,\" he said, deadpan. I laughed so hard I "
    "almost missed the bus when it finally showed up. Worth it? Honestly, yes.",
]

# Deliberately plain or formal, in the order criteria.md names them (cover
# letter, lab report, how-to). Criterion 3 uses these first three as its
# "formal human" borderline set.
MY_FORMAL = [
    # Cover letter, TEKnuova, 2026-09-12 (Google Drive "Cover Letter"), paragraph 1.
    "I would like to submit my application for the Software Engineer Intern role at TEKnuova. "
    "I am currently enrolled in my undergraduate degree of Bachelor of Science in Computer "
    "Science, at San Diego State University, set to graduate in May 2027, and have practical "
    "knowledge of developing full-stack applications, REST APIs, and artificial "
    "intelligence-based systems. The way that TEKnuova strives to create solutions using all "
    "these new technologies excites me.",
    # Lab report, STAT 550 Lab 6 (Lab6_LuisVillalon.docx), triangle simulation.
    "The true expected value of the hypotenuse is about 0.7071, and the true variance is about "
    "0.1667. The simulated values were very close to these, with an empirical mean of about "
    "0.7010 and an empirical variance of about 0.1605. These small differences between the "
    "true and imperical values are simply due to sampling error from using a finite sample of "
    "only 500 triangles rather than the full population.",
    # How-to, "How to Be an AI-Native Engineer" guide, 2026-07-28, section 2.2.
    "When code fails, resist the immediate urge to simply prompt, 'AI, fix it'. Instead, begin "
    "by investigating the issue within your codebase; read the error message carefully and "
    "locate the specific lines causing the problem. Use AI as a mirror for your reasoning — a "
    "tool to help you explain the 'why' behind the bug — rather than a shortcut for quick "
    "answers (CodePath, n.d). By seeking to understand the logic first, you ensure that you "
    "remain the architect of the solution, using automation to validate your thoughts rather "
    "than replace them.",
]

# More of my formal writing, to bring criterion 1 to 10 pieces.
MY_OTHER_FORMAL = [
    # Cover letter, TEKnuova, paragraph 3.
    "I have also worked on the topic of AI and automation by participating in an agentic AI "
    "project at NXP Semiconductors. In this project, I have worked on creating a multi-agent "
    "system for generating architecture diagrams from SystemVerilog code through the use of "
    "LangGraph, FastAPI, Next.js, and Graphviz. This involved implementing structured outputs, "
    "automatic result validation and re-attempts, as well as self-reinforcement mechanisms to "
    "increase the reliability of the LLM-based outputs.",
    # Lab report, STAT 550 Lab 6, Box-Muller / 68-95-99.7 answer.
    "My simulated proportions of 0.674, 0.959, and 0.997 are all very close to the true values "
    "of 0.68, 0.95, and 0.997. The small differences are just due to sampling error from "
    "generating only 1000 variates rather than the full population. This agreement confirms "
    "the 68-95-99.7 rule, which says that for any normal distribution, about 68% of values "
    "fall within one standard deviation of the mean, about 95% fall within two standard "
    "deviations, and about 99.7% fall within three standard deviations.",
    # How-to guide, section 2.1.
    "Debugging is a cornerstone of a software engineer's growth. Traditionally, when an error "
    "occurred, you would inspect the terminal to locate the bug and manually research a "
    "solution. While this process can be time-consuming, it is essential for your "
    "development; it builds the deep technical intuition and 'why' behind the code that leads "
    "to true learning. Even as we adopt AI tools, this foundational reasoning remains vital. "
    "Automation should be used to enhance your solution, not bypass the critical thinking "
    "that makes you a better programmer.",
    # How-to guide, section 5.1, paragraph 1.
    "As a software engineer working within a team, your responsibility extends beyond simply "
    "writing code that produces the correct output; you must also ensure that your code is "
    "maintainable by humans. This is why, once your code is functional, it is essential to "
    "use AI as a partner to refactor it for improved readability.",
    # Kanso project description (Glencliff Labs application, Google Drive).
    "Kanso is a self-improvement web application that helps users organize tasks, build "
    "consistent habits, and store notes in one centralized platform. Inspired by my personal "
    "notebook and Japanese stationery, Kanso transforms user activity into meaningful "
    "statistics and visualizations, allowing users to track their progress and see tangible "
    "evidence of their personal growth over time.",
]

# Criterion 3: lightly-edited AI — "a few sentences reworded by me". None yet
# (see GAPS above). To add: reword a few sentences of CLEARLY_AI[5] and
# CLEARLY_AI[6] yourself and paste them here.
MY_LIGHTLY_EDITED_AI = []

# ── Criterion 5: the 8 malformed bodies criteria.md names ─────────────────────
_SHORT_10_WORDS = "I wrote this sentence myself and it has ten words."
_FIFTY_THOUSAND_WORDS = "word " * 50_000
_VALID_TEXT = CLEARLY_AI[0]


SCENARIOS = [
    {
        "name": "c1 own writing",
        "criterion": 1,
        # 10 of my pieces: 2 casual, 8 formal. Target: 0 of 10 labelled ai.
        "texts": MY_CASUAL + MY_FORMAL + MY_OTHER_FORMAL,
    },
    {
        "name": "c2 clearly AI",
        "criterion": 2,
        # Target (with the next scenario): mean(AI) − mean(human) ≥ 0.30 and no
        # human piece scores above any AI piece, in every trial.
        "texts": CLEARLY_AI[:5],
    },
    {
        "name": "c2 clearly human",
        "criterion": 2,
        # Only 2 of the 5 the criterion asks for (see GAPS).
        "texts": MY_CASUAL[:5],
    },
    {
        "name": "c3 borderline",
        "criterion": 3,
        # Should be 2 lightly-edited AI + 3 formal human; only the 3 formal
        # pieces exist (see GAPS). Target: ≥ 3 of 5 unsure, none of the 3 formal
        # pieces labelled ai. Part (a) — all three labels appear — is read
        # across this scenario and both c2 scenarios together.
        "texts": MY_LIGHTLY_EDITED_AI + MY_FORMAL[:3],
    },
    {
        "name": "c4 appeals",
        "criterion": 4,
        # Target: 10 of 10 appeals return 200 + under_review, each with a
        # matching appeal entry in GET /log (reasoning verbatim) and the original
        # decision entry unchanged; plus 404 / 409 / 400 on the three bad appeals.
        "appeals": {
            "texts": CLEARLY_AI,
            "reasoning": "I wrote this myself and I'd like a person to review it.",
        },
    },
    {
        "name": "c5 bad input",
        "criterion": 5,
        # Target: each one gets the contract's 4xx and error code, no
        # content_id/guess/label, one rejection entry in the log, in under 2s.
        "bodies": [
            {"text": "", "creator_id": "eval_c5_empty"},
            {"text": "   \n\t  ", "creator_id": "eval_c5_whitespace"},
            {"creator_id": "eval_c5_no_text"},
            {"text": None, "creator_id": "eval_c5_null"},
            {"text": 12345, "creator_id": "eval_c5_number"},
            {"text": _VALID_TEXT},  # no creator_id
            {"text": _SHORT_10_WORDS, "creator_id": "eval_c5_ten_words"},
            {"text": _FIFTY_THOUSAND_WORDS, "creator_id": "eval_c5_huge"},
        ],
        "expect": [
            "400 missing_text",
            "400 missing_text",
            "400 missing_text",
            "400 missing_text",
            "400 missing_text",
            "400 missing_creator_id",
            "400 text_too_short",
            "413 text_too_long",
        ],
    },
]


def _placeholder_problems(i, scenario, texts):
    problems = []
    for j, text in enumerate(texts, 1):
        if not str(text).strip():
            problems.append(
                f"scenario {i}, text {j} is empty — if an empty submission is what "
                f"you're testing, use 'bodies' instead of 'texts'"
            )
        elif str(text).startswith("REPLACE ME"):
            problems.append(
                f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                f"the placeholder"
            )
    return problems


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    names = set()
    for i, scenario in enumerate(SCENARIOS, 1):
        name = scenario.get("name")
        if not name:
            problems.append(f"scenario {i} has no name")
        elif name[:12] in names:
            problems.append(
                f"scenario {i} ('{name}') shares its first 12 characters with "
                f"another scenario, so they'd share creator_ids"
            )
        else:
            names.add(name[:12])

        kinds = [k for k in ("texts", "bodies", "appeals") if scenario.get(k)]
        if len(kinds) != 1:
            problems.append(
                f"scenario {i} ('{name}') needs exactly one of texts / bodies / "
                f"appeals, has {kinds or 'none'}"
            )
            continue

        if kinds == ["bodies"]:
            bodies = scenario["bodies"]
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            expect = scenario.get("expect")
            if expect is not None and len(expect) != len(bodies):
                problems.append(f"scenario {i}: 'expect' must have one entry per body")
            continue

        if kinds == ["appeals"]:
            appeals = scenario["appeals"]
            if not str(appeals.get("reasoning", "")).strip():
                problems.append(f"scenario {i}: appeals need a 'reasoning'")
            problems += _placeholder_problems(i, scenario, appeals.get("texts") or [])
            continue

        problems += _placeholder_problems(i, scenario, scenario["texts"])
    return problems
