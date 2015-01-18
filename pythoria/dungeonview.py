#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygcurse, pygame
from pythoria.dungeon import Dungeon

pygame.font.init()

PLAYER = '\N{WHITE SMILING FACE}' # Unicode for a smile


class DungeonView(pygcurse.PygcurseSurface):
    font = pygame.font.Font(pygame.font.match_font('consolas'), 18)

    def __init__(self, dungeon, width, height):
        self.dungeon = dungeon
        super(DungeonView, self).__init__(width, height, DungeonView.font)
        self.autoupdate = False
        
    def draw(self, x=0, y=0, width=None, height=None):
        "Draw the dungeon and the player."
        self.setscreencolors()
        self.cursor = (0, 0)
        for y_offset, line in enumerate(self.dungeon[y:height+y]):
            for x_offset, tile in enumerate(line[x:width+x]):
                if tile.visible:
                    self.putchar(tile.value, bgcolor=(30, 30, 30), x=x_offset, y=y_offset)
                else:
                    self.putchar(' ', x=x_offset, y=y_offset)
        if self.dungeon.player:
            for light_x, light_y in self.dungeon.player.fov:
                if not self.dungeon[light_x, light_y].block_light:
                    self.settint(30, 30, 0, (light_x-x, light_y-y, 1, 1))
            self.putchar(PLAYER, x=self.dungeon.player.x-x, y=self.dungeon.player.y-y)
        
        self.update()

def clamp(value, min_, max_):
    return min(max(value, min_), max_)
    
class ScrollingView:
    def __init__(self, dungeon):
        self.width, self.height = 15, 15
        
        self.dungeon_view = DungeonView(dungeon, self.width, self.height)
        
        self.dungeon_width = dungeon.width
        self.dungeon_height = dungeon.height
        self.player = dungeon.player
    
    def draw(self):
        self.left = clamp(self.player.x - self.width // 2, 0, self.dungeon_width)
        self.top = clamp(self.player.y - self.height // 2, 0, self.dungeon_height)
        self.dungeon_view.draw(self.left, self.top, self.width, self.height)
        
    def blitto(self, *args, **kwargs):
        self.dungeon_view.blitto(*args, **kwargs)
        

if __name__ == '__main__':
    import dungeon, player
    win = pygcurse.PygcurseWindow(40,30)
    level1 = Dungeon.load_from_file('../test/map.txt')
    level1.add_player(player.Player(1, 1))
    view = DungeonView(level1)
    view.draw()
    view.blitto(win.surface)
    win.blittowindow()
    
    pygcurse.waitforkeypress()
