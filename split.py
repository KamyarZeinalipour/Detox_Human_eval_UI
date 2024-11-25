import os
import pandas as pd
import argparse
import random

def split_into_batches(dataset_path, num_batches, output_dir, crossval_percentage):
    """
    Splits a dataset into a specified number of batches and optionally marks some for cross-evaluation.

    Parameters:
    - dataset_path (str): Path to the dataset file (CSV format).
    - num_batches (int): Number of batches to create.
    - output_dir (str): Directory where batches will be saved.
    - crossval_percentage (float): Percentage of batches to mark for cross-evaluation.
    """
    # Load the dataset
    dataset = pd.read_csv(dataset_path)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Calculate batch size
    batch_size = len(dataset) // num_batches
    remainder = len(dataset) % num_batches  # Handle any remainder

    # Determine the batches to mark for cross-evaluation
    crossval_count = max(1, round(num_batches * (crossval_percentage / 100)))
    crossval_batches = random.sample(range(1, num_batches + 1), crossval_count)
    print(f"Batches selected for cross-evaluation: {crossval_batches}")

    start_idx = 0
    for i in range(1, num_batches + 1):
        # Calculate the end index for the batch
        end_idx = start_idx + batch_size + (1 if i <= remainder else 0)
        
        # Slice the dataset for the current batch
        batch = dataset.iloc[start_idx:end_idx]
        
        # Determine the filename, adding "_crossval" if marked for cross-evaluation
        is_crossval = i in crossval_batches
        batch_suffix = "_crossval" if is_crossval else ""
        batch_filename = os.path.join(output_dir, f"batch_{i}{batch_suffix}.csv")
        
        # Save the batch
        batch.to_csv(batch_filename, index=False)
        print(f"Batch {i} ({len(batch)} samples) saved to {batch_filename}.")
        
        # Update start index for the next batch
        start_idx = end_idx

def main():
    parser = argparse.ArgumentParser(description="Split a dataset into multiple batches with cross-evaluation marking.")
    parser.add_argument("dataset_path", type=str, help="Path to the dataset file (CSV format).")
    parser.add_argument("num_batches", type=int, help="Number of batches to create.")
    parser.add_argument("--output_dir", type=str, default="batches", help="Directory to save batches (default: 'batches').")
    parser.add_argument("--crossval_percentage", type=float, default=0.0, help="Percentage of batches for cross-evaluation (default: 0%).")
    
    args = parser.parse_args()
    
    split_into_batches(args.dataset_path, args.num_batches, args.output_dir, args.crossval_percentage)

if __name__ == "__main__":
    main()
