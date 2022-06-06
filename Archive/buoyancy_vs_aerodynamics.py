CD0 = self.CD
ilist = np.arange(0, 10, 1)
ratios = []
T0 = self.cruise_thrust
T = T0
for i in ilist:
    self.gondola.z_cg = - self.radius - self.gondola.height / 2
    self.gondola.x_cg = -0.44
    self.z_eng = self.gondola.z_cg
    self.x_eng = self.gondola.x_cg
    self.estimateCG()
    alpha = (T * self.z_eng - self.MTOM * g * self.x_cg) / (self.MTOM * g * self.z_cg)
    CL = alpha * 2 / 3
    CDL = CL ** 2
    self.CD = CD0 + CDL
    T = self.CD / CD0 * T0
    print('alpha', 57.3 * alpha)
    print('thrust', T)
    L = CL * 0.5 * rho * self.cruiseV ** 2 * self.ref_area
    ratio = 1 - L / (self.MTOM * g)
    print('Ratio: ', ratio)
    self.MTOM = ratio * self.MTOM
    self.sizeBalloon()
    self.MTOM = sum(self.mass.values())
    ratios.append(ratio)
plt.plot(ilist, ratios)
plt.grid()
plt.show()