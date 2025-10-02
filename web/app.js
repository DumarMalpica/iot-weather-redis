const ctx = document.getElementById("tempChart").getContext("2d");

const tempChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [{
      label: "Temperatura (°C)",
      data: [],
      borderColor: "rgba(75, 192, 192, 1)",
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    scales: {
      x: { title: { display: true, text: "Tiempo" } },
      y: { title: { display: true, text: "Temperatura (°C)" } }
    }
  }
});

// Simulación: aquí en el futuro conectarías WebSocket/Fetch al subscriber
setInterval(() => {
  const fakeTemp = (20 + Math.random() * 10).toFixed(1);
  const now = new Date().toLocaleTimeString();

  tempChart.data.labels.push(now);
  tempChart.data.datasets[0].data.push(fakeTemp);
  tempChart.update();
}, 2000);