import fastapi
import os

app = fastapi.FastAPI()


@app.get("/function_list")
async def return_list():
    path = "./mw_codes/"
    file_list = list(
        map(lambda filename: os.path.splitext(filename)[0], os.listdir(path))
    )
    # print ("file_list: {}".format(file_list))
    return file_list


@app.get("/get_function_code/{function_name}")
async def read_item(function_name):
    path = "./mw_codes/"
    file_list = os.listdir(path)
    for filename in file_list:
        if function_name == os.path.splitext(filename)[0]:
            with open(
                os.path.join(path, f"{function_name}.py"),
                encoding="utf8",
                mode="r",
            ) as file:
                function_code = file.read()

            return {
                "function_name": function_name,
                "function_code": function_code,
            }
    return "NOT_FOUND"
