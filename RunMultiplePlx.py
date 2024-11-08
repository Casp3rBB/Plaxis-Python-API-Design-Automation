import plxscripting
import os
import re
from datetime import datetime
from typing import List

s_i = s_i
g_i = g_i

# Author = Kinen Ma
# Version_date = 2023-11-17

def split_string(s):
    return [x.strip().strip("'") for x in re.split(",(?=(?:[^']*'[^']*')*[^']*$)", s)]

def BatchCalculate():

    models = []
    while True:
        files = input('({} nos.) Please enter full file path, enter "done" to end: '.format(len(models)))
        file = split_string(files)
        if file[0].lower() == 'done': 
            break
        else: 
            for x in file:
                models.append(x)

    t0 = datetime.now()
    t1 = datetime.now()

    for i, model in enumerate(models):
        print('Running model {} out of {}'.format(i+1, len(models)))
        
        s_i.open(model)
        g_i.calculate()
        g_i.save()

        t_now = datetime.now()
        print('Model run time: {} \t Total run time: {}'.format(t_now-t1, t_now-t0))
        t1 = t_now


if __name__ == '__main__':
    BatchCalculate()
