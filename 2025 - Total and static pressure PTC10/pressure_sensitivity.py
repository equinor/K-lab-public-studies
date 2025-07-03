'''
This script calculates and visualizes the relative difference between total pressure and static pressure 
as a function of velocity (up to 300 m/s) for natural gas at a static pressure of 1 bara. The calculations are based on 
the ASME PTC 10-1997 standard, using the GERG-2008 equation of state for determining gas properties. 
'''

import matplotlib.pyplot as plt
import numpy as np
import pvtlib

def static_to_total_pressure(P_static, V, rho):
    """
    Calculate the total pressure based on static pressure, velocity, and density, according to ASME PTC 10-1997.

    Parameters
    ----------
    P_static : float
        Static pressure in Pascals.
    V : float
        Velocity in m/s.
    rho : float
        Density in kg/m^3.

    Returns
    -------
    float
        Total pressure in Pascals.
    """
    return P_static + 0.5 * rho * V**2


def total_to_static_pressure(P_total, V, rho):
    """
    Calculate the static pressure based on total pressure, velocity, and density, according to ASME PTC 10-1997.

    Parameters
    ----------
    P_total : float
        Total pressure in Pascals.
    V : float
        Velocity in m/s.
    rho : float
        Density in kg/m^3.

    Returns
    -------
    float
        Static pressure in Pascals.
    """
    return P_total - 0.5 * rho * V**2


# Constants
P_static = 1.0 # Static pressure in [bara]

# Specify temperature and composition
T = 20.0 # Temperature [C]

composition = {
    'N2' : 1.0,
    'CO2' : 1.0,
    'C1' : 90.0,
    'C2' : 5.0,
    'C3' : 2.0,
    'iC4' : 0.5,
    'nC4' : 0.5
}

# Set up AGA8 object for GERG-2008 equation. This process runs the setup for the given equation, and is only needed once.
gerg = pvtlib.AGA8('GERG-2008')

# Calculate gas properties (default pressure and temperature units are bara and C)
gas_properties = gerg.calculate_from_PT(
    composition=composition,
    pressure=P_static,
    temperature=T,
)

# Velocity range
velocities = np.linspace(0, 300, 100)  # 0 to 300 m/s
# Arrays to store results
P_static_values = []
P_relative_diff_total_static = []

# Perform sensitivity calculation for pressure
for V in velocities:
    P_total = static_to_total_pressure(P_static*10**5, V, gas_properties['rho'])/10**5  # Convert to bara
    
    P_static_values.append(P_static)
    relative_difference = 100 * (P_total - P_static) / P_static
    P_relative_diff_total_static.append(relative_difference)

# Plot the relative pressure difference
plt.figure(figsize=(10, 6))
plt.plot(velocities, P_relative_diff_total_static, label="Relative Difference (%)", color="blue")
plt.xlabel("Velocity [m/s]")
plt.ylabel(r"$\frac{P_{tot} - P_{stat}}{P_{stat}}$ [%]", fontsize=14)
plt.title('Effect of dynamic pressure for natural gas at 1 bara static pressure')
plt.legend()
plt.grid()
plt.savefig('relative_pressure_difference_vs_velocity.png', dpi=300, bbox_inches='tight')
plt.show()

