import asyncio
import json
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

CHANNEL = "weather_channel"

@app.on_event("startup")
async def startup_event():
    app.state.redis = redis.Redis(host="localhost", port=6379, db=0)
    app.state.pubsub = app.state.redis.pubsub()
    await app.state.pubsub.subscribe(CHANNEL)
    print(f"Suscrito al canal: {CHANNEL}")

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.pubsub.unsubscribe(CHANNEL)
    await app.state.redis.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Cliente conectado al WebSocket")

    try:
        async for message in app.state.pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await websocket.send_json(data)
    except Exception as e:
        print("❌ Error:", e)
    finally:
        await websocket.close()
        print("Cliente desconectado")
