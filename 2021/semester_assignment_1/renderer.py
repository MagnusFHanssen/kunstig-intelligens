import os
import pygame
import sys
import time
from pygame.locals import *


class Renderer:
    SAND = ord('1')
    CAC_1 = ord('2')
    CAC_2 = ord('3')
    B_UL = ord('4')
    B_UM = ord('5')
    B_UR = ord('6')
    B_RM = ord('7')
    B_LR = ord('8')
    B_LM = ord('9')
    B_LL = ord('a')
    B_ML = ord('b')
    B_IC = ord('c')

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Agent Visualisation')
        self.screen = pygame.display.set_mode((1440, 900), 0, 32)
        self.display = pygame.Surface((1440, 900))
        self.sand = [pygame.image.load(os.path.join('images', 'sand0.png')).convert_alpha(),
                     pygame.image.load(os.path.join('images', 'sand1.png')).convert_alpha(),
                     pygame.image.load(os.path.join('images', 'sand2.png')).convert_alpha(),
                     pygame.image.load(os.path.join('images', 'sand3.png')).convert_alpha()]

        self.cactus = [pygame.image.load(os.path.join('images', 'cactus1.png')).convert_alpha(),
                       pygame.image.load(os.path.join('images', 'cactus2.png')).convert_alpha()]

        self.blocks = {Renderer.B_UL: pygame.image.load(os.path.join('images', 'b_ul.png')).convert_alpha(),
                       Renderer.B_UM: pygame.image.load(os.path.join('images', 'b_um.png')).convert_alpha(),
                       Renderer.B_UR: pygame.image.load(os.path.join('images', 'b_ur.png')).convert_alpha(),
                       Renderer.B_RM: pygame.image.load(os.path.join('images', 'b_rm.png')).convert_alpha(),
                       Renderer.B_LR: pygame.image.load(os.path.join('images', 'b_lr.png')).convert_alpha(),
                       Renderer.B_LM: pygame.image.load(os.path.join('images', 'b_lm.png')).convert_alpha(),
                       Renderer.B_LL: pygame.image.load(os.path.join('images', 'b_ll.png')).convert_alpha(),
                       Renderer.B_ML: pygame.image.load(os.path.join('images', 'b_ml.png')).convert_alpha(),
                       Renderer.B_IC: pygame.image.load(os.path.join('images', 'b_ic.png')).convert_alpha()
                       }
        self.bh_image = pygame.image.load(os.path.join('images', 'bounty_hunter.png')).convert_alpha()
        self.bandit_image = pygame.image.load(os.path.join('images', 'bandit.png')).convert_alpha()
        self.assistant_image = pygame.image.load(os.path.join('images', 'assistant.png')).convert_alpha()

        self.bg = pygame.image.load(os.path.join('images', 'desert.png')).convert_alpha()

        f = open(os.path.join('resources', 'render_map.txt'))
        self.map_data = [[ord(c) for c in row] for row in f.read().split('\n')]
        f.close()

    def print_map(self):
        print(self.map_data)

    def update(self, bounty_hunter=None, bandit=None, assistant=None):
        self.display.fill((0, 0, 0))
        self.display.blit(self.bg, (0, 0))

        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                self.display.blit(self.sand[((y + 1) % 2) * 2 + ((x + 1) % 2)], (680 + (x - y)*32, 100 + (x + y) * 16))

                if bounty_hunter:
                    if x % 2 == 0 and y % 2 == 0 and (x-2)/2 == bounty_hunter[1] and (y-2)/2 == bounty_hunter[0]:
                        self.display.blit(self.bh_image, (680 + (x - y)*32 - 8, 100 + (x + y) * 16 - 90))
                        bounty_hunter = None
                if bandit:
                    if x % 2 == 0 and y % 2 == 0 and (x-2)/2 == bandit[1] and (y-2)/2 == bandit[0]:
                        self.display.blit(self.bandit_image, (680 + (x - y)*32 - 8, 100 + (x + y) * 16 - 90))
                        bandit = None
                if assistant:
                    if x % 2 == 0 and y % 2 == 0 and (x-2)/2 == assistant[1] and (y-2)/2 == assistant[0]:
                        self.display.blit(self.assistant_image, (680 + (x - y)*32 - 8, 100 + (x + y) * 16 - 90))
                        assistant = None

                if tile == Renderer.CAC_1:
                    self.display.blit(self.cactus[0], (680 + (x - y)*32 + 16, 100 + (x + y) * 16 - 8))
                elif tile == Renderer.CAC_2:
                    self.display.blit(self.cactus[1], (680 + (x - y)*32 + 16, 100 + (x + y) * 16 - 56))
                elif tile == Renderer.B_UL:
                    self.display.blit(self.blocks[Renderer.B_UL], (680 + (x - y) * 32 + 7, 100 + (x + y) * 16 - 40))
                elif tile == Renderer.B_UM:
                    self.display.blit(self.blocks[Renderer.B_UM], (680 + (x - y) * 32 + 6, 100 + (x + y) * 16 - 54))
                elif tile == Renderer.B_UR:
                    self.display.blit(self.blocks[Renderer.B_UR], (680 + (x - y) * 32, 100 + (x + y) * 16 - 56))
                elif tile == Renderer.B_RM:
                    self.display.blit(self.blocks[Renderer.B_RM], (680 + (x - y) * 32, 100 + (x + y) * 16 - 64))
                elif tile == Renderer.B_LR:
                    self.display.blit(self.blocks[Renderer.B_LR], (680 + (x - y) * 32 + 8, 100 + (x + y) * 16 - 66))
                elif tile == Renderer.B_LM:
                    self.display.blit(self.blocks[Renderer.B_LM], (680 + (x - y) * 32 + 8, 100 + (x + y) * 16 - 66))
                elif tile == Renderer.B_LL:
                    self.display.blit(self.blocks[Renderer.B_LL], (680 + (x - y) * 32 + 31, 100 + (x + y) * 16 - 55))
                elif tile == Renderer.B_ML:
                    self.display.blit(self.blocks[Renderer.B_ML], (680 + (x - y) * 32 + 11, 100 + (x + y) * 16 - 57))
                elif tile == Renderer.B_IC:
                    self.display.blit(self.blocks[Renderer.B_IC], (680 + (x - y) * 32 + 5, 100 + (x + y) * 16 - 58))

        for event in pygame.event.get():
            if event.type == QUIT:
                Renderer.quit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                Renderer.quit()

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        pygame.display.update()
        time.sleep(1)

    @staticmethod
    def quit():
        pygame.quit()
