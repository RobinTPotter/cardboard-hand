import network
import socket
import machine

# --- Setup Access Point ---
ap = network.WLAN(network.AP_IF)
ap.config(essid="PicoW_AP", password="12345678")
ap.active(True)

print("Access Point started")
print("SSID:", ap.config("essid"))
print("IP address:", ap.ifconfig()[0])

# --- Simple Web Server ---
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Web server listening on:", addr)

while True:
    cl, client_addr = s.accept()
    print("Client connected from", client_addr)

    request = cl.recv(1024).decode()
    print("Request:", request)

    # Handle LED control
    if "/test/" in request:
        num = int(request.replace("/test/",""))
        testing.test(num)

    knobs = [f"<input type=\"button\" onclick=\"test/{p}\">" for p in range(30)]

    # Load HTML and replace state
    html = f"""<html>
<body>
{knobs}</body>
</html>
"""

    # Send response
    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    cl.send(html)
    cl.close()

