# Transport Simulation Dashboard

A web-based transport layer simulation system that allows users to control
simulation components and monitor real-time network performance metrics such as
Round Trip Time (RTT), Throughput, and Packet Loss.

This project is designed for academic and learning purposes.

---

## Objective

To simulate transport-layer communication and analyze network performance
parameters using a Python-based backend and a web dashboard interface.

---

## Project Structure

├── app.py # Flask backend server
├── transport_sim.py # Transport simulation logic
├── run.bat # Windows startup script
├── results.json # Generated simulation results
├── static/
│ ├── style.css # Dashboard styling
│ └── script.js # Client-side scripts
└── templates/
└── index.html # Web dashboard UI


---

## Features

- Start and stop simulation components
- Real-time monitoring of:
  - Round Trip Time (RTT)
  - Throughput
  - Packet Loss
- System activity logs
- Simple and interactive web interface

---

## Technologies Used

- Python
- Flask
- HTML, CSS, JavaScript

---

## How to Run

1. Install Python 3.x
2. Install required dependency:
   ```bash
   pip install flask
Run the application:

run.bat
or

python app.py
Open a browser and visit:

http://localhost:5000
Output
The system displays live transport metrics and logs through the web dashboard.
Simulation results are stored in results.json.

Academic Use
This project is developed as part of a transport/network simulation practical
for educational purposes.

Author
Sagar Rawat"# transport-simulation-dashboard" 
# transport-simulation-dashboard
