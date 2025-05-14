#!/usr/bin/env python3
"""
FACT-G Scoring Tool

This script calculates scores for the Functional Assessment of Cancer Therapy - General (FACT-G)
questionnaire, including all subscales and the FACT-G total score.

Usage:
    python FACT_G_scoring.py --input data.csv --output results.csv
"""

import argparse
import pandas as pd
import numpy as np


def calculate_subscale_score(df, cols, reverse_items=None, subscale_name=""):
    """
    Calculate subscale scores according to FACT scoring guidelines, only if >=50% items are answered
    
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
    
    # Calculate the number of items and the 50% threshold
    total_items = len(cols)
    min_items_required = total_items / 2  # 50% threshold
    
    # Count non-NaN items for each row
    score_cols = [f"{col}_score" for col in cols]
    num_answered_items = df[score_cols].notna().sum(axis=1)
    
    # Calculate subscale score: sum of scores * number of items / number of answered items
    # Only calculate if >=50% items are answered
    df[f"{subscale_name}_subscale_score"] = np.where(
        num_answered_items >= min_items_required,
        (df[score_cols].sum(axis=1, skipna=True) * len(cols)) / 
        df[score_cols].notna().sum(axis=1),
        np.nan
    )
    
    return df


def calculate_fact_g_scores(df):
    """
    Calculate all FACT-G scores including subscales and FACT-G total score
    
    Parameters:
    df (DataFrame): DataFrame containing the FACT-G questionnaire responses
    
    Returns:
    DataFrame: DataFrame with added score columns
    """
    # Define all subscale columns
    pwb_cols = [f"gp{i}" for i in range(1, 8)]  # Physical Well-Being, 7 items
    swb_cols = [f"gs{i}" for i in range(1, 8)]  # Social/Family Well-Being, 7 items
    ewb_cols = [f"ge{i}" for i in range(1, 7)]  # Emotional Well-Being, 6 items
    fwb_cols = [f"gf{i}" for i in range(1, 8)]  # Functional Well-Being, 7 items

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

    # Calculate FACT-G total score (PWB + SWB + EWB + FWB)
    fact_g_items = pwb_cols + swb_cols + ewb_cols + fwb_cols  # 27 items
    fact_g_item_cols = [f"{col}_score" for col in fact_g_items]
    fact_g_num_answered = df[fact_g_item_cols].notna().sum(axis=1)
    fact_g_min_items = 22  # 80% of 27 items = 21.6, rounded up to 22

    df["fact_g_total"] = np.where(
        # Condition 1: All subscales must be non-NaN (already ensures 50% of items per subscale)
        (df["pwb_subscale_score"].notna()) & 
        (df["swb_subscale_score"].notna()) & 
        (df["ewb_subscale_score"].notna()) & 
        (df["fwb_subscale_score"].notna()) &
        # Condition 2: At least 80% of FACT-G items must be answered
        (fact_g_num_answered >= fact_g_min_items),
        df["pwb_subscale_score"] + df["swb_subscale_score"] + 
        df["ewb_subscale_score"] + df["fwb_subscale_score"],
        np.nan
    )
    
    return df


def extract_fact_g_columns(df):
    """
    Extract only the columns needed for FACT-G scoring
    
    Parameters:
    df (DataFrame): Original DataFrame with all columns
    
    Returns:
    DataFrame: DataFrame with only FACT-G relevant columns
    """
    # Extract columns needed for FACT-G scoring with the patient id
    columns_to_extract = ["id"] + \
                        [f"gp{i}" for i in range(1, 8)] + \
                        [f"gs{i}" for i in range(1, 8)] + \
                        [f"ge{i}" for i in range(1, 7)] + \
                        [f"gf{i}" for i in range(1, 8)]

    # Check which columns actually exist in the dataframe
    existing_columns = [col for col in columns_to_extract if col in df.columns]
    
    return df[existing_columns]


def main():
    """Main function to parse arguments and run the scoring"""
    parser = argparse.ArgumentParser(description='Calculate FACT-G scores from questionnaire data')
    parser.add_argument('--input', required=True, help='Path to input CSV file')
    parser.add_argument('--output', required=True, help='Path to output CSV file')
    
    args = parser.parse_args()
    
    try:
        # Read the input file
        print(f"Reading input file: {args.input}")
        df = pd.read_csv(args.input)
        
        # Extract relevant columns
        print("Extracting FACT-G relevant columns")
        df_extracted = extract_fact_g_columns(df)
        
        # Calculate scores
        print("Calculating FACT-G scores")
        df_scored = calculate_fact_g_scores(df_extracted)
        
        # Save results
        print(f"Saving results to: {args.output}")
        df_scored.to_csv(args.output, index=False)
        
        print("FACT-G scoring completed successfully!")
        
        # Display summary statistics
        score_columns = ["pwb_subscale_score", "swb_subscale_score", "ewb_subscale_score", 
                         "fwb_subscale_score", "fact_g_total"]
        
        print("\nSummary Statistics:")
        print(df_scored[score_columns].describe().round(2))
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())