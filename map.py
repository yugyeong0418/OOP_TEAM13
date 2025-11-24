import pygame

class MapManager:
    """
    맵 진행 + 분기 + 엔딩(클리어/재수강/기숙사)을 모두 관리하는 클래스

    맵 구성:
      - baeknyon      : 백년관
      - library       : 도서관
      - student       : 학생회관
      - myeongsu      : 명수당 (학생회관에서 GPA>=2.0일 때 진입)
      - gyoyang       : 교양관
      - classroom     : 강의실 (도착 = 클리어)

    특수 맵:
      - jaesugang     : 재수강 화면
      - dorm          : 기숙사 화면

    상태(state):
      - "playing"         : 일반 진행중
      - "ending_clear"    : 클리어 엔딩(강의실)
      - "ending_retake"   : 재수강 엔딩
      - "ending_sleep"    : 기숙사 엔딩
    """

    def __init__(self, window_W, window_H, font_path="DNFBitBitTTF.ttf",
                 map_duration_ms=30000):
        self.window_W = window_W
        self.window_H = window_H
        self.duration = map_duration_ms  # 맵 하나당 30초

        # ---------- 폰트 ----------
        self.font = pygame.font.Font(font_path, 40)
        self.font_big = pygame.font.Font(font_path, 80)

        # ---------- 맵 이미지 로드 ----------
        self.images = {
            "baeknyon":   self._load("OOP_TEAM13/image/Main_Building.png"),
            "library":    self._load("OOP_TEAM13/image/University_Library.png"),
            "student":    self._load("OOP_TEAM13/image/Student_Hall.png"),
            "myeongsu":   self._load("OOP_TEAM13/image/Bonus_Stage.png"),
            "gyoyang":    self._load("OOP_TEAM13/image/Liberal_Arts_Building.png"),
            "classroom":  self._load("OOP_TEAM13/image/강의실.png"),
            # 엔딩 전용 배경
            "jaesugang":  self._load("OOP_TEAM13/image/재수강.png"),
            "dorm":       self._load("OOP_TEAM13/image/기숙사.png"),
        }

        # ---------- 진행 상태 ----------
        self.current_stage = "baeknyon"   # 시작 맵
        self.stage_start_ticks = None     # 해당 맵 시작 시간
        self.state = "playing"           # playing / ending_clear / ending_retake / ending_sleep

        # 명수당 진입 여부
        self.entered_myeongsu = False

        # 엔딩 타이머 (강의실 클리어 연출용)
        self.ending_start_ticks = None
        self.ENDING_SHOW_TIME = 3000   # 강의실 이미지만 3초
        self.ENDING_FADE_TIME = 2000   # 이후 2초 페이드아웃

    # -------------------------------------------------
    # 내부용: 이미지 로드 & 스케일
    # -------------------------------------------------
    def _load(self, path):
        img = pygame.image.load(path).convert()
        img = pygame.transform.scale(img, (self.window_W, self.window_H))
        return img

    # -------------------------------------------------
    # 외부에서 게임 시작 / 재시작 시 호출
    # -------------------------------------------------
    def reset(self):
        self.current_stage = "baeknyon"
        self.stage_start_ticks = None
        self.state = "playing"
        self.entered_myeongsu = False
        self.ending_start_ticks = None

    # -------------------------------------------------
    # 매 프레임 호출: GPA, HP를 보고 다음 맵 / 엔딩으로 이동
    # -------------------------------------------------
    def update(self, gpa: float, hp: int):
        # 엔딩 상태에서는 더 이상 진행 안 함
        if self.state != "playing":
            return

        now = pygame.time.get_ticks()

        # 처음 진입할 때 시작 시간 설정
        if self.stage_start_ticks is None:
            self.stage_start_ticks = now

        elapsed = now - self.stage_start_ticks

        # -------------------- 백년관 → 도서관 --------------------
        if self.current_stage == "baeknyon":
            if elapsed >= self.duration:
                self.current_stage = "library"
                self.stage_start_ticks = now

        # -------------------- 도서관 → 학생회관 --------------------
        elif self.current_stage == "library":
            if elapsed >= self.duration:
                self.current_stage = "student"
                self.stage_start_ticks = now

        # -------------------- 학생회관 로직 --------------------
        elif self.current_stage == "student":

            # GPA 2.0 미만 → 즉시 재수강 엔딩
            if gpa < 2.0:
                self.state = "ending_retake"
                self.ending_start_ticks = pygame.time.get_ticks()
                return

            # GPA 2.0 이상 → 명수당 진입
            elif (gpa >= 2.0) and (not self.entered_myeongsu):
                self.current_stage = "myeongsu"
                self.stage_start_ticks = now
                self.entered_myeongsu = True


        # -------------------- 명수당 로직 --------------------
        elif self.current_stage == "myeongsu":
            # 일정 시간 버틴 뒤 GPA 확인
            if elapsed >= self.duration:
                if gpa >= 3.0:
                    # GPA 3.0 이상 → 교양관
                    self.current_stage = "gyoyang"
                    self.stage_start_ticks = now
                else:
                    # GPA 3.0 미만 → 재수강 엔딩
                    self.state = "ending_retake"
                    self.ending_start_ticks = pygame.time.get_ticks()

        # -------------------- 교양관 로직 --------------------
        elif self.current_stage == "gyoyang":
            # 강의실 도착 전 맵에서 체력 0 이하 → 기숙사 엔딩
            if hp <= 0:
                self.state = "ending_sleep"
                self.ending_start_ticks = pygame.time.get_ticks()
            # 체력 남아 있고 30초 버티면 강의실 클리어
            elif elapsed >= self.duration:
                self.current_stage = "classroom"
                self.stage_start_ticks = now
                self.state = "ending_clear"
                self.ending_start_ticks = pygame.time.get_ticks()

        # classroom은 별도 진행 없음 (엔딩에서 사용)

    # -------------------------------------------------
    # 매 프레임 호출: 현재 상태에 맞는 화면 그리기
    # -------------------------------------------------
    def draw(self, screen):
        # --------- 일반 진행 중 ---------
        if self.state == "playing":
            screen.blit(self.images[self.current_stage], (0, 0))
            return

        # --------- 재수강 엔딩 ---------
        if self.state == "ending_retake":
            screen.blit(self.images["jaesugang"], (0, 0))

            title = self.font_big.render("재수강...", True, (255, 255, 255))
            sub = self.font.render("BOO...는 재수강을 해야합니다...", True, (255, 255, 255))

            screen.blit(title, title.get_rect(center=(self.window_W // 2, self.window_H // 2 - 40)))
            screen.blit(sub, sub.get_rect(center=(self.window_W // 2, self.window_H // 2 + 40)))
            return

        # --------- 기숙사 엔딩 ---------
        if self.state == "ending_sleep":
            screen.blit(self.images["dorm"], (0, 0))

            title = self.font_big.render("잠...", True, (255, 255, 255))
            sub = self.font.render("BOO...는 자야합니다...", True, (255, 255, 255))

            screen.blit(title, title.get_rect(center=(self.window_W // 2, self.window_H // 2 - 40)))
            screen.blit(sub, sub.get_rect(center=(self.window_W // 2, self.window_H // 2 + 40)))
            return

        # --------- 클리어 엔딩 (강의실) ---------
        if self.state == "ending_clear":
            now = pygame.time.get_ticks()
            elapsed = now - self.ending_start_ticks

            # 1) 강의실 이미지 3초
            screen.blit(self.images["classroom"], (0, 0))

            # 2) 이후 2초 페이드아웃
            if elapsed > self.ENDING_SHOW_TIME:
                fade_elapsed = elapsed - self.ENDING_SHOW_TIME
                alpha = min(255, int(255 * (fade_elapsed / self.ENDING_FADE_TIME)))

                fade_surface = pygame.Surface((self.window_W, self.window_H))
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))

            # 3) 텍스트
            title = self.font_big.render("클리어!", True, (255, 255, 255))
            sub = self.font.render("BOO가 강의실에 도착 했습니다!", True, (255, 255, 255))

            screen.blit(title, title.get_rect(center=(self.window_W // 2, self.window_H // 2 - 40)))
            screen.blit(sub, sub.get_rect(center=(self.window_W // 2, self.window_H // 2 + 40)))
            return

    # -------------------------------------------------
    # 편의 프로퍼티
    # -------------------------------------------------
    @property
    def is_playing(self) -> bool:
        return self.state == "playing"

    @property
    def is_finished(self) -> bool:
        return self.state != "playing"

