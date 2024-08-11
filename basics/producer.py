import asyncio
import json
import logging
import time

import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_signal_logging(pc):

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        logger.info("Connection state is %s", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()


def setup_producer_logic():
    pc = RTCPeerConnection()
    add_signal_logging(pc)

    @pc.on("datachannel")
    def on_datachannel(channel):
        print("Data channel created by consumer")

        async def send_pings():
            while True:
                channel.send("ping %d" % time.time())
                await asyncio.sleep(1)

        if channel.readyState == "open":
            asyncio.ensure_future(send_pings())
        else:
            @channel.on("open")
            def on_open():
                asyncio.ensure_future(send_pings())

    return pc


async def producer():
    pc = setup_producer_logic()
    async with websockets.connect("ws://127.0.0.1:8000/ws") as ws:
        # Receive session description from consumer
        data = await ws.recv()
        obj = RTCSessionDescription(**json.loads(data))
        print(json.loads(data)['sdp'])
        await pc.setRemoteDescription(obj)
        # Build and send answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        answer_data = json.dumps({
            "sdp": pc.localDescription.sdp, 
            "type": pc.localDescription.type
        })
        await ws.send(answer_data)
        print("Signalling done, keeping loop running for one minute")
        # Signalling done, keep loop running for one minute
        await asyncio.sleep(60)
        await pc.close()


asyncio.run(producer())
