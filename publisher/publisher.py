import time
import requests
import redis
import json
import datetime

# Configuración de Redis
r = redis.Redis(host="localhost", port=6379, db=0)

# Ejemplo: Open-Meteo API (no requiere API key)
API_URL = "https://api.open-meteo.com/v1/forecast?latitude=5.07&longitude=-75.52&current_weather=true"
CHANNEL = "weather_channel" 

SENSORS = {
    "Bogotá, Colombia": (4.7110, -74.0721),
    "Buenos Aires, Argentina": (-34.6037, -58.3816),
    "Lima, Perú": (-12.0464, -77.0428),
    "Santiago, Chile": (-33.4489, -70.6693),
    "Quito, Ecuador": (-0.1807, -78.4678),
    "La Paz, Bolivia": (-16.4897, -68.1193),
    "Montevideo, Uruguay": (-34.9011, -56.1645),
    "Asunción, Paraguay": (-25.2637, -57.5759),
    "Caracas, Venezuela": (10.4806, -66.9036),
    "Georgetown, Guyana": (6.8013, -58.1551),
}


def get_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather = data.get("current_weather", {})

        return {
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed"),
            "time": weather.get("time"),
        }

    except Exception as e:
        return None

def main():

    while True:
        for city, (lat, lon) in SENSORS.items():
            weather_data = get_weather(lat, lon)

            if weather_data:
                weather_data.update({
                    "city": city,
                    "sensor_id": city.lower().replace(" ", "_"),
                    "timestamp": datetime.datetime.now().isoformat()
                })

                r.publish(CHANNEL, json.dumps(weather_data))

            time.sleep(1)

        time.sleep(5)

if __name__ == "__main__":
    main()