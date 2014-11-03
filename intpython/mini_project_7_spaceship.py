# Interactive Python Coursera Mini Project 7: Sapceship

# Initial implementation of classic arcade game, Asteroids. This implementation only includes the ship's physics, 
# one rock that spawns every second, and a missile that is refirable, but never dissapears.
import simplegui
import math
import random

# Global Definitions
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# Art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# Debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png, 
# debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# Nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# Splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# Ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# Missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# Asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# Animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# Sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# Transformation handler helper functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def rand_ang(minimum, maximum):
    return minimum + ((maximum - minimum) * random.random())


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        thrust_state = [self.image_center[0]+self.image_size[0],self.image_center[1]]
        if self.thrust:
            canvas.draw_image(ship_image,thrust_state,self.image_size,self.pos,self.image_size,self.angle)
        else:
            canvas.draw_image(ship_image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

    def update(self):
        # Update ship's position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Rotation of ship
        self.angle += self.angle_vel

        # Friction on the ship
        c = 0.01
        self.vel[0] *= (1-c)
        self.vel[1] *= (1-c)

        # Acceleration by thruster
        self.acc = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += 0.1 * self.acc[0]
            self.vel[1] += 0.1 * self.acc[1]

        # Keep on canvas
        if self.pos[0] >= WIDTH or self.pos[0] <= 0:
            self.pos[0] %= WIDTH
        if self.pos[1] >= HEIGHT or self.pos[1] <= 0:
            self.pos[1] %= HEIGHT

    # Functions to increase and decrease angular velocity
    def increase_angle_vel(self, vel):
        self.angle_vel += vel

    def decrease_angle_vel(self, vel):
        self.angle_vel -= vel

    # Function to begin thrust
    def ship_thrust(self, sound):
        self.thrust = sound
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    # Function to launch missile
    def launch(self):
        global a_missile
        shot = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * shot[0], self.pos[1] + self.radius * shot[1]]
        missile_vel = [self.vel[0] + 5 * shot[0], self.vel[1] + 5 * shot[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # Update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Rotation sprite
        self.angle += self.angle_vel
        
        # Keep sprite on canvas
        if self.pos[0] >= WIDTH or self.pos[0] <= 0:
            self.pos[0] %= WIDTH
        if self.pos[1] >= HEIGHT or self.pos[1] <= 0:
            self.pos[1] %= HEIGHT     

# Keydown event handler
def keydown_handler(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.decrease_angle_vel(0.1)
    if key == simplegui.KEY_MAP["right"]:
        my_ship.increase_angle_vel(0.1)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.ship_thrust(True)
    if key == simplegui.KEY_MAP["space"]:
        my_ship.launch()

# Keyup event handler        
def keyup_handler(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP["up"]:
         my_ship.ship_thrust(False)

def draw(canvas):
    global time
    
    # Animated background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Draw Lives and Score
    canvas.draw_text("Lives: " + str(lives), [85, 50], 30, "White")
    canvas.draw_text("Score: " + str(score), [590, 50], 30, "White")

    # Draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # Update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
# Timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    
    a_rock.vel[0] = random.randrange(-2,3)
    a_rock.vel[1] = random.randrange(-2,3)
    a_rock.pos[0] = random.randrange(0,800)
    a_rock.pos[1] = random.randrange(0,600)
    a_rock.angle_vel = rand_ang(-.1, 0.1)
    
# Initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# Initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# Event handler registration
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# Begin game immediately upon launching program
timer.start()
frame.start()