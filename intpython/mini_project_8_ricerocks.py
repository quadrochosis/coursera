# Interactive Python Coursera Mini Project 8: RiceRocks

# Initial implementation of classic arcade game, Asteroids. The player is given 3 lives to destroy as many asteroids
# as they can. Each asteroid destroyed equals ten points.
import simplegui
import math
import random

# Global Definitions
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
last_score = 0

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
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# Transformation handlers
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # Angle update
        self.angle += self.angle_vel
        
        # Position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # Velocity update
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    # Turns thrust sound on/off
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
     
    # Shoots missile   
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
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
        global started
        if started:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]),self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # Angle update
        self.angle += self.angle_vel
        
        # Position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        if self.age >= self.lifespan:
            return True
        elif self.age < self.lifespan:
            return False
    
    # Collision handler   
    def collide(self,other_object):
        rock_pos = self.pos
        rock_radius = self.radius
        other_object_pos = other_object.pos
        other_object_radius = other_object.radius
        d = dist(rock_pos,other_object_pos)
        if d < (rock_radius + other_object_radius):
            return True
        elif d > (rock_radius + other_object_radius):
            return False

# Group-object collision handler
def g_collide(group, other_object):
    global lives,explosion_group
    collisions = 0
    for i in list(group):
        if i.collide(other_object):
            group.remove(i)
            explosion_group.add(Sprite(i.pos,i.vel,0,0,explosion_image,explosion_info))
            explosion_sound.play()
            collisions += 1
            if other_object == my_ship and lives > 0:
                lives -= 1
    return collisions

# Group-group collision handler
def gg_collide(group1,group2):
    global score,last_score
    collisions1 = 0
    for i in list(group1):
        for j in list(group2):
            collisions = g_collide(group2,i)
            if i.collide(j):
                group1.remove(i)
                collisions1 += collisions
                score += 10
                last_score = score
    return collisions1
                
# Sprite processing
def process_sprite_group(canvas,group):
    for i in list(group):
        i.update()
        i.draw(canvas)
        
        if i.update():
            group.remove(i)  
        
# Ship controls key handlers  
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# Mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

# Main draw handler
def draw(canvas):
    global time, started, lives, score, rock_group, last_game_score
    
    # Animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas,rock_group)
    process_sprite_group(canvas,missile_group)
    process_sprite_group(canvas,explosion_group)
    
    # update ship and sprites
    my_ship.update()
    g_collide(rock_group,my_ship)
    gg_collide(missile_group,rock_group)
    
    # Previous game score update
    score_label.set_text(str(last_score))
    
    # Play soundtrack
    soundtrack.play()

    # Draw splash screen at startup
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        lives = 3
        score = 0
        soundtrack.rewind()

    if lives == 0:
        started = False
        rock_group = set([])

# Rock spawn handler   
def rock_spawner():
    global a_rock,rock_group,my_ship,score
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.randrange(0,1), random.randrange(0,1)]
    if score > 50:
        rock_vel = [random.randrange(0,2), random.randrange(0,2)]
    if score > 100:
        rock_vel = [random.randrange(0,3), random.randrange(0,3)]
    if score > 150:
        rock_vel = [random.randrange(0,4), random.randrange(0,4)]
    
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    if started and len(rock_group) < 12 and dist(rock_pos,my_ship.pos) > 150:
        rock_group.add(a_rock)        
            
# Initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# Initialize ship, rocks, missiles and explosions
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# Handler registration
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
label = frame.add_label(" Asteroids ")
space = frame.add_label("")
label = frame.add_label("Controls:")
label = frame.add_label("* Up -> Thrust")
label = frame.add_label("* Left/Right -> Turn")
label = frame.add_label("* Space -> Missiles")
space = frame.add_label("")
label = frame.add_label("Last Game Score: ")
score_label = frame.add_label(str(score))
timer = simplegui.create_timer(1000.0, rock_spawner)

# Begin game at startup
timer.start()
frame.start()