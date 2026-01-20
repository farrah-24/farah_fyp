
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Define the path to the dataset
FILE_PATH = '/workspaces/Final-Year-Project-FIND/src/dataset/delhiaqi.csv'

def load_data(file_path):
    """
    Loads data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded data, or None if the file is not found.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return None
    
    try:
        data = pd.read_csv(file_path)
        # Convert 'Date' column to datetime, if it exists
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

def get_numeric_columns(data):
    """
    Identifies numeric columns in the DataFrame.

    Args:
        data (pandas.DataFrame): The input DataFrame.

    Returns:
        list: A list of names of numeric columns.
    """
    return data.select_dtypes(include=np.number).columns.tolist()

def plot_single_histogram(data, column, output_path):
    """
    Creates and saves a styled histogram for a single column with a KDE overlay.

    Args:
        data (pandas.DataFrame): The DataFrame containing the data.
        column (str): The name of the column to plot.
        output_path (str): The path to save the output image.
    """
    if column not in data.columns:
        print(f"Error: Column '{column}' not found in the dataset.")
        return

    if data[column].isnull().all():
        print(f"Warning: Column '{column}' contains only missing values. Skipping plot.")
        return

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")

    # Drop missing values for plotting
    column_data = data[column].dropna()
    
    # Automatic bin calculation using seaborn's default ('auto')
    sns.histplot(column_data, kde=True, bins='auto')
    
    # Add a mean line
    mean_val = column_data.mean()
    plt.axvline(mean_val, color='r', linestyle='--', label=f'Mean: {mean_val:.2f}')
    
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.legend()
    
    # Save the plot
    save_path = os.path.join(output_path, f'histogram_{column}.png')
    plt.savefig(save_path)
    plt.close()
    print(f"Saved single histogram to '{save_path}'")

def plot_all_histograms(data, output_path):
    """
    Creates and saves histograms for all numeric columns in the dataset.

    Args:
        data (pandas.DataFrame): The DataFrame containing the data.
        output_path (str): The path to save the output image.
    """
    numeric_columns = get_numeric_columns(data)
    if not numeric_columns:
        print("No numeric columns found to plot.")
        return

    sns.set_style("whitegrid")
    
    # Calculate grid size
    num_plots = len(numeric_columns)
    cols = 3
    rows = (num_plots // cols) + (1 if num_plots % cols > 0 else 0)
    
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
    axes = axes.flatten() # Flatten to 1D array for easy iteration

    for i, col in enumerate(numeric_columns):
        ax = axes[i]
        
        # Drop missing values for the current column
        column_data = data[col].dropna()

        if column_data.empty:
            ax.set_title(f'{col}\n(No Data)')
            ax.set_xticks([])
            ax.set_yticks([])
            continue

        # Plot histogram
        sns.histplot(column_data, kde=True, ax=ax, bins='auto')
        
        # Add mean line
        mean_val = column_data.mean()
        ax.axvline(mean_val, color='r', linestyle='--', label=f'Mean: {mean_val:.2f}')
        
        ax.set_title(f'Histogram of {col}')
        ax.set_xlabel('')
        ax.set_ylabel('Frequency')
        ax.legend()

    # Hide unused subplots
    for i in range(num_plots, len(axes)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    
    # Save the combined plot
    save_path = os.path.join(output_path, 'all_numeric_histograms.png')
    plt.savefig(save_path)
    plt.close()
    print(f"Saved combined histograms plot to '{save_path}'")

def main():
    """
    Main function to load data and generate plots.
    """
    print("Starting data analysis and visualization script...")
    
    # Load the data
    data = load_data(FILE_PATH)
    
    if data is not None:
        print("Data loaded successfully.")
        
        # Define output directory
        output_dir = '/workspaces/Final-Year-Project-FIND/src/output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # --- Plotting Options ---
        # Option 1: Plot a single histogram (e.g., for PM2.5)
        print("\n1. Generating a single column histogram...")
        plot_single_histogram(data, 'PM2.5', output_dir)
        
        # Option 2: Plot histograms for all numeric columns
        print("\n2. Generating histograms for all numeric columns...")
        plot_all_histograms(data, output_dir)
        
        print("\nScript finished.")

if __name__ == '__main__':
    main()
