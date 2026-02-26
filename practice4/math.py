import math
#1
degree = 15
radian = degree * math.pi / 180
print( round(radian, 6))

#2
height = 5
base1 = 5
base2 = 6
trapezoid_area = (base1 + base2) / 2 * height
print(trapezoid_area)

#3
n = 4
a = 25
polygon_area = (n * a**2) / (4 * math.tan(math.pi / n))
print( int(polygon_area))

#4
base = 5
height_para = 6
parallelogram_area = base * height_para
print( float(parallelogram_area))