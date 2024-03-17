import random
from math import degrees, atan

import colors
from colors import *
import pygame
from entity import *
from functions import positions_field, calculate_angular_coefficient, intersection_ordinate, nearest_point, \
    get_color_name, get_value_from, set_value_to
from global_vars import Global


def untangle(field, ij, color, chain=None):
    if chain is None:
        chain = set()
    i, j = ij
    odd_i = [(1, 0), (2, 0), (1, 1), (-1, 1), (-2, 0), (-1, 0)]
    even_i = [(1, -1), (2, 0), (1, 0), (-1, 0), (-2, 0), (-1, -1)]
    for a, b in odd_i if i % 2 != 0 else even_i:
        if (i + a, j + b) in chain:
            continue
        if 0 <= i + a < len(field) and 0 <= j + b < len(field[0]) and field[i + a][j + b].color == color:
            chain.add((i + a, j + b))
            chain = chain | untangle(field, (i + a, j + b), color, chain)
    if chain:
        chain.add(ij)
    return chain


def look_for(field, x, y):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j].x == x and field[i][j].y == y:
                return i, j


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Игра")

        self.score = 0
        self.shots = 0
        self.coming_down_in = 5
        self.crnt_clr = random.choice(colors.hexagon_color_variety)
        self.nxt_clr = random.choice(colors.hexagon_color_variety)

        self.screen = pygame.display.set_mode((Global().width, Global().height))
        self.screen.fill(color=white)
        self.background = load_image("background.jpg")
        self.clock = pygame.time.Clock()

        self.field = []
        self.empty_places = []
        self.cannon = Cannon(270, 910, Global().cannon_sprites)
        self.projectile = Projectile(self.cannon.x, self.cannon.y, 20, Global().projectile_sprites, color=self.crnt_clr)
        self.projectile.is_ready_to_deploy = True
        self.pos_field = positions_field(radius=20)
        i = 0
        for row in self.pos_field:
            field_row = []
            for x, y in row:
                if i < 11:
                    hexagon = Hexagon(x, y, 20, Global().hexagon_sprites)
                    field_row.append(hexagon)
                else:
                    empty = Empty(x, y, 20, Global().empty_sprites)
                    field_row.append(empty)
                    self.empty_places.append((x, y))
            i += 1
            self.field.append(field_row)

        self.mouse_pos = 0, 0
        self.is_taking_aim = False
        self.running = False

    def loop(self):
        self.running = True
        while self.running:
            self.mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Exit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.projectile.is_ready_to_deploy:
                            self.launch_projectile()
                            self.shots += 1
                    elif event.button == 3:
                        self.is_taking_aim = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.is_taking_aim = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        for hexagon in Global().hexagon_sprites:
                            if hexagon.rect.collidepoint(self.mouse_pos):
                                i, j = look_for(self.field, hexagon.x, hexagon.y)
                                print(i, j, id(self.field[i][j]), "Hexagon")
                                break
                        else:
                            for empty in Global().empty_sprites:
                                if empty.rect.collidepoint(self.mouse_pos):
                                    i, j = look_for(self.field, empty.x, empty.y)
                                    print(i, j, id(self.field[i][j]), "Empty")
                                    break
                    elif event.key == pygame.K_ESCAPE:
                        return "Menu"
            self.screen.fill(white)
            self.screen.blit(self.background, (0, 0))

            k = calculate_angular_coefficient(self.mouse_pos, (self.cannon.x, self.cannon.y))
            if self.is_taking_aim:
                wall_x = 0 if self.mouse_pos[0] < self.cannon.x else Global().width
                wall_y = intersection_ordinate(k, (self.cannon.x, self.cannon.y), wall_x)
                pygame.draw.line(self.screen, red, (self.cannon.x, self.cannon.y), (wall_x, wall_y))
            angle = degrees(atan(k))
            rotation_angle = 90 - abs(angle) if angle >= 0 else abs(angle) - 90
            self.cannon.rotate_to(rotation_angle)
            if self.projectile.is_collided:
                if self.projectile.y >= 630:
                    self.update_values()
                    return "Game over"
                nearest_place = nearest_point((self.projectile.x, self.projectile.y), self.empty_places)
                self.empty_places.remove(nearest_place)
                color = self.projectile.color
                hexagon = Hexagon(*nearest_place, 20, Global().hexagon_sprites, color=color)
                for i in range(len(self.field)):
                    for j in range(len(self.field[i])):
                        if (self.field[i][j].x, self.field[i][j].y) == nearest_place:
                            self.field[i][j].kill()
                            chain = untangle(self.field, (i, j), hexagon.color)
                            if not chain:
                                Global().hitting_sound.play()
                                self.field[i][j] = hexagon
                            else:
                                Global().destruction_sound.play()
                                self.field[i][j] = Empty(*nearest_place, 20, Global().empty_sprites)
                                hexagon.kill()
                                for p, q in chain:
                                    pos = self.field[p][q].x, self.field[p][q].y
                                    self.field[p][q].kill()
                                    self.field[p][q] = Empty(pos[0], pos[1], 20, Global().empty_sprites)
                                    self.empty_places.append(pos)
                                self.score += len(chain) - 1
                            break
                self.projectile.kill()
                clr = self.nxt_clr
                self.projectile = Projectile(self.cannon.x, self.cannon.y, 20, Global().projectile_sprites, color=clr)
                self.nxt_clr = random.choice(colors.hexagon_color_variety)
                self.projectile.is_ready_to_deploy = True

                if self.score < 45:
                    self.coming_down_in = 6
                elif self.score < 60:
                    self.coming_down_in = 5
                elif self.score < 75:
                    self.coming_down_in = 4
                elif self.score < 90:
                    self.coming_down_in = 3
                if self.shots > 0 and self.shots % self.coming_down_in == 0:
                    self.move_down()

            pygame.draw.line(self.screen, gray_red, (0, 630), (Global().width, 630), 3)
            self.draw_text()
            Global().all_sprites.update()
            Global().all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(Global().fps)

        self.update_values()
        return "Game over"

    def draw_text(self):
        font30 = pygame.font.Font(None, 30)
        font25 = pygame.font.Font(None, 25)
        score = font30.render(f"Счёт: {self.score}", True, black, pink_lavender)
        shots = font30.render(f"Выстрелы: {self.shots}", True, black, pink_lavender)
        shots_to_coming_down = font30.render(f"Спуск через: {self.coming_down_in - self.shots % self.coming_down_in}",
                                             True, black, pink_lavender)
        exit_info = font25.render("Нажмите Esc, чтобы закончить игру и вернуться в меню", True, gray, seashell)
        exit_info_rect = exit_info.get_rect()
        exit_info_rect.centerx, exit_info_rect.centery = Global().width // 2, 645
        nxt_clr = font30.render(f"Дальше: {get_color_name(self.nxt_clr)}", True, self.nxt_clr, snow_white)
        self.screen.blit(score, (0, 700))
        self.screen.blit(shots, (0, 740))
        self.screen.blit(shots_to_coming_down, (0, 780))
        self.screen.blit(exit_info, exit_info_rect)
        self.screen.blit(nxt_clr, (self.cannon.x + 50, self.cannon.y))

    def update_values(self):
        record = get_value_from("record")
        if record < self.score:
            set_value_to("record", self.score)
        set_value_to("last_score", self.score)

    def move_down(self):
        field = []
        for i in range(-2, 0):
            for j in range(len(self.field[i])):
                x, y = self.field[i][j].x, self.field[i][j].y
                if (x, y) in self.empty_places:
                    self.empty_places.remove((x, y))

                self.field[i][j].kill()
        for i in range(len(self.field) - 3, -1, -1):
            row = []
            for j in range(len(self.field[i])):
                row.append(self.field[i][j])
                self.field[i][j].x, self.field[i][j].y = self.pos_field[i + 2][j]
            field.append(row)
        for i in range(2):
            row = []
            for j in range(len(self.field[i])):
                hexagon = Hexagon(*self.pos_field[i][j], 20, Global().hexagon_sprites)
                row.append(hexagon)
            field.append(row)
        field.reverse()
        self.field = field
        for i in range(-2, 0):
            for j in range(len(self.field[i])):
                if type(self.field[i][j]) == Hexagon:
                    self.running = False

    def launch_projectile(self):
        Global().shot_sound.play()
        mx, my = self.mouse_pos
        cx, cy = self.cannon.x, self.cannon.y
        direction = mx - cx, my - cy
        length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        normalized = direction[0] / length, direction[1] / length
        self.projectile.direction = normalized
        self.projectile.is_ready_to_deploy = False
