# main.py

import pygame
import sys

from game import Game
from board import GRID_SIZE

import ui
from effects import EffectManager

pygame.init()


# ==================================================
# WINDOW
# ==================================================

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Block Blast"
)

clock = pygame.time.Clock()


# ==================================================
# UI INIT
# ==================================================

ui.init_ui()


# ==================================================
# GAME
# ==================================================

game = Game()

effects = EffectManager()


# ==================================================
# BOARD SETTINGS
# ==================================================

CELL_SIZE = 60

BOARD_X = 50
BOARD_Y = 50

BOARD_WIDTH = GRID_SIZE * CELL_SIZE
BOARD_HEIGHT = GRID_SIZE * CELL_SIZE


# ==================================================
# COLORS
# ==================================================

BACKGROUND = (
    20,
    22,
    35
)

GRID_COLOR = (
    45,
    50,
    70
)

EMPTY_CELL = (
    35,
    40,
    55
)


# ==================================================
# DRAGGING
# ==================================================

dragging_piece = None

drag_piece_index = -1

drag_offset_x = 0
drag_offset_y = 0

mouse_x = 0
mouse_y = 0


# ==================================================
# HELPERS
# ==================================================

def board_cell_from_mouse():

    mx, my = pygame.mouse.get_pos()

    gx = (
        mx - BOARD_X
    ) // CELL_SIZE

    gy = (
        my - BOARD_Y
    ) // CELL_SIZE

    return gx, gy


def inside_board(
    gx,
    gy
):

    return (
        0 <= gx < GRID_SIZE and
        0 <= gy < GRID_SIZE
    )


# ==================================================
# BOARD DRAWING
# ==================================================

def draw_board():

    for y in range(GRID_SIZE):

        for x in range(GRID_SIZE):

            rect = pygame.Rect(

                BOARD_X +
                x * CELL_SIZE,

                BOARD_Y +
                y * CELL_SIZE,

                CELL_SIZE - 2,
                CELL_SIZE - 2
            )

            pygame.draw.rect(
                screen,
                EMPTY_CELL,
                rect,
                border_radius=8
            )

            value = game.board.grid[y][x]

            if value != 0:

                pygame.draw.rect(
                    screen,
                    value,
                    rect.inflate(
                        -8,
                        -8
                    ),
                    border_radius=8
                )


# ==================================================
# BOARD OUTLINE
# ==================================================

def draw_board_outline():

    rect = pygame.Rect(

        BOARD_X - 5,
        BOARD_Y - 5,

        BOARD_WIDTH + 10,
        BOARD_HEIGHT + 10
    )

    pygame.draw.rect(
        screen,
        GRID_COLOR,
        rect,
        3,
        border_radius=12
    )


# ==================================================
# PIECE DRAWING
# ==================================================

def draw_drag_piece():

    global dragging_piece

    if dragging_piece is None:
        return

    mx, my = pygame.mouse.get_pos()

    px = mx - drag_offset_x
    py = my - drag_offset_y

    ui.draw_piece(
        screen,
        dragging_piece,
        px,
        py,
        30
    )


# ==================================================
# PLACEMENT PREVIEW
# ==================================================

def draw_preview():

    if dragging_piece is None:
        return

    gx, gy = board_cell_from_mouse()

    preview_cells = []

    valid = game.board.can_place(
        dragging_piece,
        gx,
        gy
    )

    for px, py in dragging_piece.shape:

        preview_cells.append(
            (
                gx + px,
                gy + py
            )
        )

    ui.draw_highlight(
        screen,
        preview_cells,
        CELL_SIZE,
        BOARD_X,
        BOARD_Y,
        valid
    )


# ==================================================
# SCORE EFFECTS
# ==================================================

def trigger_clear_effect(
    lines,
    score
):

    if lines <= 0:
        return

    effects.spawn_score_text(
        f"+{score}",
        350,
        100,
        (255,255,255)
    )

    effects.spawn_particles(
        300,
        250,
        (255,220,60),
        50
    )

    effects.shake_screen(
        8,
        15
    )


# ==================================================
# RESTART BUTTON
# ==================================================

restart_button = restart_button = ui.Button(650, 320, 180, 55, "Restart")

# ==================================================
# PIECE TRAY HITBOXES
# ==================================================

def get_tray_piece_rect(
    piece,
    index
):

    positions = [
        150,
        410,
        670
    ]

    cell_size = 24

    width = (
        piece.get_width()
        * cell_size
    )

    height = (
        piece.get_height()
        * cell_size
    )

    x = positions[index]
    y = 600

    return pygame.Rect(
        x,
        y,
        width,
        height
    )


# ==================================================
# PICKUP PIECE
# ==================================================

def try_pickup_piece():

    global dragging_piece
    global drag_piece_index

    global drag_offset_x
    global drag_offset_y

    mx, my = pygame.mouse.get_pos()

    for i, piece in enumerate(
        game.pieces
    ):

        if piece is None:
            continue

        rect = get_tray_piece_rect(
            piece,
            i
        )

        if rect.collidepoint(
            mx,
            my
        ):

            dragging_piece = piece

            drag_piece_index = i

            drag_offset_x = (
                mx - rect.x
            )

            drag_offset_y = (
                my - rect.y
            )

            return True

    return False


# ==================================================
# PLACE PIECE
# ==================================================

def try_place_piece():

    global dragging_piece
    global drag_piece_index

    if dragging_piece is None:
        return

    gx, gy = board_cell_from_mouse()

    if not game.board.can_place(
        dragging_piece,
        gx,
        gy
    ):

        dragging_piece = None
        drag_piece_index = -1

        return

    result = game.place_piece(
        drag_piece_index,
        gx,
        gy
    )

    if result:

        score_gain = (
            result[
                "score_gained"
            ]
        )

        lines = (
            result[
                "lines_cleared"
            ]
        )

        combo = (
            result[
                "combo"
            ]
        )

        trigger_clear_effect(
            lines,
            score_gain
        )

        if combo > 1:

            effects.spawn_combo(
                combo
            )

    dragging_piece = None
    drag_piece_index = -1


# ==================================================
# INPUT
# ==================================================

def handle_mouse_down():

    if game.game_over:
        return

    try_pickup_piece()


def handle_mouse_up():

    if dragging_piece:

        try_place_piece()


# ==================================================
# KEYBOARD
# ==================================================

def handle_key_down(
    event
):

    if event.key == pygame.K_r:

        game.restart()

    elif event.key == pygame.K_u:

        game.undo()


# ==================================================
# EVENT HANDLER
# ==================================================

def handle_events():

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            handle_key_down(
                event
            )

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                handle_mouse_down()

                if restart_button.clicked(
                    event
                ):

                    game.restart()

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                handle_mouse_up()
# ==================================================
# MAIN LOOP
# ==================================================

tick = 0

while True:

    clock.tick(60)

    tick += 1

    # ------------------------------
    # EVENTS
    # ------------------------------

    handle_events()

    # ------------------------------
    # UPDATE
    # ------------------------------

    effects.update()

    restart_button.update()

    # ------------------------------
    # SHAKE OFFSET
    # ------------------------------

    shake_x, shake_y = (
        effects.get_shake_offset()
    )

    # ------------------------------
    # BACKGROUND
    # ------------------------------

    ui.draw_background(
        screen,
        tick
    )

    # ==================================================
    # GAME LAYER
    # ==================================================

    game_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    # ------------------------------
    # BOARD
    # ------------------------------

    original_screen = screen
    screen = game_surface

    draw_board_outline()

    draw_board()

    draw_preview()

    # ------------------------------
    # UI
    # ------------------------------

    ui.draw_score_panel(
        screen,
        game.score,
        game.high_score
    )

    ui.draw_combo_bar(
        screen,
        game.combo
    )

    ui.draw_piece_tray(
        screen,
        game.pieces
    )

    restart_button.draw(
        screen
    )

    # ------------------------------
    # EFFECTS
    # ------------------------------

    effects.draw(
        screen,
        ui.MEDIUM_FONT,
        WIDTH
    )

    # ------------------------------
    # DRAGGED PIECE
    # ------------------------------

    draw_drag_piece()

    # ------------------------------
    # GAME OVER
    # ------------------------------

    if game.game_over:

        ui.draw_game_over(
            screen,
            game.score,
            game.high_score
        )

    # ==================================================
    # APPLY SHAKE
    # ==================================================

    screen = original_screen

    screen.blit(
        game_surface,
        (
            shake_x,
            shake_y
        )
    )

    # ==================================================
    # DEBUG INFO
    # ==================================================

    ui.draw_text(
        screen,
        f"FPS: {int(clock.get_fps())}",
        ui.SMALL_FONT,
        (150,150,150),
        15,
        15
    )

    ui.draw_text(
        screen,
        "R = Restart",
        ui.SMALL_FONT,
        (180,180,180),
        15,
        40
    )

    ui.draw_text(
        screen,
        "U = Undo",
        ui.SMALL_FONT,
        (180,180,180),
        15,
        65
    )

    # ==================================================
    # DISPLAY
    # ==================================================

    pygame.display.flip()