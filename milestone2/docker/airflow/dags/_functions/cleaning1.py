import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


#1. Function to load the transformed data to the database

def load_to_db(filename:str, table_name:str, postgres_opt:dict):
    '''
    Load the transformed data to the database
    @param filename: str, path to the parquet file
    @param table_name: str, name of the table to create
    @param postgres_opt: dict, dictionary containing postgres connection options (user, password, host,port, db)
    '''
    user, password, host, port, db = postgres_opt.values()
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df = pd.read_parquet(filename)
    # Set the index to ['customer_id', 'loan_id']
    df.set_index(['customer_id', 'loan_id'], inplace=True)
    df.to_sql(table_name, con=engine, if_exists='replace', index=True, index_label=['customer_id','loan_id'])
    # Save the DataFrame to a CSV file for the next task
    output_path = '/opt/airflow/data/fintech_db_table.csv'
    df.to_csv(output_path, index=False)
    
    return output_path


#2. function to extract and clean the data

def extract_and_clean_data(filename, output_path):

    """Wrapper function to call all cleaning functions."""

    df = load_and_preview_data(filename)
    df = standardize_dataframe(df)
    df = standardize_issue_date(df)
    df = standardize_emp_length(df)
    df = transform_grade_to_letter(df)
    df = impute_employment_data(df)
    df = impute_int_rate(df)
    df = calculate_supporting_income(df)
    df = impute_description(df)
    df = calculate_monthly_installment(df)

    # Save the cleaned DataFrame to a CSV file
    df.to_parquet(output_path, index=False)
    return df


#3. Function to extract state data from a local CSV file

def extract_state_data(file_name,output_path):
    """
    Extracts state data from a local CSV file.

    Args:
        filepath (str): Path to the local CSV file.
        output_path (str): Path to save the extracted data.
    Returns:
        pd.DataFrame: DataFrame containing the extracted state data.
    """
    # Load the state data from the CSV file
    df = pd.read_csv(file_name)

    # Save the extracted data to a parquet file
    df.to_parquet(output_path, index=False)

    return df

#4. Function to combine the extracted state data with the main DataFrame

def combine_sources (main_file,state_data,output_path):
    """
    Combines the main DataFrame with the states DataFrame to add state names.

    Args:
        df (pd.DataFrame): The main DataFrame containing loan information.
        states_df (pd.DataFrame): The DataFrame containing state codes and names.

    Returns:
        pd.DataFrame: The merged DataFrame with added state names.
    """
    # Load the main DataFrame
    df = pd.read_parquet(main_file)

    # Load the state data
    states_df = pd.read_parquet(state_data)

    # 1. Convert 'state' column values to uppercase
    df['state'] = df['state'].astype(str).str.upper()

    # 2. merge the two dataframes
    df = pd.merge(df, states_df, left_on='state', right_on='code', how='left')

    # 3. Fills missing values if state_name exists, otherwise creates it
    if 'state_name' in df.columns: 
        df['state_name'].fillna(df['name'])
    else:
        df['state_name'] = df['name']

    # 4. Drop unnecessary columns 'name' and 'code' after merging
    df.drop(columns=['name', 'code'], errors='ignore', inplace=True)

    # 5. Save the merged DataFrame to a parquet file
    df.to_parquet(output_path, index=False)
    return df

#5. Function to identify and handle outliers

def handle_outliers(filename, output_path):

    """Wrapper function to identify and handle outliers."""

    df = pd.read_csv(filename)
    
    df, outlier_columns = identify_outliers(df)
    df = handle_outlier_columns_with_log(df, outlier_columns)
    
    # Save the cleaned DataFrame to a CSV file
    df.to_csv(output_path, index=False)
    return df

#6. Function to encode categorical features

def encode_categorical_features(filename, output_path, encoding_lookup_path):
    """
    Encodes categorical features in the DataFrame and saves the encoded DataFrame and encoding lookup to the output paths.
    """
    df = pd.read_csv(filename)
    encoding_lookup = []

    # One-hot encoding
    one_hot_columns = ['home_ownership', 'verification_status', 'term', 'type', 'loan_status']
    for col in one_hot_columns:
        original_values = df[col].unique()
        df = pd.get_dummies(df, columns=[col], drop_first=False, dtype=int)

    # Label encoding for 'grade_letter', 'state', and 'addr_state'
    le = LabelEncoder()
    for col in ['grade_letter', 'state', 'addr_state']:
        df[col] = le.fit_transform(df[col])
        for original_val, encoded_val in zip(le.classes_, le.transform(le.classes_)):
            encoding_lookup.append({'column_name': col, 'original_value': original_val, 'encoded_value': encoded_val})

    # Frequency encoding for 'purpose'
    purpose_freq = df['purpose'].value_counts(normalize=True).to_dict()
    df['purpose'] = df['purpose'].map(purpose_freq)
    for original_val, encoded_val in purpose_freq.items():
        encoding_lookup.append({'column_name': 'purpose', 'original_value': original_val, 'encoded_value': encoded_val})

    # Save the encoding lookup DataFrame
    encoding_lookup_df = pd.DataFrame(encoding_lookup)
    encoding_lookup_df.to_csv(encoding_lookup_path, index=False)
    
    # Save the encoded DataFrame to a CSV file
    df.to_csv(output_path, index=False)
    
    return df, encoding_lookup_df


# --------------------------------- Helper Functions ---------------------------------------#


# Function to load and preview the data
def load_and_preview_data(file_path):

    ''' Load the data and copy it to avoid modifying the original dataset '''

    original = pd.read_csv(file_path)
    df = original.copy()
    return df

# Function to standardize the DataFrame
def standardize_dataframe(df):

    ''' Standardize the column names and string formatting '''

    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ', '_')
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    for col in categorical_cols:
        df[col] = df[col].str.lower()
    return df

# Function to standardize the issue date
def standardize_issue_date(df, issue_date_column='issue_date'):

    ''' Standardize the issue date column '''

    df[issue_date_column] = pd.to_datetime(df[issue_date_column])
    df['issue_month'] = df[issue_date_column].dt.month
    df.sort_values(by=[issue_date_column], inplace=True)
    df[issue_date_column] = df[issue_date_column].astype(str)
    return df


# Function to standardize employment length
def standardize_emp_length(df, emp_length_column='emp_length'):

    ''' Standardize the employment length column '''

    replacements = {'< 1 year': '0.5', '10+ years': '10'}
    df[emp_length_column] = df[emp_length_column].replace(replacements, regex=False)
    df[emp_length_column] = df[emp_length_column].astype(str).str.extract(r'(\d+\.?\d*)')
    df[emp_length_column] = pd.to_numeric(df[emp_length_column], errors='coerce')
    return df

# Function to transform the grade to a letter
def transform_grade_to_letter(df, grade_column='grade'):

    ''' Transform the grade column to a letter grade '''

    conditions = [
        (df[grade_column] >= 1) & (df[grade_column] <= 5),
        (df[grade_column] >= 6) & (df[grade_column] <= 10),
        (df[grade_column] >= 11) & (df[grade_column] <= 15),
        (df[grade_column] >= 16) & (df[grade_column] <= 20),
        (df[grade_column] >= 21) & (df[grade_column] <= 25),
        (df[grade_column] >= 26) & (df[grade_column] <= 30),
        (df[grade_column] >= 31) & (df[grade_column] <= 35)
    ]
    choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    df['grade_letter'] = np.select(conditions, choices, default=None)
    return df


# Function to impute employment data
def impute_employment_data(df):

    ''' Impute missing employment data '''

    if 'emp_title' not in df.columns or 'emp_length' not in df.columns:
        raise KeyError("Columns 'emp_title' and 'emp_length' must be present in the DataFrame.")
    
    mask_both_null = df['emp_title'].isna() & df['emp_length'].isna()
    mask_title_null = df['emp_title'].isna() & ~df['emp_length'].isna()
    mask_length_null = ~df['emp_title'].isna() & df['emp_length'].isna()
    df.loc[mask_both_null, ['emp_title', 'emp_length']] = ['unemployed', 0]
    df.loc[mask_title_null, 'emp_title'] = 'unknown'
    df.loc[mask_length_null, 'emp_length'] = 0.1
    return df


# Function to impute interest rate
def impute_int_rate(df, grade_column='grade_letter', term_column='term', target_column='int_rate'):

    ''' Impute missing interest rates based on the grade and term '''

    grouped_means = df.groupby([grade_column, term_column])[target_column].mean()
    missing_mask = df[target_column].isna()
    df.loc[missing_mask, target_column] = df.loc[missing_mask].apply(
        lambda row: grouped_means.get((row[grade_column], row[term_column])), axis=1
    )
    return df


# Function to impute annual income joint and calculate supporting income
def calculate_supporting_income(df):


    ''' Calculate the supporting income based on the annual income and annual income joint '''

    df['supporting_income'] = df['annual_inc_joint'] - df['annual_inc']
    df['supporting_income'] = df.apply(lambda row: 0 if pd.isnull(row['annual_inc_joint']) else row['supporting_income'], axis=1)
    df.drop('annual_inc_joint', axis=1, inplace=True)
    return df


# Function to impute description
def impute_description(df):

    ''' Impute missing descriptions based on the purpose '''

    purpose_modes = (
        df.groupby('purpose')['description']
        .apply(lambda x: x.mode().iloc[0] if not x.mode().empty else x.name)
    )
    missing_mask = df['description'].isnull()
    df.loc[missing_mask, 'description'] = df.loc[missing_mask, 'purpose'].map(purpose_modes)
    return df


# Function to calculate the monthly installment
def calculate_monthly_installment(df, P='funded_amount', term_column='term'):

    ''' Calculate the monthly installment based on the funded amount and term '''

    df['term_in_months'] = df[term_column].str.extract(r'(\d+)').astype(int)
    df['monthly_interest_rate'] = df['int_rate'] / 12
    df['monthly_installment'] = df.apply(
        lambda row: (
            row[P] * row['monthly_interest_rate'] * (1 + row['monthly_interest_rate']) ** row['term_in_months']
        ) / (
            (1 + row['monthly_interest_rate']) ** row['term_in_months'] - 1
        ) if row['monthly_interest_rate'] > 0 else row[P] / row['term_in_months'],
        axis=1
    )
    df['salary_can_cover'] = (df['annual_inc'] >= df['monthly_installment'] * 12)
    df.drop(columns=['monthly_interest_rate', 'term_in_months'], inplace=True)
    return df


# Function to identify outliers
def identify_outliers(df):

    ''' Identify outliers in the numerical columns '''

    numerical_cols = ['emp_length', 'annual_inc', 'avg_cur_bal', 'tot_cur_bal',
                      'loan_amount', 'funded_amount', 'int_rate', 'grade',
                      'supporting_income', 'monthly_installment']

    outlier_columns = []

    for col in numerical_cols:
        if col in df.columns:
            data = df[col]
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(data < lower_bound) | (data > upper_bound)]
            if not outliers.empty:
                outlier_columns.append(col)

    return df, outlier_columns


# Function to handle outlier columns with log transformation
def handle_outlier_columns_with_log(df, outlier_columns):

    ''' Handle outlier columns with log transformation '''

    for col in outlier_columns:
        if col in df.columns:
            df[col] = np.log1p(df[col])
    return df