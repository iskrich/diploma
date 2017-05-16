import matplotlib.pyplot as plt

def draw_series(series):
    plt.figure()
    series.plot()
    plt.interactive(False)
    plt.show()