function setupConsumerLogic() {
    const config = {
        iceServers: [{urls: ['stun:stun.l.google.com:19302']}],
    };

    const pc = new RTCPeerConnection(config);
    const dataChannel = pc.createDataChannel('data');

    dataChannel.onmessage = event => {
        console.log('Received: ' + event.data);
    }
    return pc
}

async function createOffer() {
    const pc = setupConsumerLogic();
    const ws = new WebSocket('/ws')
    ws.onopen = async e => {
        // Create an offer
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);
        // Wait for ICE gathering to complete
        await new Promise((resolve) => {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
        // Finished gathering ice candidates, send offer to the server
        await ws.send(JSON.stringify(pc.localDescription));
        // Await answer
        ws.onmessage = async e => {
            const answer = JSON.parse(e.data);
            await pc.setRemoteDescription(answer);
        }
    }
}

// Run createOffer after page load
createOffer().then();
