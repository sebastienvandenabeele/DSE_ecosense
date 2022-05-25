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



sensor_1 = sensors(height=0.065, width=0.065, thickness=0.04)
efficient_packing_cofigs = sensor_1.packing_configuartions(648)

# x = {"1-2-3":5, "1-2-5": 6}
# dim = list(x.keys())
# print(dim)

dimensions = list(efficient_packing_cofigs.keys())
for i in range(10):
    x,y,z = dimensions[i].split("-")
    x,y,z = int(x), int(y), int(z)
    print(f"Configuration {i+1}:")
    print(f"Packing:{x}x{y}x{z}")
    print(f"Dimensions:{sensor_1.height*x}x{sensor_1.width*y}x{sensor_1.thickness*z}\n")
