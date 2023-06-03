"""
two text rendering styles. outlined and hollow. both
use a single pixel border around the text. you might be
able to cheat a bigger border by fooling with it some.
"""
import os, sys, pygame, pygame.font, pygame.image
from pygame.locals import *


def textHollow(font, message, fontcolor):
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img

def textOutline(font, message, fontcolor, outlinecolor):
    base = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img


entry_info1 = 'Hollow, by Pete Shinners'
entry_info2 = 'Outlined, by Pete Shinners'

#this code will display our work, if the script is run...
if __name__ == '__main__':
    pygame.init()

    #create our fancy text
    white = 255, 255, 255
    grey = 100, 100, 100
    bigfont = pygame.font.Font(None, 60)
    text1 = textHollow(bigfont, entry_info1, white)
    text2 = textOutline(bigfont, entry_info2, grey, white)

    #create a window the correct size
    width = max(text1.get_width(), text2.get_width())
    height = text1.get_height() + text2.get_height()
    win = pygame.display.set_mode((width, height))
    win.fill((20, 20, 80), (0, 0, width, 30))
    win.fill((20, 20, 80), (0, height-30, width, 30))

    win.blit(text1, (0, 0))
    win.blit(text2, (0, text1.get_height()))
    pygame.display.flip()
    
    #wait for the finish
    while 1:
        event = pygame.event.wait()
        if event.type is KEYDOWN and event.key == K_s: #save it
            name = os.path.splitext(sys.argv[0])[0] + '.bmp'
            print ('Saving image to:', name)
            pygame.image.save(win, name)
        elif event.type in (QUIT,KEYDOWN,MOUSEBUTTONDOWN):
            break
'''
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)

draw_rect_alpha(screen, (0, 0, 255, 50), (screen_width/2 - 265 , screen_height/2 - 265 , 525, 525))
draw_circle_alpha(screen, (255, 0, 0, 3), (screen_width/2 - 231 + (player_position[1] * 42), screen_height/2 - 231 + (player_position[0] * 42)), 80)
draw_polygon_alpha(screen, (255, 255, 0, 127), 
[(100, 10), (100 + 0.8660 * 90, 145), (100 - 0.8660 * 90, 145)])
'''