import plxscripting
import os
from datetime import datetime
from typing import List

# Made by Kinen Ma 2023-05-23
# Version 4.0, 2023-09-06

g_o = g_o
s_o = s_o

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


class Wall:
    def __init__(self, X, Y, M, V, N, Ux, Uy): #expect a list of nodes along a wall
        self.X = X
        self.Y = Y
        self.M = M
        self.V = V
        self.N = N
        self.Ux = Ux
        self.Uy = Uy
    
    def Attribute_to_list(self):
        return [[i,j,k,l,m,n,o] for i,j,k,l,m,n,o in zip(self.X, self.Y, self.M, self.V, self.N, self.Ux, self.Uy)]

class WallGeometry:
    def __init__(self, X1, Y1, X2, Y2): #expect the two edge points of a wall only
        self.X1 = X1
        self.Y1 = Y1
        self.X2 = X2
        self.Y2 = Y2
    
    def Attribute_to_list(self):
        return([self.X1, self.X2, self.Y1, self.Y2])

class PlxWallForce:
    def __init__(self):
        self.t0 = datetime.now()
        self.phases = g_o.Phases
        self.plates = g_o.Plates
        self.arrWalls = [[] for _ in range(len(self.phases))] #[Phase][Wall]
        self.arrWallsGeometry = [WallGeometry(0, 0, 0, 0) for _ in range(len(self.plates))]
        self.arrWallsGeometryMerged = []
        self.mergedWallDict = {} # dict{plate no. : merged plate no.}
        self.res = [] #result output
        self.plaxis_path = str(g_o.generalinfo.Filename)
        self.phases_name = [str(x.Identification).replace('[' + str(x.Name) + ']', '').replace(',', '&') for x in self.phases]

        
    def GetWallForces(self):
        print('Please wait, getting forces from Plaxis...')
        for index, phase in enumerate(self.phases):
            for plate in self.plates:
                try:
                    plate_X = g_o.getresults(plate,phase,g_o.ResultTypes.Plate.X, "node")
                    plate_Y = g_o.getresults(plate,phase,g_o.ResultTypes.Plate.Y, "node")
                    plate_M = g_o.getresults(plate,phase,g_o.ResultTypes.Plate.M2D, "node")
                    plate_V = g_o.getresults(plate,phase,g_o.ResultTypes.Plate.Q2D, "node")
                    plate_N = g_o.getresults(plate,phase,g_o.ResultTypes.Plate.Nx2D, "node")
                    plate_Ux = g_o.getresults(plate,phase,g_o.ResultTypes.Plate.Ux, "node")
                    plate_Ux = [x*1000 for x in plate_Ux]
                    plate_Uy = g_o.getresults(plate,phase,g_o.ResultTypes.Plate.Uy, "node")
                    plate_Uy = [x*1000 for x in plate_Uy]

                except plxscripting.plx_scripting_exceptions.PlxScriptingError:
                    plate_X = []
                    plate_Y = []
                    plate_M = []
                    plate_V = []
                    plate_N = []
                    plate_Ux = []
                    plate_Uy = []
                
                this_plate = Wall(plate_X, plate_Y, plate_M, plate_V, plate_N, plate_Ux, plate_Uy)
                self.arrWalls[index].append(this_plate)

    def GetWallGeometry(self): #expect GetWallForces has already been executed 
        for i, phase in enumerate(self.phases):
            for j, plate in enumerate(self.plates):
                if self.arrWalls[i][j].X != []:
                    x1 = self.arrWalls[i][j].X[0]
                    y1 = self.arrWalls[i][j].Y[0]
                    x2 = self.arrWalls[i][j].X[-1]
                    y2 = self.arrWalls[i][j].Y[-1]
                    if self.arrWallsGeometry[j] == None:
                        self.arrWallsGeometry[j] = WallGeometry(x1, y1, x2, y2)
                    elif self.Distance(x1, y1, x2, y2) > self.Distance(wallgeo=self.arrWallsGeometry[j]):
                        self.arrWallsGeometry[j] = WallGeometry(x1, y1, x2, y2)

    def Distance(self, x1=None, y1=None, x2=None, y2=None, wallgeo=None):
        if wallgeo == None:
            return((x2-x1)**2 + (y2-y1)**2)**0.5
        else:
            x1 = wallgeo.X1
            y1 = wallgeo.Y1
            x2 = wallgeo.X2
            y2 = wallgeo.Y2
            return((x2-x1)**2 + (y2-y1)**2)**0.5
        
    def IsPlateContinous(self, p1:WallGeometry, p2:WallGeometry):
        def PlateAngle(p:WallGeometry):
            if p.X1 == p.X2:
                return 'vertical'
            else:
                return abs((p.Y2-p.Y1)/(p.X2-p.X1))
        
        def IsNodeCoincide(p1:WallGeometry, p2:WallGeometry):
            if (p1.X1 == p2.X1 and p1.Y1 == p2.Y1) or (p1.X1 == p2.X2 and p1.Y1 == p2.Y2) or (p1.X2 == p2.X1 and p1.Y2 == p2.Y1) or (p1.X2 == p2.X2 and p1.Y2 == p2.Y2):
                return True
            else:
                return False
        
        def MergedWallGeometry(p1:WallGeometry, p2:WallGeometry):
            if (p1.X1 == p2.X1 and p1.Y1 == p2.Y1):
                return WallGeometry(p1.X2, p1.Y2, p2.X2, p2.Y2)
            elif (p1.X1 == p2.X2 and p1.Y1 == p2.Y2):
                return WallGeometry(p1.X2, p1.Y2, p2.X1, p2.Y1)
            elif (p1.X2 == p2.X1 and p1.Y2 == p2.Y1):
                return WallGeometry(p1.X1, p1.Y1, p2.X2, p2.Y2)
            else:
                return WallGeometry(p1.X1, p1.Y1, p2.X1, p2.Y1)

        if (PlateAngle(p1) == PlateAngle(p2)) and (IsNodeCoincide(p1, p2)==True):
            return MergedWallGeometry(p1, p2)
        else:
            return False


    def MergePlate(self):
        for i, plate in enumerate(self.arrWallsGeometry):
            if i==0: 
                self.arrWallsGeometryMerged.append(plate)
                self.mergedWallDict[i] = i
            else:
                merged = False
                for j, merged_plate in enumerate(self.arrWallsGeometryMerged):
                    isPlateContinous = self.IsPlateContinous(merged_plate, plate)
                    if isPlateContinous != False:
                        self.arrWallsGeometryMerged[j] = isPlateContinous
                        self.mergedWallDict[i] = j
                        merged = True
                if merged == False:
                    self.mergedWallDict[i] = i
                    self.arrWallsGeometryMerged.append(plate)
                        

    def AppendLine(self, arr_to_append, multiline=False): # expect a list if multiline==False, else expect a list of list
        if multiline == False:
            self.res.append(','.join(map(str, arr_to_append)))
        else:
            _ = [self.res.extend((','.join(map(str, x))) for x in arr_to_append)]

    def PrintWallForce(self):
        print('time elapsed: {} seconds'.format(datetime.now()-self.t0))
        print('Please wait, processing...')
        geo_short = ['Plate No.', 'X1', 'X2', 'Y1', 'Y2']
        forces_short = ['Plate no.', 'Phase index', 'Phase name', 'X', 'Y', 'M', 'V', 'N', 'Ux', 'Uy']
        forces_unit = ['-', '-', '-', 'm', 'm', 'kNm /m', 'kN /m', 'kN /m', 'mm', 'mm']
        
        self.res = []
        self.AppendLine(['#START_GEOMETRY#'])
        self.AppendLine(geo_short)
        for i, plate in enumerate(self.arrWallsGeometryMerged):
            self.AppendLine(['{}'.format(i+1)] + plate.Attribute_to_list())
        self.AppendLine(['#END_GEOMETRY#'])
        
        self.AppendLine(['#START_WALLDATA#'])
        self.AppendLine(forces_short)
        self.AppendLine(forces_unit)
        for i, phase in enumerate(self.phases):
            for j, plate in enumerate(self.plates):
                this_plate_no = self.mergedWallDict[j]+1
                this_plate = [[this_plate_no, i+1, self.phases_name[i]] + x for x in self.arrWalls[i][j].Attribute_to_list()]
                self.AppendLine(this_plate, multiline=True)
        self.AppendLine(['#END_WALLDATA#'])

        # _ = [print(x) for x in self.res]
        plaxis_folder = os.path.dirname(self.plaxis_path)
        plaxis_name = os.path.basename(self.plaxis_path)
        datafile_name = '{}-{}.csv'.format(plaxis_name.replace('.p2dx', '_WallForces_'), datetime.now().strftime('%Y%m%d,%H-%M-%S'))
        datafile_path = os.path.join(plaxis_folder, datafile_name)
        with open(datafile_path, 'w+') as f:
            _ = [f.writelines(x+'\n') for x in self.res]
        
        print('time elapsed: {} seconds'.format(datetime.now()-self.t0))
        print('Data file saved here: \n{}'.format(datafile_path))


class Plot():
    def __init__(self):
        self.plaxis_path = str(g_o.generalinfo.Filename)
        self.plaxis_folder = os.path.dirname(self.plaxis_path)
        self.plaxis_name = os.path.basename(self.plaxis_path)
        self.datafile_name = '{}-{}.png'.format(self.plaxis_name.replace('.p2dx', '_Image_'), datetime.now().strftime('%Y%m%d,%H-%M-%S'))
        self.datafile_path = os.path.join(self.plaxis_folder, self.datafile_name)
        self.plot_phase = -1

    def FindPlotPhase(self):
        phases = [str(x) for x in g_o.Phases.Identification]

        for i, phase in enumerate(phases):
            if 'FEL' in phase.upper():
                self.plot_phase = i
                break

    def Plot(self):
        _ = g_o.getsingleresult(g_o.Phases[self.plot_phase], g_o.ResultTypes.Soil.Utot, (0, 0))
        g_o.Plots[-1].ScaleFactor = 1
        g_o.Plots[-1].zoom()
        g_o.Plots[-1].DrawFrame = False
        g_o.Plots[-1].DrawTitle = False
        g_o.Plots[-1].export(self.datafile_path, 1920, 1080)
        print('Image exported to:', self.datafile_path)



def StrutForceAutomation(x1=None, x2=None):
    f = PlxStrutForce()
    f.GetStrutForces(x1, x2)
    f.PrintStrutForce()

def WallForceAutomation():
    f = PlxWallForce()
    f.GetWallForces()
    f.GetWallGeometry()
    f.MergePlate()
    f.PrintWallForce()

def PlotImage():
    p = Plot()
    p.Plot()

def RunThis(x1=None, x2=None, to_plot_image=True):
    StrutForceAutomation(x1, x2)
    WallForceAutomation()
    if to_plot_image: PlotImage()

def RunSingle(run_strut=True, run_wall=True, to_plot_image=True):
    file = input('Please enter the full plaxis file path: ').strip("'")
    print('Loading, Please wait...')
    s_o.open(file)
    if run_strut: StrutForceAutomation(-99999, 99999)
    if run_wall: WallForceAutomation()
    if to_plot_image: PlotImage()

def RunAllInFolder(run_strut=True, run_wall=True, to_plot_image=True):
    folder = input('Please enter the folder path: ')
    print('Loading, Please wait...')
    files = os.listdir(folder)
    plaxis_files = [x for x in files if os.path.splitext(x)[1] == '.p2dx']
    for plaxis_file in plaxis_files:
        s_o.open(os.path.join(folder, plaxis_file))
        if run_strut: StrutForceAutomation(-99999, 99999)
        if run_wall: WallForceAutomation()
        if to_plot_image: PlotImage()
        s_o.close()



class Timer():
    t0 = datetime.now()

    
class NodesSettlement():
    def __init__(self, X:List[float], Uy:List[float]) -> None: #expect a list of nodes in the same phase
        self.X = X
        self.Uy = Uy


class PlxSettlement():
    def __init__(self) -> None:
        self.level = None
        self.x1 = None
        self.x2 = None
        self.result = []
        self.phases = g_o.Phases
        self.t0 = datetime.now()
        self.plaxis_path = str(g_o.generalinfo.Filename)
        self.phases_name = [str(x.Identification).replace('[' + str(x.Name) + ']', '').replace(',', '&') for x in self.phases]

    def PlxSettlement(self, x1=None, x2=None, level=None, auto=True):
        if auto:
            self.GetLevel()
        elif x1 == None or x2 == None or level == None:
            self.GetUserInputLevel()
        else:
            self.x1 = x1
            self.x2 = x2
            self.level = level
        
        self.GetSettlement()
        self.PrintSettlement()

    def GetUserInputLevel(self):
        x1, x2, level = input('Please enter the min_x, max_x, and y_level for the section cut for settlement (separated by space in between): ').split()
        self.level = level
        self.x1 = x1
        self.x2 = x2

    def GetLevel(self):
        x_list = g_o.getresults(g_o.Phases[0], g_o.ResultTypes.Soil.X, 'node')
        y_list = g_o.getresults(g_o.Phases[0], g_o.ResultTypes.Soil.Y, 'node')
        self.x1 = min(x_list)
        self.x2 = max(x_list)
        self.level = max(y_list) - 0.1 # default cut ground settlement at 100mm below ground level

    def GetSettlement(self):
        g_o.linecrosssectionplot(g_o.Plot_1, (self.x1, self.level), (self.x2, self.level))
        g_o.set(g_o.Plots[-1].ResultType, g_o.ResultTypes.Soil.Uy)
        g_o.set(g_o.Plots[-1].PlotType, g_o.PlotTypes.NodeArrows)

        for phase in g_o.Phases:
            try:
                ground_x = g_o.getcrosssectionresults(g_o.Plots[-1], phase, g_o.ResultTypes.Soil.X)
                ground_uy = g_o.getcrosssectionresults(g_o.Plots[-1], phase, g_o.ResultTypes.Soil.Uy)
            except plxscripting.plx_scripting_exceptions.PlxScriptingError:
                ground_x = []
                ground_uy = []
                
            self.result.append(NodesSettlement(ground_x, ground_uy))

    def AppendLine(self, arr_to_append, multiline=False): # expect a list if multiline==False, else expect a list of list
        if multiline == False:
            self.res.append(','.join(map(str, arr_to_append)))
        else:
            _ = [self.res.extend((','.join(map(str, x))) for x in arr_to_append)]

    def PrintSettlement(self):
        print('Please wait, processing...')
        print('Format as follow: ')
        print('Phase, x coordinate in meter')
        print('Phase, vertical settlement in meter')
        print('================================')
        
        self.res = []
        self.AppendLine(['#START_SETTLEMENT#'])
        
        for i, phase in enumerate(g_o.Phases):
            self.AppendLine([str(phase.Identification)] + ['x'] + list(self.result[i].X))
            self.AppendLine([str(phase.Identification)] + ['Uy'] + list(self.result[i].Uy))

        self.AppendLine(['#END_SETTLEMENT#'])

        plaxis_folder = os.path.dirname(self.plaxis_path)
        plaxis_name = os.path.basename(self.plaxis_path)
        datafile_name = '{}-{}.csv'.format(plaxis_name.replace('.p2dx', '_WallForces_'), datetime.now().strftime('%Y%m%d,%H-%M-%S'))
        datafile_path = os.path.join(plaxis_folder, datafile_name)
        with open(datafile_path, 'w+') as f:
            _ = [f.writelines(x+'\n') for x in self.res]
        
        print('time elapsed: {} seconds'.format(datetime.now()-self.t0))
        print('Data file saved here: \n{}'.format(datafile_path))


    


if __name__ == '__main__':
    
    pass
