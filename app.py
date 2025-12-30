import sys 
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        #set text for all labels and buttons
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        #align all buttons and labels to the center
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        #set ids for each button/label
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        #set font, font size and font weight
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;          
            }
            QLabel#city_label{
                font-size: 40px;
            }
            
            QLineEdit#city_input{
                font-size: 15px;                         
            }
            
            QPushButton#get_weather_button{
                font-size: 25px;
                font-weight: bold;
            }
            
            QLabel#temperature_label{
                font-size: 60px;       
            }
                           
            QLabel#emoji_label{
                font-size: 80px;
                font-family: "Apple Color Emoji";
            }
            
            QLabel#description_label{
                font-size: 30px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        #set api_key
        api_key = "YOUR_API_KEY_HERE"
        #get text for which city
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        #try to get data and if cod = 200, then pass the data through
        try: 
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            #return error message depending on which http error was returned
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthoried:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error("HTTP error occured:\n{http_error}")
                
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nPlease check your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")


    def display_error(self, message):  
        #if error is passed through, display the error
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message) 
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        #in case an error was displayed beforehand, reset the font size 
        self.temperature_label.setStyleSheet("font-size: 60px;")

        #get data of temperature from main
        temperature_k = data["main"]["temp"]
        #convert to celcius
        temperature_c = temperature_k - 273.15
        #get weather id
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        #edit label box to display weather. 
        self.temperature_label.setText(f"{temperature_c:.0f}℃")
        #set emoji
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        #edit label box to display description
        self.description_label.setText(weather_description)
    
    @staticmethod
    def get_weather_emoji(weather_id):
        #match the weater id with coresponding emoji
        if 200 <= weather_id <= 232:
            return "🌩️"
        elif 300 <= weather_id <= 321:
            return "⛅️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())