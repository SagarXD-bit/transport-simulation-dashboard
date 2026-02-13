async function start(mode) {
  const res = await fetch(`/start/${mode}`);
  logMessage(`▶ ${mode.charAt(0).toUpperCase() + mode.slice(1)} started`, "start");
}

async function stop(mode) {
  const res = await fetch(`/stop/${mode}`);
  logMessage(`⏹ ${mode.charAt(0).toUpperCase() + mode.slice(1)} stopped`, "stop");
}

async function updateMetrics() {
  const res = await fetch("/metrics");
  const data = await res.json();
  document.getElementById("rtt").textContent = data.rtt.toFixed(2);
  document.getElementById("throughput").textContent = data.throughput.toFixed(2);
  document.getElementById("loss").textContent = data.loss.toFixed(2);
}

function logMessage(msg, type = "info") {
  const box = document.getElementById("log-box");
  const p = document.createElement("p");
  p.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
  p.classList.add(`log-entry-${type}`);
  box.appendChild(p);
  box.scrollTop = box.scrollHeight; // auto-scroll
}

setInterval(updateMetrics, 2000);
