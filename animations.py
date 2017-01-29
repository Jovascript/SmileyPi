# Advance warning: I'm not an artist, I'm a programmer

# Colours
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
black = [0, 0, 0]
white = [255, 255, 255]
yellowy = [255, 220, 0]


# Animation for when astronaut is present.
X = green
Y = white
O = black
astronaut_here = [
    [
        O, O, O, Y, Y, O, O, O,
        O, O, Y, Y, Y, Y, O, O,
        O, O, Y, Y, Y, Y, O, O,
        O, O, O, Y, Y, O, O, O,
        O, O, Y, Y, Y, Y, O, O,
        Y, Y, Y, Y, Y, Y, Y, Y,
        Y, O, Y, Y, Y, Y, O, Y,
        Y, O, Y, Y, Y, Y, O, Y
    ],
    [
        O, O, O, X, X, O, O, O,
        O, O, X, X, X, X, O, O,
        O, O, X, X, X, X, O, O,
        O, O, O, X, X, O, O, O,
        O, O, X, X, X, X, O, O,
        X, X, X, X, X, X, X, X,
        X, O, X, X, X, X, O, X,
        X, O, X, X, X, X, O, X,
    ]
]
# Animation for when astronaut is not present.
X = red
astronaut_away = [
    [
        O, O, O, Y, Y, O, O, O,
        O, O, Y, Y, Y, Y, O, O,
        O, O, Y, Y, Y, Y, O, O,
        O, O, O, Y, Y, O, O, O,
        O, O, Y, Y, Y, Y, O, O,
        Y, Y, Y, Y, Y, Y, Y, Y,
        Y, O, Y, Y, Y, Y, O, Y,
        Y, O, Y, Y, Y, Y, O, Y
    ],
    [
        O, O, O, X, X, O, O, O,
        O, O, X, X, X, X, O, O,
        O, O, X, X, X, X, O, O,
        O, O, O, X, X, O, O, O,
        O, O, X, X, X, X, O, O,
        X, X, X, X, X, X, X, X,
        X, O, X, X, X, X, O, X,
        X, O, X, X, X, X, O, X
    ]
]

# Animation for sunrise
x = yellowy
sunrise = [
    [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, X, X, X, X, O, O,
        O, X, X, X, X, X, X, O
    ],
    [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, X, X, X, X, O, O,
        O, X, X, X, X, X, X, O,
        X, X, X, X, X, X, X, X
    ],
    [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, X, X, X, X, O, O,
        O, X, X, X, X, X, X, O,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X
    ]
]

sun_full = [
    [
        O, O, X, X, X, X, O, O,
        O, X, X, X, X, X, X, O,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        O, X, X, X, X, X, X, O,
        O, O, X, X, X, X, O, O
    ]
]