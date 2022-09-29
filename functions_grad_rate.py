import pandas as pd
import numpy.linalg as la

import functions_wrangle as fw
import functions_transition_matrix as ftm

import warnings
warnings.filterwarnings('ignore')

def traditional_six_year_grad_rates(df):
    '''
    This function takes in a DataFrame and returns a dictionary with the sememester names as the key and the six year graduation rate as the value.
    '''
    # Create a empty dictionary to store rates
    grad_rates = {}
    # Set the index for the inital start
    cohort_start_index_value = 0
    # Loop through the dataframe column names
    for col in df.columns:
        # if the 6 year grad semester from the current semester exists and it is a fall semeseter then create the grad rate
        if ((df.columns.get_loc(col) + 17) < (df.shape[1] - 1)) & (col[4:6] == '50'):
            print(f'Cohort Start Year: {col}')
            # save the name of the grad semester
            grad_semester = df.columns[df.columns.get_loc(col) + 17]
            print(f'Cohort Six Year: {grad_semester}')
            # Get the index of the first cohort member
            cohort_start = df.index[cohort_start_index_value]
            print(f'Cohort First Student: {cohort_start}')
            # get the index of the last cohort member
            cohort_end = df[col][df[col].isna() == False].index[-1]
            print(f'Cohort Last Student: {cohort_end}')
            # save the value of how many students started the cohort
            started = df.loc[cohort_start:cohort_end,col:col].shape[0]
            print(f'Students Started: {started}')
            # Save the value of how many of those students graduated
            graduated = df.loc[cohort_start:cohort_end,grad_semester:grad_semester].value_counts()['Graduated']
            print(f'Students Graduated: {graduated}')
            # Reset the value for cohort start
            ############## RECHECK ME TO MAKE SURE THIS IS WORKING CORRECTLY######################
            ############## Manually check PIDM's for start and stop ##############################
            cohort_start_index_value += started
            print(f'Students Started so far: {cohort_start_index_value}')        
            # Calculate out the graduation rate
            grad_rate = round(graduated / started, 4)
            print(f'Grad Rate: {grad_rate}\n')
            # Store that rate in the dictionary
            grad_rates[col] = grad_rate
            # Print out the relevant information
            # print(f"Starting Semester: {col},\n\
            #         Six Year Semester: {grad_semester},\n\
            #         Students Started: {started},\n\ 
            #         Students Graduated: {graduated},\n\ 
            #         Graduation Rate: {grad_rate}")
    # return the dictionary for later use
    return grad_rates

def credit_markov_six_year_t_matrix(df):
    # Names of States
    state = ['Graduated','Transferred_Out','Dropped_Out',
      'Fall_Sabbatical',
      'Fall_Freshman_1','Fall_Freshman_2',
      'Fall_Sophomore_1','Fall_Sophomore_2', 
      'Fall_Junior_1','Fall_Junior_2',
      'Fall_Senior_1','Fall_Senior_2',
      'Spring_Sabbatical',
      'Spring_Freshman_1','Spring_Freshman_2',
      'Spring_Sophomore_1','Spring_Sophomore_2',
      'Spring_Junior_1','Spring_Junior_2',
      'Spring_Senior_1', 'Spring_Senior_2',
      'Summer_Sabbatical',
      'Summer_Freshman_1','Summer_Freshman_2',
      'Summer_Sophomore_1','Summer_Sophomore_2',
      'Summer_Junior_1','Summer_Junior_2',
      'Summer_Senior_1', 'Summer_Senior_2']
    # Create T Matrix
    t_matrix = ftm.credit_overall_transition_matrix(df)
    # Calculate out 17 steps to be at last semester of 6th year
    steps = la.matrix_power(t_matrix,17)
    # Assign to a dataframe
    end_matrix = pd.DataFrame(steps, columns = state, index = state)
    
    return end_matrix

def semester_markov_six_year_t_matrix(df):
    # Names of States
    state = ['Graduated','Transferred_Out','Dropped_Out',
      'Fall_Sabbatical',
      'Fall_Freshman_1','Fall_Freshman_n',
      'Fall_Sophomore_1','Fall_Sophomore_n', 
      'Fall_Junior_1','Fall_Junior_n',
      'Fall_Senior_1','Fall_Senior_n',
      'Spring_Sabbatical',
      'Spring_Freshman_n',
      'Spring_Sophomore_1','Spring_Sophomore_n',
      'Spring_Junior_1','Spring_Junior_n',
      'Spring_Senior_1', 'Spring_Senior_n',
      'Summer_Sabbatical',
      'Summer_Freshman_n',
      'Summer_Sophomore_1','Summer_Sophomore_n',
      'Summer_Junior_1','Summer_Junior_n',
      'Summer_Senior_1', 'Summer_Senior_n']
    # Create T Matrix
    t_matrix = ftm.semester_overall_transition_matrix(df)
    # Calculate out 17 steps to be at last semester of 6th year
    steps = la.matrix_power(t_matrix,17)
    # Assign to a dataframe
    end_matrix = pd.DataFrame(steps, columns = state, index = state)
    
    return end_matrix

