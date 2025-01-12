import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Screen dimensions (9:16 aspect ratio)
width, height = 720, 1280
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dynamic Abstract Animation")

# Create output directory for frames
output_dir = "dynamic_smooth_frames"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Colors and wave settings
base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
waves = [{"amplitude": random.randint(50, 150),
          "frequency": random.uniform(0.005, 0.03),
          "speed": random.uniform(1.0, 3.0),
          "phase": random.uniform(0, math.pi * 2),
          "color": random.choice(base_colors),
          "direction": random.choice([1, -1])} for _ in range(10)]  # 10 waves with random direction

# Particle settings
particles = [{"x": random.randint(0, width),
              "y": random.randint(0, height),
              "dx": random.uniform(-2, 2),  # Smooth random movement
              "dy": random.uniform(-2, 2),
              "size": random.randint(3, 10),
              "size_delta": random.uniform(-0.2, 0.2),  # Dynamic size change
              "color": random.choice(base_colors)} for _ in range(200)]  # 200 particles

# Gradient background settings
gradient_colors = [(255, 0, 0), (0, 0, 255)]  # Start with red and blue
gradient_speed = 0.01  # Speed of gradient transition

# Frame settings
frame_rate = 30
duration_in_seconds = 10
total_frames = frame_rate * duration_in_seconds

# Linear interpolation for gradients
def interpolate_color(color1, color2, t):
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t)
    )

# Main animation loop
for frame_number in range(total_frames):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Calculate gradient background color
    t = (frame_number * gradient_speed) % 1  # Gradual transition over time
    background_color = interpolate_color(gradient_colors[0], gradient_colors[1], t)
    screen.fill(background_color)

    # Update gradient colors
    if t >= 0.99:  # Swap colors when the transition completes
        gradient_colors.reverse()

    # Draw dynamic waves
    for wave in waves:
        for x in range(0, width, 5):  # Draw vertical slices of waves
            y = int(height / 2 + wave["amplitude"] * math.sin(wave["frequency"] * x + wave["phase"]) * wave["direction"])
            pygame.draw.rect(screen, wave["color"], (x, y, 5, height - y))

        # Update wave phase and direction to make it move dynamically
        wave["phase"] += wave["speed"] / 20
        if random.random() < 0.01:  # Occasionally flip direction
            wave["direction"] *= -1

    # Draw particles
    for particle in particles:
        # Update position
        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]

        # Change size dynamically
        particle["size"] += particle["size_delta"]
        if particle["size"] < 2 or particle["size"] > 15:  # Keep sizes in range
            particle["size_delta"] *= -1

        # Bounce off walls
        if particle["x"] <= 0 or particle["x"] >= width:
            particle["dx"] *= -1
        if particle["y"] <= 0 or particle["y"] >= height:
            particle["dy"] *= -1

        # Draw the particle
        pygame.draw.circle(screen, particle["color"], (int(particle["x"]), int(particle["y"])), int(particle["size"]))

    # Save the frame as an image
    frame_filename = os.path.join(output_dir, f"frame_{frame_number:04d}.png")
    pygame.image.save(screen, frame_filename)

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(frame_rate)

# Quit Pygame
pygame.quit()

print(f"Frames saved to '{output_dir}'. Use FFmpeg to create a video.")
