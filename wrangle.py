import pandas as pd
from sklearn.model_selection import train_test_split

def acquire_data(file_name1, file_name2):
    '''
ARGS:
    - CSV FILE 1 (STRING)
    - CSV FILE 2 (STRING)
RETURNS:
    - JOINED DF (DATAFRAME)

THIS FUNCTION TAKES IN TWO CSV FILE NAMES, WRITES THE FILE DATA TO TWO PANDAS DFS, AND THEN SETS THE INDEX OF EACH 
DATAFRAME TO ITS RESPECTIVE COLUMN OF COUNTY FIPS CODES. THE DFS ARE THEN JOINED ON THOSE INDEX COLUMNS, RETURNING
ONE JOINED DF. 
    '''
    df1 = pd.read_csv(file_name1)
    df2 = pd.read_csv(file_name2)

    for file_name in [file_name1, file_name2]:
        print(f'✅ {file_name} successfully acquired.')

    print()
    # for df in [df1, df2]:
    #     print(f'There are {df.shape[0]} rows and {df.shape[1]} columns in the data.')
    #     print(f'There are {df.isna().sum().sum()} null values in the data.')
    #     print()

    # setting index for each column as column with FIPS code to join them on.
    df1.set_index('GEOID', inplace = True)
    df2.set_index('CountyId', inplace = True)

    df = df1.join(df2, how = 'inner', lsuffix = '_mvi', rsuffix = '_cd')
    print(f'✅ DataFrames successfully joined.')
    print()

    return df


def clean_data(df):
    '''
    
    '''

    # drop the row with the null value
    df.dropna(inplace = True)
    
    # filter DataFrame to have only columns in this to_keep list
    cols_to_keep = ['State_mvi', 'Th1', 'Th2', 'Th3', 'Th4', 'Th5', 'County', 'TotalPop', 'Men', 'Women',\
                'Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific', 'VotingAgeCitizen', 'Income',\
                'Poverty', 'ChildPoverty', 'WorkAtHome', 'MeanCommute', 'Employed', 'SelfEmployed',\
                'Unemployment', 'mvi']
    df = df[cols_to_keep]

    # formatting and renaming the remaining columns
        # all lowercase
    df.columns = df.columns.str.lower()

    # renaming select coluns
    df.rename(columns = {'state_mvi': 'state', 'totalpop':'pop_total', 'men':'pop_men', 'women':'pop_women',\
                           'votingagecitizen':'pop_vot_age', 'childpoverty':'child_poverty', 'workathome':'wfh',\
                           'meancommute':'avg_commute', 'self_employed':'self_employ'}, inplace = True)

    # adding new columns
    df['more_women'] = df.pop_women > df.pop_men
    df['perc_women'] = round(df.pop_women / df.pop_total*100, 1)
    print('✅ Data is cleaned.')
    print()

    return df

def prepare_data(df):
    '''
    
    '''

    # dropping x1 District of Columbia state class, in order to stratify on state, must be at least x2 unique values for each class
    df.drop(11001, inplace = True)

    # splitting data for exploration and modeling
        # creating test dataset
    train_validate, test = train_test_split(df, test_size=.2, random_state=12, stratify=df.state)

        # creating the train and test datasets
    train, validate = train_test_split(train_validate, test_size=.3, random_state=12, stratify=train_validate.state)

    # verifying the split
    print('✅ Data has been successfully split and is ready for exploration.')
    print(f'train -> {train.shape}')
    print(f'validate -> {validate.shape}')
    print(f'test -> {test.shape}')
    print()

    return train, validate, test