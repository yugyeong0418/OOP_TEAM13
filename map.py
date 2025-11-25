import pygame

class MapManager:
    """
    맵 진행 + 분기 + 엔딩(클리어/재수강/기숙사)을 모두 관리하는 클래스

    맵 구성:
      - baeknyon      : 백년관
      - library       : 도서관
      - student       : 학생회관
      - myeongsu      : 명수당 (특수 조건으로 진입)
      - gyoyang       : 교양관
      - classroom     : 강의실

    엔딩 전용 맵:
      - jaesugang     : 재수강
      - dorm          : 기숙사
    """

    def __init__(self, window_W, window_H, font_path="DNFBitBitTTF.ttf",
                 map_duration_ms=30000):
        self.window_W = window_W
        self.window_H = window_H
        self.duration = map_duration_ms  # 일반 맵 30초

        # ---------- 폰트 ----------
        self.font = pygame.font.Font(font_path, 40)
        self.font_big = pygame.font.Font(font_path, 80)

        # ---------- 이미지 로드 ----------
        self.images = {
            "baeknyon":   self._load("OOP_TEAM13/image/Main_Building.png"),
            "library":    self._load("OOP_TEAM13/image/University_Library.png"),
            "student":    self._load("OOP_TEAM13/image/Student_Hall.png"),
            "myeongsu":   self._load("OOP_TEAM13/image/Bonus_Stage.png"),
            "gyoyang":    self._load("OOP_TEAM13/image/Liberal_Arts_Building.png"),
            "classroom":  self._load("OOP_TEAM13/image/강의실.png"),
            "jaesugang":  self._load("OOP_TEAM13/image/재수강.png"),
            "dorm":       self._load("OOP_TEAM13/image/기숙사.png"),
        }

        # ---------- 진행 상태 ----------
        self.current_stage = "baeknyon"
        self.stage_start_ticks = None
        self.state = "playing"  # playing / ending_clear / ending_retake / ending_sleep

        # ---------- 아이템 상태 (명수당 조건) ----------
        self.has_B = False
        self.has_O_library = False
        self.has_O_student = False

        # ---------- 명수당 ----------
        self.myeongsu_duration = 10_000  # 10초

        # ---------- 엔딩 처리 ----------
        self.ending_start_ticks = None
        self.ENDING_SHOW_TIME = 3000  # 3초 유지
        self.ENDING_FADE_TIME = 2000  # 2초 페이드아웃

        # 엔딩 학점 표시용
        self.last_gpa = 0.0


    # -------------------------------------------------
    # 이미지 로드
    # -------------------------------------------------
    def _load(self, path):
        img = pygame.image.load(path).convert()
        img = pygame.transform.scale(img, (self.window_W, self.window_H))
        return img


    # -------------------------------------------------
    # 아이템 획득 함수 (main.py에서 호출)
    # -------------------------------------------------
    def collect_B(self):
        self.has_B = True

    def collect_O_library(self):
        self.has_O_library = True

    def collect_O_student(self):
        self.has_O_student = True


    # -------------------------------------------------
    # 게임 재시작
    # -------------------------------------------------
    def reset(self):
        self.current_stage = "baeknyon"
        self.stage_start_ticks = None
        self.state = "playing"
        self.entered_myeongsu = False

        # 아이템 상태 초기화
        self.has_B = False
        self.has_O_library = False
        self.has_O_student = False

        self.ending_start_ticks = None


    # -------------------------------------------------
    # 학점 텍스트 생성
    # -------------------------------------------------
    def _grade_text(self):
        g = self.last_gpa
        if g > 4.5: g = 4.5

        if g >= 4.5:
            return f"{g:.2f}학점 A+ 입니다"
        elif g >= 4.0:
            return f"{g:.2f}학점 A 입니다"
        elif g >= 3.5:
            return f"{g:.2f}학점 B+ 입니다"
        elif g >= 3.0:
            return f"{g:.2f}학점 B 입니다"
        else:
            return f"{g:.2f}학점입니다"


    # -------------------------------------------------
    # 맵 진행 로직
    # -------------------------------------------------
    def update(self, gpa: float, hp: int):
        if self.state != "playing":
            return

        now = pygame.time.get_ticks()
        if self.stage_start_ticks is None:
            self.stage_start_ticks = now

        elapsed = now - self.stage_start_ticks
        self.last_gpa = gpa  # 엔딩에 사용

        # ------ 백년관 ------
        if self.current_stage == "baeknyon":
            if elapsed >= self.duration:
                self.current_stage = "library"
                self.stage_start_ticks = now

        # ------ 도서관 ------
        elif self.current_stage == "library":
            if elapsed >= self.duration:
                self.current_stage = "student"
                self.stage_start_ticks = now

        # ------ 학생회관 ------
        elif self.current_stage == "student":
            # B/O/O 모두 모으면 명수당
            if self.has_B and self.has_O_library and self.has_O_student:
                self.current_stage = "myeongsu"
                self.stage_start_ticks = now

            # 30초 지나면 교양관
            elif elapsed >= self.duration:
                self.current_stage = "gyoyang"
                self.stage_start_ticks = now

        # ------ 명수당 (10초) ------
        elif self.current_stage == "myeongsu":
            if elapsed >= self.myeongsu_duration:
                self.current_stage = "gyoyang"
                self.stage_start_ticks = now

        # ------ 교양관 ------
        elif self.current_stage == "gyoyang":
            # 죽으면 기숙사 엔딩
            if hp <= 0:
                self.state = "ending_sleep"
                self.ending_start_ticks = pygame.time.get_ticks()
                return

            # 30초 버티면 강의실 → GPA 판정
            if elapsed >= self.duration:
                self.current_stage = "classroom"
                self.stage_start_ticks = now

                if gpa <= 2.5:
                    self.state = "ending_retake"
                else:
                    self.state = "ending_clear"

                self.ending_start_ticks = pygame.time.get_ticks()


    # -------------------------------------------------
    # 그리기
    # -------------------------------------------------
    def draw(self, screen):
        # 플레이 중이면 현재 맵만 출력
        if self.state == "playing":
            screen.blit(self.images[self.current_stage], (0, 0))
            return


        # ------ 재수강 엔딩 ------
        if self.state == "ending_retake":
            screen.blit(self.images["jaesugang"], (0, 0))

            t1 = self.font_big.render("재수강...", True, (255, 255, 255))
            t2 = self.font.render("BOO...는 재수강을 해야합니다...", True, (255, 255, 255))

            screen.blit(t1, t1.get_rect(center=(self.window_W//2, self.window_H//2 - 40)))
            screen.blit(t2, t2.get_rect(center=(self.window_W//2, self.window_H//2 + 40)))
            return


        # ------ 기숙사 엔딩 ------
        if self.state == "ending_sleep":
            screen.blit(self.images["dorm"], (0, 0))

            t1 = self.font_big.render("잠...", True, (255, 255, 255))
            t2 = self.font.render("BOO...는 자야합니다...", True, (255, 255, 255))

            screen.blit(t1, t1.get_rect(center=(self.window_W//2, self.window_H//2 - 40)))
            screen.blit(t2, t2.get_rect(center=(self.window_W//2, self.window_H//2 + 40)))
            return


        # ------ 클리어 엔딩 (강의실) ------
        if self.state == "ending_clear":
            now = pygame.time.get_ticks()
            elapsed = now - self.ending_start_ticks

            # 1) 강의실 화면 띄우기
            screen.blit(self.images["classroom"], (0, 0))

            # 2) 페이드아웃
            if elapsed > self.ENDING_SHOW_TIME:
                fade_elapsed = elapsed - self.ENDING_SHOW_TIME
                alpha = min(255, int(255 * (fade_elapsed / self.ENDING_FADE_TIME)))

                fade = pygame.Surface((self.window_W, self.window_H))
                fade.fill((0, 0, 0))
                fade.set_alpha(alpha)
                screen.blit(fade, (0, 0))

            # 3) 텍스트
            t1 = self.font_big.render("클리어!", True, (255, 255, 255))
            t2 = self.font.render("BOO가 강의실에 도착 했습니다!", True, (255, 255, 255))
            t3 = self.font.render(self._grade_text(), True, (255, 255, 0))

            screen.blit(t1, t1.get_rect(center=(self.window_W//2, self.window_H//2 - 60)))
            screen.blit(t2, t2.get_rect(center=(self.window_W//2, self.window_H//2)))
            screen.blit(t3, t3.get_rect(center=(self.window_W//2, self.window_H//2 + 60)))
            return


    # -------------------------------------------------
    @property
    def is_playing(self):
        return self.state == "playing"

    @property
    def is_finished(self):
        return self.state != "playing"