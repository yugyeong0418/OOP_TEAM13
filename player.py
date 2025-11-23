import pygame

class Player:
    def __init__(self, x, y, image_path, screen_width, ground_level):
        # 크기 (147 × 220)
        self.width = 147
        self.height = 220

        # 초기 위치
        self.x = x
        self.y = y

        # 속도
        self.vx = 0
        self.vy = 0

        # 물리 요소
        self.gravity = 1
        self.jump_power = -22
        self.on_ground = True

        # 이동 가능한 범위 (화면 절반까지만)
        self.left_limit = 0 + 20
        self.right_limit = screen_width // 2 - self.width - 20

        # 바닥 Y좌표
        self.ground_y = ground_level

        # 이미지 로드
        self.image = pygame.image.load("OOP_TEAM13/image/boo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # 충돌 박스
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # 키 입력 처리
    def handle_input(self, keys):
        self.vx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -8
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = 8

    # 점프 처리
    def jump(self):
        if self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

    # 물리 업데이트
    def update(self):
        # 좌우 이동
        self.rect.x += self.vx

        # 화면 절반까지만 이동 제한
        if self.rect.x < self.left_limit:
            self.rect.x = self.left_limit

        if self.rect.x > self.right_limit:
            self.rect.x = self.right_limit

        # 중력 적용
        self.vy += self.gravity
        self.rect.y += self.vy

        # 바닥 충돌 처리
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vy = 0
            self.on_ground = True

    # 부 그리기
    def draw(self, screen):
        screen.blit(self.image, self.rect)
