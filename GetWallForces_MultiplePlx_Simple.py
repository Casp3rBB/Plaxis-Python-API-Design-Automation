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

def BatchExtractWallForce_Simple():
    models = []
    get_input(models)
            
    print('===================================')
    print('Plaxis file, Plate no, X Max, X Min, Y Max, Y Min, M Max, M Min, Q Max, Q Min, Ux Max, Ux Min')

    for model in models:
        s_o.open(model)
        
        model_name = os.path.basename(model).replace(',', '')

        for i, plate in enumerate(g_o.Plates):
            moment_max = g_o.getresults(plate, g_o.Phases[-1], g_o.ResultTypes.Plate.M_EnvelopeMax2D, 'node')
            moment_min = g_o.getresults(plate, g_o.Phases[-1], g_o.ResultTypes.Plate.M_EnvelopeMin2D, 'node')
            shear_max = g_o.getresults(plate, g_o.Phases[-1], g_o.ResultTypes.Plate.Q_EnvelopeMax2D, 'node')
            shear_min = g_o.getresults(plate, g_o.Phases[-1], g_o.ResultTypes.Plate.Q_EnvelopeMin2D, 'node')
            x_coor = g_o.getresults(plate, g_o.Phases[-1], g_o.ResultTypes.Plate.X, 'node')
            y_coor = g_o.getresults(plate, g_o.Phases[-1], g_o.ResultTypes.Plate.Y, 'node')
            ux = g_o.getresults(plate, g_o.Phases[-1], g_o.ResultTypes.Plate.Ux, 'node')

            moment_max = max(moment_max)
            moment_min = min(moment_min)
            shear_max = max(shear_max)
            shear_min = min(shear_min)
            x_max = max(x_coor)
            x_min = min(x_coor)
            y_max = max(y_coor)
            y_min = min(y_coor)
            ux_max = max(ux)
            ux_min = min(ux)

            print(','.join(list(map(str, [model_name, i+1, x_max, x_min, y_max, y_min ,moment_max, moment_min, shear_max, shear_min, ux_max, ux_min]))))
        
        s_o.close()


def ExtractStageByStageWallForce_Simple():
            
    print('===================================')
    print('Plaxis file, Plate no, X Max, X Min, Y Max, Y Min, M Max, M Min, Q Max, Q Min, Ux Max, Ux Min')

    for phase in g_o.Phases:
        for i, plate in enumerate(g_o.Plates):
            try:
                moment_max = g_o.getresults(plate, phase, g_o.ResultTypes.Plate.M_EnvelopeMax2D, 'node')
                moment_min = g_o.getresults(plate, phase, g_o.ResultTypes.Plate.M_EnvelopeMin2D, 'node')
                shear_max = g_o.getresults(plate, phase, g_o.ResultTypes.Plate.Q_EnvelopeMax2D, 'node')
                shear_min = g_o.getresults(plate, phase, g_o.ResultTypes.Plate.Q_EnvelopeMin2D, 'node')
                x_coor = g_o.getresults(plate, phase, g_o.ResultTypes.Plate.X, 'node')
                y_coor = g_o.getresults(plate, phase, g_o.ResultTypes.Plate.Y, 'node')
                ux = g_o.getresults(plate, phase, g_o.ResultTypes.Plate.Ux, 'node')

                moment_max = max(moment_max)
                moment_min = min(moment_min)
                shear_max = max(shear_max)
                shear_min = min(shear_min)
                x_max = max(x_coor)
                x_min = min(x_coor)
                y_max = max(y_coor)
                y_min = min(y_coor)
                ux_max = max(ux)
                ux_min = min(ux)

                print(','.join(list(map(str, [str(phase.Identification), i+1, x_max, x_min, y_max, y_min ,moment_max, moment_min, shear_max, shear_min, ux_max, ux_min]))))
                pass
            
            except plxscripting.plx_scripting_exceptions.PlxScriptingError:
                pass

if __name__ == '__main__':
    BatchExtractWallForce_Simple()
