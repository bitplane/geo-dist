import math


class Coords:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def slope_to(self, other):
        if self.x == other.x:
            return math.inf
        return (other.y - self.y) / (other.x - self.x)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Coords({self.x}, {self.y})"


class Triangle:
    def __init__(self, A: Coords, B: Coords, C: Coords):
        self.A = A
        self.B = B
        self.C = C

    def __contains__(self, point: Coords):
        # Calculate barycentric coordinates
        denom = (self.B.y - self.C.y) * (self.A.x - self.C.x) + (
            self.C.x - self.B.x
        ) * (self.A.y - self.C.y)
        a = (
            (self.B.y - self.C.y) * (point.x - self.C.x)
            + (self.C.x - self.B.x) * (point.y - self.C.y)
        ) / denom
        b = (
            (self.C.y - self.A.y) * (point.x - self.C.x)
            + (self.A.x - self.C.x) * (point.y - self.C.y)
        ) / denom
        c = 1 - a - b

        # Check if point is inside triangle
        return 0 <= round(a, 9) <= 1 and 0 <= round(b, 9) <= 1 and 0 <= round(c, 9) <= 1

    def point_location(self, coords: Coords):
        assert coords in self

        D = Coords((self.B.x + self.C.x) / 2, self.B.y)
        m_AB = self.A.slope_to(self.B)
        m_AC = self.A.slope_to(self.C)

        E_y = F_y = (self.A.y + self.B.y) / 2

        E_x = self.A.x + ((E_y - self.A.y) / m_AB) if m_AB != float("inf") else self.A.x
        F_x = self.C.x + ((F_y - self.C.y) / m_AC) if m_AC != float("inf") else self.C.x

        E = Coords(E_x, E_y)
        F = Coords(F_x, F_y)

        triangles = [
            Triangle(self.A, E, F),
            Triangle(E, self.B, D),
            Triangle(D, E, F),
            Triangle(F, D, self.C),
        ]

        for t in triangles:
            if coords in t:
                return t

        raise Exception("Point not found in any sub-triangle")

    def plot(self, color="b"):
        import matplotlib.pyplot as plt

        x_values = [self.A.x, self.B.x, self.C.x, self.A.x]
        y_values = [self.A.y, self.B.y, self.C.y, self.A.y]

        plt.plot(x_values, y_values, color=color)

    def __eq__(self, other):
        return self.A == other.A and self.B == other.B and self.C == other.C

    def __repr__(self):
        return f"Triangle({self.A}, {self.B}, {self.C})"


def barycentric_coordinates(t: Triangle, coords: Coords):
    # t.A.x, t.A.y are coordinates for point A, similarly for B and C.
    # coords.x, coords.y are coordinates for point coords.

    denominator = (t.B.y - t.C.y) * (t.A.x - t.C.x) + (t.C.x - t.B.x) * (t.A.y - t.C.y)

    a = (
        (t.B.y - t.C.y) * (coords.x - t.C.x) + (t.C.x - t.B.x) * (coords.y - t.C.y)
    ) / denominator
    b = (
        (t.C.y - t.A.y) * (coords.x - t.C.x) + (t.A.x - t.C.x) * (coords.y - t.C.y)
    ) / denominator
    c = 1 - a - b

    return a, b, c
