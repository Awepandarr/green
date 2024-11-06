import time
import requests
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env or api.env file
load_dotenv(dotenv_path='api.env')  # Adjust if your file is api.env or .env
api_key = os.getenv("GOOGLE_API_KEY")

def save_green_spaces_to_csv(api_key, location="53.483959,-2.244644", radius=10000, types = {
    "park": [
        "Urban park",
        "Community park",
        "Public park",
        "Playground",
        "Sports field",
        "Picnic area",
        "Recreational park",
        "Walking trail",
        "Skate park",
        "Dog park",
        "Nature reserve park",
        "Adventure park",
        "Green space park",
        "Park benches",
        "Botanical park",
        "Green"
    ],
    "garden": [
        "Botanical garden",
        "Community garden",
        "Urban garden",
        "Herb garden",
        "Flower garden",
        "Vegetable garden",
        "Rooftop garden",
        "Xeriscape garden",
        "Japanese garden",
        "Herbaceous garden",
        "Tropical garden",
        "Rose garden",
        "Wildlife garden",
        "Greenhouse garden",
        "Urban farming"
    ],
    "natural_feature": [
        "Forest",
        "Wetland",
        "Riverbank",
        "Beach",
        "Mountain",
        "Hillside",
        "Stream",
        "Coastal area",
        "Wilderness area",
        "Cliff",
        "Valley",
        "Lake",
        "Wetlands",
        "Sand dune",
        "Nature trail"
    ]
}, keyword="green space"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Open a CSV file to write the data
    with open('green_spaces.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(["Name", "Latitude", "Longitude", "Type"])

        # Loop through the place types
        for place_type in types:
            params = {
                "location": location,
                "radius": radius,
                "type": place_type,
                "keyword": keyword,  # Use keyword for broader search results
                "key": api_key
            }

            while True:
                response = requests.get(url, params=params)
                data = response.json()

                if data["status"] == "OK":
                    # Write each green space to the CSV file
                    for space in data["results"]:
                        name = space.get("name")
                        lat = space["geometry"]["location"]["lat"]
                        lng = space["geometry"]["location"]["lng"]
                        type_of_place = space.get("types", ["Unknown"])[0]  # Getting the first type if available
                        
                        # Write the details into the CSV file
                        writer.writerow([name, lat, lng, type_of_place])

                    # Pagination: check if there's a next page of results
                    if "next_page_token" in data:
                        params["pagetoken"] = data["next_page_token"]
                        time.sleep(2)  # Wait a bit for the next page token to activate
                    else:
                        break
                else:
                    print("Error:", data["status"], data.get("error_message", ""))
                    break

    print("Green spaces data has been saved to 'green_spaces.csv'.")

# Run the function
if api_key:  # Ensure that the API key is not empty
    save_green_spaces_to_csv(api_key)
else:
    print("API key is missing. Please add it to your .env file.")
