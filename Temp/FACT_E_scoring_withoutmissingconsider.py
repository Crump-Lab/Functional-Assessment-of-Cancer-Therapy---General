#!/usr/bin/env python3
"""
FACT-E Scoring Tool

This script calculates scores for the Functional Assessment of Cancer Therapy - Esophageal (FACT-E)
questionnaire, including all subscales, total scores, FACT-G total score, FACT-E total score, and the Trial Outcome Index (TOI).

Usage:
    python FACT_E_scoring.py --input data.csv --output results.csv
"""

import argparse
import pandas as pd
import numpy as np


def calculate_subscale_score(df, cols, reverse_items=None, subscale_name=""):
    """
    Calculate subscale scores according to FACT scoring guidelines
    
    Parameters:
    df (DataFrame): DataFrame containing the item responses
    cols (list): List of column names for the subscale items
    reverse_items (list): List of items that need to be reverse-scored (if any)
    subscale_name (str): Name of the subscale for column naming
    
    Returns:
    DataFrame: DataFrame with added subscale score column
    """
    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Create score columns for each item
    for col in cols:
        if reverse_items and col in reverse_items:
            # Reverse scoring (4 - score)
            df[f"{col}_score"] = 4 - df[col]
        else:
            # Regular scoring
            df[f"{col}_score"] = df[col]
    
    # Calculate subscale score
    score_cols = [f"{col}_score" for col in cols]
    
    # Calculate subscale score: sum of scores * number of items / number of answered items
    df[f"{subscale_name}_subscale_score"] = (
        df[score_cols].sum(axis=1, skipna=True) * len(cols) /
        df[score_cols].notna().sum(axis=1)
    )
    
    return df


def calculate_fact_e_scores(df):
    """
    Calculate all FACT-E scores including subscales, total scores, FACT-G total score, FACT-E total score, and TOI
    
    Parameters:
    df (DataFrame): DataFrame containing the FACT-E questionnaire responses
    
    Returns:
    DataFrame: DataFrame with added score columns
    """
    # Define all subscale columns
    pwb_cols = [f"gp{i}" for i in range(1, 8)]  # Physical Well-Being
    swb_cols = [f"gs{i}" for i in range(1, 8)]  # Social/Family Well-Being
    ewb_cols = [f"ge{i}" for i in range(1, 7)]  # Emotional Well-Being
    fwb_cols = [f"gf{i}" for i in range(1, 8)]  # Functional Well-Being
    ecs_cols = [f"a_hn{i}" for i in range(1, 6)] + ["a_hn7", "a_hn10"] + \
        [f"a_e{i}" for i in range(1, 8)] + ["a_c6", "a_c2", "a_act11"]  # Esophageal Cancer Subscale

    # Calculate Physical Well-Being (PWB) subscale
    # All PWB items are reverse-scored
    df = calculate_subscale_score(df, pwb_cols, reverse_items=pwb_cols, subscale_name="pwb")

    # Calculate Social/Family Well-Being (SWB) subscale
    df = calculate_subscale_score(df, swb_cols, subscale_name="swb")

    # Calculate Emotional Well-Being (EWB) subscale
    # All EWB items except GE2 are reverse-scored
    ewb_reverse_items = [f"ge{i}" for i in range(1, 7) if i != 2]
    df = calculate_subscale_score(df, ewb_cols, reverse_items=ewb_reverse_items, subscale_name="ewb")

    # Calculate Functional Well-Being (FWB) subscale
    df = calculate_subscale_score(df, fwb_cols, subscale_name="fwb")

    # Calculate Esophageal Cancer Subscale (ECS)
    # Some ECS items are reverse-scored
    ecs_reverse_items = ["a_e1", "a_e2", "a_e3", "a_e4", "a_e5", "a_e7", "a_act11", "a_c2", "a_hn2", "a_hn3"]
    df = calculate_subscale_score(df, ecs_cols, reverse_items=ecs_reverse_items, subscale_name="ecs")

    # Calculate FACT-G total score (PWB + SWB + EWB + FWB)
    df["fact_g_total"] = (
        df["pwb_subscale_score"] +
        df["swb_subscale_score"] +
        df["ewb_subscale_score"] +
        df["fwb_subscale_score"]
    )

    # Calculate FACT-E total score (FACT-G + ECS)
    df["fact_e_total"] = df["fact_g_total"] + df["ecs_subscale_score"]

    # Calculate Trial Outcome Index (TOI) = PWB + FWB + ECS
    df["toi"] = (
        df["pwb_subscale_score"] +
        df["fwb_subscale_score"] +
        df["ecs_subscale_score"]
    )
    
    return df


def extract_fact_e_columns(df):
    """
    Extract only the columns needed for FACT-E scoring
    
    Parameters:
    df (DataFrame): Original DataFrame with all columns
    
    Returns:
    DataFrame: DataFrame with only FACT-E relevant columns
    """
    # Extract columns needed for FACT-E scoring with the patient id
    columns_to_extract = ["id"] + \
                        [f"gp{i}" for i in range(1, 8)] + \
                        [f"gs{i}" for i in range(1, 8)] + \
                        [f"ge{i}" for i in range(1, 7)] + \
                        [f"gf{i}" for i in range(1, 8)] + \
                        [f"a_hn{i}" for i in range(1, 6)] + \
                        ["a_hn7", "a_hn10"] + \
                        [f"a_e{i}" for i in range(1, 8)] + \
                        ["a_c6", "a_c2"] + ["a_act11"]

    # Check which columns actually exist in the dataframe
    existing_columns = [col for col in columns_to_extract if col in df.columns]
    
    # # If "id" is not in the dataframe, add a sequential ID
    # if "id" not in existing_columns:
    #     df = df.copy()
    #     df["id"] = range(1, len(df) + 1)
    #     existing_columns = ["id"] + [col for col in existing_columns if col != "id"]
    
    return df[existing_columns]


def main():
    """Main function to parse arguments and run the scoring"""
    parser = argparse.ArgumentParser(description='Calculate FACT-E scores from questionnaire data')
    parser.add_argument('--input', required=True, help='Path to input CSV file')
    parser.add_argument('--output', required=True, help='Path to output CSV file')
    
    args = parser.parse_args()
    
    try:
        # Read the input file
        print(f"Reading input file: {args.input}")
        df = pd.read_csv(args.input)
        
        # Extract relevant columns
        print("Extracting FACT-E relevant columns")
        df_extracted = extract_fact_e_columns(df)
        
        # Calculate scores
        print("Calculating FACT-E scores")
        df_scored = calculate_fact_e_scores(df_extracted)
        
        # Save results
        print(f"Saving results to: {args.output}")
        df_scored.to_csv(args.output, index=False)
        
        print("FACT-E scoring completed successfully!")
        
        # Display summary statistics
        score_columns = ["pwb_subscale_score", "swb_subscale_score", "ewb_subscale_score", 
                         "fwb_subscale_score", "ecs_subscale_score", "fact_g_total", 
                         "fact_e_total", "toi"]
        
        print("\nSummary Statistics:")
        print(df_scored[score_columns].describe().round(2))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 