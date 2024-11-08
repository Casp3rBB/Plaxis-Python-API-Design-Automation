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

def get_phase():
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


def BatchExtractStrutForce_Simple():
    models = []
    get_input(models)
            
    print('===================================')
    print('Plaxis file, Phase, Strut no, X, Y, Force')

    for model in models:
        s_o.open(model)
        
        model_name = os.path.basename(model).replace(',', '')

        phase = get_phase()
        phase_name = g_o.Phases[phase].Identification

        n2nX = []
        n2nY = []
        n2nM = []
        try:
            n2nX.extend(g_o.getresults(g_o.Phases[phase], g_o.ResultTypes.NodeToNodeAnchor.X, 'node'))
            n2nY.extend(g_o.getresults(g_o.Phases[phase], g_o.ResultTypes.NodeToNodeAnchor.Y, 'node'))
            n2nM.extend(g_o.getresults(g_o.Phases[phase], g_o.ResultTypes.NodeToNodeAnchor.AnchorForceMin2D, 'node'))
            pass
        except plxscripting.plx_scripting_exceptions.PlxScriptingError:
            pass
        
        try:
            n2nX.extend(g_o.getresults(g_o.Phases[phase], g_o.ResultTypes.FixedEndAnchor.X, 'node'))
            n2nY.extend(g_o.getresults(g_o.Phases[phase], g_o.ResultTypes.FixedEndAnchor.Y, 'node'))
            n2nM.extend(g_o.getresults(g_o.Phases[phase], g_o.ResultTypes.FixedEndAnchor.AnchorForceMin2D, 'node'))
            pass
        except plxscripting.plx_scripting_exceptions.PlxScriptingError:
            pass
        
        sortedzip = sorted(list(zip(n2nX, n2nY, n2nM)), key=lambda x: x[1], reverse=True)
        n2nX, n2nY, n2nM = list(zip(*sortedzip))

        for i in range(len(n2nM)):
            print(','.join(list(map(str, [model_name, phase_name, i+1, n2nX[i], n2nY[i], n2nM[i]]))))

        s_o.close()

def BatchExtractStrutForce_Full():
    models = []
    get_input(models)

    for model in models:
        s_o.open(model)
        
        s = StrutForceAutomation(-9999, 9999)
        
        s_o.close()

class Strut:
    def __init__(self, x, y, force):
        self.x = x
        self.y = y
        self.force = force

class PlxStrutForce:
    def __init__(self):
        self.arr_raw = []
        self.arr = []
        self.res = []
        self.phases = g_o.Phases
        self.t0 = datetime.now()
        self.plaxis_path = str(g_o.generalinfo.Filename)

    def GetUserInput(self):
        x1, x2 = [float(x) for x in input('Enter the range of the plaxis model by specifying the min_x and max_x you would like to consider, separated by a space in between (Only applies to strut force extraction): ').split()]
        print('Please wait, getting forces from Plaxis...')
        self.t0 = datetime.now()
        return x1, x2

    def GetStrutForces(self, x1=None, x2=None):
        if x1 == None or x2 == None:
            self.x1, self.x2 = self.GetUserInput()
        else:
            self.x1 = x1
            self.x2 = x2

        for phase in g_o.Phases:
            n2nX = []
            n2nY = []
            n2nM = []
            try:
                n2nX.extend(g_o.getresults(phase, g_o.ResultTypes.NodeToNodeAnchor.X, 'node'))
                n2nY.extend(g_o.getresults(phase, g_o.ResultTypes.NodeToNodeAnchor.Y, 'node'))
                n2nM.extend(g_o.getresults(phase, g_o.ResultTypes.NodeToNodeAnchor.AnchorForce2D, 'node'))
                pass
            except plxscripting.plx_scripting_exceptions.PlxScriptingError:
                pass
            
            try:
                n2nX.extend(g_o.getresults(phase, g_o.ResultTypes.FixedEndAnchor.X, 'node'))
                n2nY.extend(g_o.getresults(phase, g_o.ResultTypes.FixedEndAnchor.Y, 'node'))
                n2nM.extend(g_o.getresults(phase, g_o.ResultTypes.FixedEndAnchor.AnchorForce2D, 'node'))
                pass
            except plxscripting.plx_scripting_exceptions.PlxScriptingError:
                pass
            
            if n2nX == []:
                n2nX = ['-']
                n2nY = ['-']
                n2nM = ['-']

            length = len(n2nX)
            arr_to_append = []
            for i in range(length):
                if self.CheckWithinRange(n2nX[i]):
                    arr_to_append.append(Strut(n2nX[i], n2nY[i], n2nM[i]))
            self.arr.append(arr_to_append)

        self.arr_raw = self.arr.copy()
        self.MergeDuplicateY()

    def MergeDuplicateY(self):
        self.arr = []
        for stage in self.arr_raw:
            unique_instances = {}
            for a in stage:
                if a.y not in unique_instances:
                    unique_instances[a.y] = a
                elif a.force < unique_instances[a.y].force: # merge negative maximum strut force
                    unique_instances[a.y] = a
            self.arr.append(list(unique_instances.values()))

    def CheckWithinRange(self, x):
        if x == '-': 
            return False
        x = float(x)
        if x >= self.x1 and x <= self.x2: 
            return True
        else:
            return False

    def StrutLevels(self):
        s = set()
        for stage in self.arr:
            for x in stage: 
                if x.y != '-': s.add(x.y)
        return list(reversed(sorted(list(s))))

    def AppendLine(self, arr_to_append):
        self.res.append(','.join(map(str, arr_to_append)))

    def PrintStrutForce(self):
        print('time elapsed: {} seconds'.format(datetime.now()-self.t0))
        print('Please wait, processing...')
        strutlevels = self.StrutLevels()

        self.res = []
        print('================================')
        self.AppendLine(['#START_STRUTDATA#'])
        self.AppendLine(['Strut Layer'] + list(range(1, len(strutlevels)+1)))
        self.AppendLine(['Strut Level'] + strutlevels)

        for i in range(len(self.phases)):
            phase_name = str(self.phases[i].Identification).replace('[' + str(self.phases[i].Name) + ']', '').replace(',', '&')
            phase_forces_dict = {}
            phase_forces = []

            for j in self.arr[i]:
                phase_forces_dict[j.y] = j.force

            for strutlevel in strutlevels:
                if strutlevel in phase_forces_dict: 
                    phase_forces.append(phase_forces_dict[strutlevel])
                else: 
                    phase_forces.append('-')

            self.AppendLine([phase_name] + phase_forces)
        
        self.AppendLine(['#END_STRUTDATA#'])

        
        _ = [print(i) for i in self.res]
        plaxis_folder = os.path.dirname(self.plaxis_path)
        plaxis_name = os.path.basename(self.plaxis_path)
        datafile_name = '{}-{}.csv'.format(plaxis_name.replace('.p2dx', '_StrutForces_'), datetime.now().strftime('%Y%m%d,%H-%M-%S'))
        datafile_path = os.path.join(plaxis_folder, datafile_name)
        with open(datafile_path, 'w+') as f:
            _ = [f.writelines(x+'\n') for x in self.res]
        
        print('================================')
        print('time elapsed: {} seconds'.format(datetime.now()-self.t0))
        print('Data file saved here: \n{}'.format(datafile_path))

def StrutForceAutomation(x1=None, x2=None):
    f = PlxStrutForce()
    f.GetStrutForces(x1, x2)
    f.PrintStrutForce()

if __name__ == '__main__':
    BatchExtractStrutForce_Simple()

