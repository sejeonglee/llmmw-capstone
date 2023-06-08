import time

from utils import extract_python_code


async def check_run_availiable(response: str | None):
    import subprocess

    runtime_info = "Python 3.10.6"

    python_code = extract_python_code(response)
    if python_code is None:
        return True

    time.sleep(1)
    exit_code = subprocess.run(["python", "-c", python_code]).returncode
    return (
        f"- Code status: **{str( exit_code == 0)}**, Runtime: {runtime_info})"
    )
