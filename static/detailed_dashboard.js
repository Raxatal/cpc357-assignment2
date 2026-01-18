document.addEventListener("DOMContentLoaded", () => {
    const zones = ['zone1', 'zone2', 'zone3'];
    const chartInstances = {}; // Store charts here so  can call .update() later

    function refreshData() {
        fetch('/historical')
            .then(response => response.json())
            .then(data => {
                zones.forEach(zone => {
                    const zoneData = data[zone];

                    // Separate the data by sensor type first
                    // Take the 10 most recent ones for the graph
                    const tempReadings = zoneData.filter(d => d.sensor === 'temperature').slice(-10);
                    const noiseReadings = zoneData.filter(d => d.sensor === 'noise').slice(-10);

                    // Map data for Chart.js
                    const tempLabels = tempReadings.map(d => new Date(d.timestamp).toLocaleTimeString('en-US'));
                    const tempValues = tempReadings.map(d => d.value);
                    const noiseValues = noiseReadings.map(d => d.value);

                    // Update the charts. Use same labels for both to keep X-axis insync
                    updateChart(`${zone}-temp`, tempLabels, tempValues, 'Temperature (°C)', '#5c2ca5', 'rgba(92,44,165,0.2)');
                    updateChart(`${zone}-noise`, tempLabels, noiseValues, 'Noise (dB)', '#e07c5e', 'rgba(224,124,94,0.2)');
                });
            })
            .catch(err => console.error("Historical fetch failed:", err));
    }

    function updateChart(id, labels, values, label, color, bgColor) {
        const canvas = document.getElementById(`${id}-chart`);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        
        if (chartInstances[id]) {
            // Already got, just swap the data and refresh
            chartInstances[id].data.labels = labels;
            chartInstances[id].data.datasets[0].data = values;
            chartInstances[id].update('none'); // 'none' prevents the annoying jumping animation
        } else {
            // Create the chart
            chartInstances[id] = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: label,
                        data: values,
                        borderColor: color,
                        backgroundColor: bgColor,
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { 
                        legend: { labels: { color: '#ffffff' } } 
                    },
                    scales: {
                        x: { ticks: { color: '#ffffff' } },
                        y: { ticks: { color: '#ffffff' } }
                    }
                }
            });
        }
    }

    // Load data immediately, then set the loop
    refreshData();
    setInterval(refreshData, 5000);
});
