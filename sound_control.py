import pygame

# Initialize Pygame
pygame.init()

# Load a sound file
sound = pygame.mixer.Sound("sound.mp3")

# Play the sound
sound.play()

# Function to adjust volume
def adjust_volume(gesture):
    if gesture == "Thumb Up":
        sound.set_volume(min(1.0, sound.get_volume() + 0.1))  # Increase volume
    elif gesture == "Index Finger Up":
        sound.set_volume(max(0.0, sound.get_volume() - 0.1))  # Decrease volume