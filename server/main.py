#!/usr/bin/env python

import json

import asyncio
import websockets


from llmprovider import mock
from middleware import check_run_availiable


async def websocket_main(websocket):
    while True:
        wsck_req = await websocket.recv()

        req = json.loads(wsck_req)
        print(f"<<< {req}")

        response = mock.generate_response(req.get("message"))

        await websocket.send(response)
        print(f">>> response sended: {response[0:100]}")

        selected_middlewares = [check_run_availiable]

        async def run_middleware(middleware, response):
            await websocket.send(await middleware(response))

        running_middlewares = map(
            lambda m: asyncio.create_task(run_middleware(m, response)),
            selected_middlewares,
        )
        await asyncio.gather(*running_middlewares)


async def main():
    async with websockets.serve(websocket_main, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
