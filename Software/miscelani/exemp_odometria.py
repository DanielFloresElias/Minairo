import numpy as np

def calculate_odometry(encoders, ticks_per_revolution, r, D, InstantTime):
    # Calculate time differences
    dT = np.diff(InstantTime) / 1000.0  # convert ms to seconds
    
    # Calculate the change in encoder ticks
    dEncoders = np.diff(encoders, axis=0)
    
    # Calculate the distance each wheel has travelled
    delta_s = (dEncoders / ticks_per_revolution) * (2 * np.pi * r)
    
    # Calculate the velocities for each wheel
    v_wheels = delta_s / dT[:, None]
    
    # Coefficients for the inverse kinematics matrix
    sqrt3 = np.sqrt(3)
    
    # Inverse kinematics matrix
    IK_matrix = np.array([
        [-sqrt3 / 3, sqrt3 / 3, 0],
        [1 / 3, 1 / 3, -2 / 3],
        [1 / (3 * D), 1 / (3 * D), 1 / (3 * D)]
    ])
    
    # Initialize odometry values
    num_samples = len(dT)
    odometry = np.zeros((num_samples, 3))  # [v_x, v_y, omega_z]
    
    # Calculate robot velocities for each sample
    for i in range(num_samples):
        odometry[i] = np.dot(IK_matrix, v_wheels[i])
    
    # Calculate displacements
    displacements = np.cumsum(odometry[:, :2] * dT[:, None], axis=0)
    angles = np.cumsum(odometry[:, 2] * dT)
    
    return displacements, angles, odometry

# Example usage
encoders = np.array([
    [1000, 2000, 3000],
    [1100, 2100, 3100],
    [1200, 2200, 3200]
])
ticks_per_revolution = 4096
r = 0.05  # 5 cm radius
D = 0.2  # 20 cm from the center to each wheel
InstantTime = np.array([0, 100, 200])  # in milliseconds

displacements, angles, odometry = calculate_odometry(encoders, ticks_per_revolution, r, D, InstantTime)

print("Displacements (x, y):")
print(displacements)
print("Angles (z):")
print(angles)
print("Odometry (vx, vy, omega_z):")
print(odometry)
