import paho.mqtt.client as mqtt
import requests
import json

# Setup MQTT
MQTT_SERVER = "your.mqtt.server.address"
MQTT_PORT = 1883
MQTT_TOPIC = "your/topic"

# Setup Slack Webhook
SLACK_WEBHOOK_URL = "your_slack_webhook_url"

# Test the connection to the MQTT server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
        # Subcribe to the topic and test
        result, mid = client.subscribe(MQTT_TOPIC)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print(f"Subscribed to {MQTT_TOPIC} with MID {mid}")
        else:
            print(f"Failed to subscribe, error code: {result}")
    else:
        print(f"Failed to connect, return code {rc}")


# Receive messages(value) from the MQTT server
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(f"Received message: {message} from topic: '{msg.topic}'")
    
    # transfer the form to float and check the value
    try:
        value = float(message)
        print(f"Value: {value}")
        # if the value of moisture is less than 8, send a message to Slack
        if value < 8:
            payload = {'text': 'Time to have a drink'}
            response = requests.post(SLACK_WEBHOOK_URL, json=payload)
            if response.status_code != 200:
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
