import requests
from PIL import Image
from io import BytesIO
import pandas as pd
import os

# Directory where images will be stored
output_directory = 'maps'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


# Load your dataset
df = pd.read_csv('/Users/ruim/Downloads/More_Atlanta_Supply.csv')  # Make sure your dataset has 'latitude' and 'longitude' columns

# Bing Maps API key
api_key = 'AmQp_QH07fksyVSNpqSJfKSuvDmrSpHGGNHlMZG8F1JL1tzxOrvpiV6sDPAoXlNa'

# Function to fetch and save map images
def fetch_save_map(lat, lon, filename):
    url = f"https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/{lat},{lon}/19?mapSize=800,800&format=jpeg&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(os.path.join(output_directory, filename))
    else:
        print("Failed to fetch image for coordinates:", lat, lon)

# Loop through the dataset
for index, row in df.iterrows():
    filename = f"map_{index}.jpg"
    fetch_save_map(row['Latitude'], row['Longitude'], filename)