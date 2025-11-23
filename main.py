import pygame
import sys
from pygame.locals import *

# ----------------------------------
# 기본 설정
# ----------------------------------

window_W = 1200
window_H = 600
FPS = 30

pygame.init()
screen = pygame.display.set_mode((window_W, window_H))
pygame.display.set_caption("학교 가BOO자고!")
clock = pygame.time.Clock()

FONT = pygame.font.Font("DNFBitBitTTF.ttf", 50)
FONT_TITLE = pygame.font.Font("DNFBitBitTTF.ttf", 80)

# ------------------------
# 배경 이미지 로드
# ------------------------
Main_Buildging = pygame.image.load("OOP_TEAM13/image/Main_Building.png").convert()
Main_Buildging = pygame.transform.scale(Main_Buildging, (window_W, window_H))  # 창 크기에 맞게 늘리기/줄이기

Howto_Building = pygame.image.load("...").convert()  # ← 두 번째 이미지 이름
Howto_Building = pygame.transform.scale(Howto_Building, (window_W, window_H))

#----------------------------------------
# 색상 정의
# ---------------------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)


# ----------------------------------------
# 버튼(Rect) 만들기
# ----------------------------------------
btn_explain = pygame.Rect(420, 380, 150, 60)   # 게임설명 버튼
btn_start = pygame.Rect(630, 380, 150, 60)     # 게임시작 버튼
btn_start_howto = pygame.Rect(950, 520, 180, 50)  # 설명 화면 → 게임시작


# ----------------------------------------
# 현재 화면 상태
# ----------------------------------------
game_state = "menu"  # menu / howto / play


# ----------------------------------------
# 버튼 그리는 함수
# ----------------------------------------
def draw_button(rect, text):
    pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 3)
    
    txt = FONT.render(text, True, BLACK)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)


# ----------------------------------------
# 메인 루프
# ----------------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # --- 클릭 이벤트 ---
        if event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos

            if game_state == "menu":
                if btn_explain.collidepoint(mx, my):
                    game_state = "howto"

                elif btn_start.collidepoint(mx, my):
                    game_state = "play"

            elif game_state == "howto":
                if btn_start_howto.collidepoint(mx, my):
                    game_state = "play"

    # -------------------------------------------------
    # 화면 그리기
    # -------------------------------------------------
    if game_state == "menu":
        screen.blit(Main_Buildging, (0, 0))

        title = FONT_TITLE.render("학교 가BOO자고!", True, BLACK)
        screen.blit(title, (300, 40))

        draw_button(btn_explain, "게임설명")
        draw_button(btn_start, "게임시작")

    elif game_state == "howto":
        screen.blit(Howto_Building, (0, 0))
        draw_button(btn_start_howto, "게임시작")

    elif game_state == "play":
        screen.fill((120, 180, 255))  # 플레이 화면 (나중에 게임 맵 넣기)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()