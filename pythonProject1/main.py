import pygame
from sys import exit
import cutTheBit
from random import randint
from pygame.locals import *
import shutil
import traceback
import numpy as np

import tkinter as tk
from tkinter import filedialog
import os
import cutTheMusic

import gesture


def select_music():
    global chose_path
    try:
        root = tk.Tk()
        root.withdraw()


        path = filedialog.askopenfilename( title="choose the MP3 file", filetypes=[("MP3文件",'*.mp3'),("所有文件",'*.*')])
        if path:
            if not os.path.exists("music"):
                os.makedirs("music")

            chose_path = os.path.join("music",os.path.basename(path))

            if os.path.exists(chose_path):
                print("使用已有的音频")
            else:
                shutil.copy(path,chose_path)
                print(chose_path)
            t = cutTheMusic.detect_audio_peaks(chose_path) ## return 值不知道是否需要，以及是否正确
            return True
    except Exception as e:
        print(f"处理音乐文件时出错: {e}")
        traceback.print_exc()
    return False



def display_score():
    score_sur = test_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rect = score_sur.get_rect(center=(400, 50))
    screen.blit(score_sur, score_rect)


def display_lives():
    lives_sur = test_font.render(f'Lives: {lives}', False, (64, 64, 64))
    lives_rect = lives_sur.get_rect(center=(200, 50))
    screen.blit(lives_sur, lives_rect)


def ob_movement(obstacle_list):
    global lives, game_active,game_state
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 9
            screen.blit(star_surface, obstacle_rect)

            # 检查星星是否移出屏幕左侧（未被吃掉）
            if obstacle_rect.right < 0:
                obstacle_list.remove(obstacle_rect)
                lives -= 1
                if lives <= 0:
                    game_active = False
                    game_state = 'over'

        return obstacle_list
    else:
        return []


def player_animation():
    global player_surface, eat_animation
    if eat_animation > 0:
        player_surface = player_surface_t
        eat_animation -= 1
    else:
        player_surface = player_surface_1


def check_eat(obstacles):
    global score, eat_animation
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or gesture.is_index_finger_up():
        for obstacle in obstacles[:]:
            # 是否有星星可以吃
            if (player_rect.colliderect(obstacle) or
                    (player_rect.right >= obstacle.left - 20 and player_rect.right <= obstacle.right + 20)):
                obstacles.remove(obstacle)
                score += 1
                eat_animation = 10
                pygame.mixer.Sound("music/p.mp3").play()




pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Rythem Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = False  # 初始为False，等待玩家按空格开始
start_time = 0
score = 0
lives = 3  # 初始生命数
eat_animation = 0
obstacle_count = 0  # 跟踪已生成的障碍物数量
music_t = False
music_chose = False
chose_path = False

# 加载图像
background_surface = pygame.image.load("image/bg.png").convert_alpha()
star_surface = pygame.image.load('image/star.png').convert_alpha()
obstacle_rec_list = []

# 玩家角色
player_surface_1 = pygame.image.load("image/c.png").convert_alpha()
player_surface_t = pygame.image.load("image/touch.png").convert_alpha()
player_surface = player_surface_1
player_rect = player_surface.get_rect(topleft=(70, 200))

# 文字表面
score_surface = test_font.render('Score: 0', False, "red")
text_surface = test_font.render("Hello", False, 'green')
game_over_sur = test_font.render('Game Over', False, 'red')
start_sur = test_font.render('Press SPACE to Start', False, 'white')

game_win_sur = test_font.render('you win!',False,"yellow")



game_state = "start"
#载入音符表chart
s=cutTheBit.save_sec('testbit.txt')
# 计时器
obtacle_timer = pygame.USEREVENT + 1
#pygame.time.set_timer(obtacle_timer, s[0])  # 初始设置为s的第一个数值#####

while True:
    nowtime = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gesture.release()
            pygame.quit()
            exit()

        if game_active==True or game_state == "play":
            if event.type == obtacle_timer:

                ## ##可以在这里加上if条件来让单线变成多线。再根据相应的s和sit的对应值来确定相应出场的时间
                obstacle_rec_list.append(star_surface.get_rect(topleft=(600, 250)))
                obstacle_count += 1
                if chose_path:
                    s = cutTheBit.save_sec("use.txt")
                else:

                    s = cutTheBit.save_sec('testbit.txt')##老音符表

                # 生成音符时间
                if obstacle_count<=(len(s)):
                    for i in range(len(s)):
                        pygame.time.set_timer(obtacle_timer, s[i])#并非立刻发生，只是设定了一个时间区域，到点发生。所以在未发生ob的时候，代码会循环代码里的其他内容
                        #obstacle_count += 1
                        #print(s[i])##不知道为啥每次都会把所有字符都发一遍，而不是只发一遍自己的
                # elif obstacle_count>(len(s)-1) and obstacle_count<=10:
                #     pygame.time.set_timer(obtacle_timer, 1000)  # 1秒一个
                else:
                #elif not pygame.mixer.music.get_busy():
                    # not pygame.mixer.music.get_busy()
                    #if not pygame.mixer.music.get_busy():
                    game_active = False
                    game_state = "win"

            #if



                # if obstacle_count == 1:  # 第2个
                #     pygame.time.set_timer(obtacle_timer, 3000)  # 3秒后
                # elif obstacle_count == 2:
                #     pygame.time.set_timer(obtacle_timer, 5000)  # 5秒
                # elif obstacle_count >= 3:
                #     pygame.time.set_timer(obtacle_timer, 1000)  # 1秒一个
        else:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE: #开始时重置所有的，但是不重置音乐
                    if game_state == "start":
                        game_state == "play"
                        game_active = True
                        start_time = pygame.time.get_ticks()
                        score = 0
                        lives = 3  # 重置生命
                        obstacle_rec_list.clear()
                        obstacle_count = 0  # 重置计数器
                        pygame.time.set_timer(obtacle_timer, s[0])  # 重置计时器为2秒
                        music_t = False
                        music_chose = False########新加的，可能会要去掉，本段是为了检查是否添加了音乐
                       # chose_path = []
                    elif game_state == 'over' or game_state == 'win':
                        game_state = 'start'
                        game_active = False

                if event.key ==pygame.K_a and not music_chose:
                    if select_music():
                        music_chose = True
                        MUSIC_sur = test_font.render("已加载",False, 'white')

    if game_active==True or game_state == 'play':
        if music_t==False and nowtime - start_time >=1300:
            if chose_path:
                print(f"Loading custom music from: {chose_path}")
                pygame.mixer.music.load(chose_path)#######换了音乐  7/3
            else:
                pygame.mixer.music.load("music/test.mp3")
            pygame.mixer.music.play()
            music_t = True

        screen.blit(background_surface, (0, 0))
        screen.blit(text_surface, (100, 100))

        # 更新和显示分数和生命
        display_score()
        display_lives()

        # 地面线
        pygame.draw.line(screen, 'gold', (0, 300), (600, 300), 5)

        # 更新障碍物位置
        obstacle_rec_list = ob_movement(obstacle_rec_list)

        # 检查是否可以吃星星
        check_eat(obstacle_rec_list)

        # 玩家动画
        player_animation()

        # 绘制玩家
        screen.blit(player_surface, player_rect)


    else:
        screen.blit(background_surface, (0, 0))

        if lives <= 0 and game_state == 'over':  # 游戏结束
            screen.blit(game_over_sur, (200, 50))
            # 显示最终分数
            score_mess = test_font.render(f'Final Score: {score}', False, 'white')
            screen.blit(score_mess, (200, 150))

        elif  lives>0 and pygame.mixer.music.get_busy():
            wait_sur = test_font.render("waiting for the music",False,'White')
            screen.blit(wait_sur,(200,150))


        elif obstacle_count==(len(s)+1) and lives>0 and game_state =='win' :
            screen.blit(game_win_sur,(200, 50))
            score_mess = test_font.render(f'Final Score: {score}', False, 'white')
            screen.blit(score_mess, (200, 150))
            restart_sur = test_font.render(f'press SPACE to the main',False,'white')
            screen.blit(restart_sur,(150,250))
        else:  # 游戏开始前
            screen.blit(start_sur, (50, 150))
            # 显示操作说明
            instruct_sur = test_font.render('Eat stars with SPACE', False, 'white')
            screen.blit(instruct_sur, (200, 200))
            if music_chose == False:
                music_need = test_font.render("press a to add music",False,'white')
                screen.blit(music_need,(200,100))
                #screen.blit(MUSIC_sur,(50,150))


    pygame.display.update()
    clock.tick(60)