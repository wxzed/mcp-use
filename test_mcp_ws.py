import asyncio
import websockets
import json

async def test_mcp_ws():
    uri = "ws://192.168.1.35/ws"  # 替换为你的实际地址
    async with websockets.connect(uri) as ws:
        # 1. 发送 initialize 请求
        init_msg = {"id": "1", "method": "initialize", "params": {}}
        await ws.send(json.dumps(init_msg))
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            print("收到 initialize 响应：", response)
        except asyncio.TimeoutError:
            print("等待 initialize 响应超时，ESP32端未返回任何内容！")
            return

        # 2. 发送 tools/list 请求
        tools_list_msg = {"id": "2", "method": "tools/list", "params": {}}
        await ws.send(json.dumps(tools_list_msg))
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            print("收到 tools/list 响应：", response)
        except asyncio.TimeoutError:
            print("等待 tools/list 响应超时，ESP32端未返回任何内容！")
            return

        # 3. 你可以根据 tools/list 的返回内容，尝试调用某个工具
        # 例如调用 led_on 工具
        call_tool_msg = {
            "id": "3",
            "method": "tools/call",
            "params": {
                "name": "led_on",
                "arguments": {"pin": 2}
            }
        }
        await ws.send(json.dumps(call_tool_msg))
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            print("收到 tools/call 响应：", response)
        except asyncio.TimeoutError:
            print("等待 tools/call 响应超时，ESP32端未返回任何内容！")

asyncio.run(test_mcp_ws())