# **Fintech Loan Data Analysis & Preprocessing**  

## 🚀 **Project Overview**
Milestone 1 focuses on cleaning, transforming, and analyzing a fintech loan dataset to prepare it for machine learning models. This involves handling missing values, engineering new features, and performing exploratory data analysis (EDA) to uncover insights. This stage ensures consistency and reproducibility for the next phase (Milestone 2) of the ETL pipeline, where automation and data integration will be implemented.  

---  

## 📁 **Project Structure**
- [milestone1_data_preprocessing.ipynb](milestone1_data_preprocessing.ipynb) - Jupyter Notebook for preprocessing  
- [lookup_tables/](lookup_tables/) - Stores lookup tables for cleaned and transformed data after running (.ipynb) file 
- [data/](data/) - Raw datasets  
- [README.md](README.md) - Project documentation 


---  

## 🔄 **Core Methods**

### 🧹 **1. Data Cleaning**  
- Standardized column names and set appropriate indexes.  
- Unified categorical values for consistency.  
- Removed duplicate records and created lookup tables for tracking changes.  
- Analyzed and handled missing values using imputation strategies.  


### 🏗️ **2. Feature Engineering** 
- Extracted the **month number** from the issue date.  
- Created a **"Salary Can Cover"** column to assess loan affordability based on income.  
- Encoded **loan grades (A-G)** into numerical values.  
- Calculated **monthly loan installment** using loan amount, interest rate, and term.  
- **Bonus Task:** Mapped state abbreviations to full names using web scraping to enrich data.  


### 📊 **3. Exploratory Data Analysis (EDA)**   
- **Customer Growth & Loan Trends:** Analyzed loan funding trends over time.  
- **Loan Status Distribution:** Examined the classification of loans (e.g., fully paid, late, charged off).  
- **Home Ownership Trends:** Explored financial behavior among renters, homeowners, and mortgage holders.  
- **State-Wise Analysis:** Investigated income and loan funding variations by state.  
- **Job Title Insights:** Identified common job titles and their impact on income and loan funding.  


### 📏 **4. Normalization and Handling Outliers** 
- **Outliers:** Detected using the IQR method and visualized with boxplots.  
- **Normalization:** Applied Min-Max scaling to rescale numerical features to a [0,1] range.  


### 🔠 **5. Encoding**  
- Applied **one-hot encoding, frequency encoding, and ordinal encoding** where appropriate.  



### 💾 **6. Output & Saving** 
- Created lookup tables to document all transformations and imputations.  
- Saved the cleaned dataset and lookup tables as CSV files.  
- Processed data is automatically stored in the `milestone1/lookup_tables/` directory after running the notebook. Ensure this folder exists before execution to prevent errors.

---  

## ⚙️ **How to Use**   
1. **Set up your environment:** Install dependencies using:
   ```bash
   pip install -r ../requirements.txt
   ```
   (Ensure you have the required packages by installing them from `requirements.txt`.)
2. **Run the Jupyter Notebook** sequentially to apply transformations step-by-step.
3. **Use the cleaned dataset** for machine learning models after processing.
4. **Check the `lookup_tables/` directory** for transformation tracking. 

---

🏁 Milestone 1 successfully establishes a structured data preprocessing workflow, ensuring clean, consistent, and well-engineered data. These transformations lay the foundation for further automation in Milestone 2, where the ETL process will be streamlined using Apache Airflow, PostgreSQL, and Superset.

---
