#!/usr/bin/env python3

from __future__ import print_function
import requests
from datetime import datetime
from escpos.printer import Usb
import time
import os
import os.path


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


def get_weather():
   # Bristol Latitude & Longitude
   lat = 51.4545
   lon = -2.5879

   WEATHER_API_KEY = "REMOVED_WEATHER_API_KEY"
   WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"

   response = requests.get(WEATHER_URL)

   return_dictionary = {}
   if response.status_code == 200:
      data = response.json()
      report = data['weather']
      main = data['main']

      return_dictionary["condition"] = f"{report[0]['description']}"
      return_dictionary["temperature"] = main['temp']
      return_dictionary["humidity"] = main['humidity']
      return_dictionary["pressure"] = main['pressure']
      return_dictionary["icon"] = f"{report[0]['icon'][:2]}"
      return_dictionary["city"] = f"{data['name']}"
   else:
      print("Error in the HTTP request 1")
      print(response.status_code)

   return return_dictionary


def get_news():
   api_url = "https://newsapi.org/v2/top-headlines"
   query_params = {
      "language": "en",
      "category": "technology",
      "apiKey": "REMOVED_NEWS_API_KEY"
   }

   response = requests.get(api_url, params=query_params)
   
   return_list= []
   if response.status_code == 200:
      data = response.json()["articles"]
      articles = data[:3]

      for article in articles:
         return_list.append(article["title"])
   else:
      print("Error in the HTTP request 1")
      print(response.status_code)

   return return_list

def center_string(text):
   linelen = 32
   return (" " * int((linelen-len(text))/2)) + text


def main():
   # -------------------------- Weekday and Date --------------------------
   dt = datetime.now()
   days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

   # Try out different formatting options for strftime :)
   weekday = days_of_week[int(dt.weekday())]
   date = dt.strftime("%d/%m/%Y")

   # -------------------------- Weather API Call --------------------------
   weather_report = get_weather()
   # ------------------------ Google Tasks API Call ------------------------
   tasks = {"Sample List": [["Sample Task 1"], ["Sample Task 2"]], "Another List": [["Another Task"]]}
   # ---------------------------- News API Call ----------------------------
   news = get_news()
   # ---------------------------- Print It Out! ----------------------------

   # 0x456 and 0x0808 are the details we extracted from lsusb
   # 0x81 and 0x03 are the bEndpointAddress for input and output
   
   p = Usb(0x456, 0x0808, in_ep=0x81, out_ep=0x03, profile="POS-5890")

   # p.qr('https://www.youtube.com/watch?v=uHgt8giw1LY', size=8)

   p.text(f"{center_string(weekday)}\n")
   p.text(f"{center_string(date)}\n")
   p.image(f"/home/spacks/Documents/development/thermal-todos/icons/{weather_report['icon']}d.png", impl="bitImageRaster")
   p.text(f"{weather_report['city']}:\n")
   p.text(f"Temperature: {weather_report['temperature']}°C\n")
   p.text(f"Humidity: {weather_report['humidity']}%\n\n")
   p.text(f"{center_string('------------------')}\n\n")
   for tasklist in tasks:
      p.text(f"{tasklist}:\n")
      for task in tasks[tasklist]:
         p.text(f"[ ] - {task[0]}\n")
      p.text("\n")
      
   p.text(f"{center_string('------------------')}\n\n")
   for newsheadline in news:
      news_split = newsheadline.split(" - ")
      p.text(f"{news_split[0]}\n")
      p.text(f"- {news_split[1]}\n\n")

   p.text("\n\n\n")

if __name__ == '__main__':
    main()
