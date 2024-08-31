from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

# Mapping of weather conditions to Font Awesome icons
weather_icons = {
    "clear sky": "fas fa-sun",
    "few clouds": "fas fa-cloud-sun",
    "scattered clouds": "fas fa-cloud",
    "broken clouds": "fas fa-cloud",
    "shower rain": "fas fa-cloud-showers-heavy",
    "rain": "fas fa-cloud-rain",
    "thunderstorm": "fas fa-bolt",
    "snow": "fas fa-snowflake",
    "mist": "fas fa-smog",
}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check for empty strings or string with only spaces
    #if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        #city = "Kansas City"

    weather_data = get_current_weather(city)

    # City is not found by API
    if weather_data['cod'] != 200:
        return render_template('city-not-found.html')

    # Get the description and map to an icon class
    weather_description = weather_data["weather"][0]["description"].lower()
    icon_class = weather_icons.get(weather_description, "fas fa-question")

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_description.capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        icon_class=icon_class
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)