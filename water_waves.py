import pygame
from pygame.locals import *
from threading import Thread
import time


"""
Informations:
I created this program using tutorial found on this page: https://gamedevelopment.tutsplus.com/tutorials/make-a-splash-with-dynamic-2d-water-effects--gamedev-236
This program uses the Threads Python module, with this module you can change the FPS constants destined to Pygame and consequently accelerate the program.
"""


# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CAPTION = "Waves Simulation with Pygame"
FPS = 60
BLUE = (0, 103, 247)
WHITE = (255, 255, 255)


class Main:
    def __init__(self):
        """Main class"""

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

        self.time = pygame.time.Clock()
        
        # Max wave height and stable point
        self.target_height = 200
        self.tension = 0.025
        self.dampening = 0.020
        self.spread = 0.25
        # Number of loop round // Warning with a too hight value on this variable, the script will be very slower
        self.height_splash = 5
        # Initial speed
        self.init_speed = 200
        # First position
        self.init_position_x = 0
        # Second position
        self.final_position_x = 400

        # List of objects (here the objects are Springs)
        self.springs = []

        self.number_rod = self.create_number_rod()
        self.rod_width = self.create_rod_width()
        self.init_index = int(self.number_rod / self.rod_width)
        self.create_spring_list(self.rod_width)
        self.start_water_waves(self.rod_width)
        
        self.done = False

        self.run_game()


    def run_game(self):
        """Main loop"""
        
        while not self.done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONUP:
                    if self.counter.done == True:
                        pos = pygame.mouse.get_pos()
                        self.init_index = int(pos[0] / self.final_position_x * self.number_rod)
                        self.start_water_waves(self.rod_width)

            self.draw_level()
            
            for spring in self.springs:
                spring.draw(self.screen)
                
            self.time.tick(FPS)
            pygame.display.flip()


    def create_number_rod(self):
        """Have half rod on all the water"""

        return abs(int((self.init_position_x - self.final_position_x) / 2))


    def create_rod_width(self):
        """Make an size average thank to the number of rod"""

        return int((self.init_position_x + self.final_position_x) / self.number_rod)
            

    def create_spring_list(self, rod_width):
        """Create the spring list"""

        for x in range(self.init_position_x, self.final_position_x, rod_width):
            self.springs.append(Spring(x, self.target_height, rod_width))


    def start_water_waves(self, rod_width):
        """Start the waves motion at a given position"""

        self.springs[self.init_index].speed = self.init_speed
        self.counter = Counter_Waves_Motion(self)
        self.counter.start()


    def update(self):
        """Update the waves"""

        self.update_waves()
        self.create_neighbour_list()
        self.update_neighbour()
        self.test_end_water_waves()


    def test_end_water_waves(self):
        """Check if the waves are still alive"""

        count = 0

        for i in range(len(self.springs)):
            if not int(self.springs[i].speed) and not int(self.springs[i].y):
                count += 1

        if count == len(self.springs):
            self.stop_water_motion()


    def stop_water_motion(self):
        """Stop the motion of the water"""
  
        for i in range(len(self.springs)):
            self.springs[i].speed = 0
            self.springs[i].height = self.target_height
            self.springs[i].y = 0
            
   
    def update_waves(self):
        """Update the water waves
        of all the rod in the springs list"""

        for i in range(len(self.springs)):
            self.springs[i].update(self.dampening, self.tension, self.target_height)


    def create_neighbour_list(self):
        """Create the lists of height
        difference between the rods without reference"""

        self.lDeltas = list(self.springs)
        self.rDeltas = list(self.springs)


    def update_neighbour(self):
        """Update the rod beside another"""
    
        for j in range(self.height_splash):
            for i in range(len(self.springs)):

                if i > 0:
                    self.lDeltas[i] = self.spread * (self.springs[i].height - self.springs[i - 1].height)
                    self.springs[i - 1].speed += self.lDeltas[i]

                if i < len(self.springs) - 1:
                    self.rDeltas[i] = self.spread * (self.springs[i].height - self.springs[i + 1].height)
                    self.springs[i + 1].speed += self.rDeltas[i]

            self.termine_update_neighbour()


    def termine_update_neighbour(self):
        """Terminate the procedure"""

        for i in range(len(self.springs)):
            if i > 0:
                self.springs[i - 1].height += self.lDeltas[i]
            if i < len(self.springs) - 1:
                self.springs[i + 1].height += self.rDeltas[i]


    def draw_level(self):
        """Draw the level background"""

        self.screen.fill(WHITE)


class Spring:
    def __init__(self, x, target_height, rod_width):
        """Spring Creator, one spring by one"""

        self.x = x
        self.y = 0
        self.speed = 0
        self.height = target_height
        self.bottom = 400
        self.rod_width = rod_width


    def update(self, dampening, tension, target_height):
        """Update the springs, this is numerical integration
        and called Euler Method, it is simple fast and usual"""
        
        self.y = target_height - self.height
        self.speed += tension * self.y - self.speed * dampening
        self.height += self.speed


    def draw(self, screen):
        """Draw the spring,
        (Here this is a simple rod)"""

        pygame.draw.line(screen, BLUE, (self.x, self.height), (self.x, self.bottom), self.rod_width)


class Counter_Waves_Motion(Thread):
    def __init__(self, main):
        Thread.__init__(self)
        """Thread init class, (counter class)"""

        self.main = main

        self.time = 0
        self.max_time = 2
        self.time_sleep = 0.01

        self.done = False


    def run(self):
        """Run the Thread, (parallel programming)"""

        while not self.done:
            self.main.update()
            
            self.time += self.time_sleep

            if self.time >= self.max_time:
                self.done = True

            time.sleep(self.time_sleep) 


if __name__ == "__main__":
    Main()
