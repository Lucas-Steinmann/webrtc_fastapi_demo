# WebRTC FastAPI Demo

This project is the example code alongside my blog post ["WebRTC DataChannel via FastAPI by example"](www.steinm.net/blog/webrtc_fastapi_demo_basics/)

## Overview
This project demonstrates the integration of WebRTC with FastAPI. 
It includes a simple WebSocket server using FastAPI and WebRTC peer connection setup using aiortc.  

## Requirements

 * Python 3.8 or higher
 * FastAPI
 * aiortc
 * websockets

 
## Installation
 
Clone the repository:  

```bash
git clone https://github.com/Lucas-Steinmann/webrtc-fastapi-demo.git 
cd webrtc-fastapi-demo
```

Install the dependencies:  
```bash
pip install -r requirements.txt
```

## Running the Basic Application

If you run the application on different hosts, make sure to adapt the IP addresses and ports.
Also make sure the fast api server is reachable from the consumer and producer.

Terminal/Host 1: Start the FastAPI server:  

```bash
cd webrtc_fastapi_demo_basics/
fastapi dev
```

Terminal/Host 2: Run the producer:  

```bash
cd webrtc_fastapi_demo_basics/
python producer.py
```

Terminal/Host 3: Run the consumer:

```bash
cd webrtc_fastapi_demo_basics/
python consumer.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.