import fastapi
import os 

app = fastapi.FastAPI()



@app.get("/function_list")
async def return_list():
    path = "/Users/joyeongjun/Documents/abc"
    file_list = os.listdir(path)
    # print ("file_list: {}".format(file_list))
    return file_list



@app.get("/get_function_code/{function_name}")
async def read_item(function_name):

    path = "/Users/joyeongjun/Documents/abc"
    file_list = os.listdir(path)
    for i in range(file_list):
        if(function_name == file_list[i]):
            file = open(function_name,'r')
            FUN_CODE = file.read()
            file.close()
            return {"function_name": function_name,
            "function_code": FUN_CODE}
    return 'NOT_FOUND'

    