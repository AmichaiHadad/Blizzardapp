from flask import Flask, request
import requests
import os
import socket

app = Flask(__name__)

WEATHER_API_KEY = os.getenv('OPEN_WEATHER_TOKEN')
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_tel_aviv_temperature():
    try:
        params = {
            'q': 'Tel Aviv,IL',
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data['main']['temp']
    except Exception as e:
        return f"Error fetching temperature: {str(e)}"

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/')
def hello():
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    container_name = socket.gethostname()
    temperature = get_tel_aviv_temperature()
    
    return {
        'message': f'Welcome to the Blizzard Python App running on {container_name}!',
        'client_ip': client_ip,
        'tel_aviv_temperature': f'{temperature}°C',
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 