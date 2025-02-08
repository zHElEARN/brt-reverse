import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def plot_ecg_data():
    data_path = Path("data/sport/ecg_data.npy")
    if not data_path.exists():
        print("ECG data file not found.")
        return

    ecg_data = np.load(data_path)
    total_points = len(ecg_data)

    plt.figure(figsize=(12, 6))
    plt.plot(
        np.arange(total_points),
        ecg_data,
        linewidth=0.5,
        color="#2ecc71",
        label=f"ECG Signal ({total_points} points)",
    )

    plt.title(f"ECG Signal Analysis (Total Points: {total_points})", fontsize=14)
    plt.xlabel("Data Points", fontsize=12)
    plt.ylabel("Voltage (mV)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_ecg_data()
