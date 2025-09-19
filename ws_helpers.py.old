import ubinascii, uhashlib

# Perform handshake
def websocket_handshake(request):
    for line in request.split("\r\n"):
        if "Sec-WebSocket-Key" in line:
            key = line.split(":")[1].strip()
            break
    magic = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1 = uhashlib.sha1(key.encode() + magic.encode())
    accept = ubinascii.b2a_base64(sha1.digest()).strip().decode()
    response = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept}\r\n\r\n"
    )
    return response

# Decode a WebSocket frame into text
async def websocket_recv(reader):
    hdr = await reader.read(2)
    if not hdr:
        return None
    length = hdr[1] & 0x7F
    if length == 126:
        ext = await reader.read(2)
        length = int.from_bytes(ext, "big")
    mask = await reader.read(4)
    enc_payload = await reader.read(length)
    payload = bytes(b ^ mask[i % 4] for i, b in enumerate(enc_payload))
    return payload.decode()

# Encode + send a WebSocket text frame
async def websocket_send(writer, msg):
    payload = msg.encode()
    frame = bytearray([0x81])  # FIN + text frame
    length = len(payload)
    if length < 126:
        frame.append(length)
    else:
        frame.append(126)
        frame.extend(length.to_bytes(2, "big"))
    frame.extend(payload)
    await writer.awrite(frame)
