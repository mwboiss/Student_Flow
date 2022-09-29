import pandas as pd
import numpy as np
import scipy.linalg as la

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

def credit_overall_transition_matrix(cohort_states):
    """
    This function takes in a dataframe of students and there states and returns a transition matrix for every transition in the data
    
    """
    cohort_states = cohort_states.rename(columns={'201150':0, '201230':1, '201240':2, '201250':3,
                                                  '201330':4, '201340':5, '201350':6, '201430':7,
                                                  '201440':8, '201450':9, '201530':10, '201540':11,
                                                  '201550':12, '201630':13, '201640':14, '201650':15,
                                                  '201730':16, '201740':17, '201750':18, '201830':19,
                                                  '201840':20, '201850':21, '201930':22, '201940':23,
                                                  '201950':24, '202030':25, '202040':26, '202050':27,
                                                  '202130':28, '202140':29, '202150':30, '202230':31})
    cohort_states = cohort_states.reset_index()
    cohort_states = cohort_states.drop(columns=['PIDM'])

    # Create a dictionary of states each state could change into
    Graduated = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Transferred_Out = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Dropped_Out = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Sabbatical = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Freshman_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Freshman_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Sophomore_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Sophomore_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Junior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Junior_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Senior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Fall_Senior_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Sabbatical = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Freshman_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Freshman_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Sophomore_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Sophomore_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Junior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Junior_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Senior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Spring_Senior_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Summer_Sabbatical = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Summer_Freshman_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Summer_Freshman_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Summer_Sophomore_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Summer_Sophomore_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Summer_Junior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Summer_Junior_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}
 
    Summer_Senior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}

    Summer_Senior_2 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_2' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_2' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_2' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_2': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_1' : 0,'Spring_Freshman_2' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_2' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_2' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_2': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_1' : 0,'Summer_Freshman_2' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_2' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_2' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_2': 0}
    
    # Run through the dataframe and add 1 to every current states next state

    for x in range(cohort_states.shape[0]):
        for y in range(cohort_states.shape[1]-1):
            if pd.isnull(cohort_states[y][x]):
                continue
            elif pd.isnull(cohort_states[y + 1][x]):
                continue
            elif cohort_states[y][x] == 'Graduated':
                Graduated[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Transferred_Out':
                Transferred_Out[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Dropped_Out':
                Dropped_Out[cohort_states[y + 1][x]] += 1 

            elif cohort_states[y][x] == 'Fall_Sabbatical':
                Fall_Sabbatical[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Fall_Freshman_1':
                Fall_Freshman_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Fall_Freshman_2':
                Fall_Freshman_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Fall_Sophomore_1':
                Fall_Sophomore_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Fall_Sophomore_2':
                Fall_Sophomore_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Fall_Junior_1':
                Fall_Junior_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Fall_Junior_2':
                Fall_Junior_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Fall_Senior_1':
                Fall_Senior_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Fall_Senior_2':
                Fall_Senior_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Sabbatical':
                Spring_Sabbatical[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Freshman_1':
                Spring_Freshman_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Spring_Freshman_2':
                Spring_Freshman_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Sophomore_1':
                Spring_Sophomore_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Spring_Sophomore_2':
                Spring_Sophomore_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Junior_1':
                Spring_Junior_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Spring_Junior_2':
                Spring_Junior_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Senior_1':
                Spring_Senior_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Spring_Senior_2':
                Spring_Senior_2[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Summer_Sabbatical':
                Summer_Sabbatical[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Summer_Freshman_1':
                Summer_Freshman_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Summer_Freshman_2':
                Summer_Freshman_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Summer_Sophomore_1':
                Summer_Sophomore_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Summer_Sophomore_2':
                Summer_Sophomore_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Summer_Junior_1':
                Summer_Junior_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Summer_Junior_2':
                Summer_Junior_2[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Summer_Senior_1':
                Summer_Senior_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Summer_Senior_2':
                Summer_Senior_2[cohort_states[y + 1][x]] += 1  
            
    # Change that value into a probability
    Graduated_Prob = []
    for x in Graduated.values():
        Graduated_Prob.append(round(x / sum(Graduated.values()),4))

    Transferred_Out_Prob = []
    for x in Transferred_Out.values():
        Transferred_Out_Prob.append(round(x / sum(Transferred_Out.values()),4))

    Dropped_Out_Prob = []
    for x in Dropped_Out.values():
        Dropped_Out_Prob.append(round(x / sum(Dropped_Out.values()),4))

    Fall_Sabbatical_Prob = []
    for x in Fall_Sabbatical.values():
        Fall_Sabbatical_Prob.append(round(x / sum(Fall_Sabbatical.values()),4))

    Fall_Freshman_1_Prob = []
    for x in Fall_Freshman_1.values():
        Fall_Freshman_1_Prob.append(round(x / sum(Fall_Freshman_1.values()),4))
    
    Fall_Freshman_2_Prob = []
    for x in Fall_Freshman_2.values():
        Fall_Freshman_2_Prob.append(round(x / sum(Fall_Freshman_2.values()),4))

    Fall_Sophomore_1_Prob = []
    for x in Fall_Sophomore_1.values():
        Fall_Sophomore_1_Prob.append(round(x / sum(Fall_Sophomore_1.values()),4))
    
    Fall_Sophomore_2_Prob = []
    for x in Fall_Sophomore_2.values():
        Fall_Sophomore_2_Prob.append(round(x / sum(Fall_Sophomore_2.values()),4))

    Fall_Junior_1_Prob = []
    for x in Fall_Junior_1.values():
        Fall_Junior_1_Prob.append(round(x / sum(Fall_Junior_1.values()),4))
    
    Fall_Junior_2_Prob = []
    for x in Fall_Junior_2.values():
        Fall_Junior_2_Prob.append(round(x / sum(Fall_Junior_2.values()),4))

    Fall_Senior_1_Prob = []
    for x in Fall_Senior_1.values():
        Fall_Senior_1_Prob.append(round(x / sum(Fall_Senior_1.values()),4))
    
    Fall_Senior_2_Prob = []
    for x in Fall_Senior_2.values():
        Fall_Senior_2_Prob.append(round(x / sum(Fall_Senior_2.values()),4))

    Spring_Sabbatical_Prob = []
    for x in Spring_Sabbatical.values():
        Spring_Sabbatical_Prob.append(round(x / sum(Spring_Sabbatical.values()),4))

    Spring_Freshman_1_Prob = []
    for x in Spring_Freshman_1.values():
        Spring_Freshman_1_Prob.append(round(x / sum(Spring_Freshman_1.values()),4))
    
    Spring_Freshman_2_Prob = []
    for x in Spring_Freshman_2.values():
        Spring_Freshman_2_Prob.append(round(x / sum(Spring_Freshman_2.values()),4))

    Spring_Sophomore_1_Prob = []
    for x in Spring_Sophomore_1.values():
        Spring_Sophomore_1_Prob.append(round(x / sum(Spring_Sophomore_1.values()),4))
    
    Spring_Sophomore_2_Prob = []
    for x in Spring_Sophomore_2.values():
        Spring_Sophomore_2_Prob.append(round(x / sum(Spring_Sophomore_2.values()),4))

    Spring_Junior_1_Prob = []
    for x in Spring_Junior_1.values():
        Spring_Junior_1_Prob.append(round(x / sum(Spring_Junior_1.values()),4))
    
    Spring_Junior_2_Prob = []
    for x in Spring_Junior_2.values():
        Spring_Junior_2_Prob.append(round(x / sum(Spring_Junior_2.values()),4))

    Spring_Senior_1_Prob = []
    for x in Spring_Senior_1.values():
        Spring_Senior_1_Prob.append(round(x / sum(Spring_Senior_1.values()),4))
    
    Spring_Senior_2_Prob = []
    for x in Spring_Senior_2.values():
        Spring_Senior_2_Prob.append(round(x / sum(Spring_Senior_2.values()),4))

    Summer_Sabbatical_Prob = []
    for x in Summer_Sabbatical.values():
        Summer_Sabbatical_Prob.append(round(x / sum(Summer_Sabbatical.values()),4))

    Summer_Freshman_1_Prob = []
    for x in Summer_Freshman_1.values():
        Summer_Freshman_1_Prob.append(round(x / sum(Summer_Freshman_1.values()),4))
    
    Summer_Freshman_2_Prob = []
    for x in Summer_Freshman_2.values():
        Summer_Freshman_2_Prob.append(round(x / sum(Summer_Freshman_2.values()),4))

    Summer_Sophomore_1_Prob = []
    for x in Summer_Sophomore_1.values():
        Summer_Sophomore_1_Prob.append(round(x / sum(Summer_Sophomore_1.values()),4))
    
    Summer_Sophomore_2_Prob = []
    for x in Summer_Sophomore_2.values():
        Summer_Sophomore_2_Prob.append(round(x / sum(Summer_Sophomore_2.values()),4))

    Summer_Junior_1_Prob = []
    for x in Summer_Junior_1.values():
        Summer_Junior_1_Prob.append(round(x / sum(Summer_Junior_1.values()),4))
    
    Summer_Junior_2_Prob = []
    for x in Summer_Junior_2.values():
        Summer_Junior_2_Prob.append(round(x / sum(Summer_Junior_2.values()),4))

    Summer_Senior_1_Prob = []
    for x in Summer_Senior_1.values():
        Summer_Senior_1_Prob.append(round(x / sum(Summer_Senior_1.values()),4))
    
    Summer_Senior_2_Prob = []
    for x in Summer_Senior_2.values():
        Summer_Senior_2_Prob.append(round(x / sum(Summer_Senior_2.values()),4))
    
    # Transition Matrix
    ctm = np.array([Graduated_Prob, Transferred_Out_Prob, Dropped_Out_Prob,
      Fall_Sabbatical_Prob,
      Fall_Freshman_1_Prob, Fall_Freshman_2_Prob,
      Fall_Sophomore_1_Prob, Fall_Sophomore_2_Prob, 
      Fall_Junior_1_Prob, Fall_Junior_2_Prob,
      Fall_Senior_1_Prob, Fall_Senior_2_Prob,
      Spring_Sabbatical_Prob,
      Spring_Freshman_1_Prob, Spring_Freshman_2_Prob,
      Spring_Sophomore_1_Prob, Spring_Sophomore_2_Prob,
      Spring_Junior_1_Prob, Spring_Junior_2_Prob,
      Spring_Senior_1_Prob, Spring_Senior_2_Prob,
      Summer_Sabbatical_Prob,
      Summer_Freshman_1_Prob, Summer_Freshman_2_Prob,
      Summer_Sophomore_1_Prob, Summer_Sophomore_2_Prob,
      Summer_Junior_1_Prob, Summer_Junior_2_Prob,
      Summer_Senior_1_Prob, Summer_Senior_2_Prob])
    
    states =  ['Graduated','Transferred_Out','Dropped_Out',
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

    # Transtion matrix is in standard form
    credit_transition_matrix = pd.DataFrame(ctm, columns=states, index=states)

    # Transition Matrix (Assuming Transferred Out is an abosorbtion state along with Graduated and Dropped Out)

    # P = [[I O]
    #      [A B]]

    return credit_transition_matrix

def semester_overall_transition_matrix(cohort_states):
    """
    This function takes in a dataframe of students and there states and returns a transition matrix for every transition in the data
    
    """
    cohort_states = cohort_states.rename(columns={'201150':0, '201230':1, '201240':2, '201250':3,
                                                  '201330':4, '201340':5, '201350':6, '201430':7,
                                                  '201440':8, '201450':9, '201530':10, '201540':11,
                                                  '201550':12, '201630':13, '201640':14, '201650':15,
                                                  '201730':16, '201740':17, '201750':18, '201830':19,
                                                  '201840':20, '201850':21, '201930':22, '201940':23,
                                                  '201950':24, '202030':25, '202040':26, '202050':27,
                                                  '202130':28, '202140':29, '202150':30, '202230':31})
    cohort_states = cohort_states.reset_index()
    cohort_states = cohort_states.drop(columns=['PIDM'])
    
    # Create a dictionary of states each state could change into
    Graduated = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Transferred_Out = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Dropped_Out = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Sabbatical = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Freshman_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Freshman_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Sophomore_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Sophomore_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Junior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Junior_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Senior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Fall_Senior_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Spring_Sabbatical = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Spring_Freshman_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Spring_Sophomore_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Spring_Sophomore_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Spring_Junior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Spring_Junior_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Spring_Senior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Spring_Senior_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Summer_Sabbatical = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Summer_Freshman_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Summer_Sophomore_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Summer_Sophomore_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Summer_Junior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Summer_Junior_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}
 
    Summer_Senior_1 = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}

    Summer_Senior_n = {'Graduated' : 0,'Transferred_Out' : 0,'Dropped_Out' : 0,
                 'Fall_Sabbatical' : 0,
                 'Fall_Freshman_1' : 0,'Fall_Freshman_n' : 0,
                 'Fall_Sophomore_1' : 0,'Fall_Sophomore_n' : 0,
                 'Fall_Junior_1' : 0,'Fall_Junior_n' : 0,
                 'Fall_Senior_1': 0,'Fall_Senior_n': 0,
                 'Spring_Sabbatical' : 0,
                 'Spring_Freshman_n' : 0,
                 'Spring_Sophomore_1' : 0,'Spring_Sophomore_n' : 0,
                 'Spring_Junior_1' : 0,'Spring_Junior_n' : 0,
                 'Spring_Senior_1': 0, 'Spring_Senior_n': 0,
                 'Summer_Sabbatical' : 0,
                 'Summer_Freshman_n' : 0,
                 'Summer_Sophomore_1' : 0,'Summer_Sophomore_n' : 0,
                 'Summer_Junior_1' : 0,'Summer_Junior_n' : 0,
                 'Summer_Senior_1': 0, 'Summer_Senior_n': 0}
    
    # Run through the dataframe and add 1 to every current states next state

    for x in range(cohort_states.shape[0]):
        for y in range(cohort_states.shape[1]-1):
            if pd.isnull(cohort_states[y][x]):
                continue
            elif pd.isnull(cohort_states[y + 1][x]):
                continue
            elif cohort_states[y][x] == 'Graduated':
                Graduated[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Transferred_Out':
                Transferred_Out[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Dropped_Out':
                Dropped_Out[cohort_states[y + 1][x]] += 1 

            elif cohort_states[y][x] == 'Fall_Sabbatical':
                Fall_Sabbatical[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Fall_Freshman_1':
                Fall_Freshman_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Fall_Freshman_n':
                Fall_Freshman_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Fall_Sophomore_1':
                Fall_Sophomore_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Fall_Sophomore_n':
                Fall_Sophomore_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Fall_Junior_1':
                Fall_Junior_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Fall_Junior_n':
                Fall_Junior_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Fall_Senior_1':
                Fall_Senior_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Fall_Senior_n':
                Fall_Senior_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Sabbatical':
                Spring_Sabbatical[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Freshman_n':
                Spring_Freshman_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Sophomore_1':
                Spring_Sophomore_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Spring_Sophomore_n':
                Spring_Sophomore_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Junior_1':
                Spring_Junior_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Spring_Junior_n':
                Spring_Junior_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Spring_Senior_1':
                Spring_Senior_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Spring_Senior_n':
                Spring_Senior_n[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Summer_Sabbatical':
                Summer_Sabbatical[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Summer_Freshman_n':
                Summer_Freshman_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Summer_Sophomore_1':
                Summer_Sophomore_1[cohort_states[y + 1][x]] += 1
                
            elif cohort_states[y][x] == 'Summer_Sophomore_n':
                Summer_Sophomore_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Summer_Junior_1':
                Summer_Junior_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Summer_Junior_n':
                Summer_Junior_n[cohort_states[y + 1][x]] += 1

            elif cohort_states[y][x] == 'Summer_Senior_1':
                Summer_Senior_1[cohort_states[y + 1][x]] += 1
            
            elif cohort_states[y][x] == 'Summer_Senior_n':
                Summer_Senior_n[cohort_states[y + 1][x]] += 1
    
    # Change that value into a probability
    Graduated_Prob = []
    for x in Graduated.values():
        Graduated_Prob.append(round(x / sum(Graduated.values()),4))

    Transferred_Out_Prob = []
    for x in Transferred_Out.values():
        Transferred_Out_Prob.append(round(x / sum(Transferred_Out.values()),4))

    Dropped_Out_Prob = []
    for x in Dropped_Out.values():
        Dropped_Out_Prob.append(round(x / sum(Dropped_Out.values()),4))

    Fall_Sabbatical_Prob = []
    for x in Fall_Sabbatical.values():
        Fall_Sabbatical_Prob.append(round(x / sum(Fall_Sabbatical.values()),4))

    Fall_Freshman_1_Prob = []
    for x in Fall_Freshman_1.values():
        Fall_Freshman_1_Prob.append(round(x / sum(Fall_Freshman_1.values()),4))
    
    Fall_Freshman_n_Prob = []
    for x in Fall_Freshman_n.values():
        Fall_Freshman_n_Prob.append(round(x / sum(Fall_Freshman_n.values()),4))

    Fall_Sophomore_1_Prob = []
    for x in Fall_Sophomore_1.values():
        Fall_Sophomore_1_Prob.append(round(x / sum(Fall_Sophomore_1.values()),4))
    
    Fall_Sophomore_n_Prob = []
    for x in Fall_Sophomore_n.values():
        Fall_Sophomore_n_Prob.append(round(x / sum(Fall_Sophomore_n.values()),4))

    Fall_Junior_1_Prob = []
    for x in Fall_Junior_1.values():
        Fall_Junior_1_Prob.append(round(x / sum(Fall_Junior_1.values()),4))
    
    Fall_Junior_n_Prob = []
    for x in Fall_Junior_n.values():
        Fall_Junior_n_Prob.append(round(x / sum(Fall_Junior_n.values()),4))

    Fall_Senior_1_Prob = []
    for x in Fall_Senior_1.values():
        Fall_Senior_1_Prob.append(round(x / sum(Fall_Senior_1.values()),4))
    
    Fall_Senior_n_Prob = []
    for x in Fall_Senior_n.values():
        Fall_Senior_n_Prob.append(round(x / sum(Fall_Senior_n.values()),4))

    Spring_Sabbatical_Prob = []
    for x in Spring_Sabbatical.values():
        Spring_Sabbatical_Prob.append(round(x / sum(Spring_Sabbatical.values()),4))

    Spring_Freshman_n_Prob = []
    for x in Spring_Freshman_n.values():
        Spring_Freshman_n_Prob.append(round(x / sum(Spring_Freshman_n.values()),4))

    Spring_Sophomore_1_Prob = []
    for x in Spring_Sophomore_1.values():
        Spring_Sophomore_1_Prob.append(round(x / sum(Spring_Sophomore_1.values()),4))
    
    Spring_Sophomore_n_Prob = []
    for x in Spring_Sophomore_n.values():
        Spring_Sophomore_n_Prob.append(round(x / sum(Spring_Sophomore_n.values()),4))

    Spring_Junior_1_Prob = []
    for x in Spring_Junior_1.values():
        Spring_Junior_1_Prob.append(round(x / sum(Spring_Junior_1.values()),4))
    
    Spring_Junior_n_Prob = []
    for x in Spring_Junior_n.values():
        Spring_Junior_n_Prob.append(round(x / sum(Spring_Junior_n.values()),4))

    Spring_Senior_1_Prob = []
    for x in Spring_Senior_1.values():
        Spring_Senior_1_Prob.append(round(x / sum(Spring_Senior_1.values()),4))
    
    Spring_Senior_n_Prob = []
    for x in Spring_Senior_n.values():
        Spring_Senior_n_Prob.append(round(x / sum(Spring_Senior_n.values()),4))

    Summer_Sabbatical_Prob = []
    for x in Summer_Sabbatical.values():
        Summer_Sabbatical_Prob.append(round(x / sum(Summer_Sabbatical.values()),4))

    Summer_Freshman_n_Prob = []
    for x in Summer_Freshman_n.values():
        Summer_Freshman_n_Prob.append(round(x / sum(Summer_Freshman_n.values()),4))

    Summer_Sophomore_1_Prob = []
    for x in Summer_Sophomore_1.values():
        Summer_Sophomore_1_Prob.append(round(x / sum(Summer_Sophomore_1.values()),4))
    
    Summer_Sophomore_n_Prob = []
    for x in Summer_Sophomore_n.values():
        Summer_Sophomore_n_Prob.append(round(x / sum(Summer_Sophomore_n.values()),4))

    Summer_Junior_1_Prob = []
    for x in Summer_Junior_1.values():
        Summer_Junior_1_Prob.append(round(x / sum(Summer_Junior_1.values()),4))
    
    Summer_Junior_n_Prob = []
    for x in Summer_Junior_n.values():
        Summer_Junior_n_Prob.append(round(x / sum(Summer_Junior_n.values()),4))

    Summer_Senior_1_Prob = []
    for x in Summer_Senior_1.values():
        Summer_Senior_1_Prob.append(round(x / sum(Summer_Senior_1.values()),4))
    
    Summer_Senior_n_Prob = []
    for x in Summer_Senior_n.values():
        Summer_Senior_n_Prob.append(round(x / sum(Summer_Senior_n.values()),4))
    
    # Transition Matrix
    stm = np.array([Graduated_Prob, Transferred_Out_Prob, Dropped_Out_Prob,
      Fall_Sabbatical_Prob,
      Fall_Freshman_1_Prob, Fall_Freshman_n_Prob,
      Fall_Sophomore_1_Prob, Fall_Sophomore_n_Prob, 
      Fall_Junior_1_Prob, Fall_Junior_n_Prob,
      Fall_Senior_1_Prob, Fall_Senior_n_Prob,
      Spring_Sabbatical_Prob,
      Spring_Freshman_n_Prob,
      Spring_Sophomore_1_Prob, Spring_Sophomore_n_Prob,
      Spring_Junior_1_Prob, Spring_Junior_n_Prob,
      Spring_Senior_1_Prob, Spring_Senior_n_Prob,
      Summer_Sabbatical_Prob,
      Summer_Freshman_n_Prob,
      Summer_Sophomore_1_Prob, Summer_Sophomore_n_Prob,
      Summer_Junior_1_Prob, Summer_Junior_n_Prob,
      Summer_Senior_1_Prob, Summer_Senior_n_Prob])
        
    states = ['Graduated','Transferred_Out','Dropped_Out',
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
    
    # Transtion matrix is in standard form
    semester_transition_matrix = pd.DataFrame(stm, columns=states, index=states)

    # Transition Matrix (Assuming Transferred Out is an abosorbtion state along with Graduated and Dropped Out)

    # P = [[I O]
    #      [A B]]

    return semester_transition_matrix