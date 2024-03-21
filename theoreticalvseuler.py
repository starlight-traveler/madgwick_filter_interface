import pandas as pd
import matplotlib.pyplot as plt
import os

# Determine the directory of the currently executing script.
# This is useful for constructing file paths relative to the script's location,
# ensuring that the script runs correctly regardless of the current working directory.
current_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to the 'theoretical_angles.csv' file located within a subdirectory named 'csvFiles'.
# This approach allows for organized storage of data files related to the project.
theoretical_angles = os.path.join(current_dir, 'csvFiles/theoretical_angles.csv')

def load_csv(file_name):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    - file_name: The path to the CSV file to be loaded.

    Returns:
    - A pandas DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(file_name)

def plot_combined_data(df1, x1, y1, df2, x2, y2, title):
    """
    Plot data from two DataFrames on the same graph for comparison.

    Parameters:
    - df1: The first pandas DataFrame to plot.
    - x1: The column in df1 to use as the x-axis.
    - y1: The column in df1 to use as the y-axis.
    - df2: The second pandas DataFrame to plot.
    - x2: The column in df2 to use as the x-axis.
    - y2: The column in df2 to use as the y-axis.
    - title: The title of the plot.

    The function creates a plot with df1[x1] vs. df1[y1] and an adjusted plot of df2[x2] vs. df2[y2],
    where df2[x2] values are decreased by 24 and df2[y2] values are increased by 65 for visual comparison.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df1[x1], df1[y1], label=f'{y1} vs {x1} ({df1.name})')
    plt.plot(df2[x2] - 24, df2[y2] + 65, label=f'Adjusted {x2} vs Adjusted {y2} ({df2.name})')  # Adjust x2 by subtracting 24 and y2 by adding 65
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (Degrees)')
    plt.title(title)
    plt.legend()
    plt.show()

# Load the CSV files containing the Euler angles and theoretical angles data into pandas DataFrames.
# The .name attribute is used to assign a descriptive name to each DataFrame for use in the plot legend.
euler_angles = load_csv('euler_angles.csv')
theoretical_angles = load_csv(theoretical_angles)
euler_angles.name = 'Euler Angles'
theoretical_angles.name = 'Theoretical Angles'

# Plot the data from the two DataFrames on the same graph for comparison.
# The plot compares 'ORT' vs 'ORA' from the theoretical angles dataset with adjusted 'Timestamp' vs 'Pitch' from the Euler angles dataset.
plot_combined_data(theoretical_angles, 'ORT', 'ORA', euler_angles, 'Timestamp', 'Pitch', 
                   'Combined Plot of Theoretical and Euler Angles')
