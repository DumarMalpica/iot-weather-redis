import { createClient } from "redis";

const client = createClient();

async function main() {
  await client.connect();
  console.log("Conectado a Redis - esperando datos...");

  await client.subscribe("weather_channel", (message) => {
    const data = JSON.parse(message);
    console.log("Recibido:", data);

    // Aquí podrías enviar los datos a la web con websockets
    // o guardarlos en un archivo temporal
  });
}

main().catch(console.error);