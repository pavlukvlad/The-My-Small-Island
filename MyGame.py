import pygame, sys, random
import time as time_gg
from pygame.locals import *
import pygame as pg
from pygame import *
mainClock = pygame.time.Clock()
pygame.init()
pygame.mouse.set_pos(0, 0)

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = pygame.image.load(path)
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

my_font = Font('data/img/small_font.png')

#my_font.render(screen, 'Hello World!', (20, 20))
    





class player(object):
	def __init__(self, x_pos, y_pos, vel, left, right, max_health, max_stamina, stamina, health, health_regen_time, stamina_regen_time, 
		health_regen_time_count, stamina_regen_time_count, exp, lvl, stand, protection, rect, live, up, down, AnimCount):

		sprite.Sprite.__init__(self)
		self.x_pos = x_pos
		self.y_pos = y_pos

		self.vel = vel

		self.left = left
		self.right = right

		self.max_health = max_health
		self.max_stamina = max_stamina
		self.stamina = stamina
		self.health = health
		self.health_regen_time = health_regen_time
		self.stamina_regen_time = stamina_regen_time
		self.health_regen_time_count = health_regen_time_count
		self.stamina_regen_time_count = stamina_regen_time_count

		self.protection = protection
		self.rect = rect
		self.live = live
		self.up = up
		self.down = down
		self.stand = stand
		self.AnimCount = AnimCount

gravity = 1 # Гравітація

plr = player(333, 333, 1, True, False, 100, 60, 60, 100, 22, 4, 0, 0, 0, 1, False, 0, None, True, False, False, 0)
sheep = player(333, 333, 1, True, False, 5, 60, 60, 5, 22, 4, 0, 0, 0, 1, True, 0, None, True, False, False, 0)

scr_size = (1920,1080)


left_up = [10, 190]
left_up_ = [150, 190]
rigth_down = [275, 190]

class Invetory_UI_small(object):
	def __init__(self, max_slots, pos, button_pl, bar_width, bar_height):
		super(Invetory_UI_small, self).__init__()
		self.max_slots = max_slots
		self.pos = pos
		self.button_pl = button_pl
		self.bar_width = bar_width
		self.bar_height = bar_height

class Invetory_UI_big(object):
	def __init__(self, max_slots, pos, button_pl, bar_width, bar_height):
		super(Invetory_UI_big, self).__init__()
		self.max_slots = max_slots
		self.pos = pos
		self.button_pl = button_pl
		self.bar_width = bar_width
		self.bar_height = bar_height

class Invetory_Slot_UI(object):
	def __init__(self, item, num, mode):
		super(Invetory_Slot_UI, self).__init__()
		self.item = item
		self.num = num
		self.mode = mode

class Button_UI(object):
	def __init__(self, width, height, x, y):
		super(Button_UI, self).__init__()
		self.width = width
		self.height = height
		self.x = x
		self.y = y



Invetory_UI_small  = Invetory_UI_small(5, left_up, 10, 10 * 4 + 4 * 4 -2, 11)
Invetory_UI_big = Invetory_UI_big(10, [left_up[0], left_up[1]], 10, 10 * 10 + 4 * 10 -1, 10 * 1 + 3 * 2 -1)
big_invetory_enable = False
inventory_items = []
inventory_rects = []

big_inventory_bar = pg.Rect(Invetory_UI_big.pos[0], Invetory_UI_big.pos[1] - Invetory_UI_big.bar_height - (Invetory_UI_big.button_pl + 3) * (Invetory_UI_big.max_slots / 5), (Invetory_UI_big.button_pl + 4) * 5 - 4, (Invetory_UI_big.button_pl + 3) * ((Invetory_UI_big.max_slots + Invetory_UI_small.max_slots) / 5) - 3)

for inventory_slot_num in range(Invetory_UI_big.max_slots + Invetory_UI_small.max_slots):
	inventory_item = (f"none({inventory_slot_num + 1})")
	inventory_items.append(inventory_item)

x_rc = big_inventory_bar.x - Invetory_UI_big.button_pl - 4
y_rc = big_inventory_bar.y

for inventory_slot_num in range(Invetory_UI_big.max_slots + Invetory_UI_small.max_slots):

	if x_rc >= (Invetory_UI_big.button_pl + 4) * 4 and y_rc >= Invetory_UI_small.pos[1] - Invetory_UI_small.bar_height:
		y_rc = small_inventory_bar.y
		x_rc = small_inventory_bar.x - Invetory_UI_big.button_pl - 4

	if x_rc >= (Invetory_UI_big.button_pl + 4) * 4:
		x_rc = big_inventory_bar.x - Invetory_UI_big.button_pl - 4
		y_rc += Invetory_UI_big.button_pl
		y_rc += 3

	x_rc += 4
	x_rc += Invetory_UI_big.button_pl
	inventory_rects.append(pg.Rect(x_rc, y_rc, Invetory_UI_big.button_pl, Invetory_UI_big.button_pl))

pause = Button_UI(16, 8, 300, 0 + 15)

plr_idle_left = [pygame.image.load("data/img/plr/idle(left(right))/0.png"), pygame.image.load("data/img/plr/idle(left(right))/1.png"),
pygame.image.load("data/img/plr/idle(left(right))/2.png"), pygame.image.load("data/img/plr/idle(left(right))/3.png")]
plr_idle_right = []

for img in plr_idle_left:
	img_add = pygame.transform.flip(img, True, False)
	plr_idle_right.append(img_add)

plr_idle_down = [pygame.image.load("data/img/plr/idle(down)/0.png"), pygame.image.load("data/img/plr/idle(down)/1.png"),
pygame.image.load("data/img/plr/idle(down)/2.png"), pygame.image.load("data/img/plr/idle(down)/3.png")]
plr_idle_up = [pygame.image.load("data/img/plr/idle(up)/0.png"), pygame.image.load("data/img/plr/idle(up)/1.png")]

plr_run_left = [pygame.image.load("data/img/plr/run(left(right))/0.png"), pygame.image.load("data/img/plr/run(left(right))/1.png"),
pygame.image.load("data/img/plr/run(left(right))/2.png"), pygame.image.load("data/img/plr/run(left(right))/3.png")]
plr_run_right = []

for img in plr_run_left:
	img_add = pygame.transform.flip(img, True, False)
	plr_run_right.append(img_add)
plr_run_down = [pygame.image.load("data/img/plr/run(down)/0.png"), pygame.image.load("data/img/plr/run(down)/1.png"),
pygame.image.load("data/img/plr/run(down)/2.png"), pygame.image.load("data/img/plr/run(down)/3.png")]
plr_run_up = [pygame.image.load("data/img/plr/run(up)/0.png"), pygame.image.load("data/img/plr/run(up)/1.png")]

plr_punch_left = [pygame.image.load("data/img/plr/punch(left(right))/0.png"), pygame.image.load("data/img/plr/punch(left(right))/1.png")]
plr_punch_right = []

for img in plr_punch_left:
	img_add = pygame.transform.flip(img, True, False)
	plr_punch_right.append(img_add)
plr_punch_down = [pygame.image.load("data/img/plr/punch(down)/0.png"), pygame.image.load("data/img/plr/punch(down)/1.png")]
plr_punch_up = [pygame.image.load("data/img/plr/punch(up)/0.png"), pygame.image.load("data/img/plr/punch(up)/1.png")]


wood_icon = pygame.image.load("data/img/icon/wood_icon.png")
wool_icon = pygame.image.load("data/img/icon/wool_icon.png")
stick_icon = pygame.image.load("data/img/icon/stick_icon.png")
mangal_icon = pygame.image.load("data/img/icon/mangal_icon.png")
apple_icon = pygame.image.load("data/img/icon/apple_icon.png")
boat_icon = pygame.image.load("data/img/icon/boat_icon.png")
nail_icon = pygame.image.load("data/img/icon/nail_icon.png")
plr_icon = pygame.image.load("data/img/icon/plr_icon.png")
stone_icon = pygame.image.load("data/img/icon/stone_icon.png")


slot_icon = pygame.image.load("data/img/Inventory/basic_slot.png")
craft_slot_icon = pygame.image.load("data/img/Inventory/enable_slot.png")

flower_tail = [pygame.image.load("data/img/blocks/flower/0.png"), pygame.image.load("data/img/blocks/flower/1.png")]
sand_tail = [pygame.image.load("data/img/blocks/sand/00.png"), pygame.image.load("data/img/blocks/sand/01.png")]
grass_tail = [pygame.image.load("data/img/blocks/grass/0.png"), pygame.image.load("data/img/blocks/grass/1.png"), pygame.image.load("data/img/blocks/grass/01.png")]
wood_tail = pygame.image.load("data/img/blocks/tree/0.png")
stone_tail = pygame.image.load("data/img/blocks/stone/1.png")
water_tail = [pygame.image.load("data/img/blocks/water/0.png"), pygame.image.load("data/img/blocks/water/1.png"), pygame.image.load("data/img/blocks/water/2.png")]

main_bg = [pygame.image.load("data/img/main/mainbg.png"), pygame.image.load("data/img/main/main1bg.png"),
pygame.image.load("data/img/main/main2bg.png"), pygame.image.load("data/img/main/main3bg.png"),
pygame.image.load("data/img/main/main4bg.png"), pygame.image.load("data/img/main/main5bg.png"), pygame.image.load("data/img/main/main6bg.png"), pygame.image.load("data/img/main/main7bg.png")]

credit_bg = [pygame.image.load("data/img/credit/mainbg.png"), pygame.image.load("data/img/credit/main1bg.png"),
pygame.image.load("data/img/credit/main2bg.png"), pygame.image.load("data/img/credit/main3bg.png"),
pygame.image.load("data/img/credit/main4bg.png"), pygame.image.load("data/img/credit/main5bg.png"), pygame.image.load("data/img/credit/main6bg.png"), pygame.image.load("data/img/credit/main7bg.png")]

info_bg = [pygame.image.load("data/img/info/mainbg.png"), pygame.image.load("data/img/info/main1bg.png"),
pygame.image.load("data/img/info/main2bg.png"), pygame.image.load("data/img/info/main3bg.png"),
pygame.image.load("data/img/info/main4bg.png"), pygame.image.load("data/img/info/main5bg.png"), pygame.image.load("data/img/info/main6bg.png"), pygame.image.load("data/img/info/main7bg.png")]
present_bg_img = pygame.image.load("data/img/presentbg.png")

black_img = pygame.image.load("data/img/black.png")
cursor = pygame.image.load("data/img/cursor.png")

start_sound = pygame.mixer.Sound("data/sound/start.wav")



text_1 = ["1", "9", "2", "0", ",", " ", "I", " ", "f", "l", "e", "w", " ", "t", "o", " ", "L", "o", "n", "d", "o", "n", ",", " ", "b", "a", "c", "k", " ", 
"f", "o", "r", " ", "m", "y", " ", "h", "o", "m", "e", ".", " ", "T", "h", "e", " ", "w", "e", "a", "t", "h", "e", "r", " ", "w", "a", "s", " ", "s", "u",
"n", "n", "y", ",", "/", "b", "u", "t", " ", "p", "l", "a", "n", "e", " ", "w", "e", " ", "s", "t", "a", "r", "t", "e", "d", " ", "t", "o", " ", "f", "a",
"l", "l", ",", " ", "p", "l", "a", "n", "e", " ", "c", "r", "a", "s", "h", "e", "d", ".", " ", "I", " ", "m", "a", "n", "a", "g", "e", "t", " ", "t", "o", " ", "s",
"u", "r", "v", "i", "v", "e", "."]

text_2 = ["I", " ", "h", "a", "v", "e", " ", "b", "e", "e", "n", " ", "o", "n", " ", "t", "h", "i", "s", " ", "i", "s", "l", "a", "n", "d", " ", "f", "o", "r", " ", "2", "0", 
" ", "y", "e", "a", "r", "s", ".", " ", "L", "o", "w", " ", "t", "r", "e", "e", "s", ",", "/",  "s", "h", "e", "e", "p",  " ", "a", "n", "d",
" ", "p", "r", "e", "c", "i", "u", "s", " ", "f", "l", "o", "w", "e", "r", "s", " ", "g", "r", "o", "w", " ", "h", "e", "r", "e", ".",]

text_3 = ["T", "h", "i", "s", " ", "y", "e", "a", "r", " ", "s", "h", "o", "u", "l", "d", " ", "b", "e", " ", "t", "h", "e", " ", "l", "a", "s", "t", ","
"o", "n", " ", "t", "h", "i", "s", " ", "i", "s", "l", "a", "n", "d", "!", " ", "I", " ", "n", "e", "e", "d", " ", "t", "o", " ", "t", "a", "k", "e", " ", "w", "o", "o" 
"d", ",", " ", "w", "o", "o", "l", "/", "a", "n", "d", " ", "n", "a", "i", "l", "s", " ", "f", "o", "r", " ", "c", "r", "a", "f", "t", " ", "b","o", "a", "t",
" ", "a", "n", "d", " ", "f", "o", "o", "d", " ", "t", "o", " ", "e", "s", "c", "a", "p", "e", " ", "t", "h", "i", "s", " ", "i", "s", "l", "a", "n", "d", ".", ]

thank = ['T', 'h', 'a', 'n', 'k', '', 'y', 'o', 'u', '!']


class item(object):
	def __init__(self, img, rect, object_rect, width, height, mouse_have, enable, object, max_count, count, name, throw, throw_radius, _type_, size, point):
		super(item, self).__init__()
		self.img = img
		self.rect = rect
		self.object_rect = object_rect
		self.width = width
		self.height = height
		self.mouse_have = mouse_have
		self.enable = enable
		self.max_count = max_count
		self.count = count
		self.name = name
		self.throw = throw
		self.throw_radius = throw_radius
		self._type_ = _type_
		self.size = size
		self.point = point


apple = item(apple_icon, pg.Rect(0, 0, 10, 10), 0, 21, 21, False, False, None, 15, 0, "apple", False, 0, "acsesories_item", "basic", 15)
wood = item(wood_icon, pg.Rect(0, 0, 10, 10), 0, 80, 12, False, False, None, 1, 0, "wood", False, 0, "acsesories_item", "basic", 20)
boat = item(boat_icon, pg.Rect(0, 0, 10, 10), 0, 21, 21, False, False, None, 15, 0, "boat", False, 0, "acsesories_item", "basic", 15)
stone = item(stone_icon, pg.Rect(0, 0, 10, 10), 0, 21, 21, False, False, None, 15, 0, "stone", False, 0, "acsesories_item", "basic", 15)
nail = item(nail_icon, pg.Rect(0, 0, 10, 10), 0, 21, 21, False, False, None, 15, 0, "nail", False, 0, "acsesories_item", "basic", 15)
mangal = item(mangal_icon, pg.Rect(0, 0, 10, 10), 0, 21, 21, False, False, None, 15, 0, "mangal", False, 0, "acsesories_item", "basic", 15)
stick = item(stick_icon, pg.Rect(0, 0, 10, 10), 0, 21, 21, False, False, None, 15, 0, "stick", False, 0, "acsesories_item", "basic", 15)
wool = item(wool_icon, pg.Rect(0, 0, 10, 10), 0, 21, 21, False, False, None, 15, 0, "wool", False, 0, "acsesories_item", "basic", 15)

items = [apple, wood, boat, nail, stone, mangal, stick, wool]


clock = pygame.time.Clock()

scr = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display = pygame.Surface((300, 200))
mouse_click = False
class radius(object):
	def __init__(self, x_wo, y_wo, width, height):
		super(radius, self).__init__()
		self.x_wo = x_wo
		self.y_wo = y_wo
		self.width = width
		self.height = height
		

class Frame(object):
	def __init__(self, bg, buttons, run):
		super(Frame, self).__init__()
		self.bg = bg
		self.buttons = buttons
		self.run = run

history_win = False
item_gived = False

main = Frame(main_bg, [pygame.Rect(425, 280, 105, 90), pygame.Rect(705, 280, 105, 90), pygame.Rect(975, 280, 105, 90)], True)
credit = Frame(credit_bg, pygame.Rect(1010, 470, 70, 55), False)
info = Frame(info_bg, pygame.Rect(1010, 470, 70, 55), False)
game = Frame((0, 0, 0), None, False)
title_story = Frame((0, 0, 0), None, False)
start = Frame((0, 0, 0), None, True)
win = Frame((0, 0, 0), None, False)

game_run = True
FPS = 40
AnimCount = 0

text_1_True = True
text_2_True = False
text_3_True = False
x_text = False
title_story_text_1 = ""
title_story_text_2 = ""
tile_rects_count = []
num_count = 0
combo_time = 0
crafts = 0
# ----------------------------- Start Items

inventory_items[0] = "craft"

inventory_items[0] = "trash"
# ----------------------------- 
mouse_have = 0
item_is_move = False
currrent_slot = 1 # Current slot of fast slots

true_scroll = [0, 0]
speed = 0

combo = 0
combox = pg.Rect(0, 0, 0, 0)


game_map = [
['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','0','0','0','0','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','0','0','0','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','0','0','0','/','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','/','0','0','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','0','0','/','3','2','2','2','2','2','2','2','7','2','2','2','2','2','2','2','2','2','2','7','2','2','2','2','2','2','2','2','2','2','2','2','2','7','2','2','2','2','2','2','2','2','2','2','2','3','/','0','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','/','/','3','2','2','2','7','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','7','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','3','/','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','2','2','1','1','1','4','4','4','4','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','2','2','2','3','/','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','/','3','2','2','2','1','1','1','4','4','4','4','4','4','4','4','1','1','t','1','1','1','-','1','1','1','1','1','1','1','1','4','4','4','4','4','4','4','4','4','4','1','1','1','1','1','1','1','1','2','2','2','3','/','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','/','3','2','2','1','1','1','1','4','4','5','4','4','4','4','4','1','1','1','1','1','1','1','4','4','1','1','1','1','1','4','4','4','4','5','4','4','4','4','4','4','4','1','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','/','3','2','2','1','1','1','1','1','4','4','4','4','4','6','1','1','1','1','1','1','1','1','6','6','4','1','1','1','1','4','6','6','4','4','4','4','4','4','4','4','4','1','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','/','3','2','7','1','1','1','1','1','4','4','1','1','1','t','s','1','1','1','1','1','1','1','1','1','1','1','1','1','1','4','4','4','4','4','4','4','4','5','4','4','4','1','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','2','1','1','1','1','1','1','1','1','1','1','1','1','t','1','1','1','1','1','1','1','s','t','1','1','1','1','4','4','4','4','4','4','4','4','4','4','1','1','1','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','2','1','1','1','1','1','1','1','1','-','1','1','1','1','4','4','4','5','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','2','1','1','1','1','1','1','1','1','1','1','1','1','1','1','5','4','4','4','1','1','1','1','1','1','6','6','1','s','t','1','1','1','1','1','1','1','1','6','s','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','2','1','1','1','1','s','t','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','-','1','1','1','1','1','1','1','1','1','1','1','1','1','2','7','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','2','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','s','t','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','7','2','1','1','1','4','4','4','4','4','4','4','4','1','1','1','1','1','1','1','1','1','4','4','4','4','4','4','1','1','1','1','1','1','1','t','1','1','1','1','1','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','2','1','1','4','5','4','4','4','6','6','4','4','4','1','1','1','1','1','1','1','4','4','4','4','4','4','4','4','4','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','-','1','2','7','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','/','3','2','2','1','1','1','4','4','4','4','4','4','4','4','4','4','1','1','1','-','1','1','1','1','4','4','4','4','4','4','4','1','1','1','1','1','1','4','4','4','4','4','4','4','4','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0'],
['0','0','0','0','0','0','/','3','2','2','1','1','1','4','4','4','4','4','4','5','4','4','4','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','4','4','5','4','4','4','4','4','4','4','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0'],
['0','0','0','0','0','0','/','3','2','7','1','1','1','1','4','4','4','4','4','4','4','4','4','1','1','1','1','1','1','6','6','1','1','1','1','s','t','1','1','1','1','1','1','4','4','4','4','4','4','5','4','4','4','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0'],
['0','0','0','0','0','0','/','3','2','2','2','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','6','6','6','1','1','1','1','1','1','1','1','1','1','1','1','1','6','4','4','4','4','4','4','4','1','1','1','1','1','2','2','2','3','/','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','2','2','1','1','1','1','1','1','s','t','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','2','2','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','/','3','2','7','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','7','2','2','2','2','2','7','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','3','/','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','/','3','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','7','2','2','2','2','2','2','3','/','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','0','/','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','3','/','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','0','0','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','/','0','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
]



tile_rects_count = []
num_count = 0
y = 0
for layer in game_map:
	x = 0
	for tile in layer:
		num_count += 1
		if tile == "s":
			tile_rects_count.append([pygame.Rect(x*16,y*16,16,16), 5, num_count, "s", game_map.index(layer), layer.index(tile)])
			pygame.draw.rect(display, (255, 0, 0), pygame.Rect(x*16-true_scroll[0],y*16-true_scroll[1],16,16))
				
		if tile == "t":
			tile_rects_count.append([pygame.Rect(x*16,y*16,16,16), 10, num_count, "t", game_map.index(layer), layer.index(tile)])
			pygame.draw.rect(display, (255, 0, 0), pygame.Rect(x*16-true_scroll[0],y*16-true_scroll[1],16,16))
		x += 1
	y += 1



plr.rect = pygame.Rect(512, 272, 16, 16) # Rect of plr
crafts = []

# Colision
def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

# Plr colision
def move(rect,movement,tiles):
    collision_types = {"top":False,"bottom":False,"right":False,"left":False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
    return rect, collision_types




def draw_ui(item):
    global small_inventory_bar, big_inventory_bar, skill_bar, big_invetory_enable, inventory_items, skill_slots, mouse_rect, mouse_have, item_is_move, inventory_rects, currrent_slot, crafts, mouse_click, item_gived
    crafts = []

    
    num_none = 0
    keys = pg.key.get_pressed()
    mouse_pos = pg.mouse.get_pos()
    mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
    mouse = pg.mouse.get_pressed()

    q_num=0
    o_num=0

    pg.draw.rect(display, (5,5,5), (0,0, scr_size[0], 13)) # Line




    pg.draw.rect(display, (16, 13, 30), (10, 25, 25, 25)) # Plr fon
    display.blit(plr_icon, (10, 25))
    pg.draw.rect(display, (0, 0, 0), (10, 25, 25, 25), 2) # Plr fon counter


    pg.draw.rect(display, (12, 12, 12), (10, 50, 25, 5)) # Plr fon
    pg.draw.rect(display, (0, 100, 0), (10, 50, 25, 5)) # Plr lvl
    pg.draw.rect(display, (0, 0, 0), (10, 50, 25, 5), 2) # Plr fon counter

    pg.draw.rect(display, (15, 15, 15), (10, 55, 25, 5)) # Plr helth fon
    pg.draw.rect(display, (110, 0, 0), (10, 55, plr.health/(plr.max_health/25), 5)) # Plr health
    pg.draw.rect(display, (5, 5, 5), (10, 55, 25, 5), 2) # Plr health fon counter

    pg.draw.rect(display, (15, 15, 15), (10, 60, 25, 5)) # Plr Stamina Fon
    pg.draw.rect(display, (0, 0, 100), (10, 60, plr.stamina/(plr.max_stamina/25), 5)) # Plr Stamina
    pg.draw.rect(display, (5, 5, 5), (10, 60, 25, 5), 2) # Plr Stamina Fon Counter

    x_c = big_inventory_bar.x
    y_c = big_inventory_bar.y - (Invetory_UI_big.button_pl + Invetory_UI_big.button_pl//2)
    for x in range(4):
    	if big_invetory_enable:
    		pygame.draw.rect(display, (0, 0, 0), pg.Rect(x_c - 1, y_c - 1, Invetory_UI_big.button_pl + 1, Invetory_UI_big.button_pl + 1), 2)

    		display.blit(craft_slot_icon, (x_c, y_c))
    		if x == 0:
    			display.blit(nail_icon, (x_c, y_c))
    			crafts.append(["nail", pg.Rect(x_c - 1, y_c - 1, Invetory_UI_big.button_pl + 1, Invetory_UI_big.button_pl + 1), True, 2])
    			if stone.count < 1:
    				display.blit(black_img, (x_c, y_c))
    				crafts[x][2] = False


    		if x == 1:
    			display.blit(mangal_icon, (x_c, y_c))
    			crafts.append(["mangal", pg.Rect(x_c - 1, y_c - 1, Invetory_UI_big.button_pl + 1, Invetory_UI_big.button_pl + 1), True, 1])
    			if wood.count < 3 or stone.count < 2:
    				display.blit(black_img, (x_c, y_c))
    				crafts[x][2] = False


    		if x == 2:
    			display.blit(stick_icon, (x_c, y_c))
    			crafts.append(["stick", pg.Rect(x_c - 1, y_c - 1, Invetory_UI_big.button_pl + 1, Invetory_UI_big.button_pl + 1), True, 2])
    			if wood.count < 1:
    				display.blit(black_img, (x_c, y_c))
    				crafts[x][2] = False


    		if x == 3:
    			display.blit(boat_icon, (x_c, y_c))
    			crafts.append(["boat", pg.Rect(x_c - 1, y_c - 1, Invetory_UI_big.button_pl + 1, Invetory_UI_big.button_pl + 1), True, 1])
    			if wood.count < 3 or wool.count < 3 or nail.count < 5 or stick.count < 3 or mangal.count < 1:
    				display.blit(black_img, (x_c, y_c))
    				crafts[x][2] = False



    		x_c += Invetory_UI_big.button_pl + 3

    for craft in crafts:
    	if mouse_click and pygame.Rect.colliderect(mouse_rect, craft[1]):
    		if craft[2]:
    			if not (craft[0] in inventory_items):
    				for itemor in inventory_items:
    					if itemor.count("none(") >= 1:
    						for crafted_item in items:
    							if crafted_item.name == craft[0] and not item_gived:
    								inventory_items[inventory_items.index(itemor)] = crafted_item.name
    								crafted_item.count += craft[3]
    								item_gived = True

    			else:
    				for crafted_item in items:
    					if crafted_item.name == craft[0]:
    						crafted_item.count += craft[3]

    		item_gived = False

    		if craft[0] == "nail" and craft[2]:
    			stone.count -= 1

    		if craft[0] == "stick" and craft[2]:
    			wood.count -= 1

    		if craft[0] == "boat" and craft[2]:
    			wood.count -= 4
    			wool.count -= 3
    			nail.count -= 6
    			stick.count -= 2
    			mangal.count -= 1

    		if craft[0] == "mangal" and craft[2]:
    			wood.count -= 3
    			stone.count -= 2

    		mouse_click=False



    #Draw big inventory
    if big_invetory_enable:
        pg.draw.rect(display, (26, 23, 50), big_inventory_bar)
        pg.draw.rect(display, (0, 0, 0), pygame.Rect(big_inventory_bar.x - 2, big_inventory_bar.y -2, big_inventory_bar.width+2, big_inventory_bar.height+2), 2)

    # Item x and y, if big inventory enable
    if big_invetory_enable:
        x_it = big_inventory_bar.x
        y_it = big_inventory_bar.y


    for item_object in inventory_items:

    	if big_invetory_enable:
    		q_num += 1
    		inventory_slot_rect = pg.Rect(x_it, y_it, Invetory_UI_big.button_pl, Invetory_UI_big.button_pl)
    		display.blit(slot_icon, (inventory_slot_rect.x, inventory_slot_rect.y))
    		x_it += Invetory_UI_big.button_pl
    		x_it += 4

    		if x_it >= (Invetory_UI_big.button_pl + 4) * 5:
    			x_it = big_inventory_bar.x
    			y_it += Invetory_UI_big.button_pl
    			y_it += 3

    	number_of_mouse_have = 0

    	for item_o in items:
    		if not item_o.mouse_have:
    			number_of_mouse_have += 1

    		if number_of_mouse_have == len(items):
    			mouse_have = 0

    	if big_invetory_enable:  
    		if item_object == "craft":
    			display.blit(craft_slot_icon, (inventory_slot_rect.x, inventory_slot_rect.y.rect.y))

    		if item_object.count("none") == 0 and item_object != ("craft"):
    			for item_o in items:
    				if item_object == item_o.name:
    					item_o.rect.x = inventory_slot_rect.x
    					item_o.rect.y = inventory_slot_rect.y

    					if mouse[0] and pg.Rect.colliderect(mouse_rect, item_o.rect) and mouse_have == 0:
    						item_o.mouse_have = True

    					if mouse[0] and item_o.mouse_have:
    						item_o.rect.x = mouse_pos[0]
    						item_o.rect.y = mouse_pos[1]
    						mouse_have = 1

    					elif not mouse[0]:
    						item_o.mouse_have = False

    					display.blit(item_o.img, (item_o.rect.x, item_o.rect.y))

    					if not item_o.mouse_have:
    						my_font.render(display, f"{item_o.count}", (item_o.rect.x, item_o.rect.y))

    if item_is_move:

        for rect in inventory_rects:
            o_num += 1
            num_none = 0

            for item_o in items:
                if item_o.name in inventory_items:
                    if pg.Rect.colliderect(pg.Rect(item_o.rect.x, item_o.rect.y, 1, 1), rect):

                        if pg.Rect.colliderect(pg.Rect(item_o.rect.x, item_o.rect.y, 1, 1), pg.Rect(big_inventory_bar.x, big_inventory_bar.y, Invetory_UI_big.button_pl, Invetory_UI_big.button_pl)):
                            item_o.count = 0

                        elif rect.x != item_o.rect.x - 15 and rect.y != item_o.rect.y - 5:
                            inventory_items[inventory_items.index(item_o.name)] = inventory_items[inventory_rects.index(rect)]
                            inventory_items[inventory_rects.index(rect)] = item_o.name
                            item_is_move = False


    # item clear

    for item_name in items:
        if item_name.count <= 0 and item_name.name in inventory_items:
            for name in inventory_items:
                item_name.mouse_have = False
                count_none = name.count("none(")
                num_none += count_none

            inventory_items[inventory_items.index(item_name.name)] = f"none({num_none + 1})"

        if item_name.throw and item_name.name in inventory_items:
            for name in inventory_items:
                item_name.mouse_have = False
                count_none = name.count("none(")
                num_none += count_none

            inventory_items[inventory_items.index(item_name.name)] = f"none({num_none + 1})"

    if keys[pg.K_1]:
        currrent_slot = 1

    elif keys[pg.K_2]:
        currrent_slot = 2

    elif keys[pg.K_3]:
        currrent_slot = 3

    elif keys[pg.K_4]:
        currrent_slot = 4

    pg.draw.rect(display, (24,24,24), (pause.x, pause.y, pause.width, pause.height))
    pg.draw.rect(display, (0,0,0), (pause.x, pause.y, pause.width, pause.height), 2)

    for item_o in items:
    	if item_o.enable:
    		pygame.draw.rect(display, item_o.img, item_o.rect, 2)


def AnimationLoader():
	global combo, combox, tile_rects_count, combo_time
	if plr.AnimCount + 1 >= FPS:
		plr.AnimCount = 0

	if combo_time >= FPS * 5:
		combo_time = 0

	if combo == 1 and plr.left:
		display.blit(plr_punch_left[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))
		combo_time += 1

	if combo_time == FPS * 5:
		combox = pg.Rect((plr.rect.x - 12) - scroll[0], (plr.rect.y + (plr.rect.height // 2))-scroll[1], 12, 3)

	if combo == 1 and plr.right:
		display.blit(plr_punch_right[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))
		combo_time += 1
		if combo_time == FPS * 5:
			combox = pg.Rect((plr.rect.x + 12) - scroll[0], (plr.rect.y + (plr.rect.height // 2))-scroll[1], 12, 3)

	if combo == 1 and plr.up:
		display.blit(plr_punch_up[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))
		combo_time += 1
		if combo_time == FPS * 5:
			combox = pg.Rect((plr.rect.x + (plr.rect.width // 2))-scroll[0], (plr.rect.y - plr.rect.height)-scroll[1], 3, 12)

	if combo == 1 and plr.down:
		display.blit(plr_punch_down[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))
		combo_time += 1
		if combo_time == FPS * 5:
			combox = pg.Rect((plr.rect.x + (plr.rect.width // 2))-scroll[0], (plr.rect.y + plr.rect.height)-scroll[1], 3, 12)


	if combo == 2 and plr.left:
		display.blit(plr_punch_left[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))
		combo_time += 1
		if combo_time == FPS * 5:
			combox = pg.Rect((plr.rect.x - 12) - scroll[0], (plr.rect.y + (plr.rect.height // 2))-scroll[1], 12, 3)

	if combo == 2 and plr.right:
		display.blit(plr_punch_right[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))
		combo_time += 1
		if combo_time == FPS * 5:
			combox = pg.Rect((plr.rect.x + 12) - scroll[0], (plr.rect.y + (plr.rect.height // 2))-scroll[1], 12, 3)
	if combo == 2 and plr.up:
		display.blit(plr_punch_up[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))
		combo_time += 1
		if combo_time == FPS * 5:
			combox = pg.Rect((plr.rect.x + (plr.rect.width // 2))-scroll[0], (plr.rect.y - plr.rect.height)-scroll[1], 3, 12)

	if combo == 2 and plr.down:
		display.blit(plr_punch_down[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))
		combo_time += 1
		if combo_time == FPS * 5:
			combox = pg.Rect((plr.rect.x + (plr.rect.width // 2))-scroll[0], (plr.rect.y + plr.rect.height)-scroll[1], 3, 12)


	elif plr.stand and plr.left and combo == 0:
		display.blit(plr_idle_left[plr.AnimCount // 10], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))

	elif plr.stand and plr.right and combo == 0:
		display.blit(plr_idle_right[plr.AnimCount // 10], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))

	elif plr.stand and plr.down and combo == 0:
		display.blit(plr_idle_down[plr.AnimCount // 10], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))

	elif plr.stand and plr.up and combo == 0:
		display.blit(plr_idle_up[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))




	elif plr.up and combo == 0:
		display.blit(plr_run_up[plr.AnimCount // 20], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))

	elif plr.down and combo == 0:
		display.blit(plr_run_down[plr.AnimCount // 10], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))

	elif plr.left and combo == 0:
		display.blit(plr_run_left[plr.AnimCount // 10], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))

	elif plr.right and combo == 0:
		display.blit(plr_run_right[plr.AnimCount // 10], (plr.rect.x-scroll[0], plr.rect.y-scroll[1]))

	plr.AnimCount += 1

	y = 0
	num_count = 0
	for layer in game_map:
		x = 0
		for tile in layer:
			num_count += 1
			if tile == "s":
				for tile in tile_rects_count:
					if tile[2] == num_count and tile[3] == "s":
						tile[0] = pygame.Rect(x*16 - scroll[0],y*16 - scroll[1],16,16)

			if tile == "t":
				for tile in tile_rects_count:
					if tile[2] == num_count and tile[3] == "t":
						tile[0] = pygame.Rect(x*16 - scroll[0],y*16 - scroll[1],16,16)

			x += 1
		y += 1

	hit_list = []
	for tile in tile_rects_count:
		if pygame.Rect.colliderect(tile[0], combox):
			hit_list.append(tile)
	for tilers in hit_list:
		tilers[1] -= 1

def game_update():
	mouse_pos = pygame.mouse.get_pos()
	for item in inventory_items:
		draw_ui(item)
	AnimationLoader()
	mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
	display.blit(cursor, (mouse_rect.x, mouse_rect.y))
	scr.blit(pygame.transform.scale(display,scr.get_size()),(0, 0))

	pygame.display.update()

def menu_update():
	pygame.display.flip()

def Update_start_scr():
	start_sound.play(0)
	scr.blit(pygame.transform.scale(present_bg_img,scr.get_size()),(0,0))
	pygame.display.update()
	time_gg.sleep(0.5)

while game_run:
	text_time = 0
	skip_text = False
	while start.run:
		clock.tick(FPS)
		Update_start_scr()
		start.run = False

	while main.run:
		clock.tick(FPS)

		mouse_pos = pygame.mouse.get_pos()
		pygame.mouse.set_visible(False)
		mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)


		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()

			if event.type == MOUSEBUTTONDOWN:
				if pygame.Rect.colliderect(mouse_rect, main.buttons[0]):
					game.run = True
					pygame.mouse.set_pos(149, 93)
					main.run = False

				elif pygame.Rect.colliderect(mouse_rect, main.buttons[1]):
					credit.run = True
					main.run = False

				elif pygame.Rect.colliderect(mouse_rect, main.buttons[2]):
					info.run = True
					main.run = False

		if AnimCount + 1 >= FPS:
			AnimCount = 0

		scr.blit(pygame.transform.scale(main_bg[AnimCount // 5],scr.get_size()),(0,0))
		scr.blit(pygame.transform.scale(cursor, (50, 50)), (mouse_rect.x, mouse_rect.y))


		AnimCount += 1

		menu_update()

	while credit.run:
		mouse_pos = pygame.mouse.get_pos()
		pygame.mouse.set_visible(False)
		mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()

			if event.type == MOUSEBUTTONDOWN:
				if pygame.Rect.colliderect(mouse_rect, credit.buttons):
					main.run = True
					credit.run = False

		if AnimCount + 1 >= FPS:
			AnimCount = 0

		scr.blit(pygame.transform.scale(credit_bg[AnimCount // 5],scr.get_size()),(0,0))
		scr.blit(pygame.transform.scale(cursor, (50, 50)), (mouse_rect.x, mouse_rect.y))
		AnimCount += 1

		menu_update()

	while info.run:
		mouse_pos = pygame.mouse.get_pos()

		pygame.mouse.set_visible(False)
		mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()

			if event.type == MOUSEBUTTONDOWN:
				if pygame.Rect.colliderect(mouse_rect, info.buttons):
					main.run = True
					info.run = False

		if AnimCount + 1 >= FPS:
			AnimCount = 0

		scr.blit(pygame.transform.scale(info_bg[AnimCount // 5],scr.get_size()),(0,0))
		scr.blit(pygame.transform.scale(cursor, (50, 50)), (mouse_rect.x, mouse_rect.y))


		AnimCount += 1

		menu_update()









	while game.run:
		keys = pygame.key.get_pressed()
		if not history_win:
			title_story.run = True
			game.run = False
		pygame.mouse.set_visible(False)

		true_scroll[0] += (plr.rect.x-true_scroll[0]-152)/20
		true_scroll[1] += (plr.rect.y-true_scroll[1]-106)/20
		scroll = true_scroll.copy()
		scroll[0] = int(scroll[0])
		scroll[1] = int(scroll[1])
		mouse_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)

		mouse_pos = pygame.mouse.get_pos()
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()

				if event.key == K_e and big_invetory_enable:
					big_invetory_enable = False

				elif event.key == K_e and not big_invetory_enable:
					big_invetory_enable = True

			if event.type == MOUSEBUTTONUP and mouse_have == 1:
				item_is_move = True

			if event.type == MOUSEBUTTONDOWN and event.button == 5 and currrent_slot < 4:
				currrent_slot += 1

			if event.type == MOUSEBUTTONDOWN and event.button == 4 and currrent_slot > 1:
				currrent_slot -= 1

			if event.type != MOUSEBUTTONDOWN:
				combo = 0
				combox = pg.Rect(0, 0, 0, 0)

			elif event.type == MOUSEBUTTONDOWN and (combo == 0 or combo == 1):
				combo += 1

			elif event.type == MOUSEBUTTONDOWN and combo == 2:
				combo -= 1

			if event.type == MOUSEBUTTONUP:
				mouse_click = True

			elif event.type != MOUSEBUTTONUP:
				mouse_click = False

		display.fill((77, 48, 199))

		tile_rects = []
		y = 0
		for layer in game_map:
			x = 0
			for tile in layer:
				if tile == "2":
					display.blit(sand_tail[1], (x*16-scroll[0],y*16-scroll[1]))
				if tile == "-":
					display.blit(grass_tail[0], (x*16-scroll[0],y*16-scroll[1]))
					
				if tile == "1":
					display.blit(grass_tail[2], (x*16-scroll[0],y*16-scroll[1]))
				if tile == "4":
					display.blit(grass_tail[1], (x*16-scroll[0],y*16-scroll[1]))
				if tile == "5":
					display.blit(flower_tail[0], (x*16-scroll[0],y*16-scroll[1]))
				if tile == "6":
					display.blit(flower_tail[1], (x*16-scroll[0],y*16-scroll[1]))
				if tile == "s":
					display.blit(grass_tail[2], (x*16-scroll[0],y*16-scroll[1]))
					display.blit(stone_tail, (x*16-scroll[0],y*16-scroll[1]))
					tile_rects.append(pygame.Rect(x*16,y*16,16,16))
				if tile == "t":
					display.blit(grass_tail[2], (x*16-scroll[0],y*16-scroll[1]))
					display.blit(wood_tail, (x*16-scroll[0],y*16-scroll[1]-5))
					tile_rects.append(pygame.Rect(x*16,y*16,14,14))
				if tile == "7":
					display.blit(sand_tail[0], (x*16-scroll[0],y*16-scroll[1]))
				if tile == "0":
					display.blit(water_tail[0], (x*16-scroll[0],y*16-scroll[1]))
				if tile == "3":
					display.blit(water_tail[2], (x*16-scroll[0],y*16-scroll[1]))
					tile_rects.append(pygame.Rect(x*16,y*16,16,16))
				if tile == "/":
					display.blit(water_tail[1], (x*16-scroll[0],y*16-scroll[1]))
					
				x += 1
			y += 1

		player_movement = [0,0]
		if keys[K_d]:
			player_movement[0] += plr.vel
			plr.right = True
			plr.left = False
			plr.stand = False
			plr.up = False
			plr.down = False

		if keys[K_a]:
			player_movement[0] -= plr.vel
			plr.left = True
			plr.right = False
			plr.stand = False
			plr.up = False
			plr.down = False

		if keys[K_w]:
			player_movement[1] -= plr.vel
			plr.up = True
			plr.left = False
			plr.right = False
			plr.stand = False
			plr.down = False


		if keys[K_s]:
			player_movement[1] += plr.vel
			plr.down = True
			plr.left = False
			plr.right = False
			plr.stand = False
			plr.up = False

		elif not keys[K_d] and not keys[K_a] and not keys[K_w] and not keys[K_s]:
			plr.stand = True

		for tile in tile_rects_count:

			if tile[1] == 0 and tile[3] == "t":
				game_map[tile[4]][tile[5]] = "1"
				apple_count_xd = random.randint(0, 4)
				if not ("wood" in inventory_items):
					for itemor in inventory_items:
						if itemor.count("none(") == 1 and not item_gived:
							inventory_items[inventory_items.index(itemor)] = "wood"
							wood.count += 1
							item_gived = True
				else:
					wood.count += 1

				item_gived = False

				if not ("apple" in inventory_items):
					for itemor in inventory_items:
						if itemor.count("none(") == 1 and not item_gived:
							inventory_items[inventory_items.index(itemor)] = "apple"
							apple.count = apple_count_xd
							item_gived = True
				else:
					apple.count += apple_count_xd

			item_gived = False

			if tile[1] == 0 and tile[3] == "s":
				game_map[tile[4]][tile[5]] = "1"
				if not ("stone" in inventory_items):
					for itemor in inventory_items:
						if itemor.count("none(") == 1 and not item_gived:
							inventory_items[inventory_items.index(itemor)] = "stone"
							stone.count += 1
							item_gived = True
				else:
					stone.count += 1
				item_gived = False

				if not ("wool" in inventory_items):
					for itemor in inventory_items:
						if itemor.count("none(") == 1 and not item_gived:
							inventory_items[inventory_items.index(itemor)] = "wool"
							wool.count = 5
							item_gived = True

				else:
					wool.count += 1

			item_gived = False

		plr.rect,collisions = move(plr.rect,player_movement,tile_rects)

		if boat.mouse_have:
			game.run = False
			win.run = True

		game_update()



	while title_story.run:
		pygame.mouse.set_visible(False)
		item_gived = False

		title_story_text_1 = ""
		title_story_text_2 = ""
		x_text = False

		if text_time == FPS:
			text_time = 0
		text_time += 1	
		clock.tick(FPS)
		display.fill((0, 0, 0))
		skip_text = False

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()

				if event.key == K_SPACE:
					skip_text = True

		scr.blit(pygame.transform.scale(display,scr.get_size()),(0,0))

		pygame.display.update()

		if text_1_True:
			for x in text_1:
				if x == "/":
					x_text = True

				if x_text:
					title_story_text_2 += x

				if not x_text:
					title_story_text_1 += x

				my_font.render(display, title_story_text_1, (20, 40))
				my_font.render(display, title_story_text_2, (20, 60))

				scr.blit(pygame.transform.scale(display,scr.get_size()),(0,0))
				pygame.display.update()

				if len(title_story_text_1 + title_story_text_2) == len(text_1):
					while not skip_text:

						for event in pygame.event.get():
							if event.type == KEYDOWN:
								if event.key == K_ESCAPE:
									sys.exit()

								if event.key == K_SPACE:
									skip_text = True

						my_font.render(display, "Press Space, if you read this", (60, 80))

						scr.blit(pygame.transform.scale(display,scr.get_size()),(0,0))
						pygame.display.update()

					text_1_True = False
					text_2_True = True

		elif text_2_True:
			for x in text_2:
				if x == "/":
					x_text = True

				if x_text:
					title_story_text_2 += x

				if not x_text:
					title_story_text_1 += x

				my_font.render(display, title_story_text_1, (20, 40))
				my_font.render(display, title_story_text_2, (20, 60))

				scr.blit(pygame.transform.scale(display,scr.get_size()),(0,0))
				pygame.display.update()

				if len(title_story_text_1 + title_story_text_2) == len(text_2):
					while not skip_text:

						for event in pygame.event.get():
							if event.type == KEYDOWN:
								if event.key == K_ESCAPE:
									sys.exit()

								if event.key == K_SPACE:
									skip_text = True

						my_font.render(display, "Press Space, if you read this", (60, 80))

						scr.blit(pygame.transform.scale(display,scr.get_size()),(0,0))
						pygame.display.update()

					text_2_True = False
					text_3_True = True

		elif text_3_True:
			for x in text_3:
				if x == "/":
					x_text = True

				if x_text:
					title_story_text_2 += x

				if not x_text:
					title_story_text_1 += x

				my_font.render(display, title_story_text_1, (20, 40))
				my_font.render(display, title_story_text_2, (20, 60))

				scr.blit(pygame.transform.scale(display,scr.get_size()),(0,0))
				pygame.display.update()

				if len(title_story_text_1 + title_story_text_2) == len(text_3):
					while not skip_text:

						for event in pygame.event.get():
							if event.type == KEYDOWN:
								if event.key == K_ESCAPE:
									sys.exit()

								if event.key == K_SPACE:
									skip_text = True

						my_font.render(display, "Press Space, if you read this", (60, 80))

						scr.blit(pygame.transform.scale(display,scr.get_size()),(0,0))
						pygame.display.update()

					history_win = True
					pygame.mouse.set_pos(149, 93)
					game.run = True
					title_story.run = False

	while win.run:
		pygame.mouse.set_visible(False)
		display.fill((0, 0, 0))
		my_font.render(display, "Thank you, you help!", (20, 40))
		my_font.render(display, "Space for End...", (40, 60))

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()

				if event.key == K_SPACE:
					skip_text = True

		scr.blit(pygame.transform.scale(display,scr.get_size()),(0,0))

		pygame.display.update()

pygame.quit()

