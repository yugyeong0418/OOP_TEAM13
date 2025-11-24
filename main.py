import pygame
import sys
from pygame.locals import *
from player import Player
from map import MapManager

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

# GPA & HP 기본값
gpa = 0.0
hp = 3

# 맵 매니저 생성
map_manager = MapManager(window_W, window_H)

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
    pygame.draw.rect(screen, (255,255,255), rect)
    pygame.draw.rect(screen, (0,0,0), rect, 3)
    txt = FONT.render(text, True, (0,0,0))
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
            if game_state == "play" and map_manager.is_playing:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # 마우스 클릭 입력 (버튼 클릭)
        elif event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos

            # ----------- 메인 화면 -----------
            if game_state == "menu":

                if btn_explain.collidepoint(mx, my):
                    game_state = "howto"

                elif btn_start.collidepoint(mx, my):
                    game_state = "play"
                    map_manager.reset()
                    gpa = 0.0
                    hp = 3

            # ----------- 게임설명 화면 -----------
            elif game_state == "howto":
                if btn_start_howto.collidepoint(mx, my):
                    game_state = "play"
                    map_manager.reset()
                    gpa = 0.0
                    hp = 3

    # ================= 화면 그리기 =================
    if game_state == "menu":
        screen.blit(Main_Buildging, (0, 0))
        title = FONT_TITLE.render("학교 가BOO자고!", True, (0,0,0))
        screen.blit(title, (260, 40))
        draw_button(btn_explain, "게임설명")
        draw_button(btn_start, "게임시작")

    elif game_state == "howto":
        screen.blit(Howto_Building, (0, 0))
        draw_button(btn_start_howto, "게임시작")

    elif game_state == "play":

        # 1) 맵 업데이트 (GPA/HP 조건 판단 포함)
        map_manager.update(gpa, hp)

        # 2) 맵 그리고 엔딩 상태면 알아서 그려줌
        map_manager.draw(screen)

        # 3) 진행 중인 경우에만 플레이어 동작 가능
        if map_manager.is_playing:
            keys = pygame.key.get_pressed()
            player.handle_input(keys)
            player.update()
            player.draw(screen)

        # 4) (참고) GPA & HP를 화면에 띄우려면 아래 추가 가능
        gpa_text = FONT.render(f"GPA: {gpa:.2f}", True, (0,0,0))
        hp_text = FONT.render(f"HP: {hp}", True, (0,0,0))
        screen.blit(gpa_text, (20, 20))
        screen.blit(hp_text, (20, 60))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()