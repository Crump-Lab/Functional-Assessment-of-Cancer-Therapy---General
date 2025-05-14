# Functional Assessment of Cancer Therapy - General (FACT-G)

## Overview
This repository provides an implementation for scoring the Functional Assessment of Cancer Therapy - General (FACT-G) questionnaire and its subscales, including: physical well-being, social/family well-being, emotional well-being, and functional well-being. The implementation ensures accurate calculation of all subscale scores while handling reverse-scored items and missing values according to version 4 of the FACT-E scoring guidelines (https://www.facit.org/measures/fact-g).

## Features
These files provide a complete solution for FACT-G scoring that can be run from the command line. The script:
1. Extracts relevant columns from the input data
2. Defines all subscales and their items.
3. Creates a reusable function for calculating subscale scores.
4. Handles reverse-scored items appropriately.
5. Calculates all subscale scores with proper handling of reverse-scored items
6. Calculates all FACT-G components:
   - **Physical Well-Being (PWB)**
   - **Social/Family Well-Being (SWB)**
   - **Emotional Well-Being (EWB)**
   - **Functional Well-Being (FWB)**
   - **FACT-G total** (PWB + SWB + EWB + FWB)
7. Outputs the results to a CSV file
8. Displays summary statistics
9. Follows standard FACT scoring guidelines, including:
   - Proper handling of missing values.
   - Scaling scores based on the number of answered items.

## Missing data
1. 50% Rule for Subscale Score Calculation: Each subscale score (PWB, SWB, EWB, FWB) should only be calculated if at least 50% of the items within that subscale are answered.
2. 80% Rule and All Component Subscales Valid for Composite Score Calculation: The FACT-G total score must meet both conditions:
    - At least 80% of the items within the composite score must be completed.
    - All component subscales must have valid scores (i.e., each subscale must have at least 50% of its items answered).
      
**Reference**: https://www.facit.org/scoring 

## Installation
To use this implementation, clone the repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/Crump-Lab/Functional-Assessment-of-Cancer-Therapy---General.git FACT_G

# Navigate to the project directory
cd FACT_G

# Install required dependencies
pip install -r requirements.txt
```

## Usage
To score the FACT-G questionnaire, run the following command:

```bash
python FACT_G_scoring.py --input data.csv --output results.csv
```

### Example

```bash
python FACT_G_scoring.py --input ./Temp/EsophagealBank-EmotionalDistress_DATA_2025-02-13_1201.csv --output ./results/results.csv
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
5. **FACT-G Total** - Sum of PWB, SWB, EWB, and FWB

The tool handles reverse-scored items and properly scales scores based on the number of answered items.

## Input Data Format

The input CSV file should contain columns with the following naming convention:
- Physical Well-Being: gp1, gp2, ..., gp7
- Social Well-Being: gs1, gs2, ..., gs7
- Emotional Well-Being: ge1, ge2, ..., ge6
- Functional Well-Being: gf1, gf2, ..., gf7

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
