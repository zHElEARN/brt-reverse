import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_acceleration_data():
    data_path = Path("data/acc_data.npz")
    if not data_path.exists():
        print("Acceleration data file not found.")
        return

    acc_data = np.load(data_path, allow_pickle=True)
    min_length = min(len(acc_data["x"]), len(acc_data["y"]), len(acc_data["z"]))

    plt.figure(figsize=(12, 6))
    plt.plot(
        np.arange(min_length),
        acc_data["x"][:min_length],
        color="#e74c3c",
        alpha=0.7,
        label="X-axis",
    )
    plt.plot(
        np.arange(min_length),
        acc_data["y"][:min_length],
        color="#2ecc71",
        alpha=0.7,
        label="Y-axis",
    )
    plt.plot(
        np.arange(min_length),
        acc_data["z"][:min_length],
        color="#3498db",
        alpha=0.7,
        label="Z-axis",
    )

    plt.title(f"Triaxial Acceleration (Points: {min_length})", fontsize=14)
    plt.xlabel("Data Points", fontsize=12)
    plt.ylabel("Acceleration (g)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_acceleration_data()
