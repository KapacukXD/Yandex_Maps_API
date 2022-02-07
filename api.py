import os
import sys
import pygame
import requests
from io import BytesIO

min_spn, max_spn = 0.0005, 0.008

l1, l2 = 37.621094, 55.753605
spn1, spn2 = 0.002, 0.002
response = requests.get(f"http://static-maps.yandex.ru/1.x/?ll=37.621094,55.753605&spn=0.002,0.0022&l=map")


def change_response():
    global response
    ll, spn = f'{l1},{l2}', f'{spn1},{spn2}'
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}2&l=map"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)


def show_map(screen):
    screen.fill((0, 0, 0))
    screen.blit(pygame.image.load(BytesIO(response.content)), (0, 0))
    pygame.display.flip()


change_response()

pygame.init()
screen = pygame.display.set_mode((600, 450))
show_map(screen)
running = True
ch = False
while running:
    for event in pygame.event.get():
        pygame.display.set_caption('Яндекс Карты')
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == 1073741899:
                if min_spn < spn1:
                    spn1 -= 0.0005
                    spn2 -= 0.0005
                    ch = True
            elif event.key == 1073741902:
                if max_spn > spn1:
                    spn1 += 0.0005
                    spn2 += 0.0005
                    ch = True
        if ch:
            change_response()
            show_map(screen)
pygame.quit()
