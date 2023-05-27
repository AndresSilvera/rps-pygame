import pygame
import random
 
# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

def intersect(x1, y1, x2, y2, rad1, rad2):
    if ((x2-x1)**2 + (y2-y1)**2)**0.5 <= rad2 + rad1:
        return True
    else:
        return False
    


types = ("rock", "paper", "scissors")

def rps_logic(t1, t2):
    # returns True if t1 wins, False otherwise (t2 wins)
    if t1 == "rock" and t2 == "paper":
        return False
    if t1 == "paper" and t2 == "rock":
        return True
    if t1 == "scissors" and t2 == "paper":
        return True
    if t1 == "paper" and t2 == "scissors":
        return False
    if t1 == "rock" and t2 == "scissors":
        return True
    if t1 == "scissors" and t2 == "rock":
        return False
    return False


class Player:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.rad = 20
        self.max_speed = 6
    
    def update(self):
        closest_prey = (None, float('inf'))
        closest_predator = (None, float('inf'))
        for p in players:
            if p == self:
                continue
            dx = p.x - self.x
            dy = p.y - self.y
            dist = ((self.x-p.x)**2 + (self.y-p.y)**2)**0.5
            if dist == 0:
                continue
            # push ourselves and other (p) by half the overlap distance to not overlap anymore
            overlap = (p.rad + self.rad) - dist
            if overlap > 0: # was an intersection
                self.x -= dx * (0.5 * overlap / dist)
                self.y -= dy * (0.5 * overlap / dist)
                p.x += dx * (0.5 * overlap / dist)
                p.y += dy * (0.5 * overlap / dist)
                # change type if rps logic says so
                if rps_logic(self.type, p.type): # we win!
                    p.type = self.type
                else:
                    self.type = p.type # we lose
            
            # find the closest prey
            p_is_prey = rps_logic(self.type, p.type)
            if p_is_prey:
                if closest_prey[0] is None or dist < closest_prey[1]:
                    closest_prey = (p, dist)
            elif self.type != p.type:
                if closest_predator[0] is None or dist < closest_predator[1]:
                    closest_predator = (p, dist)
            

        # chase towards the closest prey
        if closest_prey[0] is not None:
            dx = closest_prey[0].x - self.x
            dy = closest_prey[0].y - self.y
            hypot = (dx**2 + dy**2)**0.5
            self.x += dx * (self.max_speed / hypot)
            self.y += dy * (self.max_speed / hypot)

        # run away from the closest predator
        if closest_predator[0] is not None:
            dx = closest_predator[0].x - self.x
            dy = closest_predator[0].y - self.y
            hypot = (dx**2 + dy**2)**0.5
            self.x -= dx * (self.max_speed / hypot)
            self.y -= dy * (self.max_speed / hypot)
        
        # wraparound logic
        self.x = min(max(self.x, 0), screensize[0])
        self.y = min(max(self.y, 0), screensize[1])
        
    
    def draw(self):
        c = red # rock
        if self.type == "paper":
            c = green
            width = 2 * self.rad
            pygame.draw.rect(screen, c, pygame.Rect(self.x - 0.5 * width, self.y - 0.5 * width, width, width))
        elif self.type == "scissors":
            c = blue
            pygame.draw.polygon(screen, c, ((self.x, self.y + self.rad), # top point
                                            (self.x - self.rad, self.y - self.rad),  # bottom left
                                            (self.x + self.rad, self.y - self.rad)) # bottom right
                                            )
        if self.type == "rock":
            pygame.draw.circle(screen, c, (self.x, self.y), self.rad)

def main():
    for p in players:
        p.update()
    for p in players:
        p.draw()
    rock_count = len([p for p in players if p.type == "rock"])
    paper_count = len([p for p in players if p.type == "paper"])
    scissor_count = len([p for p in players if p.type == "scissors"])
    if rock_count == len(players):
        print("rock wins!")
        pygame.quit()
        exit()
    elif paper_count == len(players):
        print("paper wins!")
        pygame.quit()
        exit()
    elif scissor_count == len(players):
        print("scissors wins!")
        pygame.quit()
        exit()
    else:
        print(f"#rock: {rock_count}\t#paper: {paper_count}\t#scissors:{scissor_count}")

pygame.init()

# Set the height and width of the screen
screensize = [1200, 750]
screen = pygame.display.set_mode(screensize)
 
pygame.display.set_caption("Rock paper scissors sim")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

players = []
for i in range(30):
    type = types[i % 3]
    x = random.randint(0, screensize[0])
    y = random.randint(0, screensize[1])
    p = Player(x, y, type)
    players.append(p)

# -------- Main Program Loop -----------
fractal_level = 5
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            type = types[random.randint(0,2)]
            p = Player(pos[0], pos[1], type)
            players.append(p)

 
    # Set the screen background
    screen.fill(white)
 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    main()
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 20 frames per second
    clock.tick(20)
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()