import ustruct as struct

async def ws_recv_frame(reader):
    """Receive one WebSocket frame and return its decoded text payload."""
    hdr = await reader.read(2)
    if not hdr:
        return None
    length = hdr[1] & 127
    if length == 126:
        ext = await reader.read(2)
        length = int.from_bytes(ext, "big")
    elif length == 127:
        ext = await reader.read(8)
        length = int.from_bytes(ext, "big")
    mask = await reader.read(4)
    enc_payload = await reader.read(length)
    payload = bytes(b ^ mask[i % 4] for i, b in enumerate(enc_payload))
    return payload.decode()

async def ws_send_frame(writer, msg):
    """Send a text WebSocket frame."""
    payload = msg.encode()
    hdr = bytearray([0x81])  # FIN + text frame
    length = len(payload)
    if length < 126:
        hdr.append(length)
    elif length < (1 << 16):
        hdr.append(126)
        hdr.extend(struct.pack("!H", length))
    else:
        hdr.append(127)
        hdr.extend(struct.pack("!Q", length))
    writer.write(hdr + payload)
    await writer.drain()
