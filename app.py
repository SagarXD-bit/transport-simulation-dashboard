from flask import Flask, render_template, jsonify
import subprocess, os, json, signal

app = Flask(__name__)
processes = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start/<mode>")
def start(mode):
    if mode not in ["server", "client", "controller"]:
        return "Invalid mode", 400

    if mode == "server":
        cmd = ["python", "transport_sim.py", "server", "--protocol", "tcp", "--host", "0.0.0.0", "--port", "9000"]
    elif mode == "client":
        cmd = ["python", "transport_sim.py", "client", "--protocol", "tcp", "--host", "127.0.0.1", "--port", "9000", "--packets", "100", "--payload", "1000"]
    else:  # controller
        cmd = ["python", "transport_sim.py", "run_experiments", "--iface", "eth0", "--protocol", "tcp", "--packets", "100", "--payload", "1000"]

    p = subprocess.Popen(cmd)
    processes[mode] = p
    return f"{mode} started!"

@app.route("/stop/<mode>")
def stop(mode):
    p = processes.get(mode)
    if p and p.poll() is None:
        os.kill(p.pid, signal.SIGTERM)
        return f"{mode} stopped!"
    return f"{mode} not running."

@app.route("/metrics")
def metrics():
    if not os.path.exists("results.json"):
        return jsonify({"rtt": 0, "throughput": 0, "loss": 0})
    with open("results.json") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
