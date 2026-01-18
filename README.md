
<h1>Smart Library Zone Monitoring System</h1>

<p>
This repository contains the implementation of a proof-of-concept IoT application developed for
<b>CPC357: IoT Architecture & Smart Applications (Assignment 2)</b>.
The project demonstrates the design and development of a cloud-based IoT monitoring system using
Google Cloud Platform (GCP), simulated sensor data, and a web-based dashboard.
</p>

<hr>

<h2>1. Project Overview</h2>

<p>
The Smart Library Zone Monitoring System is designed to help library staff monitor environmental
conditions across multiple zones within a library. Each zone reports temperature and noise level
readings, which are collected, stored, and visualized through a web interface.
</p>

<p>
For this assignment, sensor data is simulated to represent real-world IoT devices.
The system focuses on demonstrating IoT architecture concepts, cloud deployment, data flow,
and basic security considerations rather than hardware implementation.
</p>

<p><b>Monitored Parameters:</b></p>
<ul>
    <li>Temperature (°C)</li>
    <li>Noise Level (dB)</li>
</ul>

<p><b>Monitored Zones:</b></p>
<ul>
    <li>Zone 1</li>
    <li>Zone 2</li>
    <li>Zone 3</li>
</ul>

<hr>

<h2>2. High-Level System Architecture (Overview)</h2>

<p>
The system follows a layered IoT architecture consisting of device simulation, communication,
cloud processing, data storage, and application layers.
</p>

<p>
<b>[Figure Placeholder]</b><br>
<i>Figure 1: High-level system architecture diagram</i>
</p>

<p>
At a high level:
</p>

<ul>
    <li>Simulated sensors publish data using MQTT</li>
    <li>An MQTT broker (Mosquitto) runs on a GCP VM</li>
    <li>A Python subscriber processes and validates incoming data</li>
    <li>Validated data is stored in MongoDB</li>
    <li>A Flask web application displays real-time and historical data</li>
</ul>

<hr>

<h2>3. Development Environment</h2>

<h3>3.1 Cloud Platform</h3>

<ul>
    <li>Google Cloud Platform (GCP)</li>
    <li>Compute Engine Virtual Machine</li>
    <li>Machine Type: e2-medium</li>
    <li>Operating System: Ubuntu 22.04 LTS (amd64, jammy)</li>
</ul>

<h3>3.2 Software Stack</h3>

<ul>
    <li>Python 3</li>
    <li>Flask (Web Application)</li>
    <li>MongoDB 6.0</li>
    <li>MQTT (Mosquitto Broker)</li>
    <li>Paho MQTT Client</li>
</ul>

<hr>

<h2>4. Development Process</h2>

<p>
This section outlines the step-by-step development process used to build and run the system.
This process is designed so the project can be deployed by cloning the repository directly
onto a GCP VM.
</p>

<h3>4.1 VM Setup on GCP</h3>

<ol>
    <li>Create a new Compute Engine VM on GCP</li>
    <li>Select Ubuntu 22.04 LTS as the operating system</li>
    <li>Choose e2-medium machine type</li>
    <li>Default settings for the rest</li>
</ol>

<p><b>[Screenshot Placeholder]</b><br>
<i>Figure 2: GCP VM instance configuration page</i></p>

<h3>4.2 Firewall Configuration</h3>

<p>
The following firewall rules were configured on GCP:
</p>

<ul>
    <li><b>allow-flask-5000</b> – Allows access to the Flask web application</li>
    <li><b>allow-mqtt-1883</b> – Allows MQTT communication</li>
</ul>

<p>
Currently, these rules allow traffic from all IP addresses (0.0.0.0/0) for development and testing.
In an ideal deployment, access would be restricted to trusted sensor devices and internal library PCs within the library itself.
</p>

<h3>4.3 Installing Dependencies</h3>

<p>
After connecting to the VM via SSH, the repository is cloned and dependencies are installed:
</p>

<p><b>Example Codes to Run:</b><br></p>

<pre>
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git curl gnupg -y

# Install MQTT broker
sudo apt install mosquitto mosquitto-clients -y
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Install MongoDB 6.0
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor

echo "deb [ arch=amd64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] \
https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt update
sudo apt install mongodb-org -y
sudo systemctl enable mongod
sudo systemctl start mongod

# Clone repository and install Python dependencies
git clone &lt;repository-url&gt;
cd &lt;repository-folder&gt;
pip3 install -r requirements.txt

# Run system components in separate terminals
python3 app.py
python3 mqtt_to_mongo.py
python3 sensor_simulator.py
</pre>

<h3>4.4 Running the System Components</h3>

<p>
The system is designed to run using three separate terminal sessions on the same VM:
</p>

<ul>
    <li><b>Terminal 1:</b> Flask Web Application (<code>app.py</code>)</li>
    <li><b>Terminal 2:</b> MQTT Subscriber to MongoDB (<code>mqtt_to_mongo.py</code>)</li>
    <li><b>Terminal 3:</b> Sensor Data Simulator (<code>sensor_simulator.py</code>)</li>
</ul>

<p><b>[Screenshot Placeholder]</b><br>
<i>Figure 3: Three VM terminal sessions running different system components.</i></p>

<h3>4.5 Data Flow Execution</h3>

<ol>
    <li>The sensor simulator publishes temperature and noise data to MQTT topics</li>
    <li>The MQTT broker receives and forwards messages</li>
    <li>The subscriber validates and processes incoming data</li>
    <li>Validated data is stored in MongoDB</li>
    <li>The Flask app retrieves and displays the data on the dashboard</li>
</ol>

<h2>5. Security Considerations</h2>

<p>
Several basic security measures were considered and implemented in this project.
</p>

<h3>5.1 Implemented Security Measures</h3>

<ul>
    <li>MQTT broker and MongoDB run only within the GCP VM</li>
    <li>Firewall rules control access to exposed services</li>
    <li>MongoDB authentication is enabled with a dedicated user account</li>
    <li>Backend-only database access (no direct frontend access)</li>
    <li>Input validation in MQTT subscriber to ensure data integrity</li>
</ul>

<h3>5.2 Limitations and Future Improvements</h3>

<ul>
    <li>No TLS/SSL encryption for MQTT or Flask endpoints</li>
    <li>No user authentication for the web dashboard</li>
    <li>Firewall rules currently allow all IPs for testing</li>
</ul>

<p>
Future enhancements could include TLS-enabled MQTT (MQTTS), IP-restricted firewall rules,
and role-based user authentication for the dashboard.
</p>

<hr>

<h2>Notes</h2>

<p>
This project serves as a proof-of-concept IoT system focused on architecture, cloud deployment,
and data handling. The use of simulated data allows development and testing without physical
hardware while still reflecting real-world IoT workflows.
</p>

