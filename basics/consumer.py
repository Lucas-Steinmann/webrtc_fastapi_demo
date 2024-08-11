import asyncio
import json
import logging

import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def setup_consumer_logic():
    config = RTCConfiguration(
        iceServers=[RTCIceServer(urls="stun:stun.l.google.com:19302")]
    )
    pc = RTCPeerConnection(config)
    channel = pc.createDataChannel("data")

    @channel.on("message")
    def on_message(message):
        print("Received message:", message)

    return pc


async def consumer():
    pc = setup_consumer_logic()
    async with websockets.connect("ws://127.0.0.1:8000/ws") as ws:
        # Set offer locally, aiortc will automatically gather ICE candidates
        await pc.setLocalDescription(await pc.createOffer())
        # Send offer to server via our websocket
        offer_data = json.dumps({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })
        await ws.send(offer_data)
        print("Offer sent")
        # Wait for answer
        data = await ws.recv()
        obj = RTCSessionDescription(**json.loads(data))
        await pc.setRemoteDescription(obj)
        # Signalling done, keep loop running for one minute
        print("Signalling done, keeping loop running for one minute")
        await asyncio.sleep(60)
        await pc.close()


asyncio.run(consumer())
