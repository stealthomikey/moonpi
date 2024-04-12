# Import statements
from sense_hat import SenseHat
import paho.mqtt.client as paho
import sys
import os
import shutil
import csv
import time
import threading  # Import threading module for running MQTT loop in a separate thread

# Initialize Sense HAT
sense = SenseHat()

# File paths for saving user data
user_data_file = "user_data.csv"

# Dictionary to store the last selected movie for each user
last_selected_movies = {}

# List of options
options = ["name", "movie", "pic"]

# Index of the currently selected option
selected_option_index = 0

# List to store user-defined names
user_defined_names = []

# Function to display the current option
def display_option(option):
    sense.show_message(option)

# Function to select a name and play movies
def select_name():
    print("Select a name:")
    # Display user-defined names
    for name in user_defined_names:
        print(name)
    # Get the user's name
    user_name = input("Enter your name: ")
    # Check if the user's name exists
    if user_name in user_defined_names:
        if user_name in last_selected_movies:
            print(f"Welcome back, {user_name}! Your last selected movie was: {last_selected_movies[user_name]}")
        else:
            print(f"Welcome, {user_name}!")
        # Set the directory for the user's movies
        movie_dir = os.path.join("movies", user_name)
        # Check if the movie directory exists
        if os.path.exists(movie_dir):
            # List the user's movies
            user_movies = os.listdir(movie_dir)
            print("Your movies:")
            for i, movie in enumerate(user_movies, 1):
                print(f"{i}. {movie}")
            # Ask the user to select a movie
            movie_index = int(input("Select a movie: ")) - 1
            # Check if the selected index is valid
            if 0 <= movie_index < len(user_movies):
                selected_movie = user_movies[movie_index]
                print(f"Playing {selected_movie}...")
                # Simulate playing the movie (replace this with actual playback logic)
                time.sleep(5)  # Simulate playback time
                # Remember the last selected movie for this user
                last_selected_movies[user_name] = selected_movie
                # Save the updated last selected movies to file
                save_user_data()
            else:
                print("Invalid movie selection!")
        else:
            print("You don't have any movies yet!")
    else:
        print("User not found!")
    # Simulate some processing time
    time.sleep(2)

# Function to upload and rename a movie
def movie_upload():
    print("Movie upload:")
    # Get the user's name
    user_name = input("Enter your name: ")
    # Check if the user's name exists
    if user_name in user_defined_names:
        # Get the path of the movie file to upload
        movie_path = input("Enter the path of the movie file to upload: ")
        if os.path.exists(movie_path):
            # Set the destination directory for the movie file
            destination_dir = os.path.join("movies", user_name)
            # Check if the destination directory exists, if not create it
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            # Get the new name for the movie file
            new_movie_name = input("Enter the new name for the movie file: ")
            # Copy the movie file to the destination directory with the new name
            shutil.copy(movie_path, os.path.join(destination_dir, new_movie_name))
            print("Movie uploaded successfully!")
            # Check if the user already had a last selected movie
            if user_name in last_selected_movies:
                # Update the last selected movie only if a new movie is uploaded
                last_selected_movies[user_name] = new_movie_name
            else:
                # Set the last selected movie for this user
                last_selected_movies[user_name] = new_movie_name
        else:
            print("File not found!")
    else:
        print("User not found!")
    # Simulate some processing time
    time.sleep(2)

# Function to upload and rename a picture
def picture_upload():
    print("Picture upload:")
    # Get the path of the picture file to upload
    picture_path = input("Enter the path of the picture file to upload: ")
    if os.path.exists(picture_path):
        # Get the user's name
        user_name = input("Enter your name: ")
        # Check if the user's name already exists
        if user_name in user_defined_names:
            print("User name already in use!")
            return  # Exit function if name already in use
        else:
            # Add the user's name to the list of user-defined names
            user_defined_names.append(user_name)
            # Save user data to CSV file
            save_user_data()
        # Set the destination directory for the picture file
        destination_dir = "pictures"
        # Check if the destination directory exists, if not create it
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        # Get the new name for the picture file (user_name)
        new_picture_name = user_name + os.path.splitext(picture_path)[1]  # Use user_name as file name
        # Copy the picture file to the destination directory with the new name
        shutil.copy(picture_path, os.path.join(destination_dir, new_picture_name))
        print("Picture uploaded successfully!")
    else:
        print("File not found!")
    # Simulate some processing time
    time.sleep(2)

# Function to save user data to CSV file
def save_user_data():
    with open(user_data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["UserDefinedNames", "LastSelectedMovies"])
        for name in user_defined_names:
            # Get the last selected movie for the user or set a default value if not present
            last_selected_movie = last_selected_movies.get(name, "default_movie.mp4")
            writer.writerow([name, last_selected_movie])

# Function to load user data from CSV file
def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                user_defined_names.append(row[0])
                # Load last selected movie for the user, or use a default value if not present
                last_selected_movies[row[0]] = row[1] if len(row) > 1 else "default_movie.mp4"

# Load user data when the application starts
load_user_data()

# Function to find the last selected movie for a specific user
def find_last_movie_for_user(search_name):
    for name, last_movie in last_selected_movies.items():
        if name.lower() == search_name.lower():
            print(f"The last selected movie for {name} was: {last_movie}")
            return
    print(f"No movie found for {search_name}")

# Function to handle joystick events and navigation
def handle_navigation(event):
    global selected_option_index
    if event.action == "pressed":
        if event.direction == "left":
            selected_option_index = (selected_option_index - 1) % len(options)
        elif event.direction == "right":
            selected_option_index = (selected_option_index + 1) % len(options)
        elif event.direction == "down":
            if options[selected_option_index] == "name":
                select_name()
            elif options[selected_option_index] == "movie":
                movie_upload()
            elif options[selected_option_index] == "pic":
                picture_upload()

# MQTT on message callback
def on_message(client, userdata, msg):
    if msg.topic == "moonPi":
        user_name = msg.payload.decode()
        find_last_movie_for_user(user_name)

# MQTT client setup
client = paho.Client()
client.on_message = on_message

# MQTT connection to broker
if client.connect("192.168.87.41", 1883, 60) != 0:
    print("Couldn't connect to broker")
    sys.exit(-1)

# MQTT subscribe to topic
client.subscribe("moonPi")

# Function to run MQTT loop in a separate thread
def mqtt_loop():
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Disconnecting from MQTT broker...")
        client.disconnect()

# Start the MQTT loop in a separate thread
mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

# Main loop
while True:
    # Display the current option
    display_option(options[selected_option_index])

    # Wait for joystick input
    for event in sense.stick.get_events():
        handle_navigation(event)
