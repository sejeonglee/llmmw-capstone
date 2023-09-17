import re

text = "Today is June 30, 2021."
pattern = '\d+'

result = re.findall(pattern, text)
print(result)
