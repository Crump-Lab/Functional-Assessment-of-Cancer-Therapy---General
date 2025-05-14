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


def calculate_fact_e_scores(df):
    """
    Calculate all FACT-E scores including subscales, total scores, FACT-G total score, FACT-E total score, and TOI
    
    Parameters:
    df (DataFrame): DataFrame containing the FACT-E questionnaire responses
    
    Returns:
    DataFrame: DataFrame with added score columns
    """
    # Define all subscale columns
    pwb_cols = [f"gp{i}" for i in range(1, 8)]  # Physical Well-Being, 7 items
    swb_cols = [f"gs{i}" for i in range(1, 8)]  # Social/Family Well-Being, 7 items
    ewb_cols = [f"ge{i}" for i in range(1, 7)]  # Emotional Well-Being, 6 items
    fwb_cols = [f"gf{i}" for i in range(1, 8)]  # Functional Well-Being, 7 items
    ecs_cols = [f"a_hn{i}" for i in range(1, 6)] + ["a_hn7", "a_hn10"] + \
        [f"a_e{i}" for i in range(1, 8)] + ["a_c6", "a_c2", "a_act11"]  # Esophageal Cancer Subscale, 17 items

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

    # Calculate FACT-E total score (FACT-G + ECS)
    fact_e_items = fact_g_items + ecs_cols  # 27 + 17 = 44 items
    fact_e_item_cols = [f"{col}_score" for col in fact_e_items]
    fact_e_num_answered = df[fact_e_item_cols].notna().sum(axis=1)
    fact_e_min_items = 36  # 80% of 44 items = 35.2, rounded up to 36

    df["fact_e_total"] = np.where(
        # Condition 1: FACT-G and ECS must be non-NaN
        (df['fact_g_total'].notna()) & 
        (df["ecs_subscale_score"].notna()) &
        # Condition 2: At least 80% of FACT-E items must be answered
        (fact_e_num_answered >= fact_e_min_items),
        df['fact_g_total'] + df["ecs_subscale_score"],
        np.nan
    )

    # Calculate Trial Outcome Index (TOI) = PWB + FWB + ECS
    toi_items = pwb_cols + fwb_cols + ecs_cols  # 7 + 7 + 17 = 31 items
    toi_item_cols = [f"{col}_score" for col in toi_items]
    toi_num_answered = df[toi_item_cols].notna().sum(axis=1)
    toi_min_items = 25  # 80% of 31 items = 24.8, rounded up to 25

    df["toi"] = np.where(
        # Condition 1: PWB, FWB, and ECS must be non-NaN
        (df["pwb_subscale_score"].notna()) & 
        (df["fwb_subscale_score"].notna()) & 
        (df["ecs_subscale_score"].notna()) &
        # Condition 2: At least 80% of TOI items must be answered
        (toi_num_answered >= toi_min_items),
        df["pwb_subscale_score"] + df["fwb_subscale_score"] + df["ecs_subscale_score"],
        np.nan
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