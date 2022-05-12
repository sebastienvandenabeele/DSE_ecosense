from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import scipy
import random
from mayavi.mlab import *

plt.ioff()

def surface_area(a,b,c):
    p=1.6075
    return(4*np.pi*((((a*b)**p+(a*c)**p+(b*c)**p))/3)**(1/p))

def computeArea(pos):
    x, y = (zip(*pos))
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def angle(v1,v2):
    angle=np.arccos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
    return angle

def irradiance_distribution(blimp, angle_sun):
    
    
    # fig = plt.figure(figsize=plt.figaspect(1))
    # ax = fig.add_subplot(111, projection='3d')
    
    coefs = (blimp.spheroid_ratio**2, blimp.spheroid_ratio**2, 1)  
    rx, ry, rz = 1/np.sqrt(coefs)
    
    surface_total=surface_area(rx, ry, rz)
    
    length_factor=blimp.length_factor
    alpha=blimp.panel_angle
    surface=alpha/np.pi*surface_total*length_factor
    v = np.linspace(0, np.pi, 10)
    beta_vec=0
    alpha_vec=angle_sun
    # tot=[]
    # alp=[]
    # print(beta_vec)
    # for alpha_vec in np.radians(np.arange(15,62,1)):
    corr=0
    if (np.pi/2-abs(beta_vec))<alpha:
        # print("ye")
        corr=alpha-(np.pi/2-abs(beta_vec))
        if beta_vec > 0:
            u = np.linspace(-alpha+corr, alpha, 10)
        elif beta_vec <0:
            u = np.linspace(-alpha, alpha-corr, 10)
    else:
        u = np.linspace(-alpha, alpha, 10)
    
    if alpha>=np.pi/2:
        u=np.linspace(-np.pi/2,np.pi/2,10)
    
    x = rx * np.outer(np.cos(u), np.sin(v))
    y = ry * np.outer(np.sin(u), np.sin(v))
    z = rz * np.outer(np.ones_like(u), np.cos(v))
    z[z<=(length_factor*np.amin(z))]=0
    z[z>=(length_factor*np.amax(z))]=0

    vector=np.array([np.cos(alpha_vec) * np.cos(beta_vec),np.sin(beta_vec),np.sin(alpha_vec) * np.cos(beta_vec)])
    
    # X=[]
    proj_point=[]
    for i in range(len(x)):
        for j in range(len(x)):
            if z[i][j]!=0:
                # X.append([x[i][j],y[i][j],z[i][j]])
                point_vec=[x[i][j],y[i][j],z[i][j]]-vector
                dist=np.dot(point_vec,vector)
                proj=[x[i][j],y[i][j],z[i][j]]-dist*vector
                proj_point.append(proj)
        
    origin_point=np.array(proj_point[0])
    base_point=np.array(proj_point[1])
    base_vector=np.array(base_point-origin_point)
    
    
    twod_coords=[]
    twod_coords.append([0,0])
    twod_coords.append([np.linalg.norm(base_vector),0])
    for i in range(len(proj_point)-2):
        vector=proj_point[i+2]-origin_point
        # print(type(base_vector))
        ang=angle(vector,base_vector)
        l=np.linalg.norm(vector)
        twod_coords.append([np.cos(ang)*l,np.sin(ang)*l])
        
    twod_coords_temp=np.transpose(twod_coords)
    
    twod_coords=[]
    ind1=np.arange(0,10,1)
    ind2=np.arange(19,len(twod_coords_temp[0]),10)
    ind3=np.arange(len(twod_coords_temp[0])-2,len(twod_coords_temp[0])-11,-1)
    ind4=np.arange(len(twod_coords_temp[0])-20,0,-10)
    ind=np.concatenate([ind1,ind2,ind3,ind4])
    for i in ind:
        twod_coords.append([twod_coords_temp[0][i],twod_coords_temp[1][i]])
    twod_coords=np.transpose(twod_coords)
    
    # ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')
    
    # max_radius = max(rx, ry, rz)
    # for axis in 'xyz':
        # getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))
        
    # for i in proj_point:
        # ax.scatter(i[0],i[1],i[2])
        
    # plt.figure(2)
    polygon=[]
    polygon = plt.fill(twod_coords[0],twod_coords[1])
    area=computeArea(polygon[0].xy)
    
    
    # print(area)
    # print(surface)
    # print(area/surface)
    
    # alp.append(area/surface)
    # tot.concatenate((tot,np.transpose(alp)))
    # plt.close()
    # tot=np.transpose(tot)
    # print(tot)
    # print(area/surface)
    return area/surface

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# 
# ax.scatter(tot[0],tot[1],tot[2])    
# plt.show()

def plot_blimp(blimp):
    alpha=blimp.panel_angle
    length_factor=blimp.length_factor
    
    true_factor=np.arccos(length_factor/2)/np.pi    # fig = plt.figure(figsize=plt.figaspect(1))
    # ax = fig.add_subplot(111, projection='3d')
    
    coefs = (9, 9, 1)  
    rx, ry, rz = 1/np.sqrt(coefs)
    v_panel = np.linspace(0, np.pi, 100)
    u_panel = np.linspace(-alpha, alpha, 100)
    
    x_panel = np.array(rx * np.outer(np.cos(u_panel), np.sin(v_panel))*1.05)
    y_panel = np.array(ry * np.outer(np.sin(u_panel), np.sin(v_panel))*1.05)
    z_panel = np.array(rz * np.outer(np.ones_like(u_panel), np.cos(v_panel)))
    # factor_index=np.where(((length_factor*np.amin(z_panel))>z_panel)&(z_panel>(length_factor*np.amax(z_panel))))
    z_panel[z_panel<(length_factor*np.amin(z_panel))]=0
    z_panel[z_panel>(length_factor*np.amax(z_panel))]=0
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
    # ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', zorder=0.2)
        
    # max_radius = max(rx, ry, rz)
    # for axis in 'xyz':
        # getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))
    # plt.show()
