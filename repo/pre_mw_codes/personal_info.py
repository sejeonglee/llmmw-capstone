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
