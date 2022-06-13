from math import *

class sensors:
    def __init__(self, height, width, thickness):
        self.height = height
        self.width = width
        self.thickness = thickness
        self.volume = self.height*self.width*self.thickness



    def packing_configuartions(self, number_of_sensors):
        sensor_configs = dict()
        for i in range(number_of_sensors):
            for j in range(number_of_sensors):
                for k in range(number_of_sensors):
                    if i*j*k == number_of_sensors:
                        if not(str(str(min(i,j))+"-"+str(max(i,j))+"-"+str(k)) in sensor_configs.keys()):
                            sensor_configs[str(str(min(i,j))+"-"+str(max(i,j))+"-"+str(k))] = round(self.packing_dimensions_sum(i,j,k),3)
        
        sensor_configs = {k: v for k, v in sorted(sensor_configs.items(), key=lambda item: item[1])}


        return sensor_configs

    def packing_dimensions_sum(self,i,j,k):
        return self.height*i+self.width*j+self.thickness*k


    def spool_sizing(self, number_of_sensors):
        r = 0.1
        spool_width = 4*self.width
        tape_length = (number_of_sensors*self.height + number_of_sensors*0.01)/4
        while tape_length > 0:
            tape_length -= pi*r**2
            r += self.thickness
            print(tape_length, r, "loop")
        print(tape_length, r, spool_width)

    def spool_volume(self, spool_width, thickness, innerd, outerd, density):
        disk_vol = pi*outerd**2/4*thickness
        hollow_cylinder_vol = (pi*innerd**2/4 - pi*(innerd-2*thickness)**2/4)*spool_width
        volume =  2*disk_vol + hollow_cylinder_vol
        mass = volume*density
        print(volume, mass)

sensor = sensors(height=0.065, width=0.85, thickness=0.04)
# efficient_packing_cofigs = sensor.packing_configuartions(648)
# sensor.spool_sizing(551)
sensor.spool_volume(0.445, 0.004, 0.03, 0.31, 1250)
# dimensions = list(efficient_packing_cofigs.keys())
# for i in range(10):
#     x,y,z = dimensions[i].split("-")
#     x,y,z = int(x), int(y), int(z)
#     print(f"Configuration {i+1}:")
#     print(f"Packing:{x}x{y}x{z}")
#     print(f"Dimensions:{sensor_1.height*x}x{sensor_1.width*y}x{sensor_1.thickness*z}\n")
