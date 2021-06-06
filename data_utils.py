import pandas as pd

def replace_boolean_values(col):
    '''
    replace 't' with 1
    replace 'f' with 0
    fill NaN with 3
    convert columnt to INT 
    '''
    col = col.replace(to_replace='t', value=1).replace(to_replace='f', value=0)
    col.fillna(value='3', inplace=True)
    return col.astype(int)

def convert_strings_to_columns(df, col):
    '''
    INPUT:
    df - panda DataFrame containing columns with multiple categorical values as string
    col - column to be converted from string with multiple categorical values to separated columns with 0/1
        1 if column contained the particular value
        0 if not
        
    OUTPUT:
    df - new data frame with converted columns        
    '''
    columns_set = set()
    for i in range(0, df.shape[0]):
        columns_set = set.union(columns_set, df.loc[i][col].replace('"', '').replace('[', '').replace(']', '').replace(' ', '').replace('\\', '').split(sep=','))
        
    for new_col in columns_set:
        try:
            df.insert(len(df.columns), new_col, 0)
        except:
            pass
    
    for i in range(0, df.shape[0]):
        new_columns = df.loc[i].amenities.replace('"', '').replace('[', '').replace(']', '').replace(' ', '').replace('\\', '').split(sep=',')

        for new_col in new_columns:
            df.loc[i, new_col] = 1 
            
    return df, columns_set

def create_dummy_df(df, cat_cols, dummy_na):
    '''
    INPUT:
    df - pandas dataframe with categorical variables you want to dummy
    cat_cols - list of strings that are associated with names of the categorical columns
    dummy_na - Bool holding whether you want to dummy NA vals of categorical columns or not
    
    OUTPUT:
    df - a new dataframe that has the following characteristics:
            1. contains all columns that were not specified as categorical
            2. removes all the original columns in cat_cols
            3. dummy columns for each of the categorical columns in cat_cols
            4. if dummy_na is True - it also contains dummy columns for the NaN values
    '''
    
    for col in cat_cols:
        try:
            df = pd.concat([df.drop(columns=col, axis=1), pd.get_dummies(df[col], prefix=col, prefix_sep='_', drop_first=True, dummy_na=dummy_na)], axis=1)
        except:
            pass
    
    return df.copy()

  