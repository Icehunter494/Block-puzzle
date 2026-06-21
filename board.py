# board.py

GRID_SIZE = 8


class Board:

    def __init__(self):

        self.grid = []

        for y in range(GRID_SIZE):

            row = []

            for x in range(GRID_SIZE):
                row.append(0)

            self.grid.append(row)

    def clear(self):

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                self.grid[y][x] = 0

    def is_inside(self, x, y):

        return (
            0 <= x < GRID_SIZE and
            0 <= y < GRID_SIZE
        )

    def can_place(self, piece, gx, gy):

        shape = piece["shape"]

        for px, py in shape:

            x = gx + px
            y = gy + py

            if not self.is_inside(x, y):
                return False

            if self.grid[y][x] != 0:
                return False

        return True

    def place_piece(self, piece, gx, gy):

        shape = piece["shape"]

        for px, py in shape:

            x = gx + px
            y = gy + py

            self.grid[y][x] = piece["color"]

    def row_full(self, row):

        for value in self.grid[row]:

            if value == 0:
                return False

        return True

    def column_full(self, col):

        for y in range(GRID_SIZE):

            if self.grid[y][col] == 0:
                return False

        return True

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

    def clear_completed_lines(self):

        rows = self.get_completed_rows()
        cols = self.get_completed_columns()

        total_lines = len(rows) + len(cols)

        for row in rows:

            for x in range(GRID_SIZE):
                self.grid[row][x] = 0

        for col in cols:

            for y in range(GRID_SIZE):
                self.grid[y][col] = 0

        return total_lines

    def count_filled(self):

        total = 0

        for row in self.grid:

            for cell in row:

                if cell != 0:
                    total += 1

        return total

    def board_full(self):

        return self.count_filled() == (
            GRID_SIZE * GRID_SIZE
        )

    def can_place_anywhere(self, piece):

        for y in range(GRID_SIZE):

            for x in range(GRID_SIZE):

                if self.can_place(
                    piece,
                    x,
                    y
                ):
                    return True

        return False

    def has_valid_move(self, pieces):

        for piece in pieces:

            if piece is None:
                continue

            if self.can_place_anywhere(piece):
                return True

        return False

    def get_cell(self, x, y):

        if not self.is_inside(x, y):
            return None

        return self.grid[y][x]

    def set_cell(self, x, y, value):

        if not self.is_inside(x, y):
            return

        self.grid[y][x] = value

    def remove_cell(self, x, y):

        if not self.is_inside(x, y):
            return

        self.grid[y][x] = 0

    def remove_area(self, center_x, center_y, radius=1):

        removed = 0

        for dy in range(-radius, radius + 1):

            for dx in range(-radius, radius + 1):

                x = center_x + dx
                y = center_y + dy

                if self.is_inside(x, y):

                    if self.grid[y][x] != 0:

                        self.grid[y][x] = 0
                        removed += 1

        return removed

    def clear_row(self, row):

        removed = 0

        for x in range(GRID_SIZE):

            if self.grid[row][x] != 0:

                removed += 1
                self.grid[row][x] = 0

        return removed

    def clear_column(self, col):

        removed = 0

        for y in range(GRID_SIZE):

            if self.grid[y][col] != 0:

                removed += 1
                self.grid[y][col] = 0

        return removed

    def copy_grid(self):

        new_grid = []

        for row in self.grid:
            new_grid.append(row.copy())

        return new_grid

    def restore_grid(self, saved_grid):

        self.grid = []

        for row in saved_grid:
            self.grid.append(row.copy())