import matplotlib.pyplot as plt
import numpy as np


def static_to_total_temperature(T_static, V, Cp):
    """
    Calculate the total temperature based on static temperature, velocity, and specific heat capacity.
    Formula derived from ASME PTC 10-1997.

    Parameters
    ----------
    T_static : float
        Static temperature in Kelvin.
    V : float
        Velocity in m/s.
    Cp : float
        Specific heat capacity in J/(kg*K).

    Returns
    -------
    float
        Total temperature in Kelvin.
    """
    return T_static + 0.5 * V**2 / Cp

def total_to_static_temperature(T_total, V, Cp):
    """
    Calculate the static temperature based on total temperature, velocity, and specific heat capacity.
    Formula derived from ASME PTC 10-1997.

    Parameters
    ----------
    T_total : float
        Total temperature in Kelvin.
    V : float
        Velocity in m/s.
    Cp : float
        Specific heat capacity in J/(kg*K).

    Returns
    -------
    float
        Static temperature in Kelvin.
    """
    return T_total - 0.5 * V**2 / Cp

def measured_to_total_temperature(T_measured, V, Cp, rf=0.65):
    """
    Calculate the total temperature based on measured temperature, velocity, specific heat capacity, and recovery factor.
    Formula derived from ASME PTC 10-1997 (Eq 5.4.7).

    Parameters
    ----------
    T_measured : float
        Measured temperature in Kelvin.
    V : float
        Velocity in m/s.
    Cp : float
        Specific heat capacity in J/(kg*K).
    rf : float, optional
        Recovery factor (dimensionless). Default is 0.65 (typical value for air according to ASME PTC 10-1997).

    Returns
    -------
    float
        Static temperature in Kelvin.
    """
    return T_measured - (1 - rf) * 0.5 * V**2 / Cp


# Constants
T_total = 293.15  # Total temperature in Kelvin
Cp = 2080  # Specific heat capacity in J/(kg*K)
rf = 0.65  # Recovery factor (dimensionless)

# Velocity range
velocities = np.linspace(0, 300, 100)  # 0 to 300 m/s
# Arrays to store results
T_measured_values = []
T_static_values = []
T_diff_measured_static = []

# Perform sensitivity calculation
for V in velocities:
    T_static = total_to_static_temperature(T_total, V, Cp)
    T_measured = T_static + (1 - rf) * 0.5 * V**2 / Cp
    
    T_static_values.append(T_static)
    T_measured_values.append(T_measured)
    T_diff_measured_static.append(T_measured - T_static)

# Plot the difference
plt.figure(figsize=(10, 6))
plt.plot(velocities, T_diff_measured_static, label="T_measured - T_static", color="green")
plt.xlabel("Velocity (m/s)")
plt.ylabel("Measured - static temperature (K)")
plt.title(f'Measured - Static Temperature vs Velocity, recovery factor = {rf}')
plt.legend()
plt.grid()
plt.show()

plt.savefig('temperature_error_vs_velocity.png', dpi=300, bbox_inches='tight')