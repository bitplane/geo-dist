from math import sqrt
from typing import NamedTuple

import matplotlib.pyplot as plt
from geo_dist_prep.tree.pos import Pos


class Coords(NamedTuple):
    x: float
    y: float

    def __add__(self, other: "Coords") -> "Coords":
        return Coords(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coords") -> "Coords":
        return Coords(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> "Coords":
        return Coords(self.x * other, self.y * other)

    def slope(self) -> float:
        if self.x == 0:
            return float("inf")
        return self.y / self.x

    def length(self) -> float:
        return sqrt(self.x**2 + self.y**2)


class Triangle(NamedTuple):
    a: Coords
    b: Coords
    c: Coords

    @property
    def width(self) -> float:
        return self.c.x - self.b.x

    @property
    def height(self) -> float:
        """
        Returns the distance between the top and bottom of the triangle.
        If negative, the triangle is upside down.
        """
        return self.a.y - self.b.y

    def next(self, coords: Coords) -> tuple[Pos, "Triangle"]:
        """
        Given a parent triangle, return the Pos and Triangle of the next level
        of depth that contains the given coordinates.
        """
        base_mid = (self.b + self.c) * 0.5
        mid = (base_mid + self.a) * 0.5
        # splice_mid = Coords(base_mid.x, mid.y)

        dist_tip = self.a.y - coords.y
        dist_base = base_mid.y - coords.y

        if dist_tip < dist_base:
            return Pos.TIP, Triangle(
                a=self.a,
                b=(self.a + self.b) * 0.5,
                c=(self.a + self.c) * 0.5,
            )
        else:
            s = (coords - base_mid).slope()
            slope = abs(s)
            print("slope:", s, slope)
            if s >= 1:
                return Pos.CENTER, Triangle(
                    a=base_mid,
                    b=(self.a + self.b) * 0.5,
                    c=(self.a + self.c) * 0.5,
                )
            elif coords.x < mid.x:
                return Pos.LEFT_POINT, Triangle(
                    a=(self.a + self.b) * 0.5,
                    b=self.b,
                    c=(self.b + self.c) * 0.5,
                )
            else:
                return Pos.RIGHT_POINT, Triangle(
                    a=(self.a + self.c) * 0.5,
                    b=(self.b + self.c) * 0.5,
                    c=self.c,
                )

    def plot(self, colour="black"):
        import matplotlib.pyplot as plt

        plt.plot(
            [self.a.x, self.b.x, self.c.x, self.a.x],
            [self.a.y, self.b.y, self.c.y, self.a.y],
            color=colour,
        )

    def plot_rectangle(self, colour="black"):
        import matplotlib.pyplot as plt

        plt.plot(
            [self.b.x, self.b.x, self.c.x, self.c.x, self.b.x],
            [self.a.y, self.b.y, self.c.y, self.a.y, self.a.y],
            color=colour,
        )


def drill_down(triangle: Triangle, coords: Coords, depth: int):
    if depth == 0:
        return
    print("depth:", depth)
    pos, next_tri = triangle.next(coords)
    next_tri.plot(colour=["r", "g", "b"][depth % 3])
    drill_down(next_tri, coords, depth - 1)


# Initialize plot
plt.figure()

# Define the initial parent triangle and coords
parent_triangle = Triangle(Coords(0, 0), Coords(-100, -100), Coords(100, -100))
initial_coords = Coords(-20, -63.4)

# Plot the parent triangle
parent_triangle.plot()

# Drill down to depth 4, for example
drill_down(parent_triangle, initial_coords, 8)

plt.scatter([initial_coords.x], [initial_coords.y], color="b")

# Show the plot
plt.show()
