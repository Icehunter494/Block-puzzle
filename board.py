# board.py

GRID_SIZE = 8


class Board:

    def __init__(self):

        self.grid = [
            [0 for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]

    # ==========================================
    # BASIC HELPERS
    # ==========================================

    def clear(self):

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                self.grid[y][x] = 0

    def is_inside(self, x, y):

        return (
            0 <= x < GRID_SIZE and
            0 <= y < GRID_SIZE
        )

    # ==========================================
    # PIECE PLACEMENT
    # ==========================================

    def can_place(
        self,
        piece,
        gx,
        gy
    ):

        for px, py in piece.shape:

            x = gx + px
            y = gy + py

            if not self.is_inside(x, y):
                return False

            if self.grid[y][x] != 0:
                return False

        return True

    def place_piece(
        self,
        piece,
        gx,
        gy
    ):

        for px, py in piece.shape:

            x = gx + px
            y = gy + py

            self.grid[y][x] = piece.color

    # ==========================================
    # LINE DETECTION
    # ==========================================

    def row_full(self, row):

        return all(
            self.grid[row][x] != 0
            for x in range(GRID_SIZE)
        )

    def column_full(self, col):

        return all(
            self.grid[y][col] != 0
            for y in range(GRID_SIZE)
        )

    def get_completed_rows(self):

        rows = []

        for y in range(GRID_SIZE):

            if self.row_full(y):
                rows.append(y)

        return rows

    def get_completed_columns(self):

        cols = []

        for x in range(GRID_SIZE):

            if self.column_full(x):
                cols.append(x)

        return cols

    # ==========================================
    # CLEAR LINES
    # ==========================================

    def clear_completed_lines(self):

        rows = self.get_completed_rows()
        cols = self.get_completed_columns()

        for row in rows:

            for x in range(GRID_SIZE):
                self.grid[row][x] = 0

        for col in cols:

            for y in range(GRID_SIZE):
                self.grid[y][col] = 0

        return len(rows) + len(cols)

    # ==========================================
    # GAME OVER CHECKING
    # ==========================================

    def can_place_anywhere(
        self,
        piece
    ):

        for y in range(GRID_SIZE):

            for x in range(GRID_SIZE):

                if self.can_place(
                    piece,
                    x,
                    y
                ):
                    return True

        return False

    def has_valid_move(
        self,
        pieces
    ):

        for piece in pieces:

            if piece is None:
                continue

            if self.can_place_anywhere(
                piece
            ):
                return True

        return False

    # ==========================================
    # POWERUP SUPPORT
    # ==========================================

    def remove_cell(
        self,
        x,
        y
    ):

        if self.is_inside(x, y):

            self.grid[y][x] = 0

    def clear_row(
        self,
        row
    ):

        removed = 0

        for x in range(GRID_SIZE):

            if self.grid[row][x] != 0:

                self.grid[row][x] = 0
                removed += 1

        return removed

    def clear_column(
        self,
        col
    ):

        removed = 0

        for y in range(GRID_SIZE):

            if self.grid[y][col] != 0:

                self.grid[y][col] = 0
                removed += 1

        return removed

    def remove_area(
        self,
        center_x,
        center_y,
        radius=1
    ):

        removed = 0

        for dy in range(
            -radius,
            radius + 1
        ):

            for dx in range(
                -radius,
                radius + 1
            ):

                x = center_x + dx
                y = center_y + dy

                if self.is_inside(x, y):

                    if self.grid[y][x] != 0:

                        self.grid[y][x] = 0
                        removed += 1

        return removed

    # ==========================================
    # SAVE / UNDO
    # ==========================================

    def copy_grid(self):

        return [
            row.copy()
            for row in self.grid
        ]

    def restore_grid(
        self,
        saved_grid
    ):

        self.grid = [
            row.copy()
            for row in saved_grid
        ]

    # ==========================================
    # DEBUG / STATS
    # ==========================================

    def count_filled(self):

        total = 0

        for row in self.grid:

            for cell in row:

                if cell != 0:
                    total += 1

        return total

    def board_full(self):

        return (
            self.count_filled()
            ==
            GRID_SIZE * GRID_SIZE
        )