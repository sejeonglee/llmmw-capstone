import subprocess
import re
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
    [
        "/home/sejeonglee/.cache/pypoetry/virtualenvs/capstone-WiT4c78G-py3.10/bin/python",
        "-c",
        python_code,
    ],
    check=False,
).returncode

sys.exit(exit_code)
