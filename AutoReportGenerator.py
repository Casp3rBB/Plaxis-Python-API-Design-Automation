import plxscripting
import os
from datetime import datetime
from typing import List

# Made by Kinen Ma 2025-01-02
# Version 0.1, in development

g_o = g_o
s_o = s_o


class AutoReportGenerator:

    def __init__(self):
        self.t0 = datetime.now()

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

            if input_command[0] == '':
                continue
            elif input_command[0] == 'new model':
                new_model_path = input_command[1]
                self.OpenNewModel(new_model_path)
                self.InitializeNewModel()
            elif input_command[0] == 'general view':
                



    def OpenNewModel(self, model_path):
        s_o.close()
        s_o.open(model_path)

    def InitializeNewModel(self):
        self.plaxis_path = str(g_o.generalinfo.Filename)
        self.plaxis_folder = os.path.dirname(self.plaxis_path)
        self.output_folder = os.path.join(self.plaxis_path[:-5], self.t0.strftime("%Y-%m-%d %H:%M:%S"))
        
    
