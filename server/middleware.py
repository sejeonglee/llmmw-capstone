import asyncio
import subprocess
import json

import time


from utils import extract_python_code


PRE_EXAMPLES = [
    """
import sys
if sys.argv[1].startswith("Hello"):
    sys.exit(1)
sys.exit(0)
    """
]
POST_EXAMPLES = [
    """
import time
import sys

print("Hello World!")
time.sleep(2)
sys.exit(0)
    """,
    """
import sys
print("Hello@@@@@")
sys.exit(1)
""",
]


async def check_run_availiable(response: str | None):
    import subprocess

    runtime_info = "Python 3.10.6"

    python_code = extract_python_code(response)
    if python_code is None:
        return

    time.sleep(1)
    exit_code = subprocess.run(["python", "-c", python_code]).returncode
    return (
        f"- Code status: **{str( exit_code == 0)}**, Runtime: {runtime_info}"
    )


async def run_codes(codes: list[str], *args, websocket=None):
    async def run_single_code(code):
        proc = await asyncio.create_subprocess_exec(
            "python",
            "-c",
            code,
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        result = {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "returncode": proc.returncode,
        }
        if websocket:
            print(f"websocket send: {result}")

            await websocket.send(json.dumps(result))
        else:
            print(result)
        return result

    return await asyncio.gather(*map(run_single_code, codes))


async def run_codes_sync(codes: list[str], *args, websocket=None):
    async def run_single_code(code):
        proc = subprocess.run(
            ["python", "-c", code, *args],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        result = {
            "stdout": proc.stdout.decode(),
            "stderr": proc.stderr.decode(),
            "returncode": proc.returncode,
        }
        if websocket:
            print(f"websocket send: {result}")
            await websocket.send(json.dumps(result))
        else:
            print(result)
        return result

    return [await run_single_code(code) for code in codes]
