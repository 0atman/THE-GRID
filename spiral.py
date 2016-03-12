def max_previous_spiral(x, y, offset=0): 
    n = max([abs(x), abs(y)]) + offset
    return 4*n**2 - 4*n+1

def get_spiral_number(x, y):
    """
    radius is zero indexed
    """
    radius = max(abs(x), abs(y))
    mps = max_previous_spiral(x, y)
    mp2s = max_previous_spiral(x, y, -1)

    if x == 0 and y==0:
        return 0

    elif x >= 0 and y >= 0:
        """
        (3, 2) = 30
        if both are +ve,
        max previous spiral,
        add the radius 
        add y
        add radius - x
        QED
        """
        return mps + radius + y + (radius - x)

    elif x <= 0 and y >= 0:
        """
        (-2, 3) = 36
        if x is -ve
        max previous spiral,
        add radius x 3
        add abs x
        + rad - y
        QED
        """
        return mps + (radius * 3) + abs(x) + (radius - abs(y))


    elif x <= 0 and y <= 0:
        """
        (-2, -3) = 44
        if x is -ve
        max previous spiral,
        add radius x 5
        add abs y
        + rad - abs x
        """
        return mps + (radius * 5) + abs(y) + (radius - abs(x))

    elif x >= 0 and y <= 0:
        if abs(x) > abs(y):
            """
            (3, -2) = 26
            (4, -2) = 51
            if x > abs y:
            max previous spirals
            + rad - abs x
            + rad - abs y
            """
            return mps + radius - abs(x) + radius - abs(y)
        else:
            """
            (2, -3) = 48
            if x <= abs y
            max previous spirals
            + r * 7
            + abs x
            + rad - abs y
            """
            return mps + (radius * 7) + abs(x) + (radius - abs(y))
