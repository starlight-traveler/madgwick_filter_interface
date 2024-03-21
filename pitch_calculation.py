import imufusion
import matplotlib.pyplot as pyplot
import numpy
import sys
import os
import csv

current_dir = os.path.dirname(os.path.realpath(__file__))

"""
Important Considerations for Data Visualization and Analysis:

1) Recovery Triggers Visualization: The second graph specifically represents
the data for recovery triggers. This is crucial for understanding
the algorithm's response to sensor anomalies.

2) Normalization of Data: The displayed data is normalized to start at 0 degrees on 
the y-axis, which deviates from standard theoretical models. This normalization 
is employed to manage the complexity of this project. When comparing with 
theoretical models or other references, adjust the y-axis accordingly to 
align with the referenced values.

3) Graph Scaling: To enhance the readability and interpretability 
of the graphs, consider adjusting the scaling. Tailoring the scale can
significantly improve the visualization of trends and patterns within the data.

These points are based on prior experiences and are intended to guide the 
effective visualization and analysis of the data within this project.
"""


# Obtain the directory of the currently executing script.
# This is useful for building file paths relative to the script location,
# ensuring portability across different operating systems and environments.
current_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the CSV file containing rocketry launch data.
# Ensure the CSV file is located in the same directory as this script.
# Note: It's crucial to verify the data units in the CSV file to ensure compatibility with the processing algorithms.
raw_data_path = os.path.join(current_dir, 'csvFiles/rocketryLaunch.csv')

# Similarly, construct the path to any additional scripts or resources, such as 'theoreticalvseuler.py'.
# This enables easy reference and execution of supplementary Python scripts within the same directory.
theoretical_vs_euler_path = os.path.join(current_dir, 'theoreticalvseuler.py')

# Load the sensor data from the CSV file. The 'skip_header' parameter is set to 1 to ignore the first row, assuming it contains column headers.
# The delimiter is set to "," as it's the common format for CSV files.
data = numpy.genfromtxt(raw_data_path, delimiter=",", skip_header=1)

# Define the sample rate of the sensor used to collect the data. The sample rate is essential for time-series analysis and algorithms that depend on temporal resolution.
# Example: 15 Hz indicates that the sensor records 15 data points per second.
sample_rate = 15

# Initialize sensor fusion algorithms with the specified sample rate. These algorithms are used to process and interpret the raw sensor data.
# Instantiate algorithms
offset = imufusion.Offset(sample_rate)
ahrs = imufusion.Ahrs()

# Configure the AHRS (Attitude and Heading Reference System) algorithm settings according to the specific characteristics of your sensor.
# These settings include the sensor's convention, gain, gyroscope range, acceleration rejection, magnetic rejection, and the recovery trigger period.
# Adjust these values based on your sensor's specifications and the desired algorithm behavior.
ahrs.settings = imufusion.Settings(imufusion.CONVENTION_NWU, # Coordinate convention: North-West-Up
                                   0.789, # Algorithm gain (e.g., 0.5 for moderate filtering)
                                   1000,  # Gyroscope measurement range in degrees per second (dps)
                                   10,  # Acceleration rejection factor for outlier detection
                                   10,  # Magnetic field rejection factor for outlier detection
                                   4 * sample_rate) # Recovery trigger period in samples (e.g., 4 times the sample rate)

# Extract individual sensor data arrays from the loaded data set. Each sensor's data is assumed to be in consecutive columns following the timestamp column.
# Timestamps, gyroscope readings, accelerometer readings, and magnetometer readings are extracted based on their column positions in the CSV file.
timestamp = data[:, 0]  # First column: timestamps
gyroscope = data[:, 1:4]  # Second to fourth columns: gyroscope data (X, Y, Z axes)
accelerometer = data[:, 4:7]  # Fifth to seventh columns: accelerometer data (X, Y, Z axes)
magnetometer = data[:, 7:10]  # Eighth to tenth columns: magnetometer data (X, Y, Z axes)

# Calculate the time difference between each timestamp to determine the rate at which the data is processed.
delta_time = numpy.diff(timestamp, prepend=timestamp[0])

# Initialize arrays to store Euler angles, internal states of the AHRS algorithm, and flags indicating the status of various processes.
euler = numpy.empty((len(timestamp), 3))
internal_states = numpy.empty((len(timestamp), 6))
flags = numpy.empty((len(timestamp), 4))

# Loop through each data point to update the sensor fusion algorithm with the latest sensor readings and compute the Euler angles.
for index in range(len(timestamp)):
    # Apply offset correction to the gyroscope data.
    gyroscope[index] = offset.update(gyroscope[index])

    # Update the AHRS (Attitude and Heading Reference System) algorithm with the latest sensor readings and time difference.
    ahrs.update(gyroscope[index], accelerometer[index], magnetometer[index], delta_time[index])

    # Convert the current orientation from quaternion to Euler angles (Roll, Pitch, Yaw) for intuitive understanding.
    euler[index] = ahrs.quaternion.to_euler()

    # Retrieve and store the internal states of the AHRS algorithm, such as acceleration and magnetic errors.
    ahrs_internal_states = ahrs.internal_states
    internal_states[index] = numpy.array([
        ahrs_internal_states.acceleration_error,
        ahrs_internal_states.accelerometer_ignored,
        ahrs_internal_states.acceleration_recovery_trigger,
        ahrs_internal_states.magnetic_error,
        ahrs_internal_states.magnetometer_ignored,
        ahrs_internal_states.magnetic_recovery_trigger
    ])

    # Retrieve and store flags indicating the status of the AHRS algorithm's processes, such as initialization and recovery modes.
    ahrs_flags = ahrs.flags
    flags[index] = numpy.array([
        ahrs_flags.initialising,
        ahrs_flags.angular_rate_recovery,
        ahrs_flags.acceleration_recovery,
        ahrs_flags.magnetic_recovery
    ])

# Utility function to plot boolean flags (True/False) as a line plot, aiding in visualizing the status changes over time.
def plot_bool(axis, x, y, label):
    axis.plot(x, y, "tab:cyan", label=label)
    pyplot.sca(axis)
    pyplot.yticks([0, 1], ["False", "True"])
    axis.grid()
    axis.legend()

# Export the computed Euler angles to a CSV file for further analysis or record-keeping.
with open('euler_angles.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Roll', 'Pitch', 'Yaw'])  # Header row.
    for i in range(len(timestamp)):
        writer.writerow([timestamp[i], euler[i, 0], euler[i, 1], euler[i, 2]])  # Data rows.

# Execute additional Python code from 'theoreticalvseuler.py', potentially for comparison or further analysis.
with open(theoretical_vs_euler_path) as file:
    exec(file.read())

# Set up the plotting environment to visualize the Euler angles, internal states, and flags over time.
figure, axes = pyplot.subplots(nrows=11, sharex=True, gridspec_kw={"height_ratios": [6, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1]})
figure.suptitle("Euler angles, internal states, and flags")

# Plot Euler angles (Roll, Pitch, Yaw) over time using different colors for each angle.
axes[0].plot(timestamp, euler[:, 0], "tab:red", label="Roll")
axes[0].plot(timestamp, euler[:, 1], "tab:green", label="Pitch")
axes[0].plot(timestamp, euler[:, 2], "tab:blue", label="Yaw")
axes[0].set_ylabel("Degrees")
axes[0].grid()
axes[0].legend()

# Plot various flags and internal states to provide insight into the AHRS algorithm's behavior and decision-making process.
plot_bool(axes[1], timestamp, flags[:, 0], "Initialising")
plot_bool(axes[2], timestamp, flags[:, 1], "Angular rate recovery")
axes[3].plot(timestamp, internal_states[:, 0], "tab:olive", label="Acceleration error")
plot_bool(axes[4], timestamp, internal_states[:, 1], "Accelerometer ignored")
axes[5].plot(timestamp, internal_states[:, 2], "tab:orange", label="Acceleration recovery trigger")
plot_bool(axes[6], timestamp, flags[:, 2], "Acceleration recovery")
axes[7].plot(timestamp, internal_states[:, 3], "tab:olive", label="Magnetic error")
plot_bool(axes[8], timestamp, internal_states[:, 4], "Magnetometer ignored")
axes[9].plot(timestamp, internal_states[:, 5], "tab:orange", label="Magnetic recovery trigger")
plot_bool(axes[10], timestamp, flags[:, 3], "Magnetic recovery")

# Display the plot, ensuring it doesn't block the execution if running in certain environments (e.g., continuous integration systems).
pyplot.show(block="no_block" not in sys.argv)
