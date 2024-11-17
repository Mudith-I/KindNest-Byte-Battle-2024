import json
import os
import time
from geopy.distance import geodesic
import folium

# Helper function: Reverse Geocoding (Dummy Function)
def reverseGeocoding(lat, lon):
    # Placeholder for real geocoding logic
    return f"Lat: {lat}, Lon: {lon}"

# Read User Data
def read_file():
    if not os.path.exists("users.json"):
        # If users.json does not exist, create it with default data
        data = {

            "normalUsername": ["Mudith", "Sanjeev"],
            "normalPassword": ["mud!th", "s@nj33v"],
            "adminUsername": ["rahul", "adit"],
            "adminPassword": ["r@hul", "@d!t"]
        }
        with open("users.txt", "w") as f:
            json.dump(data, f, indent=4)
    else:
        with open("users.json", "r") as f:
            data = json.load(f)
    return data

# Add Camps
def addCamps(latitude, longitude, name, date, time, details):
    camp = {
        "latitude": latitude,
        "longitude": longitude,
        "name": name,
        "date": date,
        "time": time,
        "details": details
    }

    file_name = "camps.json"

    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(camp)

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# User Functionality
def userIn(user_lat , user_lon , ranges):
    #os.system('clear')
    #print("Welcome, User!")
    #user_lat = float(input("Enter your latitude: "))
    #user_lon = float(input("Enter your longitude: "))
    user_location = (user_lat, user_lon)
    #os.system('clear')

    if not os.path.exists("camps.json") or os.path.getsize("camps.json") == 0:
        print("No events found.")
 
    with open('camps.json', 'r') as f:
        events = json.load(f)

    events_with_distance = []
    for event in events:
            event_lat = float(event["latitude"])
            event_lon = float(event["longitude"])
            event_location = (event_lat, event_lon)
            distance = geodesic(user_location, event_location).kilometers
            events_with_distance.append((event, distance))

    events_with_distance.sort(key=lambda x: x[1])

    # Create a new map object centered on the user's location
    folium_map = folium.Map(location=user_location, zoom_start=10)

        # Add the search radius as a circle
    folium.Circle(
            location=user_location,
            radius=ranges * 1000,  # Convert km to meters
            color="blue",
            fill=True,
            fill_opacity=0.2,
        ).add_to(folium_map)

        # Add events to the map
    for event, distance in events_with_distance:
            if distance <= ranges:
                location = reverseGeocoding(float(event["latitude"]), float(event["longitude"]))
                details = (
                    f"<b>Name:</b> {event['name']}<br>"
                    f"<b>Date:</b> {event['date']}<br>"
                    f"<b>Time:</b> {event['time']}<br>"
                    f"<b>Details:</b> {event['details']}<br>"
                    f"<b>Distance:</b> {distance:.2f} km<br>"
                    f"<b>Location:</b> {location}"
                )
                popup = folium.Popup(details, max_width=300)
                folium.Marker(
                    location=(float(event["latitude"]), float(event["longitude"])),
                    popup=popup,
                ).add_to(folium_map)

        # Save the map to HTML
    folium_map.save("templates/generated_map.html")

# Host Functionality
def hostIn():
    os.system('clear')
    print("Welcome, Host!")
    while True:
        add_event = input("Would you like to add a new event? (y/n): ").lower()
        os.system('clear')
        if add_event == 'y':
            latitude = input("Enter latitude: ")
            longitude = input("Enter longitude: ")
            name = input("Enter event name: ")
            date = input("Enter event date (dd/mm/yyyy): ")
            time = input("Enter event time (hh:mm AM/PM): ")
            details = input("Enter event details: ")

            addCamps(latitude, longitude, name, date, time, details)
            os.system('clear')
            print("Event added successfully!\n")
        else:
            os.system('clear')
            print("Returning to main menu.")
            break

# Check User Credentials
def checkUsers(username , password, userType):

    if not userType:
        userType = "normal"

    data = read_file()

    if userType == "user":
        if username in [u.lower() for u in data["normalUsername"]]:
            i = [u.lower() for u in data["normalUsername"]].index(username)
            if password == data["normalPassword"][i]:
                return "userIn"
    elif userType == "admin":
        if username in [u.lower() for u in data["adminUsername"]]:
            i = [u.lower() for u in data["adminUsername"]].index(username)
            if password == data["adminPassword"][i]:
                return "hostIn"

    print("Login failed! Invalid username, password, or type.")
    time.sleep(5)  # Wait for 5 seconds before returning
    return False

# Main Program

if __name__ == "__main__":
    print(checkUsers("mudith" , "mudith" , "user"))
