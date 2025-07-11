import atexit
import os

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

import robot.constants as const

matplotlib.use("TkAgg")


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)
    else:
        print(file)


class PointOfApp:

    def __init__(self):
        # create plots for point of application
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.square = FancyBboxPatch(
            (-5, -5), 10, 10, alpha=0.5, boxstyle="round,pad=3"
        )
        self.ax.add_patch(self.square)
        self.ax.set_xlim(-12, 12)
        self.ax.set_ylim(-12, 12)
        (self.point,) = self.ax.plot(0, 0, "ro", markersize=10)

        animation.FuncAnimation(self.fig, self.animate, fargs=(), interval=1)
        plt.show()

        atexit.register(delete_file, const.TEMP_FILE)

    def animate(self, i):
        """
        Loop to read live sensor data and perform relevant operations.

        """
        if os.path.exists(const.TEMP_FILE) and os.path.getsize(const.TEMP_FILE) > 0:
            with open(const.TEMP_FILE, "rb") as file:
                try:  # catch OSError in case of a one line file
                    file.seek(-2, os.SEEK_END)
                    while file.read(1) != b"\n":
                        file.seek(-2, os.SEEK_CUR)
                except OSError:
                    file.seek(0)
                data = file.readline().decode()

            data = data[data.find("[") + 1 : data.find("]")]
            data = np.array(data.split(", "), dtype="float64")

            self.point.set_data(data[0], data[1])

            # Redraw the plot
            self.fig.canvas.draw()
        else:
            pass


if __name__ == "__main__":
    PointOfApp()
