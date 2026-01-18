import paho.mqtt.client as mqtt
import pymongo
from datetime import datetime, timezone

# MongoDB Setup
# User: monitor, Pass: Password123
mongo_client = pymongo.MongoClient("mongodb://monitor:Password123@localhost:27017/library_monitor")
db = mongo_client["library_monitor"]
collection = db["zone_readings"]

# MQTT Setup
BROKER = "localhost"
PORT = 1883
TOPIC = "library/#" # Subscribe to everything under library/

# Simple limits for the alert flag
THRESHOLDS = {
    "temperature": 28.0,
    "noise": 60.0
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker successfully")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed, code: {rc}")

def on_message(client, userdata, msg):
    try:
	# Input validation for topic
        # Expected topic format: library/zoneX/sensorType
        parts = msg.topic.split("/")
        if len(parts) != 3:
            return

        zone = parts[1]
        sensor = parts[2]

        # Input validation for security, don't save if incorrect format
        if zone not in ["zone1", "zone2", "zone3"] or sensor not in ["temperature", "noise"]:
            return

        try:
            val = float(msg.payload.decode("utf-8"))
        except ValueError:
            return

        # Check if this reading is over our defined limit
        is_alert = val > THRESHOLDS.get(sensor, 999.0)

        # Create the document for MongoDB
        doc = {
            "zone": zone,
            "sensor": sensor,
            "value": val,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "alert": is_alert
        }

        collection.insert_one(doc)
        print(f"Logged: {zone} {sensor} = {val} (Alert: {is_alert})")

    except Exception as e:
        print(f"Error in on_message: {e}")

# Start the MQTT loop
client = mqtt.Client("MongoSubscriber")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

print("Waiting for data...")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nClosing connection...")
    client.disconnect()
