import requests 
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'benjy2012!'
app.config['MYSQL_DB'] = 'weather_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/', methods=["GET", "POST"])
def index():
   if request.method == 'POST':
      cities_name = request.form.get('city')

      if cities_name:
         cur = mysql.connection.cursor()
         cur.callproc("spInsertNewCity", [cities_name])
         mysql.connection.commit()
         cur.close()


   cur = mysql.connection.cursor()
   cur.callproc("spGetAllCities", ())
   cities = cur.fetchall()
   cur.close()
   
   url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=9d1a51b2ab22bce1c4c257c35981bf61'  

   weather_data = []  
   for city in cities:
      response = requests.get(url.format(city['cities_name'])).json() 

      weather = {
         'city': city['cities_name'],
         'temperature': response['main']['temp'],
         'description': response['weather'][0]['description'],
         'icon': response['weather'][0]['icon']
      }

      weather_data.append(weather)
      

   return render_template('weather.html', weather_data=weather_data)






if __name__ == '__main__':
    app.run(debug=True)