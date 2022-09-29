# Library Calls
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

# Subset the DataFrame
def subset_data(df):
    # Create a DataFrame of all First time, Full time students for the Fall cohort
    first_full = df[(df.TIME_STATUS == 'UG Full-Time') & (df.STUDENT_TYPE == 'First-Time Freshman')]

    # Create a DataFrame of all First time, Part time students for the Fall cohort
    # first_part = df[(df.TIME_STATUS == 'UG Part-Time') & (df.STUDENT_TYPE == 'First-Time Freshman')]

    # Create a DataFrame of all Transfer, Full time students for the Fall cohort
    # transfer_full = df[(df.TIME_STATUS == 'UG Full-Time') & (df.STUDENT_TYPE == 'Transfer Student')]

    # Create a DataFrame of all Transfer, Part time students for the Fall cohort
    # transfer_part = df[(df.TIME_STATUS == 'UG Part-Time') & (df.STUDENT_TYPE == 'Transfer Student')]
    
    return first_full #, first_part, transfer_full, transfer_part

# Inspect DataFrame for size and percentages of different groups
def get_df_counts(df,name):
    
    Number_first_full = df[(df.TIME_STATUS == 'UG Full-Time') & (df.STUDENT_TYPE == 'First-Time Freshman')].shape[0]

    # Number_first_part = df[(df.TIME_STATUS == 'UG Part-Time') & (df.STUDENT_TYPE == 'First-Time Freshman')].shape[0]

    # Number_transfer_full = df[(df.TIME_STATUS == 'UG Full-Time') & (df.STUDENT_TYPE == 'Transfer Student')].shape[0]

    # Number_transfer_part = df[(df.TIME_STATUS == 'UG Part-Time') & (df.STUDENT_TYPE == 'Transfer Student')].shape[0]
    
    (print(f'{name[:-4]} Number of First Time Full Time Students: {Number_first_full}'))
             # {name[:-4]} Number of First TIme Part Time Students: {Number_first_part}\n\
             # {name[:-4]} Number of Transfer Full TIme Students: {Number_transfer_full},\n\
             # {name[:-4]} Number of Transfer Part Time Students: {Number_transfer_part}"))
    return


# Assign states with credits as split. 
# IE freshman_1 == 0 - 15 credits, 
    #freshman_2 = 16 - 30 credits, 
    #sophomore_1 == 31 - 45 credits, 
    #..... , 
    #senior_2 == 106 - 119,
    #graduate
def assign_credit_based_states(df,df_name):
    """
    This Function takes in a dataframe of student starting credits per semester and assigns them a state based on the amount of credits they have.
    """
    # Bring in the overall df to assign Transferred, Dropped, Graduated States
    all_cohort = pd.read_csv('all_ftf_cohorts.csv')
    # Make the students number the index
    all_cohort = all_cohort.set_index('pid')
    
    # Iterate through the columns
    for col in df.columns:
        # Skip columns that are not relavant
        if col in ['STUDENT_TYPE','TIME_STATUS']:
            continue
        # First Column should be the same as the file name and shows the first semester at the school. 
        elif col == df_name[:6]:
            df[col] = 'Freshman_1'
        # Now check the rows in each column
        else:
            for row in df[col].index:
                # Check to see if the student is in the overall dataframe that contains all first time full time students
                ############### Note all_cohort only contains first time full time students and the following will only run for the first time full time students subset ###########################
                if row in all_cohort.index:
                    # Check to see if they have a Transferred Out status in the overall dataframe and if so then assign that value in the new df
                    if all_cohort[col][row] == 'Transferred Out':
                        df[col][row] = 'Transferred_Out'
                    # Check to see if they have a Dropped Out status in the overall dataframe and if so then assign that value in the new df
                    elif all_cohort[col][row] == 'Dropped Out':
                        df[col][row] = 'Dropped_Out'
                    # Check to see if they have a Graduated status in the overall dataframe and if so then assign that value in the new df
                    elif all_cohort[col][row] == 'Graduated':
                        df[col][row] = 'Graduated'
                    # Check if there is a Nan value and if so this indicates the student took a sabbatical if the above values arent present
                    elif np.isnan(df[col][row]):
                        df[col][row] = 'Sabbatical'
                    # If none of the above cases happened we assume there is a credit value and assign what state a student is based on credit amount
                    elif (df[col][row] >= 0) and (df[col][row] <= 15):
                        df[col][row] = 'Freshman_1'
                    elif (df[col][row] > 15) and (df[col][row] <= 30):
                        df[col][row] = 'Freshman_2'
                    elif (df[col][row] > 30) and (df[col][row] <= 45):
                        df[col][row] = 'Sophomore_1'
                    elif (df[col][row] > 45) and (df[col][row] <= 60):
                        df[col][row] = 'Sophomore_2'
                    elif (df[col][row] > 60) and (df[col][row] <= 75):
                        df[col][row] = 'Junior_1'
                    elif (df[col][row] > 75) and (df[col][row] <= 90):
                        df[col][row] = 'Junior_2'
                    elif (df[col][row] > 90) and (df[col][row] <= 105):
                        df[col][row] = 'Senior_1'
                    elif (df[col][row] > 105):
                        df[col][row] = 'Senior_2'
        for row in df[col].index:
            if df[col][row] in ['Graduated','Dropped_Out','Transferred_Out']:
                continue
            elif col[4:6] == '30':
                df[col][row] = f'Spring_{df[col][row]}'
            elif col[4:6] == '40':
                df[col][row] = f'Summer_{df[col][row]}'
            elif col[4:6] == '50':
                df[col][row] = f'Fall_{df[col][row]}'
            else:
                continue
    return df

def credit_wrangle_df(string_csv_name):
        # Using the string nmae of csv file we will read in the dataframe
        df = pd.read_csv(string_csv_name)
        df = df.set_index('PIDM')
        
        # Print out proportions
        print(get_df_counts(df,string_csv_name)) 
        
        # Subset the dataframe into sub groups of student types
        first_full = subset_data(df)
        #, first_part, transfer_full, transfer_part
        # reassign data to states
        first_full = assign_credit_based_states(first_full, string_csv_name)
        # first_part = assign_credit_based_states(first_part, string_csv_name)
        # transfer_full= assign_credit_based_states(transfer_full, string_csv_name)
        # transfer_part= assign_credit_based_states(transfer_part, string_csv_name)

        return first_full#, first_part, transfer_full, transfer_part

def credit_combine_all_df():
    
    credit_df_2011_2018 = pd.DataFrame()   
    list_file_names = ['201150_cohort.csv','201250_cohort.csv','201350_cohort.csv','201450_cohort.csv',
                       '201550_cohort.csv','201650_cohort.csv','201750_cohort.csv','201850_cohort.csv']
    
    for cohort in list_file_names:
        cff = credit_wrangle_df(cohort)
        # , cfp, ctf, ctp
        credit_df_2011_2018 = pd.concat([credit_df_2011_2018, cff], axis=0)        
    
    print(f'Total Credit Count: {credit_df_2011_2018.shape}')   
    
    return credit_df_2011_2018.iloc[:,2:]

# Create semester seperated dataframe
# If first semester as class = class_1
# If second to n semester as class = class_n

def assign_semester_based_states(df, df_name):
    """
    This Function takes in a dataframe of student starting credits per semester and assigns them a state based on semesters in a class.
    """
    # Bring in the overall df to assign Transferred, Dropped, Graduated States
    all_cohort = pd.read_csv('all_ftf_cohorts.csv')
    # Make the students number the index
    all_cohort = all_cohort.set_index('pid')
    
    # Iterate through the columns
    for col in df.columns:
        # Skip columns that are not relavant
        if col in ['STUDENT_TYPE','TIME_STATUS']:
            continue
        # First Column should be the same as the file name and shows the first semester at the school. 
        elif col == df_name[:6]:
            df[col] = 'Freshman_1'
        # Now check the rows in each column
        else:
            for row in df.index:
                # Check to see if the student is in the overall dataframe that contains all first time full time students
                ### Note all_cohort only contains first time full time students and the following will only run for the first time full time students subset ###
                if row in all_cohort.index:
                    # Check to see if they have a Transferred Out status in the overall dataframe and if so then assign that value in the new df
                    if all_cohort[col][row] == 'Transferred Out':
                        df[col][row] = 'Transferred_Out'
                    # Check to see if they have a Dropped Out status in the overall dataframe and if so then assign that value in the new df
                    elif all_cohort[col][row] == 'Dropped Out':
                        df[col][row] = 'Dropped_Out'
                    # Check to see if they have a Graduated status in the overall dataframe and if so then assign that value in the new df
                    elif all_cohort[col][row] == 'Graduated':
                        df[col][row] = 'Graduated'
                    # Check if there is a Nan value and if so this indicates the student took a sabbatical if the above values arent present
                    elif np.isnan(df[col][row]):
                        df[col][row] = 'Sabbatical'
                    # If none of the above cases happened we assume there is a credit value and assign what state a student is based on credit
                    # amount and time in class
                    elif (df[col][row] >= 0) and (df[col][row] <= 30):
                        df[col][row] = 'Freshman_n'
                    elif (df[col][row] > 30) and (df[col][row] <= 60):
                        df[col][row] = 'Sophomore_1'
                    elif (df[col][row] > 60) and (df[col][row] <= 90):    
                        df[col][row] = 'Junior_1'
                    elif (df[col][row] > 90):
                        df[col][row] = 'Senior_1'
                    else:
                        df[col][row] = 'Fix_Me'
                        
        for row in df.index:
            if (df[col][row] == 'Sophomore_1') and (df.loc[row:row,:col].values[0].tolist().count('Sophomore_1') > 1):
                df[col][row] = 'Sophomore_n'
            elif (df[col][row] == 'Junior_1') and (df.loc[row:row,:col].values[0].tolist().count('Junior_1') > 1):
                df[col][row] = 'Junior_n'
            elif (df[col][row] == 'Senior_1') and (df.loc[row:row,:col].values[0].tolist().count('Senior_1') > 1):
                df[col][row] = 'Senior_n'
            else:
                continue
    
    for col in df.columns:
        for row in df.index:
            if df[col][row] in ['Graduated','Dropped_Out','Transferred_Out']:
                continue
            elif col[4:6] == '30':
                df[col][row] = f'Spring_{df[col][row]}'
            elif col[4:6] == '40':
                df[col][row] = f'Summer_{df[col][row]}'
            elif col[4:6] == '50':
                df[col][row] = f'Fall_{df[col][row]}'
            else:
                continue

    return df

def semester_wrangle_df(string_csv_name):
        # Using the string nmae of csv file we will read in the dataframe
        df = pd.read_csv(string_csv_name)
        df = df.set_index('PIDM')
        
        # Print out proportions
        print(get_df_counts(df,string_csv_name)) 
        
        # Subset the dataframe into sub groups of student types
        first_full = subset_data(df)
        # , first_part, transfer_full, transfer_part
        
        # reassign data to states
        first_full = assign_semester_based_states(first_full, string_csv_name)
        # first_part = assign_semester_based_states(first_part, string_csv_name)
        # transfer_full= assign_semester_based_states(transfer_full, string_csv_name)
        # transfer_part= assign_semester_based_states(transfer_part, string_csv_name)

        return first_full # , first_part, transfer_full, transfer_part
    

def semester_combine_all_df():
    
    semester_df_2011_2018 = pd.DataFrame()
    list_file_names = ['201150_cohort.csv','201250_cohort.csv','201350_cohort.csv','201450_cohort.csv',
                       '201550_cohort.csv','201650_cohort.csv','201750_cohort.csv','201850_cohort.csv']
    
    for cohort in list_file_names:
        sff = semester_wrangle_df(cohort)
        # , sfp, stf, stp
        semester_df_2011_2018 = pd.concat([semester_df_2011_2018, sff], axis=0)
   
    print(f'Total Semester Size: {semester_df_2011_2018.shape}')
    
    return semester_df_2011_2018.iloc[:,2:]