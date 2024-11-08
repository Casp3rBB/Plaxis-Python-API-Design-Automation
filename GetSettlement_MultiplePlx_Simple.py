import plxscripting
import os
import re
from datetime import datetime
from typing import List

s_o = s_o
g_o = g_o

# Author = Kinen Ma
# Version_date = 2024-03-06

def split_string(s):
    return [x.strip().strip("'") for x in re.split(",(?=(?:[^']*'[^']*')*[^']*$)", s)]

def get_input(models):
    while True:
        files = input('({} nos.) Please enter full file path, enter "done" to end: '.format(len(models)))
        file = split_string(files)
        if file[0].lower() == 'done': 
            break
        else: 
            for x in file:
                models.append(x)

def auto_get_phase():
    phase_FEL = -1
    phases = [x.Identification for x in g_o.Phases]
    
    for i, phase in enumerate(phases):
        if str(phase).find('FEL') != -1:
            phase_FEL = i
            break

    if phase_FEL == -1:
        return len(phases) - 1
    else:
        return phase_FEL

def choose_phase():
    print('Please choose which phase should the settlement be extracted,')
    print('Enter 1 for last stage')
    print('Enter 2 for first FEL stage')
    print('Enter 3 to choose other stages')
    sel = input('Please enter: ')
    if sel==1:
        return -1
    elif sel==2:
        return auto_get_phase()
    else:
        phases = [x.Identification for x in g_o.Phases]
        [print('{}: {}'.format(i, x)) for i, x in enumerate(phases)]
        sel_phase = input('Please choose which phase should the settlement be extracted: ') #updated needed for each model selection
        return sel_phase

def BatchExtractSettlement_Simple():
    models = []
    get_input(models)

    y = float(input('enter y level for settlement: '))
    x_split = float(input('enter x position where the settlement of LHS and RHS should split (i.e. any x within the cofferdam): '))
    phase_index = choose_phase()

    print('===================================')
    print('Plaxis file, LHS x max, LHS Uy max, LHS x atwall, LHS Uy atwall, RHS x max, RHS Uy max, RHS x atwall, RHS Uy atwall')

    for model in models:
        s_o.open(model)
        
        model_name = os.path.basename(model).replace(',', '')

        # Result for LHS
        g_o.linecrosssectionplot(g_o.Plot_1, (-1000, y), (x_split, y))
        x_coor = g_o.getcrosssectionresults(g_o.Plots[-1], g_o.Phases[-1], g_o.ResultTypes.Soil.X)
        uy = g_o.getcrosssectionresults(g_o.Plots[-1], g_o.Phases[-1], g_o.ResultTypes.Soil.Uy)
        LHS_x_max, LHS_uy_max = min(zip(x_coor, uy), key=lambda x: x[1])
        LHS_x_atwall = x_coor[-1]
        LHS_uy_atwall = uy[-1]

        # Result for RHS
        g_o.linecrosssectionplot(g_o.Plot_1, (x_split, y), (1000, y))
        x_coor = g_o.getcrosssectionresults(g_o.Plots[-1], g_o.Phases[-1], g_o.ResultTypes.Soil.X)
        uy = g_o.getcrosssectionresults(g_o.Plots[-1], g_o.Phases[-1], g_o.ResultTypes.Soil.Uy)
        RHS_x_max, RHS_uy_max = min(zip(x_coor, uy), key=lambda x: x[1])
        RHS_x_atwall = x_coor[0]
        RHS_uy_atwall = uy[0]

        print(','.join(list(map(str, [model_name, LHS_x_max, LHS_uy_max, LHS_x_atwall, LHS_uy_atwall, RHS_x_max, RHS_uy_max, RHS_x_atwall, RHS_uy_atwall]))))
    
        s_o.close()
