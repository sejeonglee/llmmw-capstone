import urllib

params = {"param1": "value1", "param2": "value2", "param3": "value3"}
query_string = urllib.urlencode(params)

print(query_string)
