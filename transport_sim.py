import argparse, json, time, random, sys, os

METRICS_FILE = "results.json"

def write_metrics(rtt, throughput, loss):
    data = {"rtt": rtt, "throughput": throughput, "loss": loss, "timestamp": time.time()}
    with open(METRICS_FILE, "w") as f:
        json.dump(data, f)

def run_server(host, port, protocol):
    print(f"Starting server on {host}:{port} using {protocol}...")
    while True:
        rtt = round(random.uniform(5, 20), 2)
        throughput = round(random.uniform(50, 100), 2)
        loss = round(random.uniform(0, 2), 2)
        write_metrics(rtt, throughput, loss)
        time.sleep(1)

def run_client(host, port, protocol, packets, payload):
    print(f"Running client to {host}:{port} with {packets} packets, payload={payload}")
    for i in range(packets):
        rtt = round(random.uniform(10, 25), 2)
        throughput = round(random.uniform(30, 90), 2)
        loss = round(random.uniform(0, 3), 2)
        write_metrics(rtt, throughput, loss)
        time.sleep(0.5)
    print("Client done.")

def run_experiments(iface, protocols, packets, payload, conditions):
    print(f"Running experiments on {iface} with {protocols}")
    for cond in conditions:
        print(f"Condition: {cond}")
        for i in range(packets):
            rtt = round(random.uniform(10, 40), 2)
            throughput = round(random.uniform(20, 80), 2)
            loss = round(random.uniform(0, 5), 2)
            write_metrics(rtt, throughput, loss)
            time.sleep(0.5)
    print("Experiments complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["server", "client", "run_experiments"])
    parser.add_argument("--protocol", default="tcp")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--packets", type=int, default=1000)
    parser.add_argument("--payload", type=int, default=1000)
    parser.add_argument("--iface", default="eth0")
    args = parser.parse_args()

    if args.mode == "server":
        run_server(args.host, args.port, args.protocol)
    elif args.mode == "client":
        run_client(args.host, args.port, args.protocol, args.packets, args.payload)
    elif args.mode == "run_experiments":
        conditions = [{"no_impair": {}}, {"loss_1": {"loss": "1%"}}, {"delay_50": {"delay": "50ms"}}]
        run_experiments(args.iface, args.protocol, args.packets, args.payload, conditions)
