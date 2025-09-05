import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parameters
m = 0.115476667  # Mass
I = 0.000438  # Moment of inertia
k = 2.518  # Spring constant
kappa = 0.0095527702   # Torsional constant
c = 0.06141767682 # Coupling constant

# Initial conditions
y0 = -0.25  # Initial vertical displacement
dy0 = 0.0  # Initial vertical velocity
theta0 = 0.0  # Initial angular displacement
dtheta0 = 0.0  # Initial angular velocity

# Time range
t_span = (0, 15)
t_eval = np.linspace(0, 15, 1000)

# Equations of motion
def wilberforce(t, state):
    y, dy, theta, dtheta = state
    d2y = (-k * y - c * theta) / m
    d2theta = (-kappa * theta - c * y) / I
    return [dy, d2y, dtheta, d2theta]

# Solve the system
sol = solve_ivp(wilberforce, t_span, [y0, dy0, theta0, dtheta0], t_eval=t_eval)

# Extract solutions
y = sol.y[0]
theta = sol.y[2]
t = sol.t

# Convert theta to arc length (s = r * theta)
r = 0.06  # Radius
s = r * theta  # Arc length

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(t, y, label='z')
plt.plot(t, s, label='θ')
plt.xlabel('Time (s)')
y_ticks = np.linspace(min(min(y), min(s)), max(max(y), max(s)), 10)  # 20 points on y-axis
plt.yticks(y_ticks)
plt.title('Equations of Motion')
plt.legend()
plt.grid()
plt.show()