import requests
from datetime import datetime
from escpos.printer import Usb
import qrcode
import json
import textwrap
import os


# -------------------------- Weekday and Date --------------------------

dt = datetime.now()
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Try out different formatting options for strftime :)
weekday = days_of_week[int(dt.weekday())]
date = dt.strftime("%d/%m/%Y")

# -------------------------- Weather API Call --------------------------

WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Bristol"
API_KEY = "Your API Key"

WEATHER_URL = WEATHER_BASE_URL + "q=" + CITY + "&appid=" + API_KEY

response = requests.get(WEATHER_URL)

if response.status_code == 200:
   data = response.json()
   main = data['main']
   temperature = main['temp']
   humidity = main['humidity']
   pressure = main['pressure']

   report = data['weather']
   print(f"{CITY:-^30}")
   print(f"Temperature: {temperature}")
   print(f"Humidity: {humidity}")
   print(f"Pressure: {pressure}")
   print(f"Weather Report: {report[0]['description']}")
else:
   print("Error in the HTTP request")

# ---------------------------- Linebreak add ----------------------------

linebreak = "----------------"

# -------------------------- TickTick API Call --------------------------

api_url = "tick tick api url"
api_key = "???"
tick_client_id = "uSo6C45l19jMGuN0Km"
tick_client_secret = "qqL&nTD)CiK4XLs55(iLHmbSau5(k+*9"

response2 = requests.get(api_url)
response2.json()

# ---------------------------- Linebreak add ----------------------------

linebreak = "----------------"

# ---------------------------- News API Call ----------------------------

api_url = "news api url"
api_key = "???"

response3 = requests.get(api_url)
response3.json()

# ---------------------------- Print It Out! ----------------------------

# 0x416 and 0x5011 are the details we extracted from lsusb
# 0x81 and 0x03 are the bEndpointAddress for input and output
p = Usb(0x416, 0x5011, in_ep=0x81, out_ep=0x03, profile="POS-5890")

# Create and print a QR code or other image
# qr = qrcode.make('https://arnon.dk')
# qr.save('qrcode.png')
# Print the qr or other image
# p.image('qrcode.png')

# Print out the text
# p.text("Hello world!\n")
# p.text("This print should work!\n")
# p.text("---------------\n\n\n")

printer = open("print.txt", "w")

printer.write("Australian News\n\n")

for article in response.json()['articles'][:headlines]:
    news = str(article['title'])
    news = textwrap.fill(news,20)
    printer.write(str(news) + "\n\n")


printer.close()