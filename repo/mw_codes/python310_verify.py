import subprocess
import re
import time


def extract_python_code(s):
    pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)
    match = pattern.search(s)
    if match:
        return match.group(1)
    else:
        return None


async def mw(response: str | None):
    runtime_info = "Python 3.10.6"

    python_code = extract_python_code(response)
    if python_code is None:
        return True

    time.sleep(1)
    exit_code = subprocess.run(
        ["python", "-c", python_code], check=False
    ).returncode
    return (
        f"- Code status: **{str( exit_code == 0)}**, Runtime: {runtime_info})"
    )
