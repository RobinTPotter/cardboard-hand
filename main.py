import network, uasyncio as asyncio
from ws_helpers import websocket_handshake, websocket_recv, websocket_send

# --- Access Point ---
ap = network.WLAN(network.AP_IF)
ap.config(essid="Slider_AP", password="12345678")
ap.active(True)
print("AP started at", ap.ifconfig()[0])

# --- HTTP + WebSocket handler ---
async def client_handler(reader, writer):
    request = await reader.read(1024)
    req_str = request.decode()

    if "Upgrade: websocket" in req_str:
        # WebSocket handshake
        response = websocket_handshake(req_str)
        await writer.awrite(response)

        # Handle incoming WebSocket messages
        while True:
            msg = await websocket_recv(reader)
            if msg is None:
                break
            print("Slider update:", msg)   # e.g. "s2:145"
            # Optionally reply
            await websocket_send(writer, "ACK:" + msg)

    else:
        # Serve HTML page
        try:
            with open("index.html") as f:
                html = f.read()
        except:
            html = "<h1>No index.html found</h1>"
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html
        await writer.awrite(response)
    await writer.aclose()

# --- Run server ---
async def main():
    server = await asyncio.start_server(client_handler, "0.0.0.0", 80)
    print("Server listening on 80")
    await server.wait_closed()

asyncio.run(main())

