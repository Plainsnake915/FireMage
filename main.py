import math
import random
import asyncio

import pygame


WIDTH, HEIGHT = 900, 600




class FireMage:
    def __init__(self, x, y, health):
        self.pos = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(1, 0)
        self.size = 25
        self.health = health

    def shoot(self, num_fireballs, pierce):
        fireballs.append(Fireball(self.pos.x, self.pos.y, self.direction, pierce))
        for _ in range(num_fireballs - 1):
            direction = self.direction.rotate(random.uniform(-10, 10))
            fireball = Fireball(self.pos.x, self.pos.y, direction, pierce)
            fireballs.append(fireball)
    def draw(self, screen):
        #screen.blit(self.image, (self.x, self.y))
        
        pygame.draw.polygon(screen, (255, 0, 0), [
                (self.pos + self.size * self.direction.rotate(-140)),
                (self.pos + self.size * self.direction.rotate(140)),
                (self.pos + self.size * self.direction),
            ],)
        for fireball in fireballs:
            fireball.update(enemies)
            fireball.draw(screen)

class Fireball:
    def __init__(self, x, y, direction, pierce):
        self.pos = pygame.math.Vector2(x, y)
        self.direction = direction
        self.speed = 5
        self.size = 10
        self.pierce = pierce

    def update(self, targets):
        self.pos += self.direction * self.speed
        if self.pos.x < 0 or self.pos.x > WIDTH or self.pos.y < 0 or self.pos.y > HEIGHT:
            fireballs.remove(self)
        for target in targets:
            if self.pos.distance_to(target.pos) < self.size + target.size:
                target.health -= 1
                target.size = 10 * target.health
                if target.health <= 0:
                    targets.remove(target)
                self.pierce -= 1
        if self.pierce <= 0:
            fireballs.remove(self)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 165, 0), (int(self.pos.x), int(self.pos.y)), self.size)

class enemy:
    def __init__(self, x, y, speed, direction, health):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(speed * math.cos(direction), speed * math.sin(direction))
        self.direction = pygame.math.Vector2(math.cos(direction), math.sin(direction))
        self.size = 10*health
        self.state = 'PATROL'
        self.health = health
        self.color = (255, 255, 255)
        self.knockback = 50

    def move(self):
        if self.state == 'PATROL':
            self.pos += self.velocity
            
        elif self.state == 'CHASE':
            self.pos += self.direction * self.velocity.length()

    def bounce(self):
        if self.pos.x - self.size < 0 or self.pos.x + self.size > WIDTH:
            self.velocity.x = -self.velocity.x
            self.pos.x = max(self.size, min(self.pos.x, WIDTH - self.size))

        if self.pos.y - self.size < 0 or self.pos.y + self.size > HEIGHT:
            self.velocity.y = -self.velocity.y
            self.pos.y = max(self.size, min(self.pos.y, HEIGHT - self.size))

    def vision(self, FireMage):
        distance = pygame.math.Vector2(FireMage.pos - self.pos)
        dot = self.direction.dot(distance.normalize())
        if dot > 0.5 and distance.length() < 200:
            self.state = 'CHASE'
            self.direction = distance.normalize()
            if distance.length() < 20:
                FireMage.pos += distance.normalize() * self.knockback
                FireMage.health -= 1
        else:
            self.state = 'PATROL'
            self.direction = self.velocity.normalize()
        
    def draw(self):
        self.move()
        self.bounce()
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect((int(self.pos.x), int(self.pos.y)), (self.size, self.size))
        )
        pygame.draw.line(
            screen,
            (0, 255, 0),
            (int(self.pos.x + self.size / 2), int(self.pos.y + self.size / 2)),
            (int(self.pos.x + self.size / 2 + self.direction.x * 20), int(self.pos.y + self.size / 2 + self.direction.y * 20)),
            2
        )

def spawner(wave, enemies):
    
    for _ in range(wave*5):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        direction = 0
        if x < WIDTH // 2:
            x = 0
        else:
            x = WIDTH
            direction = math.pi
        speed = .5 + .2*wave
        
        health = random.randint(1, 3)
        enemies.append(enemy(x, y, speed, direction, health))
    
def upgrade_damage(projectiles, pierce):
    projectiles += 1
    pierce += 1
    return projectiles, pierce

def upgrade_speed(speed, max_speed, fire_rate):
    speed += .06
    max_speed += .5

    fire_rate -= .1
    return speed, max_speed, fire_rate

def upgrade_health(health):
    health += 1
    return health

async def main():
    global fireballs, screen, enemies
    enemies = []
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fire Mage")
    clock = pygame.time.Clock()
    fire_mage = FireMage(WIDTH//2 - 50, HEIGHT//2 - 50, 3)
    velocity = pygame.math.Vector2(0, 0)
    drag = -.03
    max_speed = 1
    speed = .06
    fire_rate = 1
    projectiles = 1
    pierce = 1
    
    next_shot_time = 0
    wave = 1
    wave_time = 20000
    
    fireballs = []
    running = True
    upgrade_menu = False
    game_time = 0

    spawner(wave, enemies)
    
    while running:
        while upgrade_menu:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            upgrade_menu = False
                            running = False
                    screen.fill((0, 0, 0))
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_1]:
                        projectiles, pierce = upgrade_damage(projectiles, pierce)
                        upgrade_menu = False
                        
                    elif keys[pygame.K_2]:
                        speed, max_speed, fire_rate = upgrade_speed(speed, max_speed, fire_rate)
                        upgrade_menu = False
                        
                    elif keys[pygame.K_3]:
                        fire_mage.health = upgrade_health(fire_mage.health)
                        upgrade_menu = False
                        
            
                    font = pygame.font.Font(None, 74)
                    text1 = font.render("Press 1 to Upgrade Damage", True, (255, 0, 0))
                    text2 = font.render("Press 2 to Upgrade Speed", True, (255, 0, 0))
                    text3 = font.render("Press 3 to Upgrade Health", True, (255, 0, 0))
                    screen.blit(text1, (WIDTH/2 - text1.get_width()/2, HEIGHT/2 - text1.get_height()/2 - 100))
                    screen.blit(text2, (WIDTH/2 - text2.get_width()/2, HEIGHT/2 - text2.get_height()/2))
                    screen.blit(text3, (WIDTH/2 - text3.get_width()/2, HEIGHT/2 - text3.get_height()/2 + 100))
                    pygame.display.flip()
                    clock.tick(60)
                    await asyncio.sleep(0)  # Allow other tasks to run  
        if fire_mage.health <= 0:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        if game_time >= wave_time*wave:
            wave += 1
            spawner(wave, enemies)
            
        

        keys = pygame.key.get_pressed()
        acceleration = -.03*velocity
        mouse_pos = pygame.mouse.get_pos()

        fire_mage.direction = pygame.math.Vector2(mouse_pos) - fire_mage.pos
        fire_mage.direction = fire_mage.direction.normalize()
        acceleration = drag*velocity
        yacceleration = pygame.math.Vector2(0, 0)
        xacceleration = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]:
            yacceleration = pygame.math.Vector2(0, -1) * speed
        if keys[pygame.K_c]:
            upgrade_menu = True
            

        if keys[pygame.K_s]:
            yacceleration = pygame.math.Vector2(0, 1) * speed
        if keys[pygame.K_a]:
            xacceleration = pygame.math.Vector2(-1, 0) * speed
        if keys[pygame.K_d]:
            xacceleration = pygame.math.Vector2(1, 0) * speed
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time >= next_shot_time:
            fire_mage.shoot(projectiles, pierce)
            next_shot_time = current_time + fire_rate * 1000
        acceleration += yacceleration + xacceleration
        velocity += acceleration
        if velocity.length() > max_speed:
            velocity.scale_to_length(max_speed)
        fire_mage.pos += velocity
        screen.fill((0, 155, 50))
        
        fire_mage.draw(screen)
        for enemy in enemies:
            enemy.vision(fire_mage)
            enemy.draw()    
        pygame.display.flip()
        

        game_time += clock.tick(60) 
        await asyncio.sleep(0)  # Allow other tasks to run
    
    
    dead = True
    reset = False
    while dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dead = False
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            dead = False
            reset = True
            
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over, Press R to Restart", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        await asyncio.sleep(0)  # Allow other tasks to run
    if reset:
        await main()
    pygame.quit()
asyncio.run(main())



