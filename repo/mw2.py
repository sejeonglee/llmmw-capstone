import fastapi
import string
import wikipediaapi #사용할 api 호출

wiki=wikipediaapi.Wikipedia('ko') #한국 wikipedia 사이트로 접속하도록 셋팅하기]

page_py = wiki.page('이완용')
#print("Page - Exists: %s" % page_py.exists())
#print("Page - Title: %s" % page_py.title)
#print("Page - Summary: %s" % page_py.summary[0:200])

str = page_py.summary[0:200]

for character in string.punctuation:
    str = str.replace(character, ' ')
#print(str)

key_words = str.split(' ')
key_words = list(filter(lambda s: s!='', key_words))
print(key_words)
