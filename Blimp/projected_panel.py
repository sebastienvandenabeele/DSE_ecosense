from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import scipy
import random

plt.ioff()

def surface_area(a,b,c,p):
    return(4*np.pi*((((a*b)**p+(a*c)**p+(b*c)**p))/3)**(1/p))

def computeArea(pos):
    x, y = (zip(*pos))
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def angle(v1,v2):
    angle=np.arccos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)))
    return angle

p=1.6075
ind=[0,1,2,3,4,5,6,7,8,9,19,29,39,49,59,69,79,89,99,98,97,96,95,94,93,92,91,90,80,70,60,50,40,30,20,10]


# fig = plt.figure(figsize=plt.figaspect(1))
# ax = fig.add_subplot(111, projection='3d')

coefs = (9, 9, 1)  
rx, ry, rz = 1/np.sqrt(coefs)

surface_total=surface_area(rx, ry, rz, p)

length_factor=0.8
alpha=np.radians(30)
surface=alpha/np.pi*surface_total*length_factor
true_factor=np.arcsin(length_factor/2)/np.pi
v = np.linspace(np.pi/2-np.pi*true_factor, np.pi/2+np.pi*true_factor, 10)

tot=[]
for beta_vec in np.radians(np.arange(15,62,1)):
    alp=[]
    # print(beta_vec)
    for alpha_vec in np.radians(np.arange(15,62,1)):
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
        
        
        x = rx * np.outer(np.cos(u), np.sin(v))
        y = ry * np.outer(np.sin(u), np.sin(v))
        z = rz * np.outer(np.ones_like(u), np.cos(v))

        vector=np.array([np.cos(alpha_vec) * np.cos(beta_vec),np.sin(beta_vec),np.sin(alpha_vec) * np.cos(beta_vec)])
        
        # X=[]
        proj_point=[]
        for i in range(len(x)):
            for j in range(len(x)):
                # X.append([x[i][j],y[i][j],z[i][j]])
                point_vec=[x[i][j],y[i][j],z[i][j]]-vector
                dist=np.dot(point_vec,vector)
                proj=[x[i][j],y[i][j],z[i][j]]-dist*vector
                proj_point.append(proj)
            
        origin_point=np.array(proj_point[0])
        base_point=np.array(proj_point[1])
        base_vector=base_point-origin_point
        
        
        twod_coords=[]
        twod_coords.append([0,0])
        twod_coords.append([np.linalg.norm(base_vector),0])
        for i in range(len(proj_point)-2):
            vector=proj_point[i+2]-origin_point
            ang=angle(vector,base_vector)
            l=np.linalg.norm(vector)
            twod_coords.append([np.cos(ang)*l,np.sin(ang)*l])
            
        twod_coords_temp=np.transpose(twod_coords)
        
        twod_coords=[]
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
        plt.close()
        
        # print(area)
        # print(surface)
        # print(area/surface)
        
        alp.append([alpha_vec,beta_vec,area/surface])
    tot.append(alp)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
tot=np.transpose(tot)
ax.scatter(tot[0],tot[1],tot[2])    
plt.show()