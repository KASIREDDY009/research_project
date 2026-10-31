from __future__ import annotations

import subprocess


def test_the_job_script_installs_the_code_and_runs_the_command_with_in_and_out(tmp_path):
    from scripts.aws.run_on_sagemaker import job_script

    script = job_script('mkdir -p "$OUT/x" && echo "$IN" > "$OUT/x/in.txt"')
    lines = script.splitlines()
    assert lines[0] == "set -euo pipefail"
    assert "pip install --quiet --no-cache-dir -r requirements.txt" in lines
    assert lines[-1] == 'mkdir -p "$OUT/x" && echo "$IN" > "$OUT/x/in.txt"'
    assert subprocess.run(["bash", "-n", "-c", script]).returncode == 0
