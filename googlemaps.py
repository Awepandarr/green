import time
import folium
import requests

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
        response = requests.get(url, params=params)
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

    # Save map to an HTML file
    m.save("green_spaces_map.html")
    print("Map has been saved to 'green_spaces_map.html'")

# Run the function
plot_green_spaces_on_map(api_key="AIzaSyAFLifMTkAtTSH3iMQO1nslp1PgtG4Mwvs")
