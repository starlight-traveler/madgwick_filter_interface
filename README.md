# Sensor Fusion and Visualization Project

This project utilizes sensor data to compute and visualize Euler angles using the IMUFusion library. It processes data from gyroscopes, accelerometers, and magnetometers to estimate orientation, visualizing these estimations alongside internal algorithm states and recovery flags.

## Key Features

- Sensor data normalization and scaling for clarity.
- Recovery trigger visualization for insight into algorithm behavior.
- Euler angle computation and visualization for orientation estimation.

## Getting Started

### Prerequisites

- Python 3.x
- Libraries: IMUFusion, Matplotlib, Numpy, CSV, and OS

### Installation

Clone the repository to your local machine:

```bash
git clone (https://github.com/starlight-traveler/madgwick_filter_interface.git)
cd your-repository-directory/madgwick_filter_interface
```

Install the required Python libraries:

```bash
pip install matplotlib numpy
```

Note: `imufusion` might need to be installed from a specific source or configured according to your sensor setup.

### Usage

1. Place your sensor data file named `rocketryLaunch.csv` in the `csvFiles` directory relative to the script. Ensure the data is structured with timestamps, gyroscope, accelerometer, and magnetometer readings.

2. (Optional) Modify the `theoreticalvseuler.py` script for any additional data processing or analysis.

3. Run the main script:

```bash
python pitch_calculation.py
```

This will generate Euler angle visualizations alongside the algorithm's internal states and flags.

## Data Considerations

- **Recovery Triggers**: The second graph highlights the algorithm's response to sensor anomalies, crucial for understanding its behavior.
- **Normalization**: Data is normalized to start at 0 degrees on the y-axis. Adjust the y-axis accordingly when comparing with theoretical models.
- **Scaling**: Adjust the graph scaling to improve readability and interpretability.

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. Special thanks to the IMUFusion theme for excellent documentation.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
