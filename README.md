# Functional Assessment of Cancer Therapy - Esophageal (FACT-E)

## Overview
This repository provides an implementation for scoring the Functional Assessment of Cancer Therapy - Esophageal (FACT-E) questionnaire and its subscales, including: physical well-being, social/family well-being, emotional well-being, functional well-being, and esophagus cancer subscale. The implementation ensures accurate calculation of all subscale scores while handling reverse-scored items and missing values according to version 4 of the FACT-E scoring guidelines (https://www.facit.org/measures/fact-e).

## Features
These files provide a complete solution for FACT-E scoring that can be run from the command line. The script:
1. Extracts relevant columns from the input data
2. Defines all subscales and their items.
3. Creates a reusable function for calculating subscale scores.
4. Handles reverse-scored items appropriately.
5. Calculates all subscale scores with proper handling of reverse-scored items
6. Calculates all FACT-E components:
   - **Physical Well-Being (PWB)**
   - **Social/Family Well-Being (SWB)**
   - **Emotional Well-Being (EWB)**
   - **Functional Well-Being (FWB)**
   - **Esophageal Cancer Subscale (ECS)**
   - **FACT-G total** (PWB + SWB + EWB + FWB)
   - **FACT-E total** (FACT-G + ECS)
   - **Trial Outcome Index (TOI)** (PWB + FWB + ECS)
7. Outputs the results to a CSV file
8. Displays summary statistics
9. Follows standard FACT scoring guidelines, including:
   - Proper handling of missing values.
   - Scaling scores based on the number of answered items.

## Installation
To use this implementation, clone the repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/Crump-Lab/ESO_FACT_E.git

# Navigate to the project directory
cd ESO_FACT_E

# Install required dependencies
pip install -r requirements.txt
```

## Usage
To score the FACT-E questionnaire, run the following command:

```bash
python FACT_E_scoring.py --input data.csv --output results.csv
```

### Example

```bash
python FACT_E_scoring.py --input ESO_FACT_E/Temp/EsophagealBank-EmotionalDistress_DATA_2025-02-13_1201.csv --output ESO_FACT_E/Temp/results.csv
```

### Arguments:
- `--input`: Path to the input CSV file containing questionnaire responses.
- `--output`: Path to save the output CSV file with computed scores.

## FACT-E Scoring Details

The tool calculates the following scores:

1. **Physical Well-Being (PWB)** - Items GP1-GP7
2. **Social/Family Well-Being (SWB)** - Items GS1-GS7
3. **Emotional Well-Being (EWB)** - Items GE1-GE6
4. **Functional Well-Being (FWB)** - Items GF1-GF7
5. **Esophageal Cancer Subscale (ECS)** - Items HN1-HN5, HN7, HN10, E1-E7, C6, C2, ACT11
6. **FACT-G Total** - Sum of PWB, SWB, EWB, and FWB
7. **FACT-E Total** - FACT-G + ECS
8. **Trial Outcome Index (TOI)** - PWB + FWB + ECS

The tool handles reverse-scored items and properly scales scores based on the number of answered items.

## Input Data Format

The input CSV file should contain columns with the following naming convention:
- Physical Well-Being: gp1, gp2, ..., gp7
- Social Well-Being: gs1, gs2, ..., gs7
- Emotional Well-Being: ge1, ge2, ..., ge6
- Functional Well-Being: gf1, gf2, ..., gf7
- Esophageal Cancer Subscale: a_hn1, a_hn2, ..., a_e1, a_e2, ..., a_c6, a_c2, a_act11

Each item should be scored from 0-4 according to the FACT-E questionnaire guidelines.

## Project Description
We publish the protocol on [protocols.io](https://www.protocols.io/workspaces/crump-lab). The data will be stored on [Dataverse](https://borealisdata.ca/dataverse/crump_lab). 

## License
This project is licensed under the MIT License.

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
