#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

!! Three trials, and **your first signal runs a model, so identical input can
score differently twice.** That's exactly why repeats matter here.

This does the sending and the recording. It does not decide whether a trial
passed — that depends on the criterion you wrote, so the Verdict column comes
back blank.
"""

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])
    return [
        {"text": text, "creator_id": f"eval_{scenario['name'][:12]}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if set(body) == {"text", "creator_id"} and isinstance(body.get("text"), str):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


def log_count(requests, args):
    """How many entries the audit log holds right now (from GET /health)."""
    return requests.get(f"{args.url}/health", timeout=10).json()["log_entries"]


def last_log_entry(requests, args):
    entries = requests.get(f"{args.url}/log", params={"limit": 1}, timeout=10).json()["entries"]
    return entries[-1] if entries else None


def log_entries_for(requests, args, content_id):
    """Every audit log entry carrying this content_id, oldest first."""
    entries = requests.get(f"{args.url}/log", timeout=30).json()["entries"]
    return [e for e in entries
            if e.get("content_id") == content_id or e.get("attempted_content_id") == content_id]


def run_appeals(requests, args, scenario, trial):
    """
    Criterion 4: submit each text, appeal it with the content_id that came back,
    and check GET /log for the appeal entry and the untouched decision entry.
    Then the three appeals that must fail loudly: an unknown id (404), a second
    appeal (409), and blank reasoning (400).

    Added in unit 8 because run_eval.py otherwise only ever calls /submit.
    """
    spec = scenario["appeals"]
    url = args.url
    stamp = dt.datetime.now().strftime("%H%M%S")
    results = []

    def submit(text, n):
        body = {"text": text, "creator_id": f"eval_c4_t{trial}_{n}_{stamp}"}
        response = requests.post(f"{url}/submit", json=body, timeout=args.timeout)
        return response.status_code, response.json()

    appealed = []
    for n, text in enumerate(spec["texts"], 1):
        reasoning = f"{spec['reasoning']} (item {n}, trial {trial})"
        row = {"check": "appeal", "item": n, "sent": describe({"text": text, "creator_id": ""})}
        try:
            submit_status, submitted = submit(text, n)
            content_id = submitted.get("content_id")
            row.update({"submit_status": submit_status, "content_id": content_id,
                        "guess": submitted.get("guess")})
            before = [e for e in log_entries_for(requests, args, content_id)
                      if e.get("status") == "decided"]

            response = requests.post(f"{url}/appeal", timeout=30,
                                     json={"content_id": content_id, "reasoning": reasoning})
            reply = response.json()
            after = log_entries_for(requests, args, content_id)
            appeal_entries = [e for e in after if e.get("event") == "appeal"]
            decided_after = [e for e in after if e.get("status") == "decided"]

            row.update({
                "appeal_http": response.status_code,
                "appeal_status": reply.get("status"),
                "appeal_entries_in_log": len(appeal_entries),
                "reasoning_verbatim": bool(appeal_entries)
                                      and appeal_entries[-1].get("reasoning") == reasoning,
                "log_status": appeal_entries[-1].get("status") if appeal_entries else None,
                "decision_unchanged": len(before) == 1 and decided_after == before,
                "appeal_log_entry": appeal_entries[-1] if appeal_entries else None,
            })
            row["pass"] = (response.status_code == 200
                           and reply.get("status") == "under_review"
                           and len(appeal_entries) == 1
                           and row["reasoning_verbatim"]
                           and row["log_status"] == "under_review"
                           and row["decision_unchanged"])
            if row["pass"]:
                appealed.append(content_id)
        except Exception as exc:  # noqa: BLE001
            row.update({"pass": False, "error": f"{type(exc).__name__}: {exc}"})
        results.append(row)

    def bad_appeal(check, body, want_http, want_error, content_id):
        row = {"check": check, "sent": body, "expected": f"{want_http} {want_error}"}
        try:
            response = requests.post(f"{url}/appeal", json=body, timeout=30)
            reply = response.json()
            appeal_entries = [e for e in log_entries_for(requests, args, content_id)
                              if e.get("event") == "appeal"]
            row.update({"http": response.status_code, "error": reply.get("error"),
                        "appeal_entries_in_log": len(appeal_entries)})
            row["pass"] = response.status_code == want_http and reply.get("error") == want_error
            return row, appeal_entries
        except Exception as exc:  # noqa: BLE001
            row.update({"pass": False, "error": f"{type(exc).__name__}: {exc}"})
            return row, None

    fake_id = f"not-a-real-id-t{trial}-{stamp}"
    row, entries = bad_appeal("unknown id → 404",
                              {"content_id": fake_id, "reasoning": spec["reasoning"]},
                              404, "unknown_content_id", fake_id)
    row["pass"] = row["pass"] and entries == []   # and NO appeal entry written
    results.append(row)

    if appealed:
        first = appealed[0]
        row, entries = bad_appeal("second appeal → 409",
                                  {"content_id": first, "reasoning": spec["reasoning"]},
                                  409, "already_under_review", first)
        row["pass"] = row["pass"] and entries is not None and len(entries) == 1
        results.append(row)
    else:
        results.append({"check": "second appeal → 409", "pass": False,
                        "error": "no successful appeal to repeat"})

    # Blank reasoning on a fresh, never-appealed submission, so a 409 can't mask it.
    try:
        _, fresh = submit(spec["texts"][0], "blank")
        fresh_id = fresh.get("content_id")
        row, entries = bad_appeal("blank reasoning → 400",
                                  {"content_id": fresh_id, "reasoning": "   "},
                                  400, "missing_reasoning", fresh_id)
        row["pass"] = row["pass"] and entries == []
    except Exception as exc:  # noqa: BLE001
        row = {"check": "blank reasoning → 400", "pass": False,
               "error": f"{type(exc).__name__}: {exc}"}
    results.append(row)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            if scenario.get("appeals"):
                results = run_appeals(requests, args, scenario, trial)
                trials.append(results)
                items = [r for r in results if r["check"] == "appeal"]
                extras = [r for r in results if r["check"] != "appeal"]
                print(f"  trial {trial}: {sum(r['pass'] for r in items)}/{len(items)} appeals ok; "
                      + ", ".join(f"{r['check']} {'ok' if r['pass'] else 'FAIL'}" for r in extras))
                continue

            results = []
            expect = scenario.get("expect") or []
            for i, body in enumerate(bodies_for(scenario), 1):
                preview = describe(body)
                try:
                    log_before = log_count(requests, args)
                    started = time.perf_counter()
                    response = requests.post(f"{args.url}/submit", json=body,
                                             timeout=args.timeout)
                    elapsed = time.perf_counter() - started
                    payload = response.json() if response.content else {}
                    result = {
                        "status": response.status_code,
                        "guess": payload.get("guess"),
                        "confidence": payload.get("confidence"),
                        "model_score": payload.get("model_score"),
                        "style_score": payload.get("style_score"),
                        "label": payload.get("label"),
                        "sent": preview,
                    }
                    if scenario.get("bodies"):
                        # Criterion 5 needs more than the scores: the error code,
                        # whether a decision leaked out, the time, and the log entry.
                        last = last_log_entry(requests, args)
                        result.update({
                            "expected": expect[i - 1] if i <= len(expect) else None,
                            "error": payload.get("error"),
                            "content_id": payload.get("content_id"),
                            "elapsed_s": round(elapsed, 3),
                            "log_entries_written": log_count(requests, args) - log_before,
                            "log_entry": last,
                        })
                    results.append(result)
                except Exception as exc:  # noqa: BLE001
                    results.append({"status": None, "error": f"{type(exc).__name__}: {exc}",
                                    "sent": preview})

            trials.append(results)
            if scenario.get("bodies"):
                summary = [f"{r.get('status')} {r.get('error') or '—'}" for r in results]
            else:
                summary = [r.get("guess") or "—" for r in results]
            print(f"  trial {trial}: {', '.join(summary)}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Fill in Target from `criteria.md`, and Run and Verdict from the output",
        "underneath. Whether a trial passed depends on the criterion you wrote.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        lines.append(f"| {name} |  | {' | '.join([' '] * n)} |  |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output. Paste the relevant parts into your README — the rubric",
              "asks for the actual JSON, not a description of it.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, results in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", "", "```json",
                      json.dumps(results, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
