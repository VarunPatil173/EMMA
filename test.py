import math

# Input: length of the pendulum (in meters)
length = float(input("Enter length of pendulum (m): "))
gravity = 9.81  # Standard gravity (m/s²)

# Calculate time period
time_period = 2 * math.pi * math.sqrt(length / gravity)

# Output result
print(f"Time period: {time_period:.4f} seconds")