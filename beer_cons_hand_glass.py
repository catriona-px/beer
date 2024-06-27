import numpy as np
import matplotlib.pyplot as plt

# Constants
T_initial = 4.0  # Initial temperature of the beer (average fridge temperature) in Celsius
T_air = 30  # Ambient air temperature in Celsius
T_hand = 37  # Temperature of the hand in Celsius
heat_transfer_coefficient= 100.0  # Example: heat transfer coefficient in W/(m²·K)
heat_transfer_coefficient_hand = 50.0  # Example: heat transfer coefficient for beer in W/(m²·K)
glass_thermal_conductivity = 1.2  # Example: thermal conductivity of glass in W/m*K
specific_heat_capacity = 4186  # Specific heat capacity of water (J/kg*K)
density = 1000  # Density of water (kg/m^3)
time_step_minutes = 0.0005  # Time step in minutes
total_time_minutes = 30  # Total time in minutes

# Conversion factors
pint_to_m3 = 0.000473176  # 1 pint = 0.000473176 cubic meters

# Function to calculate the rate of warming with hand and conduction through glass
def rate_of_warming_with_hand_and_conduction(radius, height, T, T_air, T_hand, volume, heat_transfer_coefficient, specific_heat_capacity, density, glass_thickness, glass_thermal_conductivity):
    if volume > 0:
        surface_area_cylinder = 2 * np.pi * radius * height + 2 * np.pi * radius**2
        hand_coverage_ratio = 0.25  # Example: hand covers 50% of the surface
        
        # Calculate surface area covered by the hand
        surface_area_hand = hand_coverage_ratio * surface_area_cylinder
        
        # Calculate heat transfer due to ambient air
        heat_transfer_rate_air = heat_transfer_coefficient * surface_area_cylinder * (T_air - T)
        
        # Calculate heat transfer due to hand
        heat_transfer_rate_hand = heat_transfer_coefficient_hand * surface_area_hand * (T_hand - T)
        
        # Calculate heat conduction through glass cylinder
        surface_area_glass = surface_area_cylinder - surface_area_hand  # Surface area of glass exposed to air
        heat_conduction_rate = glass_thermal_conductivity * surface_area_glass * (T_air - T) / glass_thickness
        
        # Total heat transfer rate
        heat_transfer_rate_total = heat_transfer_rate_air + heat_transfer_rate_hand + heat_conduction_rate
        
        # Calculate temperature change rate
        mass = density * volume
        temperature_change_rate = heat_transfer_rate_total / (mass * specific_heat_capacity)
    else:
        temperature_change_rate = 0.0  # Set temperature change rate to 0 when volume is 0 or less
    
    return temperature_change_rate

# Function to simulate the temperature change over time with hand and glass conduction
def simulate_warming_with_conduction(radius, height, T_initial, T_air, T_hand, base_consumption_rate_pints_per_minute, heat_transfer_coefficient, specific_heat_capacity, density, glass_thickness, glass_thermal_conductivity, time_step_minutes, total_time_minutes):
    initial_volume = np.pi * radius**2 * height  # Initial volume in cubic meters
    times = np.arange(0, total_time_minutes + time_step_minutes, time_step_minutes)
    temperatures = [T_initial]
    heights = [height]
    volumes = [initial_volume]  # Initial volume in cubic meters
    T = T_initial  # Initial temperature
    volume = initial_volume
    refill_time = -1
    
    for idx, t in enumerate(times[1:]):
        if refill_time != -1 and idx > refill_time:
            volume = initial_volume
            T = T_initial  # Reset temperature to initial upon refilling
            refill_time = -1

        consumption_rate_pints_per_minute = consumption_rate_function(T, base_consumption_rate_pints_per_minute)
        volume -= consumption_rate_pints_per_minute * pint_to_m3 * time_step_minutes

        if volume <= 0:
            volume = 0
            if refill_time == -1:
                refill_time = idx + 10

        volumes.append(volume)
        height = volume / (np.pi * radius**2)
        heights.append(height)
        rate = rate_of_warming_with_hand_and_conduction(radius, height, T, T_air, T_hand, volume, heat_transfer_coefficient, specific_heat_capacity, density, glass_thickness, glass_thermal_conductivity)
        T += rate * time_step_minutes * 60  # Convert time step to seconds for the rate
        temperatures.append(T)
    
    return times[:len(temperatures)], temperatures, heights

# Function to calculate consumption rate as a function of temperature
def consumption_rate_function(T, base_consumption_rate):
    min_temp = 15  # Minimum temperature for highest consumption rate
    max_temp = 16  # Maximum temperature for lowest consumption rate
    if T < min_temp:
        return base_consumption_rate * 3  # Three times the base rate if it's colder than min_temp
    elif T > max_temp:
        return base_consumption_rate * 0.5  # Half the base rate if it's warmer than max_temp
    else:
        # Quadratic interpolation between min_temp and max_temp for a stronger effect
        return base_consumption_rate * (1 + 2 * (max_temp - T) / (max_temp - min_temp))

# Radii and heights of the two cylinders
radius1 = 0.03  # Radius of cylinder 1 in meters (3 cm)
height1 = 0.12   # Height of cylinder 1 in meters (12 cm)

# Calculate the radius for the second cylinder to have double the volume of the first cylinder
volume1 = np.pi * radius1**2 * height1
volume2 = 2 * volume1
radius2 = np.sqrt(volume2 / (np.pi * height1))

# Base consumption rates for each cylinder
base_consumption_rate_pints_per_minute1 = 0.1  # Base consumption rate in pints per minute for half pint
base_consumption_rate_pints_per_minute2 = 0.1  # Base consumption rate in pints per minute for full pint

# Constants for glass cylinder
glass_thickness = 0.005  # Example: glass thickness in meters

# Simulate warming for both cylinders with conduction through glass
times1, temperatures1, heights1 = simulate_warming_with_conduction(radius1, height1, T_initial, T_air, T_hand, base_consumption_rate_pints_per_minute1, heat_transfer_coefficient, specific_heat_capacity, density, glass_thickness, glass_thermal_conductivity, time_step_minutes, total_time_minutes)
times2, temperatures2, heights2 = simulate_warming_with_conduction(radius2, height1, T_initial, T_air, T_hand, base_consumption_rate_pints_per_minute2, heat_transfer_coefficient, specific_heat_capacity, density, glass_thickness, glass_thermal_conductivity, time_step_minutes, total_time_minutes)

# Calculate average temperatures over a time interval (e.g., last 5 minutes)
average_time_interval_minutes = 30
interval_steps = int(average_time_interval_minutes / time_step_minutes)

average_temperature1 = np.mean(temperatures1[-interval_steps:])
average_temperature2 = np.mean(temperatures2[-interval_steps:])

# Plotting temperature change
plt.figure(figsize=(10, 6))
plt.plot(times1, temperatures1, label=f'Half Pint: Radius = {radius1*100:.1f} cm, Initial Height = {height1*100:.1f} cm, Base Consumption Rate = {base_consumption_rate_pints_per_minute1:.2f} pints/min')
plt.plot(times2, temperatures2, label=f'Full Pint: Radius = {radius2*100:.1f} cm, Initial Height = {height1*100:.1f} cm, Base Consumption Rate = {base_consumption_rate_pints_per_minute2:.2f} pints/min')
plt.axhline(y=average_temperature1, color='blue', linestyle='--', label=f'Avg Temp Half Pint ({average_time_interval_minutes} min): {average_temperature1:.2f} °C')
plt.axhline(y=average_temperature2, color='orange', linestyle='--', label=f'Avg Temp Full Pint ({average_time_interval_minutes} min): {average_temperature2:.2f} °C')
plt.xlabel('Time (minutes)')
plt.ylabel('Beer Temperature (°C)')
plt.title('Beer Temperature Change Over Time with Temperature-Dependent Consumption Rate and Hand Effect')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), shadow=True, ncol=1)
plt.grid(True)
plt.tight_layout()
plt.show()
