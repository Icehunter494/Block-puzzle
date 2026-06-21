# ui.py

import pygame
import math


# ==========================================
# FONTS
# ==========================================

TITLE_FONT = None
LARGE_FONT = None
MEDIUM_FONT = None
SMALL_FONT = None


def init_ui():

    global TITLE_FONT
    global LARGE_FONT
    global MEDIUM_FONT
    global SMALL_FONT

    TITLE_FONT = pygame.font.SysFont(
        "arial",
        64,
        bold=True
    )

    LARGE_FONT = pygame.font.SysFont(
        "arial",
        40,
        bold=True
    )

    MEDIUM_FONT = pygame.font.SysFont(
        "arial",
        28
    )

    SMALL_FONT = pygame.font.SysFont(
        "arial",
        20
    )


# ==========================================
# DRAW TEXT
# ==========================================

def draw_text(
    surface,
    text,
    font,
    color,
    x,
    y,
    center=False
):

    img = font.render(
        str(text),
        True,
        color
    )

    rect = img.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(img, rect)


# ==========================================
# ROUNDED PANEL
# ==========================================

def draw_panel(
    surface,
    rect,
    color=(35,35,50),
    border=(60,60,90)
):

    pygame.draw.rect(
        surface,
        color,
        rect,
        border_radius=15
    )

    pygame.draw.rect(
        surface,
        border,
        rect,
        3,
        border_radius=15
    )


# ==========================================
# BUTTON
# ==========================================

class Button:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text

        self.hover = False

        self.scale = 1.0

    def update(self):

        mouse = pygame.mouse.get_pos()

        self.hover = self.rect.collidepoint(
            mouse
        )

        target = 1.08 if self.hover else 1.0

        self.scale += (
            target - self.scale
        ) * 0.15

    def clicked(
        self,
        event
    ):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                return self.hover

        return False

    def draw(
        self,
        surface
    ):

        color = (
            (90,140,255)
            if self.hover
            else
            (70,110,220)
        )

        w = int(
            self.rect.width *
            self.scale
        )

        h = int(
            self.rect.height *
            self.scale
        )

        rect = pygame.Rect(
            self.rect.centerx - w // 2,
            self.rect.centery - h // 2,
            w,
            h
        )

        pygame.draw.rect(
            surface,
            color,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            surface,
            (255,255,255),
            rect,
            2,
            border_radius=12
        )

        draw_text(
            surface,
            self.text,
            MEDIUM_FONT,
            (255,255,255),
            rect.centerx,
            rect.centery,
            center=True
        )


# ==========================================
# SCORE PANEL
# ==========================================

def draw_score_panel(
    surface,
    score,
    high_score
):

    panel = pygame.Rect(
        620,
        40,
        240,
        120
    )

    draw_panel(
        surface,
        panel
    )

    draw_text(
        surface,
        "SCORE",
        SMALL_FONT,
        (180,180,220),
        panel.centerx,
        20 + panel.y,
        center=True
    )

    draw_text(
        surface,
        score,
        LARGE_FONT,
        (255,255,255),
        panel.centerx,
        panel.y + 50,
        center=True
    )

    draw_text(
        surface,
        f"BEST {high_score}",
        SMALL_FONT,
        (120,255,120),
        panel.centerx,
        panel.y + 95,
        center=True
    )


# ==========================================
# COMBO BAR
# ==========================================

def draw_combo_bar(
    surface,
    combo
):

    panel = pygame.Rect(
        620,
        190,
        240,
        90
    )

    draw_panel(
        surface,
        panel
    )

    draw_text(
        surface,
        f"Combo x{combo}",
        MEDIUM_FONT,
        (255,220,60),
        panel.centerx,
        panel.y + 18,
        center=True
    )

    width = min(
        200,
        combo * 20
    )

    pygame.draw.rect(
        surface,
        (50,50,60),
        (
            panel.x + 20,
            panel.y + 55,
            200,
            18
        ),
        border_radius=10
    )

    pygame.draw.rect(
        surface,
        (255,180,60),
        (
            panel.x + 20,
            panel.y + 55,
            width,
            18
        ),
        border_radius=10
    )


# ==========================================
# PIECE DRAWING
# ==========================================

def draw_piece(
    surface,
    piece,
    px,
    py,
    cell_size
):

    color = piece.color

    for bx, by in piece.shape:

        rect = pygame.Rect(

            px + bx * cell_size,
            py + by * cell_size,

            cell_size - 2,
            cell_size - 2
        )

        pygame.draw.rect(
            surface,
            color,
            rect,
            border_radius=8
        )

        pygame.draw.rect(
            surface,
            (255,255,255),
            rect,
            2,
            border_radius=8
        )


# ==========================================
# PIECE TRAY
# ==========================================

def draw_piece_tray(
    surface,
    pieces
):

    panel = pygame.Rect(
        40,
        575,
        820,
        110
    )

    draw_panel(
        surface,
        panel
    )

    positions = [
        150,
        410,
        670
    ]

    for i, piece in enumerate(pieces):

        if piece is None:
            continue

        draw_piece(
            surface,
            piece,
            positions[i],
            600,
            24
        )


# ==========================================
# BOARD HIGHLIGHT
# ==========================================

def draw_highlight(
    surface,
    cells,
    cell_size,
    board_x,
    board_y,
    valid=True
):

    color = (
        (80,255,120)
        if valid
        else
        (255,80,80)
    )

    for x, y in cells:

        rect = pygame.Rect(
            board_x + x * cell_size,
            board_y + y * cell_size,
            cell_size,
            cell_size
        )

        pygame.draw.rect(
            surface,
            color,
            rect,
            4,
            border_radius=8
        )


# ==========================================
# GAME OVER SCREEN
# ==========================================

def draw_game_over(
    surface,
    score,
    best
):

    overlay = pygame.Surface(
        surface.get_size(),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0,0,0,180)
    )

    surface.blit(
        overlay,
        (0,0)
    )

    draw_text(
        surface,
        "GAME OVER",
        TITLE_FONT,
        (255,255,255),
        surface.get_width()//2,
        200,
        center=True
    )

    draw_text(
        surface,
        f"Score: {score}",
        LARGE_FONT,
        (255,255,255),
        surface.get_width()//2,
        300,
        center=True
    )

    draw_text(
        surface,
        f"Best: {best}",
        MEDIUM_FONT,
        (120,255,120),
        surface.get_width()//2,
        360,
        center=True
    )


# ==========================================
# BACKGROUND
# ==========================================

def draw_background(
    surface,
    tick
):

    w = surface.get_width()
    h = surface.get_height()

    for y in range(h):

        wave = int(
            math.sin(
                (y + tick) * 0.01
            ) * 8
        )

        color = (
            20 + wave,
            22 + wave,
            35 + wave
        )

        pygame.draw.line(
            surface,
            color,
            (0,y),
            (w,y)
        )