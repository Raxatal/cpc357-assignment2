from flask import Flask, render_template, jsonify
import pymongo

app = Flask(__name__)

# Connect to the local MongoDB instance
# Database name is library_monitor
mongo_client = pymongo.MongoClient("mongodb://monitor:Password123@localhost:27017/library_monitor")
db = mongo_client["library_monitor"]
collection = db["zone_readings"]

@app.route('/')
def index():
    # Just render the main landing page / home dashboard
    return render_template('index.html')

@app.route('/latest')
def latest():
    # Helper list for the zones we have in the library
    zones = ['zone1', 'zone2', 'zone3']
    latest_data = {}

    for zone in zones:
        # Get the most recent temperature reading for this zone
        # Sortin by timestamp -1 gives newest entry
        temp_doc = collection.find_one(
            {'zone': zone, 'sensor': 'temperature'},
            sort=[('timestamp', -1)]
        )
        # Do the same for noise reading
        noise_doc = collection.find_one(
            {'zone': zone, 'sensor': 'noise'},
            sort=[('timestamp', -1)]
        )

        # Store results in a dictionary, handle cases where the DB might be empty with '--'
        latest_data[zone] = {
            'temperature': round(temp_doc['value'], 2) if temp_doc else '--',
            'noise': round(noise_doc['value'], 2) if noise_doc else '--'
        }

    return jsonify(latest_data)

@app.route('/dashboard')
def dashboard_page():
    # route renders detailed charts page
    return render_template('detailed_dashboard.html')

@app.route("/historical")
def historical():
    zones = ["zone1", "zone2", "zone3"]
    historical_data = {}

    for zone in zones:
        # Fetch last 50 records per zone to fill the charts (only using latest 10)
        # Sorted ascending (1) so they appear in chronological order on the graph
        docs = list(collection.find({"zone": zone}).sort("timestamp", 1).limit(50))
        
        # MongoDB ObjectIds aren't JSON serialisable, need convert them to strings
        for doc in docs:
            doc["_id"] = str(doc["_id"])

        historical_data[zone] = docs

    return jsonify(historical_data)

if __name__ == '__main__':
    # Run on 0.0.0.0 so the VM can be accessed by its IP on the network
    app.run(host='0.0.0.0', port=5000, debug=True)
