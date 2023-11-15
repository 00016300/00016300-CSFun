import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tickcounter.util import plot_trend
from matplotlib.figure import Figure
from scipy.stats import chi2_contingency
from tkinter import ttk
import tkinter as tk

# Loading the CSV file into a DataFrame with the correct delimiter
main_data = r"C:\Users\Asus\Desktop\WIUT COURSE WORKS\Level 4\Exams\CSFun - On process\00016300\comments_cleaned.csv"  # Source of dataframe
main_data = pd.read_csv(main_data, delimiter=';')
main_data = main_data[
    ['User ID', 'ID', 'Photo ID', 'Posted Date', 'Comment', 'Created Timestamp', 'Emoji Used', 'Hashtags used count']]

# Description of the dataset
print('Dataset description:')
print('Number of columns:', main_data.shape[1])
print('Number of rows:', main_data.shape[0])
print('\nAvailable features/columns:')
print(main_data.columns.tolist())

# Displaying a sample of the dataset
print("\nSample Data:")
print(main_data.head(650))

def plot_columns(data, col_list, plot_type, n_col=2, **kwargs):
    n_row = len(col_list) // n_col + 1
    plt.figure(figsize=(n_col * 5, n_row * 4))  # Adjust the size as needed

    for i, col in enumerate(col_list):
        ax = plt.subplot(n_row, n_col, i + 1)

        if plot_type == "hist":
            sns.histplot(data=data, x=col, multiple="stack", **kwargs)

        elif plot_type == "bar":
            sns.barplot(data=data, x=col, **kwargs)

        elif plot_type == "count":
            sns.countplot(data=data, x=col, **kwargs)

        elif plot_type == "box":
            sns.boxplot(data=data, x=col, **kwargs)

        elif plot_type == "line":
            x = kwargs.get('x', None)
            sns.lineplot(data=data, x=x, y=col, ax=ax, **kwargs)

        elif plot_type == "trend":
            # Assuming plot_trend is a defined function
            x = kwargs.get('x', None)
            plot_trend(data=data, x=x, y=col, ax=ax, **kwargs)

        elif plot_type == "top":
            # Assuming 'top' is defined
            top = kwargs.get('top', 5)
            temp = data[col].value_counts()
            if top > 0:
                sns.barplot(x=temp.index[0:top], y=temp[0:top])
            else:
                sns.barplot(x=temp.index[-1:top:-1], y=temp[-1:top:-1])

        else:
            raise ValueError(f"Invalid plot_type argument: {plot_type}")

        ax.set_title(f"Distribution of {col}")

    plt.tight_layout()
    # plt.show()

# Function for identifying missing values
def identify_missing_values(dataframe):
    return dataframe.isnull().sum()

# Function to handle missing values
def handle_missing_values(dataframe, strategy='drop', fill_value=None):
     if strategy == 'drop':
        # Drop rows with missing values
        return dataframe.dropna()
     elif strategy == 'fill':
        # Fill missing values with a specified value
        return dataframe.fillna(fill_value)
     else:
        raise ValueError("Invalid strategy. Use 'drop' or 'fill'.")

# Function to convert data types
def convert_data_types(dataframe, column, new_type):
    dataframe[column] = dataframe[column].astype(new_type)
    return dataframe

# Path to the CSV file
main_data = r"C:\Users\Asus\Desktop\WIUT COURSE WORKS\Level 4\Exams\CSFun - On process\00016300\comments_cleaned.csv"  # Source of dataframe
# Reading the dataset
dataset = pd.read_csv(main_data, delimiter=';')

# Identifying missing values
missing_values = identify_missing_values(dataset)
print("Missing Values per Column:")
print(missing_values)

# Handling missing values
# Example: Drop rows with missing values
dataset_cleaned = handle_missing_values(dataset)

# Display cleaned dataset
print("\nCleaned Dataset:")
print(dataset_cleaned.head())

# Grouping by Emoji used and counting
data = {
    'Emoji used:': ['yes', 'no', 'no', 'yes', 'yes', 'no', 'yes'],
    'Count': [1, 0, 0, 1, 1, 0, 1]  # Example counts
}
dataset = pd.DataFrame(data)

# Initialize the main window
root = tk.Tk()
root.title('User Behaviour on Instagram')

# Frame for the plot
frame_plot = tk.Frame(root)
frame_plot.pack(fill='both', expand=True)

# Function to plot gender distribution pie chart within the Tkinter window
def plot_emoji_used():
    # Clearing previous figure
    for widget in frame_plot.winfo_children():
        widget.destroy()

    # Grouping by User ID and counting
    emoji_counts = dataset.groupby('User ID')['Emoji used'].sum().reset_index()

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(emoji_counts['Count'], labels=emoji_counts['Emoji used'], autopct='%1.1f%%', startangle=90)
    ax.set_title('User Behaviour')

    # Embedding the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Frame for the selector and button
    frame_controls = tk.Frame(root)
    frame_controls.pack(fill='x')

    # Label for the selector
    label = tk.Label(frame_controls, text="Choose Gender Column:")
    label.pack(side=tk.LEFT, padx=5, pady=5)

    # Run the application
    root.mainloop()
    # plt.show()
    # Count the occurrences of emoji used
    emoji_counts = main_data['Emoji Used'].value_counts().reset_index()
    emoji_counts.columns = ['Emoji Used', 'Count']

    # Set the size of the plot
    plt.figure(figsize=(12, 8))

    # Create a bar plot

    # Assuming nationality_counts is a DataFrame with columns 'Nationality' and 'Count'
    sns.barplot(x='Count', y='Nationality', hue='Nationality', data=emoji_counts, palette='Spectral', legend=False)
    # Add other customization as needed

    # Add labels and title
    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Emoji Used', fontsize=14)
    plt.title('Emoji Counts', fontsize=16)

    # Add value labels
    for index, value in enumerate(emoji_counts['Count']):
        plt.text(value, index, str(value))

# Calculating the average of specific columns
# print(main_data['Hashtags used count'].mean(skipna=False))

# Finding the minimum and maximum values of a column
# print("\nMaximum value of a column:")
# print(main_data.loc[main_data['Hashtags used count'].idxmax()])

# print("\nMinimum value of a column:")
# print(main_data.loc[main_data['Hashtags used count'].idxmin()])

# Counting the occurrences of a specific value in a column - Emoji Used (Yes/No)
# print("\nEmoji occurrence with Yes:")
# print(df[(df['Emoji Used']=='yes') & (df['Hashtags used count']>0)])
# print("\nEmoji occurrence with No:")
# print(df[(df['Emoji Used']=='no')] & (df['Hashtags used count']>0))

# Grouping the data by a specific category and calculating summary statistics
