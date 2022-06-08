import numpy as np
import pandas as pd
from py2opt.routefinder import RouteFinder
import matplotlib.pyplot as plt


def tops(x,w):
    av = np.empty(len(x))
    for index,val in enumerate(x[w:-w]):
        av[index+w] = np.max(x[index:index+w])

    av[:w] = np.max(x[:w])
    av[-w:] = np.max(x[-w:])
    return av   

def moving_average(x, w):
    return np.convolve(x, np.ones(w), mode='same') / w

def optimal_path(sensor_df,dlat,dlon,range_weight,cruise_alt):
    points = sensor_df[["lat","lon"]].values
    altitudes = sensor_df["elevation"].values
    R_matrix = np.empty((len(points),len(points)))
    h_matrix = np.empty((len(points),len(points)))
    for index,point in enumerate(points):
        distances = np.sqrt(np.sum((points-point)**2,axis=1))
        arg = np.argwhere(distances > 10./dlon).flatten()
        altitude_shifts = np.array(np.abs(altitudes - altitudes[index]),dtype=float)
        R_matrix[index,:] = distances
        h_matrix[index,:] = altitude_shifts

    Rmax,hmax = np.max(R_matrix[np.isfinite(R_matrix)]) ,  np.max(h_matrix[np.isfinite(h_matrix)])
    matrix = range_weight*R_matrix/Rmax +(1-range_weight)*h_matrix/hmax
    route_finder = RouteFinder(list(matrix),list(np.arange(len(points))), iterations=20)
    best_distance, best_route = route_finder.solve()
    return np.array(best_route,dtype=int)

            
