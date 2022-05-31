import numpy as np
from mayavi.mlab import *
import matplotlib.pyplot as plt
import pickle as pick

def unpickle(filename):
    with open('Pickle Shelf/' + filename, 'rb') as file:
        return pick.load(file)

avg_sun_elevation = 52  # [deg]
tmy = unpickle('tmy.txt')


def computeArea(pos):
    """
    Compute the area of a polygon determined by x,y coordinates.

    Parameters
    ----------
    pos : Array containing the x and y coordinates of a polygon

    Returns
    -------
    Surface area of polygon.

    """
    x, y = (zip(*pos))
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def angle(v1, v2):
    """
    Calculate the angle between two 3D vectors.

    Parameters
    ----------
    v1 : Vector 1 [x,y,z]
    v2 : Vector 2 [x,y,z]

    Returns
    -------
    angle : Angle between the input vectors in radians

    """
    angle = np.arccos(np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
    return angle


def projectPanel(blimp, angle_sun, n_iter):
    """
    Generate the projected surface ratio compared to the original surface.

    Parameters
    ----------
    blimp : blimp class
    angle_sun : Incident angle of the sun in radians

    Returns
    -------
    projected area/real area ratio

    """
    plt.ioff()
    beta_vec = 0
    alpha_vec = np.radians(angle_sun)

    # generate the ellipsoid coefficient and radii
    coefs = (blimp.spheroid_ratio**2, blimp.spheroid_ratio**2, 1)
    rx, ry, rz = 1/np.sqrt(coefs)
    rx=rx*blimp.length/2
    ry=ry*blimp.length/2
    rz=rz*blimp.length/2

    # calculate solar panel surface area
    length_factor = blimp.length_factor
    alpha = blimp.panel_angle/2
    # generate angle values for the polar solar panel coordinates
    v = np.linspace(0, np.pi, n_iter)
    corr = 0
    u = np.linspace(-alpha, alpha, n_iter)
    x_sample=rx * np.outer(np.cos(u), np.sin(v))
    # correct in case angle goes behind visual line
    if (beta_vec+np.pi/2) < alpha or (beta_vec-np.pi/2) < -alpha:
        corr = alpha-(np.pi/2-abs(beta_vec))
        if beta_vec > 0:
            u = np.linspace(-alpha+corr, alpha, n_iter)
        elif beta_vec < 0:
            u = np.linspace(-alpha, alpha-corr, n_iter)
        elif (beta_vec+np.pi/2) < alpha and (beta_vec-np.pi/2) < -alpha:
            u = np.linspace(beta_vec-np.pi/2, beta_vec+np.pi/2, n_iter)
    radius_dist=np.array([])
    for i in x_sample:
        radius_dist=np.append(radius_dist,max(i))
    # generate x,y,z coordinates
    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.outer(np.ones_like(u), np.cos(v))
    z[z <= (length_factor*np.amin(z))] = 0
    z[z >= (length_factor*np.amax(z))] = 0
    
    arc_len=radius_dist[z[0]!=0]*blimp.panel_angle
    dist=[]
    for i in range(len(z[0][z[0]!=0])-1):
        dist.append(z[0][z[0]!=0][i]-z[0][z[0]!=0][i+1])
        
    surface=sum(arc_len[:-1]*dist)
    # create solar incidence vector
    vector = np.array([np.cos(alpha_vec) * np.cos(beta_vec),
                      np.sin(beta_vec), np.sin(alpha_vec) * np.cos(beta_vec)])

    # project points on plane perpendicular to solar vector
    proj_point = []
    for i in range(len(x)):
        for j in range(len(x)):
            if z[i][j] != 0:
                q=[x[i][j], y[i][j], z[i][j]]
                p=vector*10
                n=vector
                proj = q - np.dot(q - p, n) * n
                proj_point.append(proj)
    proj_point=np.array(proj_point)
    origin_point = np.array(proj_point[0])
    base_point = np.array(proj_point[1])
    base_vector = np.array(base_point-origin_point)

    # generate 2D coordinates of the projected body
    twod_coords = []
    twod_coords.append([0, 0])
    twod_coords.append([np.linalg.norm(base_vector), 0])
    for i in range(len(proj_point)-2):
        vector2d = proj_point[i+2]-origin_point
        ang = angle(vector2d, base_vector)
        l = np.linalg.norm(vector2d)
        twod_coords.append([np.cos(ang)*l, np.sin(ang)*l])

    twod_coords_temp = np.transpose(twod_coords)
    
    twod_coords = []
    ind1 = np.arange(2*len(z[0][z[0] != 0]), 3*len(z[0][z[0] != 0]), 1)
    ind2 = np.arange(4*len(z[0][z[0] != 0])-1, len(twod_coords_temp[0])-2*len(z[0][z[0] != 0]), len(z[0][z[0] != 0]))
    ind3 = np.arange(
        len(twod_coords_temp[0])-2*len(z[0][z[0] != 0])-2, len(twod_coords_temp[0])-3*len(z[0][z[0] != 0]), -1)
    ind4 = np.arange(len(twod_coords_temp[0])-(3*len(z[0][z[0] != 0])), 2*len(z[0][z[0] != 0]), -len(z[0][z[0] != 0]))
    ind = np.concatenate([ind1, ind2, ind3, ind4])
    for i in ind:
        twod_coords.append([twod_coords_temp[0][i], twod_coords_temp[1][i]])
    twod_coords = np.transpose(twod_coords)

    # calculate area of the projected polygon
    polygon = []
    polygon = plt.fill(twod_coords[0], twod_coords[1])
    plt.close()
    area = computeArea(polygon[0].xy)
    
    return surface, area


def plot_blimp(blimp):
    """
    Plot the generated blimp in 3D

    Parameters
    ----------
    blimp : blimp class

    Returns
    -------
    None.

    """
    alpha = blimp.panel_angle
    length_factor = blimp.length_factor

    true_factor = np.arccos(length_factor/2)/np.pi
    # fig = plt.figure(figsize=plt.figaspect(1))
    # ax = fig.add_subplot(111, projection='3d')

    coefs = (9, 9, 1)
    rx, ry, rz = 1/np.sqrt(coefs)
    v_panel = np.linspace(0, np.pi, 100)
    u_panel = np.linspace(-alpha/2, alpha/2, 100)

    x_panel = np.array(rx * np.outer(np.cos(u_panel), np.sin(v_panel))*1.05)
    y_panel = np.array(ry * np.outer(np.sin(u_panel), np.sin(v_panel))*1.05)
    z_panel = np.array(rz * np.outer(np.ones_like(u_panel), np.cos(v_panel)))
    # factor_index=np.where(((length_factor*np.amin(z_panel))>z_panel)&(z_panel>(length_factor*np.amax(z_panel))))
    z_panel[z_panel < (length_factor*np.amin(z_panel))] = 0
    z_panel[z_panel > (length_factor*np.amax(z_panel))] = 0
    # print(np.shape(z_panel))
    # print(np.shape(z_panel[[factor_index[0]],[factor_index[1]]]))
    # print(np.amin(z_panel))
    # print(x_panel[factor_index[0]][factor_index[1]], y_panel[factor_index[0]][factor_index[1]], z_panel[factor_index[0]][factor_index[1]])
    mesh(x_panel, y_panel, z_panel, colormap='Blues')

    v = np.linspace(0, np.pi, 100)
    u = np.linspace(0, 2*np.pi, 100)

    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.outer(np.ones_like(u), np.cos(v))

    mesh(x, y, z, colormap="gray")
    show(blimp)
    # ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', zorder=0.2)

    # max_radius = max(rx, ry, rz)
    # for axis in 'xyz':
    # getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))
    # plt.show()

def sizeSolar(blimp, shone_area=0):
    """
    solar power estimation subroutine for iteration
    """
    blimp.area_solar, shone_area = projectPanel(blimp, avg_sun_elevation, 15)
    blimp.power_solar = (shone_area * np.mean(tmy["DNI"]) + blimp.area_solar * np.mean(tmy["DHI"])) * blimp.solar_cell.fillfac * blimp.solar_cell.efficiency
    blimp.mass['solar'] = blimp.area_solar * blimp.solar_cell.density * blimp.solar_cell.fillfac * 1.1 # margin for wiring

    if np.isnan(blimp.power_solar):
        blimp.power_solar = 0

    return blimp.area_solar, blimp.power_solar, blimp.mass['solar']



class Solarcell:
    def __init__(self, density, efficiency, width, length, area, fillfac, cost, Vmpp=0, Impp=0):
        """
        A class describing a solar cell type which can be used for the blimp
        :param density: [float] area density of solar cell [kg/m^2]
        :param efficiency: [float] solar panel efficiency (0.0-1.00) [-]
        :param width: [float] width of single solar cell [m]
        :param length: [float] length of single solar cell [m]
        :param area: [float] net area of single solar cell [m^2]
        :param fillfac: [float] fill factor, percentage of area used [-]
        :param cost: [float] unit cost of single solar cell [EUR]
        :param Vmpp: [float] Voltage at maximum power point [V]
        :param Impp: [float] Current at maximum power point [A]
        """
        self.density = density
        self.efficiency = efficiency
        self.width = width
        self.length = length
        self.area = area
        self.fillfac = fillfac
        self.cost = cost        #Unit cost in EUR


####################
# Solar Cell library
#####################

maxeon_gen3 = Solarcell(density=0.0425, efficiency=0.231, width=0.125, length=0.125, area=0.0153, fillfac=0.8, cost=3.33) #Ultra High Performance variant (conservative)
