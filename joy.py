from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
event = sense.stick.wait_for_event()
print("The joystick was {} {}".format(event.action, event.direction))
sleep(0.1)
event = sense.stick.wait_for_event()
print("The joystick was {} {}".format(event.action, event.direction))

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
                print("You selected:", options[selected_option_index])
                # Additional logic can be added here based on the selected option
                # For now, it just prints the selected option
