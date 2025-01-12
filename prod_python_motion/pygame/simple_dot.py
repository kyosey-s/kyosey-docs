import pygame
import random
import sys
import os

# Initial Setup
pygame.init()
width, height = 720, 1280  # 9:16 aspect ratio
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dynamic Moving Dots")
clock = pygame.time.Clock()

# Create output directory for frames
output_dir = "frames"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Dot Information
dots = [{"x": random.randint(0, width), 
         "y": random.randint(0, height), 
         "color": [random.randint(0, 255) for _ in range(3)],
         "dx": random.choice([-1, 1]) * random.randint(1, 3),  # X direction speed
         "dy": random.choice([-1, 1]) * random.randint(1, 3)}  # Y direction speed
        for _ in range(50)]  # 50 dots

# Frame settings
frame_rate = 30  # 30fps
duration_in_seconds = 10  # 10-second video
total_frames = frame_rate * duration_in_seconds

# Speed increase factor
acceleration = 0.05  # Dots' speed will increase by this factor every frame

# Main Loop for Animation
for frame_number in range(total_frames):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Update and draw each dot
    for dot in dots:
        # Update position
        dot["x"] += dot["dx"]
        dot["y"] += dot["dy"]

        # Increase speed over time
        dot["dx"] += dot["dx"] * acceleration
        dot["dy"] += dot["dy"] * acceleration

        # Reflect off walls
        if dot["x"] <= 0 or dot["x"] >= width:
            dot["dx"] *= -1
        if dot["y"] <= 0 or dot["y"] >= height:
            dot["dy"] *= -1

        # Draw the dot
        pygame.draw.circle(screen, dot["color"], (int(dot["x"]), int(dot["y"])), 10)
    
    # Save the frame as an image
    frame_filename = os.path.join(output_dir, f"frame_{frame_number:04d}.png")
    pygame.image.save(screen, frame_filename)
    
    # Update the display
    pygame.display.flip()
    clock.tick(frame_rate)

# Quit pygame
pygame.quit()

print(f"Frames saved to '{output_dir}'. Use FFmpeg or another tool to create a video.")
