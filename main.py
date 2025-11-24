import pygame
import sys
from pygame.locals import *
from player import Player

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

FONT = pygame.font.Font("DNFBitBitTTF.ttf", 30)
FONT_TITLE = pygame.font.Font("DNFBitBitTTF.ttf", 100)

# 바닥 높이 (부 키 220 기준)
ground_level = window_H - 220 - 50

# BOO 플레이어 생성
player = Player(
    x=100,
    y=ground_level,
    image_path="OOP_TEAM13/image/boo.png",
    screen_width=window_W,
    ground_level=ground_level
)

# ------------------------
# 배경 이미지 로드
# ------------------------
Main_Buildging = pygame.image.load("OOP_TEAM13/image/Main_Building.png").convert()
Main_Buildging = pygame.transform.scale(Main_Buildging, (window_W, window_H))

Howto_Building = pygame.image.load("OOP_TEAM13/image/Howto_Buliding.png").convert()
Howto_Building = pygame.transform.scale(Howto_Building, (window_W, window_H))

# ----------------------------------------
# 색상 정의
# ----------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# ----------------------------------------
# 버튼(Rect) 만들기
# ----------------------------------------
btn_explain = pygame.Rect(280, 460, 150, 60)        # 메인 - 게임설명 버튼
btn_start = pygame.Rect(770, 460, 150, 60)          # 메인 - 게임시작 버튼
btn_start_howto = pygame.Rect(900, 500, 180, 50)    # 설명 화면 - 게임시작 버튼

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
    # ================= 이벤트 처리 =================
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # 키보드 입력
        elif event.type == KEYDOWN:
            # 플레이 화면에서만 점프
            if game_state == "play":
                if event.key == pygame.K_SPACE:
                    player.jump()

        # 마우스 클릭 입력 (버튼 클릭)
        elif event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos

            # ----------- 메인 화면 -----------
            if game_state == "menu":
                # 게임설명 버튼
                if btn_explain.collidepoint(mx, my):
                    game_state = "howto"

                # 게임시작 버튼
                elif btn_start.collidepoint(mx, my):
                    game_state = "play"

            # ----------- 게임설명 화면 -----------
            elif game_state == "howto":
                # 설명 화면의 '게임시작' 버튼
                if btn_start_howto.collidepoint(mx, my):
                    game_state = "play"

    # ================= 화면 그리기 =================
    if game_state == "menu":
        # 메인 화면
        screen.blit(Main_Buildging, (0, 0))

        title = FONT_TITLE.render("학교 가BOO자고!", True, BLACK)
        screen.blit(title, (260, 40))  # 제목 위치는 취향껏 조정 가능

        draw_button(btn_explain, "게임설명")
        draw_button(btn_start, "게임시작")

    elif game_state == "howto":
        # 게임 설명 화면
        screen.blit(Howto_Building, (0, 0))
        draw_button(btn_start_howto, "게임시작")

    elif game_state == "play":
        # 실제 게임 화면
        screen.fill((120, 180, 255))

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update()
        player.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
