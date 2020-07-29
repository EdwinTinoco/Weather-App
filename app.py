import requests 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def index():
   cities = ["Seattle", "London"]
   
   url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=9d1a51b2ab22bce1c4c257c35981bf61'     
   

   weather_data = []  
   for city in cities:
      r = requests.get(url.format(city)).json() 

      weather = {
         'city': city,
         'temperature': r['main']['temp'],
         'description': r['weather'][0]['description'],
         'icon': r['weather'][0]['icon']
      }

      weather_data.append(weather)
      

   return render_template('weather.html', weather_data=weather_data)






if __name__ == '__main__':
    app.run(debug=True)