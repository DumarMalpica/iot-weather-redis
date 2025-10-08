const log = document.getElementById("log");

// Conecta al WebSocket
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => {
  log.textContent = "✅ Conectado al WebSocket...\n";
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  const timestamp = new Date().toLocaleTimeString();

  // Añade el JSON recibido con formato
  log.textContent += `[${timestamp}] ${JSON.stringify(data, null, 2)}\n\n`;

  // Mantiene el scroll abajo
  log.scrollTop = log.scrollHeight;
};

ws.onerror = (e) => {
  log.textContent += `❌ Error WebSocket: ${e.message}\n`;
};

ws.onclose = () => {
  log.textContent += "🔴 Conexión cerrada\n";
};
