
# Final Project - Group 35
# AUTHORS: Dillon Pullano and Gopal Sharma

"""
This terminal-based data analysis application loads in crime and community data for the city of Calgary between 2015 and 2017.
It analyzes and calculates specific aggregated statistics based on user's selected community and category of crime / disorder.
Authors: Dillon Pullano and Gopal Sharma 
"""

import numpy as np
import pandas as pd
from pandas import IndexSlice
import matplotlib as mpl
import matplotlib.pyplot as plt

def load_data():
    """
    This function loads in the excel files from the main project folder and merges them.

    Args: NONE

    Returns:
        - df_2015_2017      --> Crime data for years 2015, 2016, and 2017
        - df_stat_merged    --> Merged data from crime and historical data
    """

    # Load in the crime and disorder statistics for 2015, 2016, and 2017:
    df_2015 = pd.read_excel("Community_Crime_and_Disorder_Statistics__2015.xlsx")
    df_2016 = pd.read_excel("Community_Crime_and_Disorder_Statistics__2016.xlsx")
    df_2017 = pd.read_excel("Community_Crime_and_Disorder_Statistics__2017.xlsx")

    # Concatenate crime and order statistics:
    df_2015_2017 = pd.concat([df_2015, df_2016, df_2017], ignore_index = True)

    # Load in historical community population statistics and store only years 2015, 2016, and 2017:
    df_comm_hist = pd.read_excel("Historical_Community_Populations_1968-2017.xlsx")

    # Index using year, slice out the 2015, 2016, and 2017 years, then recombine:
    df_comm_hist = df_comm_hist.set_index(["Year"])
    df_comm_hist_2015 = df_comm_hist.loc[pd.IndexSlice[2015]]
    df_comm_hist_2016 = df_comm_hist.loc[pd.IndexSlice[2016]]
    df_comm_hist_2017 = df_comm_hist.loc[pd.IndexSlice[2017]]
    df_comm_hist = pd.concat([df_comm_hist_2015, df_comm_hist_2016, df_comm_hist_2017], ignore_index = False)

    # Merge 2 sets of data using community name as index:
    df_stat_merged = pd.merge(df_2015_2017, df_comm_hist, on=["Community Name", "Year"])

    # Remember to check for null values:
    null_counts = df_stat_merged.isnull().sum()     

    # Drop any duplicated columns:
    df_stat_merged = df_stat_merged.loc[:, ~df_stat_merged.columns.duplicated()]

    # Drop any duplicated rows:
    df_stat_merged = df_stat_merged.drop_duplicates()

    # Drop un-needed columns from combined dataframe:
    df_stat_merged = df_stat_merged.drop(['Date','ID', 'Community Center Point', 'comm_code', 'population', 'notes'], axis = 1) # Assigns the result back to df

    return df_2015_2017, df_stat_merged


def prompt_user(df_2015_2017):
    """
    This function asks the user for input variables and stores them for further use.

    Args:
        - df_2015_2017      --> Crime data for years 2015, 2016, and 2017

    Returns:
        - user_input1       --> Stores the user selection of a valid community name in Calgary
        - user_input2       --> Stores the user selection regarding community 'crime' or 'disorder'
    """
        
    # Prompt user for 'Community Name':
    while True:
        try:
            user_input1 = input("Please enter the name of a community in Calgary: ")
            
            if (user_input1.lower() in df_2015_2017["Community Name"].str.lower().unique()):
                user_input1 = user_input1.upper()   
                print(f"You have selected '{user_input1}'")
                break

            else:
                raise KeyError()
            
        except KeyError:
            print("Community name not found in the data. Please review the sample list printed above and try again.")

    # Prompt user for severity of crime (Violent / Non-Violent) statistics desired:
    while True:
        try:
            user_input2 = input(f"Do you want statistics for 'Crime' or 'Disorder' in {user_input1.upper()}? (Crime / Disorder): ")
            
            if (user_input2.upper() == "CRIME"):
                user_input2 = "Crime"
                print(f"You have selected '{user_input2}':")
                break

            elif (user_input2.upper() == "DISORDER"):
                user_input2 = "Disorder"
                print(f"You have selected '{user_input2}':")
                break

            else:
                raise ValueError()
            
        except ValueError:
            print("Incorrect user input. Please try again.")
    
    return user_input1, user_input2


def slice_user_data(df_stat_merged, user_input1, user_input2):
    """
    This function takes in all merged data and user inputs. It slices out a subset of data that corresponds to user inputs.

    Args:
        - df_stat_merged    --> Crime data for years 2015, 2016, and 2017
        - user_input1       --> Stores the user selection of a valid community name in Calgary 
        - user_input2       --> Stores the user selection regarding community 'crime' or 'disorder'

    Returns:
        - df_comm_cat       --> Subset of merged data that corresponds to user inputs
    """

    # Slice out the data associated with the 'Community Name' specified by the user:
    df_comm = df_stat_merged.set_index(["Community Name"])
    df_comm = df_comm.loc[pd.IndexSlice[user_input1]]

    # Slice out the data associated with the community crime 'Group Category' (i.e. crime vs disorder):
    df_comm_cat = df_comm.set_index(["Group Category"])
    df_comm_cat = df_comm_cat.loc[pd.IndexSlice[user_input2]]

    # Create hierarchical index of at least two levels:
    df_comm_cat = df_comm_cat.set_index(['Sector', 'Year', 'Month', 'Category'])
    
    # Sort the DataFrame based on the index:
    df_comm_cat = df_comm_cat.sort_index()

    return df_comm_cat


def add_yearly_total_columns(df_comm_cat):
    """
    This function adds a column to the data which reflects the yearly total crime.

    Args:
        - df_comm_cat       --> Subset of merged data that corresponds to user inputs

    Returns:
        - df_comm_cat_2     --> New DataFrame that has new 'Yearly_Total' column added
        - total_2015        --> Total crime from 'df_comm_cat' for 2015
        - total_2016        --> Total crime from 'df_comm_cat' for 2016
        - total_2017        --> Total crime from 'df_comm_cat' for 2017
    """

    # Set index to 'Year':
    df_comm_cat1 = df_comm_cat.reset_index()
    df_comm_cat1 = df_comm_cat1.set_index(["Year"])

    # Get totals for each year:
    total_2015 = df_comm_cat1.loc[2015]["Crime Count"].sum()
    total_2016 = df_comm_cat1.loc[2016]["Crime Count"].sum()
    total_2017 = df_comm_cat1.loc[2017]["Crime Count"].sum()

    # Get DataFrame for individual years:
    df_comm_cat_2015 = df_comm_cat1.loc[2015]
    df_comm_cat_2016 = df_comm_cat1.loc[2016]
    df_comm_cat_2017 = df_comm_cat1.loc[2017]

    # Assign total values to new column:
    df_comm_cat_2015 = df_comm_cat_2015.assign(Yearly_Total = total_2015)
    df_comm_cat_2016 = df_comm_cat_2016.assign(Yearly_Total = total_2016)
    df_comm_cat_2017 = df_comm_cat_2017.assign(Yearly_Total = total_2017)

    # Concatenate all files back together:
    df_comm_cat_2 = pd.concat([df_comm_cat_2015, df_comm_cat_2016, df_comm_cat_2017], ignore_index = False)

    return df_comm_cat_2, total_2015, total_2016, total_2017


def add_monthly_total_columns(df_comm_cat_2):
    """
    This function adds a column to the data which reflects the monthly total crime.

    Args:
        - df_comm_cat_2     --> Subset of merged data that corresponds to user inputs

    Returns:
        - df_comm_cat_3     --> New DataFrame including Year/Month/count indexing. This is used for masking later on
        - df_comm_cat_4     --> New DataFrame that has new 'Monthly Total' column added
    """

    # Reset index:
    df_comm_cat_3 = df_comm_cat_2.reset_index()
    
    # Use groupby op to calculate crime count per month for all years:
    df_comm_cat_3 = df_comm_cat_3.groupby(['Year', 'Month'])['Crime Count'].sum()  

    # Rename column for further use:
    df_comm_cat_3 = df_comm_cat_3.rename('Monthly Total')

    # Merge back with original dataframe:
    df_comm_cat_4 = pd.merge(df_comm_cat_2, df_comm_cat_3, on=["Year", "Month"])

    return df_comm_cat_3, df_comm_cat_4



def occurrence_max_min(df_comm_cat_4, user_input1, user_input2):
    """
    This function calculates and outputs the most and least common category of crime/disorder in the community.

    Args:
        - df_comm_cat_4     --> DataFrame that has our new columns added to it
        - user_input1       --> Stores the user selection of a valid community name in Calgary 
        - user_input2       --> Stores the user selection regarding community 'crime' or 'disorder'

    Returns: NONE
    """

    # Aggregate and count by category:
    df_comm_cat_5 = df_comm_cat_4.reset_index() 
    df_comm_cat_5 = df_comm_cat_5.groupby(['Category'])['Crime Count'].sum()   # Aggregation

    # Create minimum and maximum occurence masks and apply masks:
    max_mask = (df_comm_cat_5 == df_comm_cat_5.max())
    min_mask = (df_comm_cat_5 == df_comm_cat_5.min())
    max_occur = (df_comm_cat_5[max_mask]).index
    min_occur = (df_comm_cat_5[min_mask]).index

    # Output min and max results to console:
    print(f"\nThe following are the most common types of {user_input2}(s) in {user_input1} between 2015 and 2017 with {df_comm_cat_5.max()} occurrences: {' '.join(max_occur)}")
    print(f"The following are the least common types of {user_input2}(s) in {user_input1} between 2015 and 2017 with {df_comm_cat_5.min()} occurrences: {' '.join(min_occur)}")
    

def month_max_min(df_comm_cat_3, year, user_input1, user_input2):
    """
    This function finds and outputs the months with maximum and minimum crimes for a specified 'year'.

    Args:
        - df_comm_cat_3     --> DataFrame including Year/Month/count indexing.
        - user_input1       --> Stores the user selection of a valid community name in Calgary 
        - user_input2       --> Stores the user selection regarding community 'crime' or 'disorder'

    Returns: NONE
    """

    # Grab the year out of the main dataset:
    df_month = df_comm_cat_3[year]

    # Create masks for min and max count:
    max_month_mask = (df_month == df_month.max())
    min_month_mask = (df_month == df_month.min())

    # Apply masks and return index values:
    max_month_occur = (df_month[max_month_mask]).index
    min_month_occur = (df_month[min_month_mask]).index

    # Output max and min category total (crime / disorder) to terminal:
    print(f"\nThe month(s) in {year} with the most {user_input2}(s) in {user_input1} is: {' '.join(max_month_occur)}")
    print(f"The month(s) in {year} with the least {user_input2}(s) in {user_input1} is: {' '.join(min_month_occur)}")


def main():
    """
    This function is the main entry point which implements the different components of this application.

    Args: NONE

    Returns: NONE
    """

    # Print out a header for the start of program output:
    print("\n\n\n*************************************\nCalgary Crime Statistics (2015-2017)\n*************************************\n")
    print("Please see below a small list (non-exhaustive) of possible community names that can be selected for your first input:")
    print("(Acadia, Beltline, Dover, Erlton, Glenbrook, Hillhurst, Manchester, Oakridge, Wildwood, etc.)\n")
    #----------------------------------------------------------
    # Part A - Load in the data from 3 excel sheets:
    #----------------------------------------------------------
    df_2015_2017, df_stat_merged = load_data()  # Load data into main

    #----------------------------------------------------------
    # Part B - Prompt user Entry:
    #----------------------------------------------------------
    user_input1, user_input2 = prompt_user(df_2015_2017)

    #----------------------------------------------------------
    # Part C - Analysis and Calculations:
    #----------------------------------------------------------

    # Slice out the data that is specific to the user's inputs:
    df_comm_cat = slice_user_data(df_stat_merged, user_input1, user_input2)

    # Add a column for the yearly crime totals:
    df_comm_cat_2, total_2015, total_2016, total_2017 = add_yearly_total_columns(df_comm_cat)
    
    # Add a column for the yearly crime per capita:
    df_comm_cat_2["Yearly Per Capita"] = (df_comm_cat_2["Yearly_Total"] / df_comm_cat_2["Resident Count"])

    # Add a column for the monthly crime totals:
    df_comm_cat_3, df_comm_cat_4 = add_monthly_total_columns(df_comm_cat_2)

    # Use the describe method to print aggregate stats for the sliced dataset:
    print(f"\nStats for the selected community '{user_input1}' and category '{user_input2}' using the 'Describe' method: \n")
    print(df_comm_cat_4.describe())

    # Print the yearly occurence totals and dataset total:
    print(f"\nThere were a total of {total_2015 + total_2016 + total_2017} {user_input2}(s) in {user_input1} between 2015 and 2017.")
    print(f"There were a total of {total_2015} {user_input2}(s) in {user_input1} in 2015.")
    print(f"There were a total of {total_2016} {user_input2}(s) in {user_input1} in 2016.")
    print(f"There were a total of {total_2017} {user_input2}(s) in {user_input1} in 2017.")
    
    # Get the total occurences of each 'Category' and return the max and min occurences:
    occurrence_max_min(df_comm_cat_4, user_input1, user_input2)

    # Calculate and output the month with maximum and minimum crime for each year:
    for year in [2015, 2016, 2017]:
        month_max_min(df_comm_cat_3, year, user_input1, user_input2)

    #----------------------------------------------------------
    # Part D - Export Pivot, Matplotlib, and Excel file:
    #----------------------------------------------------------

    # Pivot table creation:
    df_pivot = df_comm_cat_4.pivot_table('Monthly Total', index='Year', columns='Month')
    month_order = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    # Reindex the columns of the pivot table using the custom month order
    df_pivot = df_pivot.reindex(columns=month_order)
    print("\nThe pivot table below shows the relationship between crimes and months for the given 3 year period:\n")
    print(df_pivot)

    # Use data to create bar plot:
    df_pivot = df_pivot.transpose()                                         # Transpose
    df_pivot.plot(kind='bar', figsize=(10, 6))                              # Initialize plot
    plt.xlabel('Month')                                                     # Set x-axis label   
    plt.ylabel('Monthly Total of Crimes')                                   # Set y-axis label
    plt.title(f'Monthly {user_input2} Occurances in {user_input1} by Year') # Set plot title 
    plt.legend(title='Year')                                                # Add a legend
    plt.savefig('my_figure.png')                                            # Save as .PNG image
    plt.show()                                                              # Display the plot

    # Write to an excel file and export:
    df_comm_cat_4 = df_comm_cat_4.reset_index()
    df_comm_cat_4 = df_comm_cat_4.set_index(['Sector', 'Year', 'Month', 'Category'])
    df_comm_cat_4 = df_comm_cat_4.sort_index()
    df_comm_cat_4.to_excel("Selected_Community_Data_Output.xlsx", index = True, header = True)


if __name__ == '__main__':
    main()