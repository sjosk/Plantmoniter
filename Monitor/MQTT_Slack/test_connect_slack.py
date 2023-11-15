import paho.mqtt.client as mqtt
import requests
import json
from datetime import datetime, timedelta

# Setup MQTT
MQTT_SERVER = "your.mqtt.server.address"
MQTT_PORT = 1883
MQTT_TOPIC = "your/topic"

# Setup Slack Webhook
SLACK_WEBHOOK_URL = "your_slack_webhook_url"
last_sent_time = None


# Test the connection to the MQTT server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
        # Subscribe to the topic and test
        result, mid = client.subscribe(MQTT_TOPIC)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print(f"Subscribed to {MQTT_TOPIC} with MID {mid}")
        else:
            print(f"Failed to subscribe, error code: {result}")
    else:
        print(f"Failed to connect, return code {rc}")

# Receive messages(value) from the MQTT server
def on_message(client, userdata, msg):
    global last_sent_time
    message = msg.payload.decode('utf-8')
    print(f"Received message: {message} from topic: '{msg.topic}'")

    # Get current time
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    
    try:
        value = float(message)
        print(f"Value: {value}")
        payload = None
        # Check if the current time is between 9:30 and 21:00
        # Message will be sent every 30 minutes if the value is less than 8 or greater than 300
        if 9 <= current_hour < 21 or (current_hour == 9 and current_minute >= 30):
            if value < 8:
                if last_sent_time is None or now - last_sent_time >= timedelta(minutes=30):
                    payload = {'text': 'Hi🍻 Time to have a drink'}
                    last_sent_time = now
            elif value > 300:
                if last_sent_time is None or now - last_sent_time >= timedelta(minutes=30):
                    payload = {'text': 'Hey! I need some sunshine☀️'}
                    last_sent_time = now
        else:
            payload = None

        if payload:
            response = requests.post(SLACK_WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                print("Message sent successfully")
            else:
                print(f"Failed to send message to Slack, status code: {response.status_code}")
    except ValueError:
        print("Received message is not a valid float")


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT server
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Subscribe to the topic
client.subscribe(MQTT_TOPIC)

# Start the loop
client.loop_forever()
