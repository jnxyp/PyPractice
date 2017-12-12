# ============================================================
#
# Student Name (as it appears on cuLearn): Ziwen Wang
# Student ID (9 digits in angle brackets): <101071063>
# Course Code (for this current semester): COMP1405A
#
# ============================================================

import pygame

# Initialize pygame
pygame.init()

# Declare screen valuable
windows = pygame.display.set_mode((480, 560))

# Fill all screen to color white
windows.fill((255, 255, 255))

# Start draw polygon(picture)
pygame.draw.polygon(windows, (162, 185, 205), ((230, 130), (360, 130), (360, 190), (290, 190)))

pygame.draw.polygon(windows, (55, 148, 201), ((140, 220), (140, 350), (210, 350), (270, 290), (210, 290)))

pygame.draw.polygon(windows, (124, 138, 80), ((290, 290), (360, 290), (360, 350), (230, 350)))

pygame.draw.polygon(windows, (173, 111, 195), ((290, 370), (360, 370), (360, 430), (230, 430)))

# Update to display screen
pygame.display.update()

# Save image
pygame.image.save(windows, "101071063.png")







