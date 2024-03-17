from colors import *
import pygame
from entity import *
from functions import get_value_from
from global_vars import Global


class UIElement(Sprite):
    def __init__(self, x: int, y: int, *groups):
        super().__init__(*groups, Global().ui_sprites)
        self.image: Surface | SurfaceType = ...
        self.rect: Rect | RectType = ...
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

    def update(self):
        if self.rect is Ellipsis:
            raise NotImplemented
        self.rect.centerx = self.x
        self.rect.centery = self.y


class Button(UIElement):
    def __init__(self, x: int, y: int, image: str, *groups):
        super().__init__(x, y, *groups)
        self.init_image(image)
        self.original_surface = self.image.copy()

    def increase(self):
      #  self.image = pygame.transform.scale2x(self.original_surface, 1.1)
        self.rect = self.image.get_rect()

    def decrease(self):
        self.image = self.original_surface
        self.rect = self.image.get_rect()


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Меню")

        self.screen = pygame.display.set_mode((Global().width, Global().height))
        self.screen.fill(color=white)
        self.background = load_image("background.jpg")
        self.clock = pygame.time.Clock()

        font30 = pygame.font.Font(None, 30)
        font80 = pygame.font.Font(None, 80)
        self.title = font80.render("Шестиугольники", True, black, pale_pink)
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx, self.title_rect.centery = Global().width // 2, 100
        self.last_score = font30.render(f"Счет прошлой игры: {get_value_from('last_score')}",
                                        True, black, pale_pink)
        self.last_score_text_rect = self.last_score.get_rect()
        self.last_score_text_rect.centerx, self.last_score_text_rect.centery = Global().width // 2, 220
        self.record_text = font30.render(f"Ваш рекорд: {get_value_from('record')}", True, black, dull_pink)
        self.record_text_rect = self.record_text.get_rect()
        self.record_text_rect.centerx, self.record_text_rect.centery = Global().width // 2, 250

        self.play_btn = Button(Global().width // 2, 500, "./images/Play.png")
        self.exit_btn = Button(Global().width // 2, 720, "./images/Exit.png")

        self.mouse_pos = 0, 0

    def loop(self):
        while True:
            self.mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Exit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Global().click_sound.play()
                    if self.play_btn.rect.collidepoint(self.mouse_pos):
                        return "Play"
                    elif self.exit_btn.rect.collidepoint(self.mouse_pos):
                        return "Exit"
            for sprite in Global().ui_sprites:
                if sprite.rect.collidepoint(self.mouse_pos):
                    sprite.increase()
                else:
                    sprite.decrease()

            self.screen.fill(white)
            self.screen.blit(self.background, (0, 0))
            Global().ui_sprites.update()
            Global().ui_sprites.draw(self.screen)
            self.screen.blit(self.title, self.title_rect)
            self.screen.blit(self.last_score, self.last_score_text_rect)
            self.screen.blit(self.record_text, self.record_text_rect)
            pygame.display.flip()
            self.clock.tick(Global().fps)


class GameOverMenu:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Игра закончена")

        self.screen = pygame.display.set_mode((Global().width, Global().height))
        self.screen.fill(color=white)
        self.background = load_image("background.jpg")
        self.clock = pygame.time.Clock()

        font30 = pygame.font.Font(None, 30)
        self.last_score = font30.render(f"Вы завершили игру со счетом: {get_value_from('last_score')}",
                                        True, black, pale_pink)
        self.last_score_text_rect = self.last_score.get_rect()
        self.last_score_text_rect.centerx, self.last_score_text_rect.centery = Global().width // 2, 150
        self.record_text = font30.render(f"Ваш рекорд: {get_value_from('record')}",
                                         True, black, pale_pink)
        self.record_text_rect = self.record_text.get_rect()
        self.record_text_rect.centerx, self.record_text_rect.centery = Global().width // 2, 200

        self.restart_btn = Button(Global().width // 2, 300, "./images/Restart.png")
        self.menu_btn = Button(Global().width // 2, 500, "./images/Menu.png")
        self.exit_btn = Button(Global().width // 2, 700, "./images/Exit.png")

        self.mouse_pos = 0, 0

    def loop(self):
        while True:
            self.mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Exit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Global().click_sound.play()
                    if self.restart_btn.rect.collidepoint(self.mouse_pos):
                        return "Play"
                    elif self.menu_btn.rect.collidepoint(self.mouse_pos):
                        return "Menu"
                    elif self.exit_btn.rect.collidepoint(self.mouse_pos):
                        return "Exit"
            for sprite in Global().ui_sprites:
                if sprite.rect.collidepoint(self.mouse_pos):
                    sprite.increase()
                else:
                    sprite.decrease()
            self.screen.fill(white)
            self.screen.blit(self.background, (0, 0))
            Global().ui_sprites.update()
            Global().ui_sprites.draw(self.screen)
            self.screen.blit(self.last_score, self.last_score_text_rect)
            self.screen.blit(self.record_text, self.record_text_rect)
            pygame.display.flip()
            self.clock.tick(Global().fps)
