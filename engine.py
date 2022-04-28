import pygame, math, os, sys # импортируем библиотеки
from pygame.locals import *
from settings import *
# глобальный цвет черный
global e_colorkey
e_colorkey = (0,0,0)
background = None

def set_global_colorkey(colorkey):
    global e_colorkey
    e_colorkey = colorkey

# физика игры

# тест 2d столкновений
def collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list
# столкновение в движении
def movingCollision(object, platformList):
    collision_list = []
    for obj in platformList:
        if obj.entity.obj.rect.colliderect(object):
            collision_list.append(obj)
    return collision_list


def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


def loadImage(path, alpha=False):
    if alpha:
        return pygame.image.load(path).convert_alpha()
    else:
        return pygame.image.load(path).convert()

class Font():
    def __init__(self, path):

        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
                                'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                                'a','b','c','d','e','f','g','h','i','j','k','l','m',
                                'n','o','p','q','r','s','t','u','v','w','x','y','z',
                                '.','-',',',':','+','\'','!','?','0','1','2','3','4',
                                '5','6','7','8','9']
        font_img = pygame.image.load(path).convert()
        font_img.set_colorkey(BLACK)
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                char_img.set_colorkey(BLACK)
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()



class physics_obj(object):
    def __init__(self,x,y,x_size,y_size):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.x = x
        self.y = y
        self.prevX = 0
        self.thorugh = False


class cuboid(object):
    def __init__(self,x,y,z,x_size,y_size,z_size):
        self.x = x
        self.y = y
        self.z = z
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size






def flip(img,boolean=True):
    return pygame.transform.flip(img,boolean,False)

def blit_center(surf,surf2,pos):
    x = int(surf2.get_width()/2)
    y = int(surf2.get_height()/2)
    surf.blit(surf2,(pos[0]-x,pos[1]-y))

class entity(object):



    def __init__(self,x,y,size_x,size_y,e_type): # x, y, size_x, size_y, type
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.obj = physics_obj(x,y,size_x,size_y)
        self.animation = None
        self.image = None
        self.animation_frame = 0
        self.animation_tags = []
        self.flip = False
        self.offset = [0,0]
        self.rotation = 0
        self.type = e_type # used to determine animation set among other things
        self.action_timer = 0
        self.action = ''
        self.set_action('idle') # overall action for the entity
        self.entity_data = {}
        self.alpha = None



    def set_animation_tags(self,tags):
        self.animation_tags = tags

    def set_action(self,action_id,force=False):
        if (self.action == action_id) and (force == False):
            pass
        else:
            self.action = action_id
            anim = animation_higher_database[self.type][action_id]
            self.animation = anim[0]
            self.set_animation_tags(anim[1])
            self.animation_frame = 0





    def get_drawn_img(self):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image,self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]],self.flip).copy()
        if image_to_render != None:
            center_x = image_to_render.get_width()/2
            center_y = image_to_render.get_height()/2
            image_to_render = pygame.transform.rotate(image_to_render,self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            return image_to_render, center_x, center_y

    def display(self,surface,scroll):
        image_to_render = None
        if self.animation == None:
            if self.image != None:
                image_to_render = flip(self.image,self.flip).copy()
        else:
            image_to_render = flip(animation_database[self.animation[self.animation_frame]],self.flip).copy()
        if image_to_render != None:
            center_x = image_to_render.get_width()/2
            center_y = image_to_render.get_height()/2
            image_to_render = pygame.transform.rotate(image_to_render,self.rotation)
            if self.alpha != None:
                image_to_render.set_alpha(self.alpha)
            blit_center(surface,image_to_render,(int(self.x)-scroll[0]+self.offset[0]+center_x,int(self.y)-scroll[1]+self.offset[1]+center_y))


global animation_database
animation_database = {}

global animation_higher_database
animation_higher_database = {}

# последовательность анимации, т.е. кадров
def animation_sequence(sequence,base_path,colorkey=(0,0,0),transparency=255):

    result = []
    for frame in sequence:
        image_id = base_path + base_path.split('/')[-2] + '_' + str(frame[0])
        image = pygame.image.load(image_id + '.png').convert_alpha()
        image.set_colorkey(colorkey)
        animation_database[image_id] = image.copy()
        for i in range(frame[1]):
            result.append(image_id)
    return result

def load_animations(path):
    global animation_higher_database, e_colorkey
    f = open(path + 'entity_animations.txt','r')
    line = f.readline().strip()

    while line != "":
        sections = line.split(' ')
        anim_path = sections[0]
        entity_info = anim_path.split('/')
        entity_type = entity_info[0]
        animation_id = entity_info[1]
        timings = sections[1].split(';')
        tags = sections[2].split(';')
        sequence = []
        n = 0
        for timing in timings:
            sequence.append([n,int(timing)])
            n += 1
        anim = animation_sequence(sequence,path + anim_path,e_colorkey)
        if entity_type not in animation_higher_database:
            animation_higher_database[entity_type] = {}
        animation_higher_database[entity_type][animation_id] = [anim.copy(),tags]

        line = f.readline().strip()
    f.close()
