import random
import pygame
import math
from util import *


class Player:

    def __init__(self, world_width, world_height) -> None:
        # Player settings
        self.size = 70
        self.speed = 5

        # Player initial position in the world (center of the larger world)
        self.rect = None

        self.x = world_width // 2
        self.y = world_height // 2

        self.world_width = world_width
        self.world_height = world_height
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
            
        self.score = 0
        self.ammo = 10
        self.health = 5

        self.images = [] 

        image = pygame.image.load(f'images/space_ship.png')
        image_scaled = pygame.transform.scale(image, (self.size, self.size))

        for i in range(360):
            self.images.append(pygame.transform.rotate(image_scaled, i))

        self.direction = 0
        self.velocity_direction = 0
        self.direction_input = 0 # This is the raw input returned from the keyboard. 
        self.velocity = 0

    def update_direction(self, angle_delta):
        self.direction_input += angle_delta
        self.direction = self.direction_input % 360

    def throttle(self, throttle):

        throttle = throttle * -1
        print("Throttle: ", throttle)

        direction_difference = ((self.direction - self.velocity_direction + 180) % 360 - 180) / 180

        velocity_reduction = abs(self.velocity * direction_difference) * 2.5

        print("Velocity Reduction: ", velocity_reduction)

        print("Direction Difference: ", direction_difference)
 
        if throttle < 0: # Remember. Throttle is reversed. 
            if -3 <= self.velocity:
                self.velocity += throttle
            
            self.velocity = self.velocity + velocity_reduction


        else:
            self.velocity = throttle

        self.velocity_direction = self.direction
        
        print("Velocity: ", self.velocity)
        # if self.velocity > 0 and throttle < 0:
        #     self.velocity += throttle

 
    def fly(self):
        direction_radians = math.radians(self.velocity_direction)

        y = self.velocity * math.cos(direction_radians)
        x = self.velocity * math.sin(direction_radians)

        if(0 < (self.x + x) < (self.world_width - self.size)) and (0 < (self.y + y) < (self.world_height - self.size)):
            self.x += x
            self.y += y
        else:
            self.velocity = 0
    
    
    def draw(self, screen, camera_x, camera_y):
        # player_image = self.player.images[self.player.direction]
        # self.player.rect = player_image.get_rect(center=(self.player.x, self.player.y))
        screen.blit(self.images[self.direction], (self.x - camera_x, self.y - camera_y))


class Zombie:
    def __init__(self, world_width, world_height, size=50, speed=1):
        # Spawn the zombie at a random position around the edges of the map
        self.size = size
        self.zombie_color = (0, 255, 0)
        self.world_width = world_width
        self.world_height = world_height
        self.speed = speed

        self.x, self.y = self.spawn()

        self.images = {}

        for direction in ('up', 'down', 'left', 'right'):
            image = pygame.image.load(f'images/alien_space_ship.png')
            self.images[direction] = pygame.transform.scale(image, (self.size, self.size))

        self.direction = "up"

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.rect.center = (self.x, self.y)

    def spawn(self):
        """Spawns a zombie at a random location around the edges of the world."""
        spawn_positions = [
            (random.randint(0, self.world_width - self.size), 0),  # Top edge
            (random.randint(0, self.world_width - self.size), self.world_height - self.size),  # Bottom edge
            (0, random.randint(0, self.world_height - self.size)),  # Left edge
            (self.world_width - self.size, random.randint(0, self.world_height - self.size))  # Right edge
        ]
        return random.choice(spawn_positions)


    def move_toward_player(self, player_x, player_y):
        """Moves the zombie toward the player's position, with better handling of wall collisions."""
        dx, dy = player_x - self.x, player_y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance  # Normalize
        
        # Try horizontal movement first
        new_x = self.x + dx * self.speed

        self.x = new_x

        # Try vertical movement next
        new_y = self.y + dy * self.speed

        self.y = new_y

        # Update the zombie's position and direction
        self.rect.topleft = (self.x, self.y)

        # Set direction for zombie based on movement
        if abs(dx) > abs(dy):
            if dx > 0:
                self.direction = 'right'
            else:
                self.direction = 'left'
        else:
            if dy > 0:
                self.direction = 'down'
            else:
                self.direction = 'up'


    def draw(self, screen, camera_x, camera_y):
        """Draws the zombie as a green rectangle."""
        # pygame.draw.rect(screen, self.zombie_color, self.rect)
        # pygame.draw.rect(screen, self.zombie_color, (self.rect.x - camera_x, self.rect.y - camera_y, self.size, self.size))

        # zombie.rect = zombie_image.get_rect(center=(zombie.x, zombie.y))
        screen.blit(self.images[self.direction], (self.rect.x - camera_x, self.rect.y - camera_y))

