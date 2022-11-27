import numpy as np

def get_random_points_in_circle(n, radius):
    """
    Get (x, y) coordinate of random points in a circle of radius radius
    Returns array (n, 2)

    parameters:
    n: int
        number of points to generate
    radius: float
        radius of circle to put points in
    """
    r = radius * np.sqrt(np.random.uniform(size=n))
    theta = 2 * np.pi * np.random.uniform(size=n)
    return np.vstack((r * np.cos(theta), r * np.sin(theta))).T

def get_small_err(n, scale):
    """
    Generate (x, y) corrdinate of random points obeys 2d Gaussian distribution
    to simulate ramdon error of position reconstruction

    parameters:
    n: int
        number of points to generate
    scale: float
        std of the Gaussian distribution
    """
    return np.random.normal(scale = scale, size = (n,2))