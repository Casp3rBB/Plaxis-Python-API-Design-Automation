# Project Title

This repository contains a collection of Python scripts for automating the extraction and processing of geotechnical data from PLAXIS models. The scripts are designed to streamline the workflow for analyzing cross-section results, strut forces, wall forces, settlements, and more. They provide functionalities for batch processing of multiple models and generating comprehensive reports.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
    - [SectionVaryAlongXY](#sectionvaryalongxy)
    - [Section_StageByStage](#section_stagebystage)
    - [BatchExtractSettlement_Simple](#batchextractsettlement_simple)
    - [BatchExtractStrutForce_Simple](#batchextractstrutforce_simple)
    - [BatchExtractWallForce_Simple](#batchextractwallforce_simple)
    - [BatchCalculate](#batchcalculate)
    - [Rearrange_pdf](#rearrange_pdf)
    - [RunThis](#runthis)
    - [RunSingle](#runsingle)
    - [RunAllInFolder](#runallinfolder)
- [Author](#author)

## Installation

To use the scripts in this repository, you need to have Python installed on your machine along with the following packages:

- `plxscripting`
- `PyPDF2`
- `datetime`
- `os`
- `re`
- `typing`

You can install the required packages using pip:

`pip install plxscripting PyPDF2`

## Usage

### SectionVaryAlongXY

This function prompts the user to input parameters for varying a cross-section cut along the x or y direction. It then extracts and prints the minimum and maximum normal stresses for specified phases.

### Section_StageByStage

This function extracts and prints the minimum and maximum normal total stresses for each phase along a specified cross-section.

### BatchExtractSettlement_Simple

This function allows batch processing of multiple PLAXIS models to extract settlement data along a specified y-level.

### BatchExtractStrutForce_Simple

This function extracts strut forces from multiple PLAXIS models and prints the results for each phase.

### BatchExtractWallForce_Simple

This function extracts wall forces for each phase and prints the maximum and minimum values for each force component.

### BatchCalculate

This function automates the calculation process for a batch of PLAXIS models, saving each model after calculation.

### Rearrange_pdf

This function rearranges pages of a PDF file based on the order specified in a text file.

### RunThis

This function automates the extraction of both strut and wall forces, and optionally generates a plot image.

### RunSingle

This function processes a single PLAXIS file, extracting forces and optionally generating a plot image.

### RunAllInFolder

This function processes all PLAXIS files in a specified folder, extracting forces and optionally generating plot images.

## Author

This project was created by Kinen Ma. The initial version was made on 2023-05-23, and the latest updates were made on 2024-04-12.
