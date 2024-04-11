from sense_hat import SenseHat
import time

# Initialize Sense HAT
sense = SenseHat()

# List of options
options = ["name", "movie", "picture"]

# Index of the currently selected option
selected_option_index = 0

# Function to display the current option
def display_option(option):
    sense.show_message(option)

# Function to select a name
def select_name():
    print("Select a name:")
    # Simulate selecting a name (replace this with your actual logic)
    selected_name = input("Enter a name: ")
    print("You selected:", selected_name)
    time.sleep(2)  # Simulate some processing time
    display_option(options[selected_option_index])  # Return to main navigation

# Function to select a movie
def select_movie():
    print("Select a movie:")
    # Simulate selecting a movie (replace this with your actual logic)
    selected_movie = input("Enter a movie: ")
    print("You selected:", selected_movie)
    time.sleep(2)  # Simulate some processing time
    display_option(options[selected_option_index])  # Return to main navigation

# Function to select a picture
def select_picture():
    print("Select a picture:")
    # Simulate selecting a picture (replace this with your actual logic)
    selected_picture = input("Enter a picture: ")
    print("You selected:", selected_picture)
    time.sleep(2)  # Simulate some processing time
    display_option(options[selected_option_index])  # Return to main navigation

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
                elif options[selected_option_index] == "movie":
                    select_movie()
                elif options[selected_option_index] == "picture":
                    select_picture()
