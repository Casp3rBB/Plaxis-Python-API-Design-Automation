# PLAXIS Python Design Automation

This repository contains a collection of Python scripts for automating the extraction and processing of geotechnical data from PLAXIS models. The scripts are designed to streamline the workflow for analyzing cross-section results, strut forces, wall forces, settlements, and more. They provide functionalities for batch processing of multiple models.

## Table of Contents

- [Usage](#usage)
- [Functions](#functions)
    - [Core Functions](#core-functions)
    - [Section Analysis](#section-analysis)
    - [Batch Processing](#batch-processing)
    - [Miscellaneous](#miscellaneous)
- [Author](#author)

## Usage 

To use the scripts in this repository, you need to have Plaxis 2D installed on your machine.

Open the Python interpreter in Plaxis Input or Output (depending on input automation or result extraction automation) to start using the scripts: 

![image](https://github.com/user-attachments/assets/b3b2b69c-eba6-453a-9111-a2df80e3034a)

## Functions

### Core Functions

- **StrutForceAutomation**
    
    - Extracts strut forces within a specified range of x-coordinates from the PLAXIS model.
- **WallForceAutomation**
    
    - Retrieves and processes wall forces, merging data where applicable.
- **PlotImage**
    
    - Exports an image of the current PLAXIS model, focusing on displacement results.
- **SettlementAutomation**
    
    - Extracts settlement data at specified levels and x-coordinates.

### Batch Processing

- **BatchExtractSettlement_Simple**
    
    - Processes multiple PLAXIS models to extract settlement data along a specified y-level.
- **BatchExtractStrutForce_Simple**
    
    - Extracts strut forces from multiple PLAXIS models and prints the results for each phase.
- **BatchExtractWallForce_Simple**
    
    - Extracts wall forces for each phase and prints the maximum and minimum values for each force component.
- **BatchCalculate**
    
    - Automates the calculation process for a batch of PLAXIS models, saving each model after calculation.
    - Users can input multiple file paths separated by commas, and the script will process each model in sequence. Calculation times for individual models and the total processing time are displayed.

### Section Analysis

- **SectionVaryAlongXY**
    
    - Prompts the user to input parameters for varying a cross-section along the x or y direction.
    - Extracts and prints the minimum and maximum normal stresses for specified phases.
- **Section_StageByStage**
    
    - Extracts and prints minimum and maximum total normal stresses for each phase along a specified cross-section.

### Miscellaneous

- **Rearrange_pdf**
    
    - Rearranges pages of a PDF file based on the order specified in a text file.
- **RunThis**
    
    - Automates the extraction of both strut and wall forces, and optionally generates a plot image.
- **RunSingle**
    
    - Processes a single PLAXIS file, extracting forces and optionally generating a plot image.
- **RunAllInFolder**
    
    - Processes all PLAXIS files in a specified folder, extracting forces and optionally generating plot images.

## Author

This project was created by Kinen Ma.
