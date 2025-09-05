import numpy as np

# Data for houses and suppliers
houses = [(-225, 125), (-200, 50), (-120, 150), (230, 179), (378, 35), (413, 95),
(124, 63), (364, 132), (301, 72), (241, 60), (-301, -120), (-302, 100),
 (-312, 146), (-349, 99), (155, 200), (133, 145), (-134, -98), (-143, -132),
(-152, -128), (-265, -56), (-267, -145)]
suppliers = [(205,-152),(-406,27),(156,100)]


# Constants
k = 1
cm = 50
ct = 3.44


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def revenue_gradient(x, y, houses):
    Px, Py = 0, 0
    for hx, hy in houses:
        dist_squared = (x - hx) ** 2 + (y - hy) ** 2
        Px -= 200 * (x - hx) / dist_squared ** (1.5)
        Py -= 200 * (y - hy) / dist_squared ** (1.5)
    return Px, Py

def expense_gradient(x, y, suppliers):
    Px, Py = 0, 0
    for sx, sy in suppliers:
        dist = np.sqrt((x - sx) ** 2 + (y - sy) ** 2)
        Px -= 3.44 * (x - sx) / dist
        Py -= 3.44 * (y - sy) / dist
    return Px, Py

# Gradient Descent
def optimize_location(houses, suppliers, learning_rate=0.01, tolerance=1e-6):
    x, y = -100,0  # Initial guess
    for _ in range(10000):  # Max iterations
        Rx, Ry = revenue_gradient(x, y, houses)
        Ex, Ey = expense_gradient(x, y, suppliers)
        Px, Py = Rx + Ex, Ry + Ey

        if np.sqrt(Px ** 2 + Py ** 2) < tolerance:
            break  # Convergence

        x -= learning_rate * Px
        y -= learning_rate * Py
    return x, y

def calculate_distances(x, y, points):
    distances = []
    for px, py in points:
        dist = np.sqrt((x - px) ** 2 + (y - py) ** 2)
        distances.append(float(dist))
    return distances

def print_distances(x,y):
    house_distances = calculate_distances(x, y, houses)
    supplier_distances = calculate_distances(x, y, suppliers)
    print("Distances from M to each house (R_i):", house_distances)
    print("Distances from M to each supplier (S_j):", supplier_distances)

def revenue(x,y, houses):
    rev = 0
    for hx, hy in houses:
        distance = np.sqrt((x - hx) ** 2 + (y - hy) ** 2)
        interest = 0.95 - 0.000898*distance #if distance > 0 else 0
        rev += interest
    rev *= 200
    return rev
def expenses(x,y, suppliers):
    cost = 0
    for sx,sy in suppliers:
        distance = np.sqrt((x - sx) ** 2 + (y - sy) ** 2)
        cost += distance
    cost *= 3.44
    return cost
def profit(x,y,houses,suppliers):
    p = revenue(x,y,houses) - expenses(x,y,suppliers)
    return p

def location_find(houses, suppliers, step):
    x_min, x_max = -463,463
    y_min, y_max = -254,254

    optimal_profit = 0
    optimal_x, optimal_y = None, None

    x = x_min
    while x <= x_max:
        y = y_min  # Reset y for each x
        while y <= y_max:
            current_profit = profit(x, y, houses, suppliers)
            if current_profit > optimal_profit:  # Update optimal location
                optimal_profit = current_profit
                optimal_x, optimal_y = x, y
            y += step  # Increment y by step size
        x += step  # Increment x by step size

    return optimal_x, optimal_y, optimal_profit

optimal_x, optimal_y, optimal_profit = location_find(houses, suppliers, 1)
print(f"Optimal Location: ({optimal_x}, {optimal_y}) with Profit: {optimal_profit}")

