# -*- coding: utf-8 -*-

import pygame
pygame.init()

import random, os, pyperclip
from openpyxl.utils.cell import get_column_letter as letter, column_index_from_string as num

# CREATING DERICTORIES
os.makedirs(os.path.join(os.getcwd(), 'docs'), exist_ok=True)

# SETTING DEFAUTLS

# Dicts
stats = {
    'balance': 0,
    'bpc': 1, # Banana per click
    'bps': 0, # Banana per second
    'all_time': 0, # Earned for all time
    'clicked': 0, # Click counter
}
consts = {
    'up_names': ['Stone', 'Some stones', 'Pushnoy', 'Nation Gold'],
    'up_icons': ['stone.png', 'stones.png', 'pushnoy.png', 'nation_gold.png'],
    'up_buffs': [1, 10, 75, 500],
    'up_start_costs': [15, 200, 2500, 30000]
}

# Paths
IMG_PATH = os.path.join(os.getcwd(), 'images')
DOC_PATH = os.path.join(os.getcwd(), 'docs')

# Other
success_label_hiding_frame = -1
invisible = chr(8291)


# CLASSES

class Main_Button():
    def __init__(self):
        self.click_flag = True
        self.normal_image = pygame.image.load(os.path.join(IMG_PATH, 'vadim.jpg'))
        self.clicked_image = pygame.image.load(os.path.join(IMG_PATH, 'vadim_monke.jpg'))
        self.x = 400
        self.y = 170
        self.rect = pygame.Rect((self.x, self.y), self.normal_image.get_rect().size)

    def click(self):
        if self.click_flag:
            stats['balance'] += stats['bpc']
            stats['all_time'] += stats['bpc']
            stats['clicked'] += 1
            self.click_flag = False

    def draw(self, clicked):
        if clicked:
            screen.blit(self.clicked_image, (self.x, self.y))
        else:
            screen.blit(self.normal_image, (self.x, self.y))


class Upgrade():
    def __init__(self, name, icon_filename, buff, cost, y):
        self.name = name
        self.icon = pygame.image.load(os.path.join(IMG_PATH, icon_filename))
        self.buff = buff
        self.cost = cost
        self.owned = 0

        self.y = y
        self.x = 850
        self.width = 280
        self.height = 70
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.click_flag = True
    
    def buy(self):
        if self.click_flag:
            if self.cost <= stats['balance']:
                plus_to = ('bps' if random.random() >= 0.85 else 'bpc')
                stats[plus_to] += self.buff
                self.owned += 1
                
                stats['balance'] -= self.cost
                self.cost += round(self.cost * 0.25)

            self.click_flag = False

    def draw(self, clicked):
        if clicked or self.cost > stats['balance']:
            pygame.draw.rect(screen, (40, 40, 40), self.rect, width=0)
        else:
            pygame.draw.rect(screen, (70, 70, 70), self.rect, width=0)
        screen.blit(self.icon, (self.x, self.y))
        name_surface = name_font.render(self.name, 0, (255, 255, 255))
        screen.blit(name_surface, (self.x+75, self.y-5))
        cost_surface = owncost_font.render(f'Cost: {self.cost}', 0, (150, 150, 150))
        screen.blit(cost_surface, (self.x+77, self.y+25))
        owned_surface = owncost_font.render(f'You have: {self.owned}', 0, (150, 150, 150))
        screen.blit(owned_surface, (self.x+78, self.y+45))
        buff_surface = buff_font.render(f'+{self.buff}', 0, (0, 255, 0))
        screen.blit(buff_surface, (self.x+282, self.y+25))


class Stats_show():
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def upd(self):
        self.balance_texts = [
            'Balance:',
            f"{stats['balance']}"
        ]
        self.bp_texts = [
            'Per click:',
            f"{stats['bpc']}",
            'Per second:',
            f"{stats['bps']}"
        ]
        owned_ups = 0
        for up in up_list:
            owned_ups += up.owned
        self.other_texts = [
            'During all the time:',
            f"{stats['all_time']}",
            'Times clicked:',
            f"{stats['clicked']}",
            'Total upgrades owned:',
            f"{owned_ups}"
        ]
    
    def draw(self):
        for i in range(len(self.balance_texts)):
            balance_surface = balance_font.render(self.balance_texts[i], 0, (255, 255, 255))
            screen.blit(balance_surface, (400, 30+(i*45)))
        
        for i in range(len(self.bp_texts)):
            bp_surface = bp_font.render(self.bp_texts[i], 0, (255, 255, 255))
            screen.blit(bp_surface, (20, 50+(i*40)))
        
        for i in range(len(self.other_texts)):
            other_surface = other_font.render(self.other_texts[i], 0, (255, 255, 255))
            screen.blit(other_surface, (20, 250+(i*35)))


class Save_buttons():
    def __init__(self):
        self.x1 = 400
        self.y1 = 420
        self.x2 = 615
        self.y2 = 480
        self.width = 185
        self.height = 50

        self.export_clip_rect = pygame.Rect(self.x1, self.y1, self.width, self.height)
        self.export_file_rect = pygame.Rect(self.x1, self.y2, self.width, self.height)
        self.import_clip_rect = pygame.Rect(self.x2, self.y1, self.width, self.height)
        self.import_file_rect = pygame.Rect(self.x2, self.y2, self.width, self.height)

        self.texts = {
            'export_clip': ['   Export to', '   clipboard'],
            'export_file': ['   Export to', '      file'],
            'import_clip': ['  Import from', '   clipboard'],
            'import_file': ['  Import from', '      file']
        }

        self.click_flag = True

    def export_save(self, is_file):
        if self.click_flag:
            unciphered_list = []
            unciphered_list.extend(stats.values())
            unciphered_list.extend([up.cost for up in up_list])
            unciphered_list.extend([up.owned for up in up_list])
            
            ciphered_list = [letter(num+1) for num in unciphered_list]
            ciphered_str = invisible.join(ciphered_list)

            if is_file:
                with open(os.path.join(DOC_PATH, 'clicker_progress.txt'), 'w', encoding='utf-8') as file:
                    file.write(ciphered_str)
            else:
                pyperclip.copy(ciphered_str)
            
            init_success_label()

            self.click_flag = False
            
    def import_save(self, is_file):
        if self.click_flag:
            if is_file:
                with open(os.path.join(DOC_PATH, 'clicker_progress.txt'), 'r', encoding='utf-8') as file:
                    ciphered_str = file.read()
            else:
                ciphered_str = pyperclip.paste()
            ciphered_list = ciphered_str.split(invisible)
            unciphered_list = [num(word)-1 for word in ciphered_list]

            stats.update([(list(stats.keys())[i], unciphered_list[i]) for i in range(5)])
            for i in range(5, 9):
                up_list[i-5].cost = unciphered_list[i]
            for i in range(9, 13):
                up_list[i-9].owned = unciphered_list[i]

            init_success_label()

            self.click_flag = False

    def draw(self):
        pygame.draw.rect(screen, (70, 70, 70), self.export_clip_rect)
        for i in range(len(self.texts['export_clip'])):
            surface = save_font.render(self.texts['export_clip'][i], 0, (255, 255, 255))
            screen.blit(surface, (self.x1, self.y1+(i*20)))
        pygame.draw.rect(screen, (70, 70, 70), self.export_file_rect)
        for i in range(len(self.texts['export_file'])):
            surface = save_font.render(self.texts['export_file'][i], 0, (255, 255, 255))
            screen.blit(surface, (self.x1, self.y2+(i*20)))
        pygame.draw.rect(screen, (70, 70, 70), self.import_clip_rect)
        for i in range(len(self.texts['import_clip'])):
            surface = save_font.render(self.texts['import_clip'][i], 0, (255, 255, 255))
            screen.blit(surface, (self.x2, self.y1+(i*20)))
        pygame.draw.rect(screen, (70, 70, 70), self.import_file_rect)
        for i in range(len(self.texts['import_file'])):
            surface = save_font.render(self.texts['import_file'][i], 0, (255, 255, 255))
            screen.blit(surface, (self.x2, self.y2+(i*20)))


# FUNCTIONS

def second_increase():
    stats['balance'] += stats['bps']
    stats['all_time'] += stats['bps']

def ciper(data):
    pass

def decipher(data):
    pass

def draw_success_label(frame_count):
    global success_label_hiding_frame
    if frame_count <= success_label_hiding_frame:
        success_surface = success_font.render('Success!', 0, (0, 255, 0))
        screen.blit(success_surface, (200, 488))

def init_success_label():
    global success_label_hiding_frame, frame_counter
    success_label_hiding_frame = frame_counter + FPS


# INITIALIZING OBJECTS

name_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 30)
owncost_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 22)
buff_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 20)
owncost_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 22)
balance_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 45)
bp_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 35)
other_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 25)
save_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 20)
success_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 40)
ws_font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'jbm-r.ttf'), 60)

main_button = Main_Button()
up_list = []
for i in range(len(consts['up_names'])):
    up_list.append(Upgrade(
        name = consts['up_names'][i],
        icon_filename = consts['up_icons'][i],
        buff = consts['up_buffs'][i],
        cost = consts['up_start_costs'][i],
        y = 80 + 80*i)
    )
stats_show = Stats_show()
save_buttons = Save_buttons()


# STARTING & MAINLOOP

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Clicker: KruASe edition')
clock = pygame.time.Clock()

done = False
FPS = 60
frame_counter = 0

while not done:
    clock.tick(FPS)
    screen.fill((50, 50, 50))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if event.type == pygame.MOUSEBUTTONDOWN:
        if main_button.rect.collidepoint(event.pos):
            main_button.draw(True)
            main_button.click()
        else:
            main_button.draw(False)

        for up in up_list:
            if up.rect.collidepoint(event.pos):
                up.draw(True)
                up.buy()
            else:
                up.draw(False)
        
        if save_buttons.export_clip_rect.collidepoint(event.pos):
            save_buttons.export_save(False)
        if save_buttons.export_file_rect.collidepoint(event.pos):
            save_buttons.export_save(True)
        if save_buttons.import_clip_rect.collidepoint(event.pos):
            save_buttons.import_save(False)
        if save_buttons.import_file_rect.collidepoint(event.pos):
            save_buttons.import_save(True)
    else:
        main_button.draw(False)
        main_button.click_flag = True
        for up in up_list:
            up.click_flag = True
            up.draw(False)
        save_buttons.click_flag = True
    
    stats_show.upd()
    stats_show.draw()

    save_buttons.draw()

    draw_success_label(frame_counter)

    # Aaaaaand... watersign!
    ws_surface = ws_font.render('©KruASe', 0, (100, 100, 100))
    screen.blit(ws_surface, (870, 450))

    
    if frame_counter % FPS == 0:
        second_increase()
    
    pygame.display.flip()
    frame_counter += 1
    if frame_counter == FPS*1000:
        frame_counter = 0
        success_label_hiding_frame -= FPS*1000

pygame.quit()
