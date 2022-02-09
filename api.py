import os
import sys
import pygame
import requests
from io import BytesIO
map_types = ['map', 'sat', 'sat,skl']
map_type = 0
min_spn, max_spn = 0.0005, 0.008
scale = 5
l1, l2 = 37.621094, 55.753605
spn1, spn2 = 0.002, 0.002

response = requests.get(f"http://static-maps.yandex.ru/1.x/?ll=37.621094,55.753605&spn=0.002,0.0022&l=map")


def change_response():
    global response
    map = map_types[map_type]
    ll, spn = f'{l1},{l2}', f'{spn1},{spn2}'
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}2&l={map}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)


def show_map(screen):
    map = map_types[map_type]
    screen.fill((0, 0, 0))
    screen.blit(pygame.image.load(BytesIO(response.content)), (0, 0))
    screen.blit(sat_im, (sat_x, sat_y))
    pygame.display.flip()


def show_sat(screen):
    screen.blit(sat_im, (sat_x, sat_y))
    pygame.display.flip()


change_response()

pygame.init()
screen = pygame.display.set_mode((600, 450))
sat_x, sat_y, sat_w, sat_h = 560, 20, 21, 20
sat_im_dark = pygame.image.load('space_dark.png').convert_alpha()
sat_im_dark = pygame.transform.scale(sat_im_dark, (sat_w, sat_h))
sat_im_light = pygame.image.load('space_light.png').convert_alpha()
sat_im_light = pygame.transform.scale(sat_im_light, (sat_w, sat_h))
sat_im = sat_im_dark
show_map(screen)
running = True
ch = False
sat_ch = False
while running:
    for event in pygame.event.get():
        pygame.display.set_caption('Яндекс Карты')
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if sat_y < y < sat_y + sat_h and sat_x < x < sat_x + sat_w:
                sat_ch = True
            else:
                sat_ch = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if sat_ch:
                map_type = (map_type + 1) % 3
                ch = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == 1073741899:
                if min_spn < spn1:
                    spn1 -= 0.0005
                    spn2 -= 0.0005
                    scale -= 1
                    ch = True
            elif event.key == 1073741902:
                if max_spn > spn1:
                    spn1 += 0.0005
                    spn2 += 0.0005
                    scale += 1
                    ch = True
            elif event.key == 1073741906:
                if l2 + 0.0001 * scale < 90:
                    l2 += 0.0001 * scale
                    ch = True
            elif event.key == 1073741905:
                if -90 < l2 - 0.0001 * scale:
                    l2 -= 0.0001 * scale
                    ch = True
            elif event.key == 1073741904:
                if -180 < l1 - 0.0001 * scale:
                    l1 -= 0.0001 * scale
                    ch = True
            elif event.key == 1073741903:
                if l1 + 0.0001 * scale < 180:
                    l1 += 0.0001 * scale
                    ch = True
        sat_im = sat_im_dark
        if sat_ch:
            sat_im = sat_im_light
        show_sat(screen)
        if ch:
            change_response()
            show_map(screen)
pygame.quit()
