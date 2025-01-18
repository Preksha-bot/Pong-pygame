# -*- coding: utf-8 -*-
import pygame
import sys
import random
pygame.init()
pygame.font.init()
pygame.mixer.init()

font_big=pygame.font.Font(None,55)
font_small=pygame.font.Font(None,36)

window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pong Game", "The pong")



def move_comp_paddle(pong_ball,paddle_comp,pad_c_y):
    speed_compPaddle=7
    if paddle_comp.centery <pong_ball.centery:
        pad_c_y += speed_compPaddle
    elif paddle_comp.centery >pong_ball.centery:
        pad_c_y -= speed_compPaddle
        
    pad_c_y = max(0, min(pad_c_y, 500))  # Ensure it stays within 0 to 500
    return pad_c_y
    

def reset_round(ball_x,ball_y,speed_ball_x,speed_ball_y):
    ball_x=400
    ball_y=300
    valid_speeds=[x for x in range(-8,9) if x not in range(-2,3)]
    speed_ball_x=random.choice(valid_speeds)
    speed_ball_y=random.choice(valid_speeds)
    return ball_x,ball_y,speed_ball_x,speed_ball_y


def main_game_loop():
    
    global score_player
    global score_comp
    
    timer1 = pygame.time.Clock()
    ball_x =400 
    
    pad_c_x =10
    pad_c_y =250
    pad_p_x =780
    pad_p_y =250
    score_comp=0
    score_player=0

    speed_playPaddle=7
    speed_ball_x=-3
    speed_ball_y=3
    ball_y =300
    
    exit_text=font_small.render("exit",True,(52,52,52))
    exit_rect=exit_text.get_rect(center=(50,550))
    
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()
                
           
        # Fill screen with a color
        window.fill((193, 100, 99))  # RGB: Blue
        pygame.draw.line(window,(50,60,150),(400,0),(400,600),5)
        pong_ball=pygame.draw.circle(window,(100,50,0), (ball_x,ball_y), 16)
        paddle_comp=pygame.draw.rect(window,(70,143,73),(pad_c_x,pad_c_y,10,100))
        paddle_player=pygame.draw.rect(window,(70,143,73),(pad_p_x,pad_p_y,10,100))
        score_p_text= font_big.render(str(score_player),True,(225,225,225))
        window.blit(score_p_text,(600,15))
        score_c_text= font_big.render(str(score_comp),True,(225,225,225))
        window.blit(score_c_text,(200,15))
        pygame.draw.rect(window,(225,0,0),exit_rect)
        window.blit(exit_text,(30,540))
        
        
        if score_comp >=5 or score_player >=5:
            pygame.mixer.music.load('gameOver.wav')
            pygame.mixer.music.play(0)
            game_over = True
        
        
        
        ball_x += speed_ball_x
        ball_y += speed_ball_y

    # Check for collision with top and bottom boundary
        if ball_y <= 20 or (ball_y >= 590 - 8):
            speed_ball_y *= -1  # Reverse y-direction
            
        pad_c_y=move_comp_paddle(pong_ball,paddle_comp,pad_c_y)
            
        if paddle_comp.collidepoint((ball_x-8,ball_y)) or paddle_player.collidepoint((ball_x+8,ball_y)) :
            speed_ball_x *= -1
        elif ball_x < 20:
            score_player += 1
            ball_x, ball_y, speed_ball_x, speed_ball_y = reset_round(ball_x, ball_y, speed_ball_x, speed_ball_y)
        elif ball_x > pad_p_x :
            score_comp += 1
            ball_x, ball_y, speed_ball_x, speed_ball_y = reset_round(ball_x, ball_y, speed_ball_x, speed_ball_y)

        keys = pygame.key.get_pressed() 
        if keys[pygame.K_UP] and (pad_p_y>0) :
            pad_p_y -= speed_playPaddle
        if keys[pygame.K_DOWN]and (pad_p_y<520):
            pad_p_y += speed_playPaddle
       
            

        # Update display
        pygame.display.flip()
        
        timer1.tick(60)

    # Quit Pygame
    show_gameEnd()

def show_gameEnd():
    game_over_text=font_big.render("Game over",True,(214,126,44))
    try_text=font_small.render("Try again",True,(8,133,161))
    quit_text=font_small.render("Quit",True,(175,54,60))
    
    # Get rectangles for positioning
    game_over_rect = game_over_text.get_rect(center=(400, 150))
    play_again_rect = try_text.get_rect(center=(400, 300))
    quit_rect = quit_text.get_rect(center=(400, 400))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if Play Again is clicked
                if play_again_rect.collidepoint(mouse_pos):
                    score_comp =0
                    score_player=0
                    main_game_loop()
                    return
                # Check if Quit is clicked
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()
                    
                    
        window.fill((231,199,31))
        window.blit(game_over_text,game_over_rect)
        window.blit(try_text,play_again_rect)
        window.blit(quit_text,quit_rect)
        
        pygame.display.flip()
        
if __name__ == "__main__":
    main_game_loop()
    
