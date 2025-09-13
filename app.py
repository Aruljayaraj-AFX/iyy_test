from fastapi import FastAPI, WebSocket
import asyncio
import paho.mqtt.client as mqtt

app = FastAPI()

clients = {}  # {websocket: topic}

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic
    # Send payload to all clients subscribed to this topic
    for ws, subscribed_topic in clients.items():
        if subscribed_topic == topic:
            asyncio.create_task(ws.send_text(payload))

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("broker.mqtt.cool", 1883, 60)
mqtt_client.loop_start()

@app.websocket("/ws/bulb")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    await websocket.accept()
    clients[websocket] = topic
    mqtt_client.subscribe(topic)  # subscribe dynamically
    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except:
        pass
    finally:
        mqtt_client.unsubscribe(topic)
        clients.pop(websocket, None)

@app.get("/publish/{topic}/{state}")
async def publish_topic(topic: str, state: str):
    mqtt_client.publish(topic, state)
    return {"topic": topic, "state": state}
