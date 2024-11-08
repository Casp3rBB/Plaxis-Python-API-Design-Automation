import plxscripting
import os
import re
from datetime import datetime
from typing import List

s_o = s_o
g_o = g_o

# Author = Kinen Ma
# Version_date = 2024-04-12

def SectionVaryAlongXY():
    to_vary = input('Cross section cut vary along x or y: ').lower()

    if to_vary == 'x':
        x1 = float(input('Enter start x: '))
        x2 = float(input('Enter end x: '))
        y1 = float(input('Enter y1: '))
        y2 = float(input('Enter y2: '))
    elif to_vary == 'y':
        x1 = float(input('Enter x1: '))
        x2 = float(input('Enter x2: '))
        y1 = float(input('Enter start y: '))
        y2 = float(input('Enter end y: ')) 
    else:
        print('Please enter x or y only')
        0/0

    increment = float(input('Please enter increment in meter: '))

    print('x, phase 1 min, phase 1 max, phase 2 min, phase 2 max')

    if to_vary == 'x':
        while x1 < x2:
            g_o.linecrosssectionplot(g_o.Plot_1, (x1, y1), (x1, y2))
            s1 = g_o.getcrosssectionresults(g_o.Plots[-1], g_o.Phases[2], g_o.ResultTypes.Soil.SigxxT)
            s1_max = max(s1)
            s1_min = min(s1)
            s2 = g_o.getcrosssectionresults(g_o.Plots[-1], g_o.Phases[13], g_o.ResultTypes.Soil.SigxxT)
            s2_max = max(s2)
            s2_min = min(s2)
            # g_o.delete(g_o.Plots[-1])
            print('SigxxT')
            print(x1, s1_min, s1_max, s2_min, s2_max, sep=',')
            x1 += increment
    elif to_vary == 'y':
        while y1 < y2:
            g_o.linecrosssectionplot(g_o.Plot_1, (x1, y1), (x1, y2))
            s1 = g_o.getcrosssectionresults(g_o.Plots[-1], g_o.Phases[2], g_o.ResultTypes.Soil.SigyyT)
            s1_max = max(s1)
            s1_min = min(s1)
            s2 = g_o.getcrosssectionresults(g_o.Plots[-1], g_o.Phases[13], g_o.ResultTypes.Soil.SigyyT)
            s2_max = max(s2)
            s2_min = min(s2)
            # g_o.delete(g_o.Plots[-1])
            print('SigyyT')
            print(x1, s1_min, s1_max, s2_min, s2_max, sep=',')
            y1 += increment


def Section_StageByStage():

    x1 = float(input('Enter x1: '))
    x2 = float(input('Enter x2: '))
    y1 = float(input('Enter y1: '))
    y2 = float(input('Enter y2: '))
    x_or_y = input('Enter x or y for Total stress on x or y direction: ')

    print('Phase, Normal_Total_Stress_Min, Normal_Total_Stress_Max')

    g_o.linecrosssectionplot(g_o.Plot_1, (x1, y1), (x2, y2))
    
    for phase in g_o.Phases:
        if x_or_y == 'x':
            s1 = g_o.getcrosssectionresults(g_o.Plots[-1], phase, g_o.ResultTypes.Soil.SigxxT)
        elif x_or_y == 'y':
            s1 = g_o.getcrosssectionresults(g_o.Plots[-1], phase, g_o.ResultTypes.Soil.SigyyT)
        else: 
            0/0
        s1_max = max(s1)
        s1_min = min(s1)
        
        print(str(phase.Identification).replace('['+str(phase.Name+']'), '').replace(',', '_'), s1_min, s1_max, sep=',')

    print('Total stress result on the {} direction', x_or_y)

