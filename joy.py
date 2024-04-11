from sense_hat import SenseHat
import os
import shutil
import csv
import time

# Initialize Sense HAT
sense = SenseHat()

# File paths for saving user data
user_data_file = "user_data.csv"

# List of options
options = ["name", "movie upload", "picture upload"]

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
            else:
                print("Invalid movie selection!")
        else:
            print("You don't have any movies yet!")
    else:
        print("User not found!")
    # Simulate some processing time
    time.sleep(2)
    display_option(options[selected_option_index])  # Return to main navigation

# Function to upload and rename a movie
def movie_upload():
    print("Movie upload:")
    # Get the path of the movie file to upload
    movie_path = input("Enter the path of the movie file to upload: ")
    if os.path.exists(movie_path):
        # Get the user's name
        user_name = input("Enter your name: ")
        # Add the user's name to the list of user-defined names
        user_defined_names.append(user_name)
        # Save user data to CSV file
        save_user_data()
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
    else:
        print("File not found!")
    # Simulate some processing time
    time.sleep(2)
    display_option(options[selected_option_index])  # Return to main navigation

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
        # Add the user's name to the list of user-defined names
        user_defined_names.append(user_name)
        # Save user data to CSV file
        save_user_data()
        # Set the destination directory for the picture file
        destination_dir = os.path.join("pictures", user_name)
        # Check if the destination directory exists, if not create it
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        # Get the new name for the picture file
        new_picture_name = input("Enter the new name for the picture file: ")
        # Copy the picture file to the destination directory with the new name
        shutil.copy(picture_path, os.path.join(destination_dir, new_picture_name))
        print("Picture uploaded successfully!")
    else:
        print("File not found!")
    # Simulate some processing time
    time.sleep(2)
    display_option(options[selected_option_index])  # Return to main navigation

# Function to save user data to CSV file
def save_user_data():
    with open(user_data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["UserDefinedNames"])
        for name in user_defined_names:
            writer.writerow([name])

# Function to load user data from CSV file
def load_user_data():
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                user_defined_names.append(row[0])

# Load user data when the application starts
load_user_data()

# Main loop
while True:
    # Display the current option
    display_option(options[selected_option_index])

    # Wait for joystick input
    for event in sense.stick.get_events():
        if event.action == "pressed":
            if event.direction == "left":
                selected_option_index = (selected_option_index - 1) % len(options)
            elif event.direction == "right":
                selected_option_index = (selected_option_index + 1) % len(options)
            elif event.direction == "down":
                if options[selected_option_index] == "name":
                    select_name()
                elif options[selected_option_index] == "movie upload":
                    movie_upload()
                elif options[selected_option_index] == "picture upload":
                    picture_upload()
