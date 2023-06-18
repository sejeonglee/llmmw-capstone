import fastapi
import os

app = fastapi.FastAPI()


@app.get("/function_list")
async def return_list():
    def get_files_list(path: os.PathLike | str) -> list[str]:
        return list(
            map(
                lambda filename: os.path.splitext(filename)[0],
                os.listdir(path),
            )
        )

    return {
        "pre_middlewares": get_files_list("./pre_mw_codes"),
        "post_middlewares": get_files_list("./post_mw_codes"),
    }


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
