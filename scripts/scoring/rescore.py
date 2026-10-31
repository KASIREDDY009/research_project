"""Re-score the nine evaluation runs locally with one setting changed: the detector seed, the window size
(windows stay non-overlapping), or the share of the fault-free training part used (the clean-data check).
Each re-scoring uses this code with a copy of configs/default.yaml in which only that setting
differs (scripts/scoring/evaluate_run.py --config). Each run's raw/ folder is copied, so the run data is
never written to.

Usage (from the repository root, with the artefact's environment active):
  python scripts/scoring/rescore.py seed 42,1,2,3,4,5,6,7,8,9,10  -> results/rescoring/seeds/seed<S>/run<i>/<app>/
  python scripts/scoring/rescore.py window 10,50                  -> results/rescoring/windows/window<W>/run<i>/<app>/
  python scripts/scoring/rescore.py share 0.25,0.5,0.75           -> results/rescoring/training-share/share<F>/run<i>/<app>/
"""
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODE = sys.argv[1]
WORK = os.path.join(REPO, "results", "rescoring", "configs")
SETS = (("run1", "run2", "run3"), ("run4", "run5", "run6"), ("run7", "run8", "run9"))
# Similar-application partner of each run and application: the three pairings within each set.
PAIRS = {}
for a, b, c in SETS:
    for x, y in (((a, "orders"), (b, "bookings")), ((a, "bookings"), (c, "orders")), ((b, "orders"), (c, "bookings"))):
        PAIRS[x], PAIRS[y] = y, x


def config_copy(name, *changes):
    """configs/default.yaml with the given lines changed."""
    os.makedirs(WORK, exist_ok=True)
    path = os.path.join(WORK, f"{name}.yaml")
    text = open(os.path.join(REPO, "configs", "default.yaml")).read()
    for old, new in changes:
        assert text.count(old) == 1, f"{old!r} must occur once in default.yaml"
        text = text.replace(old, new)
    open(path, "w").write(text)
    return path


def one(config, out, run, app):
    dest = os.path.join(out, run, app)
    if os.path.exists(os.path.join(dest, "processed", "results.json")):
        return 0, f"{os.path.relpath(dest, REPO)}: already scored"
    os.makedirs(dest, exist_ok=True)
    if not os.path.exists(os.path.join(dest, "raw")):
        shutil.copytree(os.path.join(REPO, "results", "runs", run, app, "raw"), os.path.join(dest, "raw"))
    prun, papp = PAIRS[(run, app)]
    r = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "scoring", "evaluate_run.py"), dest, "--config", config,
                        "--similar-source", os.path.join(REPO, "results", "runs", prun, papp, "raw", "events.jsonl")],
                       capture_output=True, text=True)
    open(os.path.join(dest, "evaluate.log"), "w").write(r.stdout + r.stderr)
    return r.returncode, f"{run}/{app} -> {os.path.relpath(out, REPO)}: exit {r.returncode}"


def main():
    runs = [(r, a) for s in SETS for r in s for a in ("orders", "bookings")]
    values = sys.argv[2].split(",")
    jobs = []
    for v in values:
        if MODE == "seed":
            name, config = f"seed{v}", config_copy(f"seed{v}", ("seed: 42\n", f"seed: {int(v)}\n"))
            out = os.path.join(REPO, "results", "rescoring", "seeds", name)
        elif MODE == "window":
            name = f"window{int(v)}"
            config = config_copy(name, ("  window_size: 20\n", f"  window_size: {int(v)}\n"),
                                 ("  step_size: 20\n", f"  step_size: {int(v)}\n"))
            out = os.path.join(REPO, "results", "rescoring", "windows", name)
        elif MODE == "share":
            name = f"share{float(v)}"
            config = config_copy(name, ("  train_share: 1.0\n", f"  train_share: {float(v)}\n"))
            out = os.path.join(REPO, "results", "rescoring", "training-share", name)
        else:
            raise SystemExit("mode must be seed, window or share")
        jobs += [(config, out, r, a) for r, a in runs]
    failed = 0
    with ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "4"))) as ex:
        for code, msg in ex.map(lambda j: one(*j), jobs):
            print(msg, flush=True)
            failed += code != 0
    if failed:
        raise SystemExit(f"{failed} of {len(jobs)} scorings failed; see evaluate.log in each folder")


if __name__ == "__main__":
    main()
