document.addEventListener("DOMContentLoaded", () => {
    // Threshold constants for UI alertt
    const noiseThreshold = 60; 
    const tempHigh = 28;       
    const tempLow = 24;        
    const acDefault = 24;

    const updateData = () => {
        fetch('/latest')
            .then(response => response.json())
            .then(data => {
                for (const [zone, readings] of Object.entries(data)) {
                    const zoneBox = document.querySelector(`.zone-box[data-zone="${zone}"]`);
                    
                    if (zoneBox) {
                        const tempEl = zoneBox.querySelector('.temp-value');
                        const noiseEl = zoneBox.querySelector('.noise-value');

                        // Show the numeric values
                        tempEl.textContent = readings.temperature + ' °C';
                        noiseEl.textContent = readings.noise + ' dB';

                        // Change border color if it's too noisy
                        if (readings.noise > noiseThreshold) {
                            zoneBox.style.border = '4px solid red';
                        } else {
                            zoneBox.style.border = '2px solid #5c2ca5';
                        }

                        // Change font color for abnormal tem
                        if (readings.temperature > tempHigh) {
                            tempEl.style.color = 'red';
                        } else if (readings.temperature < tempLow) {
                            tempEl.style.color = 'blue';
                        } else {
                            tempEl.style.color = '#ffffff';
                        }
                    }
                }
            })
            .catch(err => console.error("Error updating dashboard:", err));
    };

    // Run every 5 seconds
    updateData();
    setInterval(updateData, 5000);

    // Set initial AC value on all zone boxes
    document.querySelectorAll('.ac-temp').forEach(el => {
        el.textContent = acDefault + ' °C';
    });

    // Handle the +/- buttons for the AC controls (just for demo purpose)
    document.querySelectorAll('.temp-adjust-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const zoneBox = e.target.closest('.zone-box');
            const acEl = zoneBox.querySelector('.ac-temp');
            let acTemp = parseFloat(acEl.textContent) || acDefault;

            if (btn.dataset.action === 'up') {
                acTemp += 1;
            } else if (btn.dataset.action === 'down') {
                acTemp -= 1;
            }

            acEl.textContent = acTemp.toFixed(1) + ' °C';
        });
    });
});
