import sys
import uasyncio as asyncio
import ujson
import network
import ubinascii
import usocket as socket
import uhashlib
from ws_helpers import ws_recv_frame, ws_send_frame
from update import *
from config import *

print("hello")

# ----------------------------
# HTTP + WebSocket handler
# ----------------------------
async def handle_client(reader, writer):
    try:
        req = await reader.readline()
        if not req:
            await writer.aclose()
            return

        headers = {}
        while True:
            line = await reader.readline()
            if line == b"\r\n":
                break
            k, v = line.decode().split(":", 1)
            headers[k.strip()] = v.strip()

        if "Upgrade" in headers and headers["Upgrade"].lower() == "websocket":
            key = headers.get("Sec-WebSocket-Key", "")
            import ubinascii, uhashlib
            sha1 = uhashlib.sha1(key.encode() + b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11")
            accept = ubinascii.b2a_base64(sha1.digest()).strip().decode()
            resp = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                "Sec-WebSocket-Accept: " + accept + "\r\n\r\n"
            )
            await writer.awrite(resp)

            print("about to load config")
            # Send saved config to client
            cfg = load_config()
            if cfg:
                await ws_send_frame(writer, "init:" + ujson.dumps(cfg))

            while True:
                msg = await ws_recv_frame(reader)
                if msg is None:
                    break

                #print(msg[:min(len(msg),10)])
                if msg.startswith("reinit:"):
                    try:
                        data = ujson.loads(msg[7:])
                        print("Init values:", data)
                        save_config(data)
                        reinitialize(data)
                    except Exception as e:
                        print("Bad init JSON:", e)
                else:
                    print("Realtime update:", msg)
                    realtime_update(msg)

            await writer.aclose()
        else:
            try:
                with open("index.html") as f:
                    html = f.read()

                with open("slider.html") as f:
                    slider = f.read()

                sliders = "\n".join([slider.replace("s1",f"s{s}") for s in range(2,6)])
                html = html.replace("<!-- rest1 -->", sliders)

                sliders = "\n".join(["""setupSlider("s1", "s1val");
setupSlider("s1min", "s1valmin");
setupSlider("s1max", "s1valmax");
""".replace("s1", f"s{s}") for s in range(2,6)])
                html = html.replace("<!-- rest2 -->", sliders)

                await writer.awrite("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")

                for i in range(0, len(html), 512):
                    await writer.awrite(html[i:i+512])
                await writer.drain()
            except:
                resp = "HTTP/1.0 404 NOT FOUND\r\n\r\n"
                await writer.awrite(resp)

            await writer.aclose()

    except Exception as e:
        print("Client error:", e)
        sys.print_exception(e)
        try:
            await writer.aclose()
        except:
            pass

# ----------------------------
# Main entry point
# ----------------------------
async def main():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="My_MicroPython_AP", password="12345678")
    print("AP running at:", ap.ifconfig())

    cfg = load_config()
    if cfg:
        print("Restored config:", cfg)

    srv = await asyncio.start_server(handle_client, "0.0.0.0", 80)
    print("Listening on 0.0.0.0:80")
    await srv.wait_closed()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server stopped")
