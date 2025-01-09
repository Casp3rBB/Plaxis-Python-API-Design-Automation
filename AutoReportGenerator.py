import plxscripting
import os
from datetime import datetime
from typing import List

# Made by Kinen Ma 2025-01-02
# Version 0.1, in development

g_o = g_o
s_o = s_o


class AutoReportGenerator:

    EXPORT_WIDTH = 1920
    EXPORT_HEIGHT = 1080

    def __init__(self):
        self.t0 = datetime.now()
        self.plaxis_path = ''
        self.plaxis_folder = ''
        self.output_folder = ''

    def AutoReportGenerator(self):
        self.InputFileReader()
        self.ParseInput()

    def InputFileReader(self):
        input_file = input('Please enter the input file full path: ')
        input_file = input_file.strip("'")
        self.input_commands = []
        with open(input_file) as f:
            self.input_commands.extend(f.readlines())
        self.input_commands = [x.strip('\n') for x in self.input_commands]

    def ParseInput(self):
        for idx, input_command in enumerate(self.input_commands):
            input_command = input_command.lower()
            input_command = input_command.split('|')
            input_command = [x.strip() for x in input_command]
            print(input_command[0]) # **********************************************PRINT******************

            if input_command[0] == '':
                continue
            elif input_command[0] == 'open model':
                # New Model | Model Full Path
                model_path = input_command[1]
                self.OpenModel(model_path)
                self.InitializeNewModel()
            elif input_command[0] == 'general view':
                # General View | Scale
                scale = float(input_command[1])
                self.Command_GeneralView(scale)
            elif input_command[0] == 'cross section cut':
                # Cross Section Cut | x1 | y1 | x2 | y2 | Plot Type | Result Type | *Phases
                x1 = float(input_command[1])
                y1 = float(input_command[2])
                x2 = float(input_command[3])
                y2 = float(input_command[4])
                plot_type = input_command[5]
                result_type = input_command[6]
                self.Command_CrossSectionCut(x1, y1, x2, y2, plot_type, result_type)



    def OpenModel(self, model_path):
        s_o.close()
        s_o.open(model_path)

    def InitializeNewModel(self):
        self.plaxis_path = str(g_o.generalinfo.Filename)
        self.plaxis_folder = os.path.dirname(self.plaxis_path)
        self.output_folder = self.plaxis_path[:-5] + ' - ' + self.t0.strftime("%Y-%m-%d %H.%M.%S")

    def ExportView(self, viewname):
        filename = os.path.join(self.output_folder, viewname)
        g_o.Plots[-1].export(filename, self.EXPORT_WIDTH, self.EXPORT_HEIGHT)

    def Command_GeneralView(self, scale):
        g_o.Plots[-1].ScaleFactor = scale
        for idx, phase in enumerate(g_o.Phases):
            g_o.set(g_o.Plots[-1].Phase, phase)
            viewname = 'General View - {} - {}'.format(idx+1, phase.Identification)
            self.ExportView(viewname)

    def Command_CrossSectionCut(self, x1, y1, x2, y2, plot_type, result_type):

        
    
