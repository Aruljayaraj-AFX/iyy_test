from fastapi import FastAPI
import paho.mqtt.client as mqtt

app = FastAPI()

MQTT_BROKER = "broker.mqtt.cool"
MQTT_PORT   = 1883
MQTT_TOPIC  = "home/bulb"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

@app.get("/ON")
async def turn_on():
    client.publish(MQTT_TOPIC, "ON")
    return {"status": "ON"}

@app.get("/OFF")
async def turn_off():
    client.publish(MQTT_TOPIC, "OFF")
    return {"status": "OFF"}
