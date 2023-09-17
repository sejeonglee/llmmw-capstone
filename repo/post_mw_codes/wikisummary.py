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
        > 1
    ):
        sys.exit(0)

sys.exit(1)
