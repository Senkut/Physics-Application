import math
from core.constants import PPM
# IMPORANTES SE SUELE USAR COMO TIEMPO dt QUE ES DELTA TIME  PARA QUE EL MOVIENTO SEA FLUIDO
"""
x =  posicion final    (metros)
x0 = posicion inicial  (metros)
v = velocidad final    (mestros/segundos)
v0 = velocidad incial  (metros/segundos)
a = aceleracion        (mestros/(segundos)^2)
t = tiempo             (segundos)
"""

def mru_pos(x0, v , t):
    return x0 +  (v * t)*PPM
 
def mrua_pos(x0, v0, a, t):
   x =(v0 * t )+ (0.5 * a * (t**2))
   return x0 + x*PPM
def mrua_vel(v0, a , t):
    return v0 + a * t

def circular_pos(center, radius, angle):
    x = center.x + radius * math.cos(angle)
    
    y = center.y + radius * math.sin(angle)
    
    return x, y