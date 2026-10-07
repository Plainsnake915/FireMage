import math
import random
import asyncio

import pygame


WIDTH, HEIGHT = 900, 600




class FireMage:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(1, 0)
        self.size = 25

    def shoot(self, num_fireballs):
        for _ in range(num_fireballs):
            direction = self.direction.rotate(random.uniform(-10, 10))
            fireball = Fireball(self.pos.x, self.pos.y, direction, 1)
            fireballs.append(fireball)
    def draw(self, screen):
        #screen.blit(self.image, (self.x, self.y))
        
        pygame.draw.polygon(screen, (255, 0, 0), [
                (self.pos + self.size * self.direction.rotate(-140)),
                (self.pos + self.size * self.direction.rotate(140)),
                (self.pos + self.size * self.direction),
            ],)
        for fireball in fireballs:
            fireball.update()
            fireball.draw(screen)

class Fireball:
    def __init__(self, x, y, direction, pierce):
        self.pos = pygame.math.Vector2(x, y)
        self.direction = direction
        self.speed = 5
        self.size = 10
        self.pierce = pierce

    def update(self):
        self.pos += self.direction * self.speed
        if self.pos.x < 0 or self.pos.x > WIDTH or self.pos.y < 0 or self.pos.y > HEIGHT:
            fireballs.remove(self)
        if self.pierce <= 0:
            fireballs.remove(self)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 165, 0), (int(self.pos.x), int(self.pos.y)), self.size)




async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fire Mage")
    clock = pygame.time.Clock()
    fire_mage = FireMage(WIDTH//2 - 50, HEIGHT//2 - 50)
    velocity = pygame.math.Vector2(0, 0)
    drag = -.03
    max_speed = 1
    speed = .06
    fire_rate = 1
    next_shot_time = 0
    global fireballs
    fireballs = []
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
            
        if keys[pygame.K_s]:
            yacceleration = pygame.math.Vector2(0, 1) * speed
        if keys[pygame.K_a]:
            xacceleration = pygame.math.Vector2(-1, 0) * speed
        if keys[pygame.K_d]:
            xacceleration = pygame.math.Vector2(1, 0) * speed
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time >= next_shot_time:
            fire_mage.shoot(1)
            next_shot_time = current_time + fire_rate * 1000
        acceleration += yacceleration + xacceleration
        velocity += acceleration
        if velocity.length() > max_speed:
            velocity.scale_to_length(max_speed)
        fire_mage.pos += velocity
        screen.fill((0, 155, 50))
        
        fire_mage.draw(screen)
        pygame.display.flip()

        clock.tick(120) 
        await asyncio.sleep(0)  # Allow other tasks to run

    pygame.quit()
asyncio.run(main())



