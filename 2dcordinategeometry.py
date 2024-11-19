import math

class CoordinateGeometry2D:
    def __init__(self, x, y):
        """Initializes a point with coordinates (x, y)."""
        self.x = x
        self.y = y

    def __repr__(self):
        """Represents the point as a string in (x, y) format."""
        return f"({self.x}, {self.y})"

    def add(self, other):
        """Adds the current point to another point."""
        return CoordinateGeometry2D(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        """Subtracts another point from the current point."""
        return CoordinateGeometry2D(self.x - other.x, self.y - other.y)

    def distance_to(self, other):
        """Calculates the distance to another point."""
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def midpoint_to(self, other):
        """Calculates the midpoint between the current point and another point."""
        return CoordinateGeometry2D((self.x + other.x) / 2, (self.y + other.y) / 2)

    def distance_to_line(self, line):
        """Calculates the distance from the point to a line (Line2D object)."""
        return abs(line.A * self.x + line.B * self.y + line.C) / math.sqrt(line.A**2 + line.B**2)

    def is_collinear_with(self, p2, p3):
        """Checks if three points are collinear using area of triangle method."""
        area = self.x * (p2.y - p3.y) + p2.x * (p3.y - self.y) + p3.x * (self.y - p2.y)
        return area == 0


class Line2D:
    def __init__(self, A, B, C):
        """Initializes a line in the form Ax + By + C = 0."""
        self.A = A
        self.B = B
        self.C = C

    def __repr__(self):
        """Represents the line as a string."""
        return f"{self.A}x + {self.B}y + {self.C} = 0"

    @staticmethod
    def from_points(p1, p2):
        """Creates a line in the form Ax + By + C = 0 passing through two points."""
        A = p2.y - p1.y
        B = p1.x - p2.x
        C = -(A * p1.x + B * p1.y)
        return Line2D(A, B, C)

    def slope(self):
        """Calculates the slope of the line."""
        if self.B == 0:
            return None  # Vertical line
        return -self.A / self.B

    def slope_intercept_form(self):
        """Converts the line to the slope-intercept form y = mx + b."""
        if self.B == 0:
            return None  # Vertical line (no slope-intercept form)
        m = -self.A / self.B
        b = -self.C / self.B
        return f"y = {m}x + {b}"

    def angle_with(self, other):
        """Calculates the angle between two lines in degrees."""
        m1 = self.slope()
        m2 = other.slope()

        # Handle vertical line cases
        if m1 is None and m2 is None:  # Both lines are vertical
            return 0  # Parallel vertical lines
        elif m1 is None or m2 is None:  # One line is vertical
            return 90  # Perpendicular to a non-vertical line
        elif 1 + m1 * m2 == 0:  # Perpendicular lines
            return 90

        # General case
        angle_rad = math.atan(abs((m1 - m2) / (1 + m1 * m2)))
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def is_parallel_to(self, other):
        """Checks if the current line is parallel to another line."""
        return self.A * other.B == self.B * other.A

    def is_coincident_with(self, other):
        """Checks if the current line is coincident with another line."""
        return self.is_parallel_to(other) and \
               self.A * other.C == other.A * self.C and \
               self.B * other.C == other.B * self.C

    def is_intersecting_with(self, other):
        """Checks if the current line is intersecting with another line."""
        return not self.is_parallel_to(other) and not self.is_coincident_with(other)

    def intersection_with(self, other):
        """Finds the intersection point of the current line with another line."""
        determinant = self.A * other.B - other.A * self.B
        if determinant == 0:
            return None  # Lines are parallel or coincident
        x = (self.B * other.C - other.B * self.C) / determinant
        y = (other.A * self.C - self.A * other.C) / determinant
        return CoordinateGeometry2D(x, y)

    @staticmethod
    def intersection_of_lines_from_points(p1, p2, p3, p4):
        """Finds the intersection of lines formed by two pairs of points."""
        line1 = Line2D.from_points(p1, p2)
        line2 = Line2D.from_points(p3, p4)
        return line1.intersection_with(line2)

    @staticmethod
    def perpendicular_from_point(p, line):
        """Finds the perpendicular line to the given line passing through point p."""
        if line.B == 0:
            return Line2D(1, 0, -p.x)  # Vertical line through p
        slope_perp = -line.A / line.B  # Perpendicular slope
        C = p.y - slope_perp * p.x
        return Line2D(slope_perp, -1, C)


# Example Usage
p1 = CoordinateGeometry2D(0, 0)
p2 = CoordinateGeometry2D(2, 2)
p3 = CoordinateGeometry2D(0, 2)
p4 = CoordinateGeometry2D(2, 0)

line1 = Line2D.from_points(p1, p2)
line2 = Line2D.from_points(p3, p4)

print("Line 1 (from p1 and p2):", line1)
print("Line 2 (from p3 and p4):", line2)

# Distance between points
print("Distance between p1 and p2:", p1.distance_to(p2))

# Midpoint
print("Midpoint between p1 and p2:", p1.midpoint_to(p2))

# Distance to a line
print("Distance from p1 to Line 2:", p1.distance_to_line(line2))

# Check collinearity
print("Are p1, p2, p3 collinear?", p1.is_collinear_with(p2, p3))

# Intersection of lines
intersection = line1.intersection_with(line2)
print("Intersection of Line 1 and Line 2:", intersection)

# Parallel and coincident checks
print("Are Line 1 and Line 2 parallel?", line1.is_parallel_to(line2))
print("Are Line 1 and Line 2 coincident?", line1.is_coincident_with(line2))

# Angle between lines
print("Angle between Line 1 and Line 2:", line1.angle_with(line2), "degrees")

# Perpendicular line from a point
perpendicular_line = Line2D.perpendicular_from_point(p1, line1)
print("Perpendicular Line from p1 to Line 1:", perpendicular_line)

# Intersection of lines formed by points
intersection_points = Line2D.intersection_of_lines_from_points(p1, p2, p3, p4)
print("Intersection point of lines formed by p1-p2 and p3-p4:", intersection_points)
