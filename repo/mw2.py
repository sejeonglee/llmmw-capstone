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

point = 0
gpt_str = "대한민국 역사 속 인물 이완용은 한국의 독립운동가이자 정치인으로, 대한민국의 초기에 중요한 역할을 맡았습니다. 다음은 이완용에 대한 몇 가지 중요한 사실들입니다: 1. 출생과 교육: 이완용(이영희)은 1902년 3월 5일에 충청남도 보령에서 태어났습니다. 그는 현대사학, 법학을 전공하며 일본 유학 시절에는 독립운동에 참여하였습니다. 2. 일제 강점기 활동: 일제의 압박과 식민지 지배에 항거하기 위해 이완용은 대한독립촉성회, 한인애국단 등의 독립운동 단체에서 활동하였습니다. 1909년 일본에서 개최된 한인학교 학생들의 항일 독립운동인 을사사변에 참여한 것으로 알려져 있습니다. 3. 독립운동가로서의 역할: 대한독립촉성회 활동을 통해 이완용은 독립운동에 적극적으로 참여하였으며, 유학 동료인 안창호와 긴밀한 협력 관계를 유지하였습니다. 그는 조선의 독립과 국권 회복을 위해 힘썼으며, 독립 이후에는 독립운동가로서의 업적으로 인정받았습니다. 4. 대한민국 정치인으로의 활동: 대한민국의 독립 이후, 이완용은 한국독립당을 창당하고 이를 통해 정치적인 활동을 이어갔습니다. 1948년에는 대한민국 임시정부의 수석부총리로 임명되었으며, 이후 대한민국 국회의원으로 활동하였습니다. 이완용은 독립운동가로서의 업적과 정치인으로서의 활동을 통해 대한민국의 독립과 국가 발전에 기여한 인물로 평가받고 있습니다. 그의 역사적인 업적은 대한민국의 독립운동사와 정치사에서 중요한 위치를 차지하고 있습니다."

for i in range(len(key_words)):
    if(key_words[i] in gpt_str):
        point += 1 

if(point > len(key_words)/2):
    print('꽤 정확하네요')
else :
    print('틀린 정보입니다')
