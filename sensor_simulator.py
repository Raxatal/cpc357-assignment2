import paho.mqtt.client as mqtt
import random
import time
from datetime import datetime

# Settings
BROKER = "localhost" 
PORT = 1883
ZONES = ["zone1", "zone2", "zone3"]
SENSORS = ["temperature", "noise"]

# Setup the client
client = mqtt.Client("SimulatedSensorPublisher")
client.connect(BROKER, PORT, 60)

print("Publisher started. Sending data every 5 seconds...")

try:
    while True:
        for zone in ZONES:
            # Generate some random fake data
            temp_value = round(random.uniform(22.0, 30.0), 2)
            noise_value = round(random.uniform(40.0, 70.0), 2)

            # Package it with a timestamp
            readings = {
                "temperature": temp_value,
                "noise": noise_value,
                "timestamp": datetime.utcnow().isoformat()
            }

            for sensor in SENSORS:
                # Topic structure: library/zone1/temperature
                topic = f"library/{zone}/{sensor}"
                payload = str(readings[sensor])
                
                client.publish(topic, payload)
                print(f"[{zone}] {sensor}: {payload}")

        # Wait 5 seconds before next loop
        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopping simulation...")
    client.disconnect()
