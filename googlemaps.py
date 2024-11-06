import time
import folium
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env or api.env file
load_dotenv(dotenv_path='api.env')  # Adjust if your file is api.env or .env
api_key = os.getenv("GOOGLE_API_KEY")

def plot_green_spaces_on_map(api_key, location="53.483959,-2.244644", radius=5000, type="park"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,
        "type": type,
        "key": api_key
    }

    # Create a map centered around Manchester
    m = folium.Map(location=[53.483959, -2.244644], zoom_start=12)

    while True:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()

            if data["status"] == "OK":
                for space in data["results"]:
                    lat = space["geometry"]["location"]["lat"]
                    lng = space["geometry"]["location"]["lng"]
                    name = space.get("name")

                    # Add a marker for each green space
                    folium.Marker([lat, lng], popup=name).add_to(m)

                # Check for next page token (pagination)
                if "next_page_token" in data:
                    params["pagetoken"] = data["next_page_token"]
                    time.sleep(2)  # wait a bit for the token to activate
                else:
                    break
            else:
                print("Error:", data["status"], data.get("error_message", ""))
                break
        except requests.exceptions.RequestException as e:
            print("An error occurred with the request:", e)
            break

    # Save map to an HTML file
    m.save("green_spaces_map.html")
    print("Map has been saved to 'green_spaces_map.html'")

# Run the function
if api_key:  # Ensure that the API key is not empty
    plot_green_spaces_on_map(api_key)
else:
    print("API key is missing. Please add it to your .env file.")
