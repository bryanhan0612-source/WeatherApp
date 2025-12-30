# WeatherApp
A simple weather app built using Python, PyQt5, and the OpenWeather API.
Users can enter any city name and see the current temperature, weather description, and a matching emoji. 

Technologies Used
- Python 3
- PyQt5 (GUI)
- Requests (HTTP requests)
- OpenWeatherMap API

How to run the app:
1. Clone or download the project
2. Install all dependencies if not done already
- pip install PyQt5 requests
3. Run the application

API Key Setup:
1. Create an account at https://openweathermap.org/api
2. Generate your API key
3. Replace the API key in the code - api_key = "YOUR_API_KEY_HERE"

Error Handling:
This application handles 
- Invalid city names
- Network issues
- API errors (400–504)
- Timeouts and connection failures

Important Note: This application was originally designed for macOS as it uses Apple Color Emoji to render all emojis. For all windows users, replace the emoji font with "font-family: Segoe UI Emoji;"

Created by Bryan Han

For learning PyQt5, APIs, and GUI development in Python.
