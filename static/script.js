const readingChart = new Chart(document.getElementById("readingChart"), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Sensor Reading (PPM)', data: [], borderColor: '#007BFF', fill: true, backgroundColor: 'rgba(0,123,255,0.2)', tension: 0.4 }] }
});

const alertChart = new Chart(document.getElementById("alertChart"), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Alert Value (PPM)', data: [], borderColor: '#dc3545', fill: true, backgroundColor: 'rgba(220,53,69,0.2)', tension: 0.4 }] }
});

function fetchLatest() {
    fetch('/data').then(res => res.json()).then(data => {
        if (!data.value) return;
        const time = new Date(data.timestamp).toLocaleTimeString();
        document.getElementById("readingValue").textContent = data.value.toFixed(2);
        document.getElementById("readingTime").textContent = new Date(data.timestamp).toLocaleString();

        readingChart.data.labels.push(time);
        readingChart.data.datasets[0].data.push(data.value);
        if (readingChart.data.labels.length > 20) {
            readingChart.data.labels.shift();
            readingChart.data.datasets[0].data.shift();
        }
        readingChart.update();

        if (data.value > 200) {
            document.getElementById("alertTile").classList.add("blink");
            document.getElementById("alertTile").textContent = "ALERT";
        } else {
            document.getElementById("alertTile").classList.remove("blink");
            document.getElementById("alertTile").textContent = "ACTIVE";
        }

        fetch('/history/alerts').then(r => r.json()).then(alerts => {
            const today = new Date().toISOString().split("T")[0];
            document.getElementById("alertCount").textContent = alerts[today] || 0;
        });

        fetch('/history/alert-events').then(res => res.json()).then(events => {
            alertChart.data.labels = events.map(e => new Date(e.timestamp).toLocaleTimeString());
            alertChart.data.datasets[0].data = events.map(e => e.value);
            alertChart.update();
        });
    });
}
setInterval(fetchLatest, 5000);
fetchLatest();

function showModal(id) {
    document.getElementById(id).style.display = 'flex';
    if (id === 'readingModal') {
        fetch('/history/readings').then(res => res.json()).then(data => {
            new Chart(document.getElementById('readingHistoryChart'), {
                type: 'line',
                data: {
                    labels: data.map(d => d.day),
                    datasets: [{ label: 'Avg Reading', data: data.map(d => d.average), borderColor: '#007BFF', backgroundColor: 'rgba(0,123,255,0.2)', fill: true }]
                }
            });
        });
    } else if (id === 'alertModal') {
        fetch('/history/alerts').then(res => res.json()).then(data => {
            new Chart(document.getElementById('alertHistoryChart'), {
                type: 'bar',
                data: {
                    labels: Object.keys(data),
                    datasets: [{ label: 'Alerts Per Day', data: Object.values(data), backgroundColor: 'rgba(255,99,132,0.4)', borderColor: '#dc3545' }]
                }
            });
        });
    }
}
function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}