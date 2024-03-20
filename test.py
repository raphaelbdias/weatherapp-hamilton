import requests

# Function to convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_short_term_forecast():
    # Call OpenWeather API for short-term forecast (5 days)
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = '38ee75152fc50c6dc6762efbfa6d2a62'
    city = 'Hamilton' 
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    
    # Extract relevant weather information
    weather_data = []
    for forecast in data['list']:
        weather_info = {
            'DateTime': forecast['dt_txt'],
            'Temperature': forecast['main']['temp'],
            'Feels Like' : forecast['main']['feels_like'],
            'Weather': forecast['weather'][0]['main'],
            'description': forecast['weather'][0]['description'],
            'weather_icon': forecast['weather'][0]['icon'],
            'wind gusts': forecast['wind']['gust'],
            'Wind Speed': forecast['wind']['speed'],
            'Clouds': forecast['clouds']['all'],
            'Humidity': forecast['main']['humidity']
        }
        weather_data.append(weather_info)
    
    return weather_data

# Thresholds for risk assessment
thresholds = {
    "Wind Speed": [
        {"range": (10, 20), "category": "watch"},
        {"range": (20, 30), "category": "alert"},
        {"min": 30, "category": "warning"}
    ],
    "Temperature": [
        {"range": (-30, -20), "category": "warning"},
        {"range": (-20, -10), "category": "alert"},
        {"range": (20, 30), "category": "watch"},
        {"min": 30, "category": "warning"}  # Adjusted to only "warning" category without range
    ],
    "Humidity": [
        {"range": (0, 20), "category": "warning"},
        {"range": (20, 40), "category": "alert"},
        {"min": 40, "category": "warning"}  # Adjusted to only "warning" category without range
    ],
    "Clouds": [
        {"min": 0, "category": "No risk"},
        {"range": (1, 50), "category": "watch"},
        {"range": (50, 100), "category": "alert"},
        {"min": 100, "category": "warning"}
    ]
}
# Get short-term forecast data
forecast_data_list = get_short_term_forecast()

# Initialize risk categories for each forecast
risk_categories_list = []

# Iterate over each forecast data dictionary
for forecast_data in forecast_data_list:
    # Convert temperatures from Kelvin to Celsius
    forecast_data["Temperature"] = kelvin_to_celsius(forecast_data["Temperature"])
    forecast_data["Feels Like"] = kelvin_to_celsius(forecast_data["Feels Like"])

    # Initialize risk categories for the current forecast
    risk_categories = {}

    # Determine risk categories for each parameter in the current forecast
    for parameter, parameter_thresholds in thresholds.items():
        parameter_value = forecast_data.get(parameter)
        if parameter_value is not None:
            risk_category = None  # Initialize risk category
            for threshold in parameter_thresholds:
                if "range" in threshold:
                    min_value, max_value = threshold["range"]
                    if min_value <= parameter_value < max_value:
                        risk_category = threshold["category"]
                        break
                elif "min" in threshold:
                    min_value = threshold["min"]
                    if parameter_value >= min_value:
                        risk_category = threshold["category"]
                        break
            if risk_category == "warning":
                risk_categories[parameter] = {"value": parameter_value, "risk": risk_category}
            else:
                risk_categories[parameter] = {"value": parameter_value, "risk": risk_category if risk_category else "No risk"}
        else:
            # Handle missing data for the parameter
            risk_categories[parameter] = {"value": "missing", "risk": "data missing"}

    # Add the risk categories for the current forecast to the list
    risk_categories_list.append(risk_categories)

# Output risk categories for each forecast
for index, risk_categories in enumerate(risk_categories_list, start=1):
    print(f"Forecast {index} risk categories:")
    for parameter, values in risk_categories.items():
        print(f"{parameter}: Value = {values['value']}, Risk = {values['risk']}")
    print()