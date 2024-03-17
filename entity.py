from random import choice

import pygame.transform
from pygame.mask import from_surface, Mask
from pygame.sprite import Sprite
from pygame.rect import Rect, RectType
from pygame.surface import Surface, SurfaceType

from colors import hexagon_color_variety
from global_vars import Global
from functions import load_image, draw_hexagon


class Entity(Sprite):
    def __init__(self, x: int, y: int, *groups):
        super().__init__(*groups, Global().all_sprites)
        self.image: Surface | SurfaceType = ...
        self.rect: Rect | RectType = ...
        self.mask: Mask = ...
        self.x, self.y = x, y

    def init_image(self, source: str | Surface | SurfaceType):
        if type(source) == str:
            self.image = load_image(source)
        else:
            self.image = source
            self.image = self.image.convert()
            self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.mask = from_surface(self.image)

    def check_collision(self):
        pass

    def update(self):
        if self.rect is Ellipsis:
            raise NotImplemented
        self.rect.centerx = self.x
        self.rect.centery = self.y


class Cannon(Entity):
    def __init__(self, x: int, y: int, *groups):
        super().__init__(x, y, *groups)
        surface = load_image("./images/Cannon.png")
        self.original_surface = pygame.transform.scale(surface, (60, 83))
        self.init_image(self.original_surface)
        self.is_taking_aim = False

    def rotate_to(self, angle: float):
        rotated = pygame.transform.rotate(self.original_surface, angle)
        self.init_image(rotated)


class Hexagon(Entity):
    def __init__(self, x: int, y: int, size: int, *groups, color: tuple = ()):
        super().__init__(x, y, *groups)
        self.size = size
        self.color = choice(hexagon_color_variety) if not color else color
        self.init_image(draw_hexagon(self.size, self.color))

    def update(self):
        super(Hexagon, self).update()
        self.check_collision()


class Empty(Hexagon):
    def __init__(self, x: int, y: int, size: int, *groups):
        super().__init__(x, y, size, *groups, color=(1, 1, 1))
        self.image.set_alpha(0)


class Projectile(Hexagon):
    def __init__(self, x: int, y: int, size: int, *groups, color: tuple = ()):
        super().__init__(x, y, size, *groups, color=color)
        self.direction = 0, 0
        self.is_collided = False
        self.is_ready_to_deploy = False

    def check_collision(self):
        collisions = pygame.sprite.groupcollide(Global().projectile_sprites, Global().hexagon_sprites, False, False,
                                                collided=pygame.sprite.collide_mask)
        if collisions and not self.is_collided:
            self.direction = 0, 0
            self.is_collided = True

    def update(self):
        self.check_collision()
        if not (self.size <= self.x <= Global().width - self.size):
            Global().bounce_sound.play()
            self.direction = -self.direction[0], self.direction[1]
        self.x += self.direction[0] * Global().projectile_speed
        self.y += self.direction[1] * Global().projectile_speed
        super(Projectile, self).update()
