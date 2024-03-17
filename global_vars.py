import pygame

pygame.mixer.init()


class Global(object):
    _instance = None

    width = 540
    height = 960
    fps = 60
    all_sprites = pygame.sprite.Group()
    cannon_sprites = pygame.sprite.Group()
    hexagon_sprites = pygame.sprite.Group()
    projectile_sprites = pygame.sprite.Group()
    empty_sprites = pygame.sprite.Group()

    ui_sprites = pygame.sprite.Group()
    projectile_speed = 10

    volume = 1.0
    click_sound = pygame.mixer.Sound("./sounds/click.wav")
    shot_sound = pygame.mixer.Sound("./sounds/shot.wav")
    bounce_sound = pygame.mixer.Sound("./sounds/bounce.wav")
    hitting_sound = pygame.mixer.Sound("./sounds/hitting.wav")
    destruction_sound = pygame.mixer.Sound("./sounds/chain.wav")

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def set_volume(self, volume: float):
        self.volume = volume
        self.click_sound.set_volume(volume)
        self.shot_sound.set_volume(volume)
        self.bounce_sound.set_volume(volume)
        self.hitting_sound.set_volume(volume)
        self.destruction_sound.set_volume(volume)

    def clear(self):
        for sprite in self.all_sprites:
            sprite.kill()
        for sprite in self.ui_sprites:
            sprite.kill()
