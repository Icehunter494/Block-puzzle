# game.py

from board import Board
from pieces import generate_piece_set


class Game:

    def __init__(self):

        self.board = Board()

        self.score = 0
        self.high_score = 0

        self.combo = 0
        self.max_combo = 0

        self.turns = 0

        self.total_lines_cleared = 0
        self.total_blocks_placed = 0

        self.game_over = False

        self.pieces = generate_piece_set()

        self.last_board = None
        self.last_score = 0
        self.last_combo = 0

    # =====================================
    # SAVE STATE FOR UNDO
    # =====================================

    def save_state(self):

        self.last_board = self.board.copy_grid()
        self.last_score = self.score
        self.last_combo = self.combo

    # =====================================
    # UNDO
    # =====================================

    def undo(self):

        if self.last_board is None:
            return False

        self.board.restore_grid(self.last_board)

        self.score = self.last_score
        self.combo = self.last_combo

        self.last_board = None

        return True

    # =====================================
    # SCORE
    # =====================================

    def calculate_score(
        self,
        blocks_placed,
        lines_cleared
    ):

        score = blocks_placed * 10

        if lines_cleared == 1:
            score += 100

        elif lines_cleared == 2:
            score += 300

        elif lines_cleared == 3:
            score += 600

        elif lines_cleared == 4:
            score += 1000

        elif lines_cleared >= 5:
            score += 1500 + (
                (lines_cleared - 5) * 300
            )

        combo_bonus = int(
            score * (self.combo * 0.15)
        )

        score += combo_bonus

        return score

    # =====================================
    # COMBO
    # =====================================

    def update_combo(
        self,
        lines_cleared
    ):

        if lines_cleared > 0:

            self.combo += 1

            if self.combo > self.max_combo:
                self.max_combo = self.combo

        else:

            self.combo = 0

    # =====================================
    # REFILL TRAY
    # =====================================

    def refill_pieces(self):

        empty = True

        for piece in self.pieces:

            if piece is not None:
                empty = False

        if empty:

            self.pieces = generate_piece_set()

    # =====================================
    # GAME OVER CHECK
    # =====================================

    def check_game_over(self):

        if self.board.has_valid_move(
            self.pieces
        ):
            return False

        self.game_over = True
        return True

    # =====================================
    # REMOVE PIECE FROM TRAY
    # =====================================

    def consume_piece(
        self,
        index
    ):

        if (
            0 <= index <
            len(self.pieces)
        ):

            self.pieces[index] = None

    # =====================================
    # PLACE PIECE
    # =====================================

    def place_piece(
        self,
        piece_index,
        grid_x,
        grid_y
    ):

        if self.game_over:
            return False

        if (
            piece_index < 0 or
            piece_index >= len(self.pieces)
        ):
            return False

        piece = self.pieces[piece_index]

        if piece is None:
            return False

        if not self.board.can_place(
            piece,
            grid_x,
            grid_y
        ):
            return False

        self.save_state()

        self.board.place_piece(
            piece,
            grid_x,
            grid_y
        )

        blocks_placed = piece.block_count()

        self.total_blocks_placed += (
            blocks_placed
        )

        lines_cleared = (
            self.board.clear_completed_lines()
        )

        self.total_lines_cleared += (
            lines_cleared
        )

        self.update_combo(
            lines_cleared
        )

        gained_score = (
            self.calculate_score(
                blocks_placed,
                lines_cleared
            )
        )

        self.score += gained_score

        if self.score > self.high_score:

            self.high_score = self.score

        self.consume_piece(
            piece_index
        )

        self.refill_pieces()

        self.turns += 1

        self.check_game_over()

        return {
            "success": True,
            "score_gained": gained_score,
            "lines_cleared": lines_cleared,
            "combo": self.combo
        }

    # =====================================
    # RESTART
    # =====================================

    def restart(self):

        self.board = Board()

        self.score = 0

        self.combo = 0
        self.max_combo = 0

        self.turns = 0

        self.total_lines_cleared = 0
        self.total_blocks_placed = 0

        self.game_over = False

        self.pieces = generate_piece_set()

        self.last_board = None

    # =====================================
    # STATS
    # =====================================

    def get_stats(self):

        return {

            "score":
                self.score,

            "high_score":
                self.high_score,

            "combo":
                self.combo,

            "max_combo":
                self.max_combo,

            "turns":
                self.turns,

            "lines":
                self.total_lines_cleared,

            "blocks":
                self.total_blocks_placed,

            "game_over":
                self.game_over
        }