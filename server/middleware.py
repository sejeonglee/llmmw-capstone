import asyncio
import subprocess
import json

import time


from utils import extract_python_code


PRE_EXAMPLES = [
    {
        "name": "not starts with Hello",
        "code": """
import sys
if sys.argv[1].startswith("Hello"):
    sys.exit(1)
sys.exit(0)
    """,
    },
    {
        "name": "금칙어 여부",
        "code": """
import sys
if sys.argv[1].find("forbidden") != -1:
    sys.exit(1)
sys.exit(0)
    """,
    },
]
POST_EXAMPLES = [
    #     {
    #         "name": "always pass",
    #         "code": """
    # import time
    # import sys
    # print("Hello World!")
    # time.sleep(2)
    # sys.exit(0)
    #     """,
    #     },
    #     {
    #         "name": "always error",
    #         "code": """
    # import sys
    # print("Hello@@@@@")
    # sys.exit(1)
    # """,
    #     },
    {
        "name": "check errors in Python 3.10",
        "code": """
import subprocess
import re
import time
import sys

def extract_python_code(s):
    pattern = re.compile(r"```python(.*?)```", re.DOTALL)
    match = pattern.search(s)
    if match:
        return match.group(1)
    else:
        return None


runtime_info = "Python 3.10.6"  # TODO: Hard Coded
response = sys.argv[1]
python_code = extract_python_code(response)
if python_code is None:
    sys.exit(0)

exit_code = subprocess.run(
    ["/home/sejeonglee/.cache/pypoetry/virtualenvs/capstone-WiT4c78G-py3.10/bin/python", "-c", python_code], check=False
).returncode

sys.exit(exit_code)
""",
    },
    {
        "name": "check errors in Python 3.6",
        "code": """
import subprocess
import re
import time
import sys

def extract_python_code(s):
    pattern = re.compile(r"```python(.*?)```", re.DOTALL)
    match = pattern.search(s)
    if match:
        return match.group(1)
    else:
        return None


runtime_info = "Python 3.6.15"  # TODO: Hard Coded
response = sys.argv[1]
python_code = extract_python_code(response)
if python_code is None:
    sys.exit(0)

exit_code = subprocess.run(
    ["/home/sejeonglee/.cache/pypoetry/virtualenvs/venv-3-6-15-gMqX61pc-py3.6/bin/python", "-c", python_code], check=False
).returncode

sys.exit(exit_code)
""",
    },
]


async def check_run_availiable(response: str | None):
    import subprocess

    runtime_info = "Python 3.10.6"

    python_code = extract_python_code(response)
    if python_code is None:
        return

    time.sleep(1)
    exit_code = subprocess.run(
        ["python", "-c", python_code], check=False
    ).returncode
    return (
        f"- Code status: **{str( exit_code == 0)}**, Runtime: {runtime_info}"
    )


async def run_codes(func_list: list[dict[str, str]], *args, websocket=None):
    async def run_single_code(funcs):
        name = funcs.get("name")
        code = funcs.get("code")
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
            "name": name,
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "returncode": proc.returncode,
            "error": (proc.returncode != 0),
        }
        if websocket:
            print(f"websocket send: {result}")
            await websocket.send(
                json.dumps({**result, "response_type": "post_result"})
            )
        else:
            print(result)
        return result

    return await asyncio.gather(*map(run_single_code, func_list))


async def run_codes_sync(
    func_list: list[dict[str, str]], *args, websocket=None
):
    async def run_single_code(name, code):
        proc = subprocess.run(
            ["python", "-c", code, *args],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            check=False,
        )
        result = {
            "name": name,
            "stdout": proc.stdout.decode(),
            "stderr": proc.stderr.decode(),
            "returncode": proc.returncode,
            "error": (proc.returncode != 0),
        }
        if websocket:
            print(f"websocket send: {result}")
            await websocket.send(
                json.dumps({**result, "response_type": "pre_result"})
            )
        else:
            print(result)
        return result

    return [
        await run_single_code(func.get("name"), func.get("code"))
        for func in func_list
    ]
