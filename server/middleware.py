import asyncio
import subprocess
import json

import time


from utils import extract_python_code


PRE_EXAMPLES = [
    {
        "name": "private-info",
        "code": """
import re
import sys

patterns = {
    "id_number": r"(\d{6}[ ,-]-?[1-4]\d{6})|(\d{6}[ ,-]?[1-4])",
    "driver_license": r"(\d{2}-\d{2}-\d{6}-\d{2})",
    "phone_number": r"(\d{2,3}[ ,-]-?\d{2,4}[ ,-]-?\d{4})",
    "email": r"(([\w!-_\.])*@([\w!-_\.])*\.[\w]{2,3})",
    "credit_card": r"[34569][0-9]{3}[-~.[ ]][0-9]{4}[-~.[ ]][0-9]{4}[-~.[ ]][0-9]{4}",
}

response = sys.argv[1]

for pattern in patterns.values():
    if re.search(pattern, response):
        sys.exit(1)
sys.exit(0)

    """,
    },
    {
        "name": "forbidden-words",
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
        "name": "python310",
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

print(python_code)


if python_code is None:
    sys.exit(0)

exit_code = subprocess.run(
    ["/home/sejeonglee/.cache/pypoetry/virtualenvs/capstone-WiT4c78G-py3.10/bin/python", "-c", python_code], check=False
).returncode

sys.exit(exit_code)
""",
    },
    {
        "name": "python36",
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

print(python_code)
    
exit_code = subprocess.run(
    ["/home/sejeonglee/.pyenv/versions/3.6.15/bin/python", "-c", python_code], check=False
).returncode

sys.exit(exit_code)
""",
    },
    {
        "name": "wikipedia",
        "code": """
import re
import sys
from konlpy.tag import Okt
import wikipediaapi

pattern = r"(\S*[^하|키])[은|는]\s([^\.]*)"
entities = re.findall(pattern, sys.argv[1])
print(sys.argv[1])


okt = Okt()
wiki = wikipediaapi.Wikipedia("ko")

for entity, desc in entities:
    page_py = wiki.page(entity)
    if not page_py.exists():
        continue
    summary = page_py.summary
    print(set(okt.nouns(summary)).intersection(set(okt.nouns(sys.argv[1]))))
    if (
        len(set(okt.nouns(summary)).intersection(set(okt.nouns(sys.argv[1]))))
        > 2
    ):
        sys.exit(0)

sys.exit(1)
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
    return f"- Code status: **{str( exit_code == 0)}**, Runtime: {runtime_info}"


async def run_codes(
    func_list: list[dict[str, str]], *args, websocket=None, uuid=None
):
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
                json.dumps(
                    {**result, "response_type": "post_result", "uuid": uuid}
                )
            )
        else:
            print(result)
        return result

    return await asyncio.gather(*map(run_single_code, func_list))


async def run_codes_sync(
    func_list: list[dict[str, str]], *args, websocket=None, uuid=None
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
                json.dumps(
                    {**result, "response_type": "pre_result", "uuid": uuid}
                )
            )
        else:
            print(result)
        return result

    return [
        await run_single_code(func.get("name"), func.get("code"))
        for func in func_list
    ]
