def generate_response(req):
    if req.find("Python 3") != -1 or req.find("파이썬 3") != -1:
        return """
Python 3에서는 `urllib.parse` 모듈을 사용하여 쿼리 스트링을 생성할 수 있습니다. `urllib.parse.urlencode()` 함수를 사용하여 파라미터를 쿼리 스트링으로 변환할 수 있습니다. 다음은 예시 코드입니다:

```python
import urllib.parse

params = {'param1': 'value1', 'param2': 'value2', 'param3': 'value3'}
query_string = urllib.parse.urlencode(params)

print(query_string)
```

위의 코드를 실행하면 다음과 같은 출력이 나타납니다:

```
param1=value1&param2=value2&param3=value3
```

위 코드에서 `params` 변수는 변환하려는 parameter들을 담은 딕셔너리입니다. `urllib.parse.urlencode()` 함수는 이 딕셔너리를 입력받아 parameter들을 쿼리 스트링으로 변환합니다. 반환되는 `query_string` 변수는 변환된 쿼리 스트링을 담고 있습니다. 이후 쿼리 스트링을 HTTP 요청의 URL 뒤에 붙이면 됩니다.
        """
    return """
Python 2에서 `urllib.urlencode` 함수를 사용하여 parameter를 쿼리 스트링으로 변환할 수 있습니다. 다음은 `urllib.urlencode` 함수를 사용한 예시 코드입니다:

```python
import urllib

params = {'param1': 'value1', 'param2': 'value2', 'param3': 'value3'}
query_string = urllib.urlencode(params)

print(query_string)
```

위의 코드를 실행하면 다음과 같은 출력이 나타납니다:

```
param1=value1&param2=value2&param3=value3
```

위 코드에서 `params` 변수는 변환하려는 parameter들을 담은 딕셔너리입니다. `urllib.urlencode` 함수는 이 딕셔너리를 입력받아 parameter들을 쿼리 스트링으로 변환합니다. 반환되는 `query_string` 변수는 변환된 쿼리 스트링을 담고 있습니다. 이후 쿼리 스트링을 HTTP 요청의 URL 뒤에 붙이면 됩니다."""
