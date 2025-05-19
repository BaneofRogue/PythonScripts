import asyncio
import websockets

async def handler(websocket):
    async for message in websocket:
        print(f"Received message on port {websocket.local_address[1]}:")
        print(message)

async def start_server(port):
    server = await websockets.serve(handler, "127.0.0.1", port)
    print(f"Server listening on ws://127.0.0.1:{port}")
    return server

async def main():
    servers = await asyncio.gather(*(start_server(port) for port in range(5002, 5003)))
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
