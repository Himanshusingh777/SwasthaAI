const form = document.getElementById('moodForm');
const tips = document.getElementById('tips');
const chartCanvas = document.getElementById('moodChart');

// Submit form data
form.addEventListener('submit', async(e) => {
    e.preventDefault();

    const entry = {
        date: document.getElementById('date').value,
        mood: +document.getElementById('mood').value,
        anxiety: +document.getElementById('anxiety').value,
        sleep: +document.getElementById('sleep').value,
        energy: +document.getElementById('energy').value,
        note: document.getElementById('note').value.trim()
    };

    // Save mood entry to backend
    const res = await fetch('/api/mood', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry)
    });

    if (res.ok) {
        tips.innerText = '';

        // Show helpful tips if mood is low or anxiety is high
        if (entry.mood <= 2 || entry.anxiety >= 4) {
            tips.innerText = '🧠 Try deep breathing, journaling, or visit https://mentalhealth.org.uk for help.';
        }

        alert("✅ Mood successfully logged!");
        form.reset();
        loadChart(); // Refresh the chart
    } else {
        alert("❌ Failed to log mood. Please try again.");
    }
});

// Load mood chart
async function loadChart() {
    const res = await fetch('/api/mood');
    const data = await res.json();

    const labels = data.map(d => d.date);
    const moodScores = data.map(d => d.mood);

    // Destroy existing chart if it exists
    if (window.moodChartInstance) {
        window.moodChartInstance.destroy();
    }

    window.moodChartInstance = new Chart(chartCanvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mood Over Time',
                data: moodScores,
                fill: true,
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.2)',
                tension: 0.3
            }]
        },
        options: {
            scales: {
                y: {
                    suggestedMin: 1,
                    suggestedMax: 5,
                    title: {
                        display: true,
                        text: 'Mood (1 = Low, 5 = High)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

// Load chart on page load
loadChart();