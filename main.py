import streamlit as st
import requests
import pandas as pd


## Pull data

facility = pd.read_excel("data/data_20240308_combined_v2.xlsx")
future = pd.read_excel("data/Future_Annual_Hamilton.xlsx")
pcic = pd.read_excel("data/PCIC_Hamilton_Climate.xlsx")

# Function to call OpenWeather API for short-term forecast
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
    # print(data['list'][0])
    
    return weather_data

# Function to retrieve PCIC data for long-term forecast
def get_long_term_forecast(year):
    # Replace this with your actual PCIC data retrieval logic
    # For demonstration, let's assume we return some dummy data
    pcic_data = []
    for month in range(1, 13):
        monthly_data = {
            'DateTime': f'{year}-{month}-01',  # Example date
            'Temperature': 20,
            'Precipitation': 'Low',
            'Season': 'Summer',
            'Extreme Weather': 'None',
            'Frosting': 'None',
            'Freeze': 'None'
        }
        pcic_data.append(monthly_data)
    return pcic_data

# Function to perform historical comparison and risk assessment
def perform_analysis(forecast_data):
    # Historical comparison logic
    # Risk assessment logic
    # For demonstration, let's assume no historical comparison or risk assessment
    pass

# Function to generate report
def generate_report(forecast_type, forecast_data):
    # Report generation logic
    # For demonstration, let's assume we print the forecast data
    st.subheader(f'{forecast_type} Forecast Data:')
    for data in forecast_data:
        st.write(data)

# Main function
def main():
    st.title('Weather Analysis and Risk Mitigation')
    
    # Get user input for forecast type
    forecast_type = st.radio("Choose forecast type:", ('Short Term', 'Long Term'))
    
    if forecast_type == 'Short Term':
        # Call function to get short-term forecast data
        forecast_data = get_short_term_forecast()
    else:
        # Allow user to choose year for long-term forecast
        selected_year = st.number_input("Enter the year:", min_value=1900, max_value=2022, value=2022)
        # Call function to get long-term forecast data
        forecast_data = get_long_term_forecast(selected_year)
    
    # Perform analysis (historical comparison and risk assessment)
    perform_analysis(forecast_data)
    
    # Generate report
    generate_report(forecast_type, forecast_data)

# Run the app
if __name__ == "__main__":
    main()
