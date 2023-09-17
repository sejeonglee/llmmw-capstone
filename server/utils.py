def extract_python_code(s):
    import re

    pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)
    match = pattern.search(s)
    if match:
        return match.group(1)
    else:
        return None
