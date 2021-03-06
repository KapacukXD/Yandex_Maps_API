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
mark = ''
cur_address = ''
cur_index = ''

response = requests.get(f"http://static-maps.yandex.ru/1.x/?ll=37.621094,55.753605&spn=0.002,0.0022&l=map")


def geocode(address):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                       "geocode": address,
                       "format": "json"}
    response = requests.get(geocoder_request, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError
    features = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return features


def get_ll_span(address):
    global cur_address, cur_index
    toponym = geocode(address)
    cur_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    try:
        cur_index = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['postal_code']
    except Exception:
        pass
    if not toponym:
        return None, None
    toponym_coodrinates = toponym['Point']['pos']
    tlo, tla = toponym_coodrinates.split(' ')
    return tlo, tla


def change_response():
    global response
    map = map_types[map_type]
    ll, spn = f'{l1},{l2}', f'{spn1},{spn2}'
    if mark:
        mark_p = f'&pt={mark}'
    else:
        mark_p = ''
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}2&l={map}{mark_p}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)


def show_map(screen):
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
show_ind = False
sat_ch = False
font = pygame.font.Font(None, 26)
font2 = pygame.font.Font(None, 18)
clock = pygame.time.Clock()
input_box = pygame.Rect(5, 5, 140, 32)
reset_but = pygame.Rect(5, 375, 133, 30)
ind_but = pygame.Rect(5, 335, 80, 30)
address_box = pygame.Rect(5, 415, 500, 30)
color_inactive = pygame.Color('gray')
color_active = pygame.Color('white')
color = color_inactive
txt_color = pygame.Color('black')
active = False
text = ''
txt_res_but = font.render('Сбросить точку', True, txt_color)
txt_ind_but = font.render('Индекс', True, txt_color)
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
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            if reset_but.collidepoint(event.pos):
                mark = ''
                cur_address = ''
                cur_index = ''
                ch = True
            if ind_but.collidepoint(event.pos):
                show_ind = not show_ind
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if active:
                if event.key == pygame.K_RETURN:
                    tlo, tla = get_ll_span(text)
                    text = ''
                    if tlo:
                        l2, l1 = float(tla), float(tlo)
                        mark = f'{l1},{l2}'
                        ch = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
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
            ch = False
        pygame.draw.rect(screen, color, input_box, 0)
        pygame.draw.rect(screen, color_active, ind_but, 0)
        pygame.draw.rect(screen, color_active, reset_but, 0)
        pygame.draw.rect(screen, color_active, address_box, 0)
        txt_surface = font.render(text, True, txt_color)
        if show_ind:
            cont = cur_index + ' ' + cur_address
        else:
            cont = cur_address
        if len(cont) > 76:
            cont = cont[:73] + '...'
        txt_address = font2.render(cont, True, txt_color)
        cont = ''
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        screen.blit(txt_res_but, (6, 380))
        screen.blit(txt_address, (7, 424))
        screen.blit(txt_ind_but, (10, 340))
        pygame.display.flip()
        clock.tick(30)
pygame.quit()
