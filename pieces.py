# pieces.py

import random


# ==================================================
# COLORS
# ==================================================

COLORS = [
    (255, 85, 85),      # red
    (85, 255, 85),      # green
    (85, 170, 255),     # blue
    (255, 200, 85),     # yellow
    (255, 85, 255),     # magenta
    (85, 255, 255),     # cyan
    (255, 140, 70),     # orange
]


# ==================================================
# SHAPES
# ==================================================

SHAPES = [

    # single

    {
        "name": "single",
        "weight": 12,
        "shape": [
            (0, 0)
        ]
    },

    # domino

    {
        "name": "domino_h",
        "weight": 10,
        "shape": [
            (0, 0),
            (1, 0)
        ]
    },

    {
        "name": "domino_v",
        "weight": 10,
        "shape": [
            (0, 0),
            (0, 1)
        ]
    },

    # triple

    {
        "name": "triple_h",
        "weight": 9,
        "shape": [
            (0, 0),
            (1, 0),
            (2, 0)
        ]
    },

    {
        "name": "triple_v",
        "weight": 9,
        "shape": [
            (0, 0),
            (0, 1),
            (0, 2)
        ]
    },

    # square

    {
        "name": "square2",
        "weight": 8,
        "shape": [
            (0,0),
            (1,0),
            (0,1),
            (1,1)
        ]
    },

    # line 4

    {
        "name": "line4_h",
        "weight": 7,
        "shape": [
            (0,0),
            (1,0),
            (2,0),
            (3,0)
        ]
    },

    {
        "name": "line4_v",
        "weight": 7,
        "shape": [
            (0,0),
            (0,1),
            (0,2),
            (0,3)
        ]
    },

    # line 5

    {
        "name": "line5_h",
        "weight": 5,
        "shape": [
            (0,0),
            (1,0),
            (2,0),
            (3,0),
            (4,0)
        ]
    },

    {
        "name": "line5_v",
        "weight": 5,
        "shape": [
            (0,0),
            (0,1),
            (0,2),
            (0,3),
            (0,4)
        ]
    },

    # L shapes

    {
        "name": "L1",
        "weight": 8,
        "shape": [
            (0,0),
            (0,1),
            (1,1)
        ]
    },

    {
        "name": "L2",
        "weight": 8,
        "shape": [
            (0,0),
            (1,0),
            (0,1)
        ]
    },

    {
        "name": "L3",
        "weight": 8,
        "shape": [
            (0,0),
            (1,0),
            (1,1)
        ]
    },

    {
        "name": "L4",
        "weight": 8,
        "shape": [
            (1,0),
            (0,1),
            (1,1)
        ]
    },

    # large L

    {
        "name": "big_L",
        "weight": 5,
        "shape": [
            (0,0),
            (0,1),
            (0,2),
            (1,2)
        ]
    },

    # T

    {
        "name": "T",
        "weight": 5,
        "shape": [
            (0,0),
            (1,0),
            (2,0),
            (1,1)
        ]
    },

    # plus

    {
        "name": "plus",
        "weight": 3,
        "shape": [
            (1,0),
            (0,1),
            (1,1),
            (2,1),
            (1,2)
        ]
    },

    # corner block

    {
        "name": "corner",
        "weight": 6,
        "shape": [
            (0,0),
            (1,0),
            (0,1)
        ]
    },

    # big square

    {
        "name": "square3",
        "weight": 3,
        "shape": [
            (0,0),
            (1,0),
            (2,0),

            (0,1),
            (1,1),
            (2,1),

            (0,2),
            (1,2),
            (2,2)
        ]
    }
]


# ==================================================
# PIECE CLASS
# ==================================================

class Piece:

    def __init__(
        self,
        shape,
        color,
        name
    ):

        self.shape = shape
        self.color = color
        self.name = name

        self.selected = False

    def get_width(self):

        max_x = 0

        for x, y in self.shape:

            if x > max_x:
                max_x = x

        return max_x + 1

    def get_height(self):

        max_y = 0

        for x, y in self.shape:

            if y > max_y:
                max_y = y

        return max_y + 1

    def block_count(self):

        return len(self.shape)

    def to_dict(self):

        return {
            "shape": self.shape,
            "color": self.color,
            "name": self.name
        }


# ==================================================
# GENERATION
# ==================================================

def choose_shape():

    weights = []

    for entry in SHAPES:
        weights.append(entry["weight"])

    return random.choices(
        SHAPES,
        weights=weights,
        k=1
    )[0]


def generate_piece():

    data = choose_shape()

    return Piece(
        data["shape"],
        random.choice(COLORS),
        data["name"]
    )


def generate_piece_set():

    return [
        generate_piece(),
        generate_piece(),
        generate_piece()
    ]


# ==================================================
# SPECIAL PIECES
# ==================================================

def generate_rainbow_piece():

    piece = generate_piece()

    piece.color = (
        random.randint(50,255),
        random.randint(50,255),
        random.randint(50,255)
    )

    return piece


def generate_bomb_piece():

    return Piece(
        [(0,0)],
        (255,40,40),
        "bomb"
    )