
# game.py
#
# Holds all init call, event, update, draw loops
# 
# Written by Evan

from pygame import key
from consts import *
from input import Input
#from keyboard import Keyboard
#from mouse import Mouse
from entities import Player
from map import Map

import pygame

from menu import BattleMenu, Menu
from pokemon import Pokedex

class Game:
    
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Pokemon Indigo')
        self.screen = pygame.display.set_mode(SCREEN_REZ)
        self.clock = pygame.time.Clock()

        # init keyboard for user input events
        #self.keyboard = Keyboard()

        #self.mouse = Mouse()
        self.input = Input()

        # Game running (Start Screen, Start Intro), Game playing (Game, Battle)
        self.RUNNING, self.PLAYING = True, False

        # 1 = Start Screen, 2 = Start Intro, 3 = Game, 4 = Battle 
        self.STATE = 2

        self.pokedex = Pokedex(self)
        
        #self.game_init()

    def menu_init(self):
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.load('sounds/title.wav')
        pygame.mixer.music.play(-1)  
        self.menu = Menu(self)

    def game_init(self):

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.floor_tiles = pygame.sprite.LayeredUpdates()
        self.struct_tiles = pygame.sprite.LayeredUpdates()
        self.decor_tiles = pygame.sprite.LayeredUpdates()
        self.shadow_tiles = pygame.sprite.LayeredUpdates()
        self.encouter_tiles = pygame.sprite.LayeredUpdates()
        self.entity_sprites = pygame.sprite.LayeredUpdates()

        # Game Music
        pygame.mixer.music.load('sounds/pallet_town.WAV')
        pygame.mixer.music.play(1)  

        # init Map object
        self.map = Map(self, ['overworld.tmx'])
        # int Player object
        self.player = Player(self, SCREEN_W//2-PLAYER_SPRITE_SIZE[0]//2, SCREEN_H//2-PLAYER_SPRITE_SIZE[1]//2)
        #self.player = Player(self, 0, 0)

        for sprite in self.all_sprites:
            sprite.rect.x -= ORIGIN[0]*TILE_SIZE
            sprite.rect.y -= ORIGIN[1]*TILE_SIZE

        self.player.rect.x += ORIGIN[0]*TILE_SIZE
        self.player.rect.y += ORIGIN[1]*TILE_SIZE
        
        #for floor_tile in self.floor_tiles:
        #    print(floor_tile.rect)

    def battle_preinit(self):
        self.battlemenu = BattleMenu(self)
        #self.battlemenu.infobox.add_sentences('lol')

    def battle_init(self):
        pygame.mixer.music.load('sounds/Battle.wav')
        pygame.mixer.music.play(-1) 
        self.battlemenu.set_enemy(self.player.encouter_pokemon)
        self.battlemenu.render_enemy()
        self.battlemenu.infobox.increment_sentences()
        #self.battlemenu.infobox.add_sentences('lol')

    def menu_events(self):
        self.input.get_events()
        # Check for pause or exit
        self.RUNNING = not self.input.EXIT_GAME
        #self.PLAYING = not self.keyboard.EXIT_GAME

        # Check for space and start game
        if self.input.SPACE:
            #
            #self.screen.fill(pygame.Color('black'))
            #pygame.display.flip()
            pygame.mixer.music.stop()
            self.game_init()
            self.battle_preinit()
            
            #self.game_draw()
            #self.unfade()
            self.PLAYING = True
            self.STATE = 3

    def game_events(self):

        self.input.get_events()
        # Check for pause or exit
        self.RUNNING = not self.input.EXIT_GAME
        self.PLAYING = not self.input.EXIT_GAME

        # Running 
        if self.input.SHIFT:
            #if sum(self.input.get_motion_keys()) == 1:
                # Check key
                if self.input.UP:
                    # Move all sprites (Tiles, Entities, etc)
                    for sprite in self.all_sprites:
                        sprite.rect.y += PLAYER_RUNNING_VEL
                    # Move player back, player is in all_sprites (keep screen on player)
                    self.player.vel.y += -PLAYER_RUNNING_VEL
                    # Set facing direction
                    self.player.facing = 'up'
                elif self.input.DOWN:
                    for sprite in self.all_sprites:
                        sprite.rect.y += -PLAYER_RUNNING_VEL
                    self.player.vel.y += PLAYER_RUNNING_VEL
                    self.player.facing = 'down'
                elif self.input.LEFT:
                    for sprite in self.all_sprites:
                        sprite.rect.x += PLAYER_RUNNING_VEL
                    self.player.vel.x += -PLAYER_RUNNING_VEL
                    self.player.facing = 'left'
                elif self.input.RIGHT:
                    for sprite in self.all_sprites:
                        sprite.rect.x += -PLAYER_RUNNING_VEL
                    self.player.vel.x += PLAYER_RUNNING_VEL
                    self.player.facing = 'right'
        # Walking
        else:
            if self.input.UP: 
                for sprite in self.all_sprites:
                    sprite.rect.y += PLAYER_WALKING_VEL
                self.player.vel.y += -PLAYER_WALKING_VEL        
                self.player.facing = 'up'
            elif self.input.DOWN:
                for sprite in self.all_sprites:
                    sprite.rect.y += -PLAYER_WALKING_VEL
                self.player.vel.y += PLAYER_WALKING_VEL
                self.player.facing = 'down'
            elif self.input.LEFT:
                for sprite in self.all_sprites:
                    sprite.rect.x += PLAYER_WALKING_VEL
                self.player.vel.x += -PLAYER_WALKING_VEL
                self.player.facing = 'left'
            elif self.input.RIGHT:
                for sprite in self.all_sprites:
                    sprite.rect.x += -PLAYER_WALKING_VEL
                self.player.vel.x += PLAYER_WALKING_VEL
                self.player.facing = 'right'

        if self.input.HEAL:
            pokemon = self.player.pokemon[0]
            pokemon_max_hp = pokemon.get_static_stat_val('hp')
            pokemon.set_dynamic_stat_val('hp', pokemon_max_hp)
            self.input.reset_bools()

        # DEBUG: Will be removed later
        #if self.input.SPACE:
        #    self.battle_init()
        #    self.STATE = 4

    def battle_events(self):
        
        self.input.get_events()
        #self.input.get_key_bouncing_events()
        # Check for pause or exit
        self.RUNNING = not self.input.EXIT_GAME
        self.PLAYING = not self.input.EXIT_GAME

        mx, my = self.input.get_pos()
       
        


        if self.input.SPACE and not self.battlemenu.animate_init and not self.battlemenu.animate:
            self.battlemenu.infobox.increment_sentences()
            self.battlemenu.infobox_lines = []
            self.input.reset_bools()

        self.battlemenu.check_mouse(mx, my, self.input.M_LEFT)
        self.input.reset_bools()


        
    def game_update(self):
        #self.entity_sprites.update()
        self.all_sprites.update()
        #self.follow_route()
        #self.input.reset_bools()
        #self.reload_sprites()
        #print(self.player.pos)

    def menu_update(self):
        self.menu.update()

    def battle_update(self):
        self.battlemenu.update()

    # TODO
    def follow_route(self):
        if self.map.route['goto']:
            self.map.transition(self.map.route)
            w, h = self.map.get_floor_layer_size()
            self.all_sprites.add(self.player)
            p_x = self.map.route['place'][0]*TILE_SIZE
            p_y = self.map.route['place'][1]*TILE_SIZE
            #vel_x = p_x-self.player.rect.x
            #vel_y = p_y-self.player.rect.y
            print('p', p_x, p_y)
            print('rect', self.player.rect.x, self.player.rect.y)
            #print('vels', vel_x, vel_y)
            
            #for sprite in self.all_sprites:
            #    sprite.rect.x += vel_x
            #    sprite.rect.y += vel_y

            self.player.rect.y = p_y#h*TILE_SIZE-PLAYER_SPRITE_SIZE[1]
            self.player.rect.x = p_x#w//2*TILE_SIZE
            #SCREEN_W//2-PLAYER_SPRITE_SIZE[0]//2, SCREEN_H//2-PLAYER_SPRITE_SIZE[1]//2
            #self.player.rect.x -= vel_x
            #self.player.rect.y -= vel_y
            #self.player.rect.x = SCREEN_W//2-PLAYER_SPRITE_SIZE[0]//2
            #self.player.rect.y =  SCREEN_H//2-PLAYER_SPRITE_SIZE[1]//2
            #self.map.route['goto'] = False
    
    # Draw all sprites
    def game_draw(self):
        # Set screen to black
        self.screen.fill(pygame.Color('black'))
        # draw all sprites
        for sprite in self.all_sprites:
            if abs(self.player.rect.x-sprite.rect.x) <= SCREEN_W:
                if abs(self.player.rect.y-sprite.rect.y) <= SCREEN_H:
                    sprite.draw(self.screen)
        # update display
        pygame.display.flip()
        # try to say at set FPS
        self.clock.tick(FPS)

    def menu_draw(self):
        self.screen.fill(pygame.Color('white'))
        self.menu.draw(self.screen)
        # update display
        pygame.display.flip()
        # try to say at set FPS
        self.clock.tick(FPS)

    def battle_draw(self):
        self.screen.fill(pygame.Color('white'))
        self.battlemenu.draw(self.screen)
        # update display
        pygame.display.flip()
        # try to say at set FPS
        self.clock.tick(FPS)

    def game_loop(self):
        self.game_events()
        self.game_update()
        self.game_draw()      

    def menu_loop(self):
        self.menu_events()
        self.menu_update()
        self.menu_draw()  

    # TODO
    def battle_loop(self):
        self.battle_events()
        self.battle_update()
        self.battle_draw()

    
    def fade(self):
        surf = pygame.Surface(SCREEN_REZ)
        surf.fill(pygame.Color('black'))
        for alpha in range(0, 255):
            surf.set_alpha(alpha)
            self.screen.blit(surf, surf.get_rect())
            pygame.display.flip()
            self.clock.tick(FPS)

    def unfade(self):
        surf = pygame.Surface(SCREEN_REZ)
        surf.fill(pygame.Color('black'))
        for alpha in range(64, 0, -1):
            surf.set_alpha(alpha)
            self.screen.blit(surf, surf.get_rect())
            pygame.display.flip()
            self.clock.tick(FPS)
    

    # Quit game
    def quit(self):
        self.RUNNING = False
        self.PLAYING = False

