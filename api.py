import os
import sys
import pygame
import requests

ll, spn = '37.621094,55.753605', '0.002,0.002'
map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}2&l=map"
response = requests.get(map_request)
if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)


def show_map(screen):
    screen.fill((0, 0, 0))
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    os.remove(map_file)


pygame.init()
screen = pygame.display.set_mode((600, 450))
show_map(screen)
running = True
while running:
    for event in pygame.event.get():
        pygame.display.set_caption('Яндекс Карты')
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
pygame.quit()
