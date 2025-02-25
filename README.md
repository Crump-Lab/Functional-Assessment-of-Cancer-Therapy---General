# Crump Lab FACT-E 

## Overview
This repository provides an implementation for scoring the Functional Assessment of Cancer Therapy - Esophageal (FACT-E) questionnaire for ESO (esophageal) projects under the academic research lab at McGill University. It includes physical well-being, social/family well-being, emotional well-being, functional well-being, and esophagus cancer subscale. The implementation ensures accurate calculation of all subscale scores while handling reverse-scored items and missing values according to standard FACT scoring guidelines.

## Features
This implementation:
1. Defines all subscales and their items.
2. Creates a reusable function for calculating subscale scores.
3. Handles reverse-scored items appropriately.
4. Calculates all FACT-E components:
   - **Physical Well-Being (PWB)**
   - **Social/Family Well-Being (SWB)**
   - **Emotional Well-Being (EWB)**
   - **Functional Well-Being (FWB)**
   - **Esophageal Cancer Subscale (ECS)**
   - **FACT-G total** (PWB + SWB + EWB + FWB)
   - **FACT-E total** (FACT-G + ECS)
   - **Trial Outcome Index (TOI)** (PWB + FWB + ECS)
5. Follows standard FACT scoring guidelines, including:
   - Proper handling of missing values.
   - Scaling scores based on the number of answered items.

## Project Description
We publish the protocol on [protocols.io](https://www.protocols.io/workspaces/crump-lab). The data will be stored on [Dataverse](https://borealisdata.ca/dataverse/crump_lab). 

## Usage
This repository serves as a template to score the FACT-E. 

## Repository Structure

    ESO_project/ 
        ├── docs                    # Documentation, papers, and reports 
        ├── Temp                    # Temporary files
        ├── notebooks               # Jupyter notebooks 
        ├── results                 # Analysis outputs, figures, etc. 
        ├── requirements.txt        # Python package dependencies
        ├── .gitignore              # Files to ignore in Git
        ├── .readthedocs.yaml       # host documentation
        ├── LICENSE
        └── README.md

## Contact
[Jin Kweon](mailto:jin.kweon@mail.mcgill.ca), [Trafford Crump](mailto:trafford.crump@mcgill.ca)
