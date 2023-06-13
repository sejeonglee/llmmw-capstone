#!/usr/bin/env python

import json

import asyncio
import websockets


from llmprovider import chatgpt as llm
from middleware import run_codes, run_codes_sync
from middleware import PRE_EXAMPLES, POST_EXAMPLES


async def websocket_main(websocket):
    while True:
        wsck_req = await websocket.recv()

        req = json.loads(wsck_req)
        print(f"<<< {req}")

        pre_results = await run_codes_sync(
            PRE_EXAMPLES, req.get("message"), websocket=websocket
        )
        if any(map(lambda result: result.get("returncode") != 0, pre_results)):
            await websocket.send("Error: pre code failed")
            continue
        print(pre_results)

        response = llm.generate_response(req.get("message"))

        await websocket.send(response)
        print(f">>> response sended: {response[0:100]}")

        post_results = await run_codes(POST_EXAMPLES, websocket=websocket)
        print(post_results)


async def main():
    async with websockets.serve(websocket_main, "localhost", 8765):  # type: ignore
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
