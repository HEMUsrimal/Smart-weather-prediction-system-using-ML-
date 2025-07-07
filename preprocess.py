import pandas as pd
import os

def preprocess_weather_data():
    print("📁 Current Working Directory:", os.getcwd())

    # Load weather and location data
    weather = pd.read_csv('data/weather.csv')
    locations = pd.read_csv('data/locations.csv')

    # Merge on location_id
    df = weather.merge(locations, on='location_id')

    # ✅ Parse date column correctly
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, format='mixed')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    # ✅ Convert sunrise and sunset to hour integers (optional)
    df['sunrise'] = pd.to_datetime(df['sunrise'], format='%H:%M', errors='coerce').dt.hour
    df['sunset'] = pd.to_datetime(df['sunset'], format='%H:%M', errors='coerce').dt.hour
    df['daylight_hours'] = df['sunset'] - df['sunrise']

    # ✅ Drop unnecessary columns
    df.drop(columns=[
        'date',
        'sunrise',
        'sunset',
        'utc_offset_seconds',
        'timezone',
        'timezone_abbreviation',
        'location_id'
    ], inplace=True)

    # ✅ Handle missing values
    df = df.dropna()  # You can change to df.fillna(method='ffill') if preferred

    # ✅ One-hot encode city_name
    df = pd.get_dummies(df, columns=['city_name'], drop_first=True)

    # ✅ Save cleaned dataset
    output_path = 'data/cleaned_data.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to: {output_path}")
    print("🎉 Preprocessing complete.")

if __name__ == '__main__':
    preprocess_weather_data()
