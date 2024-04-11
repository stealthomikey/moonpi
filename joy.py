from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
event = sense.stick.wait_for_event()
print("The joystick was {} {}".format(event.action, event.direction))
sleep(0.1)
event = sense.stick.wait_for_event()
print("The joystick was {} {}".format(event.action, event.direction))


import pygame
import time

# Initialize pygame
pygame.init()

# Function to display options
def display_options(options):
    for option in options:
        print(option)

# Main function
def main():
    options = ["name", "movie", "picture"]
    selected_option = 0
    
    while True:
        # Display options
        display_options(options)
        
        # Wait for joystick input (simulate for demonstration)
        time.sleep(0.5)
        
        # Simulate joystick input (replace with actual joystick input)
        joystick_input = input("Enter joystick input (up/down): ")
        
        # Handle joystick input
        if joystick_input == "up":
            selected_option = (selected_option - 1) % len(options)
        elif joystick_input == "down":
            selected_option = (selected_option + 1) % len(options)
        elif joystick_input == "select":
            print("You selected:", options[selected_option])
            # Additional logic to display more options or perform actions
            
        # Clear screen (for demonstration)
        print("\033c", end="")  # Clear screen escape sequence (works in most terminals)

if __name__ == "__main__":
    main()
