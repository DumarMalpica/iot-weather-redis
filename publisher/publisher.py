import time
import requests
import redis
import json

# Configuración de Redis
r = redis.Redis(host="localhost", port=6379, db=0)

# Ejemplo: Open-Meteo API (no requiere API key)
API_URL = "https://api.open-meteo.com/v1/forecast?latitude=5.07&longitude=-75.52&current_weather=true"

def get_weather():
    """Consulta API pública de clima"""
    response = requests.get(API_URL)
    data = response.json()
    weather = data.get("current_weather", {})
    return {
        "temperature": weather.get("temperature"),
        "windspeed": weather.get("windspeed"),
        "time": weather.get("time"),
    }

def main():
    while True:
        weather_data = get_weather()
        r.publish("weather_channel", json.dumps(weather_data))
        print(f"Publicado: {weather_data}")
        time.sleep(5)  # cada 5 segundos

if __name__ == "__main__":
    main()