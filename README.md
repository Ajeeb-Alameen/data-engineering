# 🚀 Data Engineering Project

## 📌 Project Overview

This project, developed as part of the **Data Engineering** course at **the German University in Cairo (GUC)**, focuses on **cleaning, transforming, and automating data processing** for a fintech loan dataset. It is structured into two milestones:
**Milestone 1** handles data cleaning, transformation, and consistency through reusable preprocessing functions. **Milestone 2** automates this workflow using Apache Airflow, stores the cleaned data in PostgreSQL, and visualizes insights with Apache Superset, creating a scalable and reproducible ETL pipeline.

1. **Milestone 1: Data Preprocessing**
   - Standardize column names and categorical features for consistency.
   - Handle missing values and outliers using appropriate techniques.
   - Engineer new features and encode categorical variables.
   - Normalize numerical data for consistency and scalability.
   - Implement all preprocessing steps as functions to ensure modularity and reusability.

2. **Milestone 2: ETL Pipeline & Visualization**
   - Containerize the pipeline using **Docker**.
   - Automate the ETL workflow using **Apache Airflow**.
   - Store processed data in **PostgreSQL**.
   - Visualize insights using **Apache Superset**.

---

## 🏰️ Project Structure

- [README.md](README.md) - Project overview
- [requirements.txt](requirements.txt) - Dependencies of the entire project
- **[milestone1/](milestone1/)** - Notebooks and scripts for data preprocessing
  - **[data/](milestone1/data/)** - Raw data used in preprocessing
  - **[lookup_tables/](milestone1/lookup_tables/)** - Directory for processed data CSV files.
  - [milestone1_data_preprocessing.py](milestone1\milestone1_data_preprocessing.ipynb) - Preprocessing script
  - [milestone1_description.pdf](milestone1/milestone1_description.pdf) - Milestone 1 requirements
  - [dataset_description.pdf](milestone1/dataset_description.pdf) - Dataset documentation
  - [README.md](milestone1/README.md) - Milestone 1 documentation
- **[milestone2/](milestone2/)** - Airflow DAGs, SQL scripts, and Superset setup
  - [README.md](milestone2/README.md) - Milestone 2 documentation
  - [milestone2_description.pdf](milestone2/milestone2_description.pdf) - Milestone 2 requirements
  - [dag_graph_screenshot.png](milestone2/dag_graph_screenshot.png) - DAG workflow screenshot
  - [fintech_dashboard.pdf](milestone2/fintech_dashboard.pdf) - Superset Dashboard report
  - **[docker/](milestone2/docker/)** - Containerized services setup
    - **[airflow/](milestone2/docker/airflow/)** - Airflow setup
      - [docker-compose.yml](milestone2/docker/airflow/docker-compose.yml) - Docker config for ETL automation
      - **[data/](milestone2/docker/airflow/data/)** - Raw data for ETL process
      - **[dags/](milestone2/docker/airflow/dags/)** - Airflow DAG scripts
        - [data_cleaning_dag.py](milestone2/docker/airflow/dags/data_cleaning_dag.py) - DAG for data cleaning
        - **[_functions/](/milestone2/docker/airflow/dags/_functions/)** - ETL functions
          - [cleaning1.py](/milestone2/docker/airflow/dags/_functions/cleaning1.py) - Cleaning function
    - **[postgres/](/milestone2/docker/postgres/)** - PostgreSQL and pgAdmin setup
      - [docker-compose.yml](/milestone2/docker\postgres\docker-compose.yml.yml) - PostgreSQL setup
    - **[superset/](/milestone2/docker/superset/)** - Superset setup
      - [docker-compose.yml](/milestone2/docker/superset/docker-compose.yml) - Superset configuration

Each milestone has its own **README** with setup instructions. Detailed requirements are in the accompanying PDFs.

---

## 📊 Tools & Technologies

- **Python, Pandas, NumPy** - Data Cleaning & Processing
- **Apache Airflow** - Workflow Orchestration
- **PostgreSQL** - Database Management
- **Apache Superset** - Data Visualization
- **Docker** - Containerization

---
## 📥 How to Download & Use This Project

### **1️⃣ Clone the Repository (Recommended)**
If you have Git installed, clone the repository using:
```bash
git clone https://github.com/Ajeeb-Alameen/data-engineering.git
```
Then, navigate to the project folder:
```bash
cd data-engineering
```

### **2️⃣ Download as a ZIP File (Alternative Method)**
1. Go to the **GitHub repository**.
2. Click on the **"Code"** button.
3. Select **"Download ZIP"**.
4. Extract the ZIP file on your local machine.

### **3️⃣ Install Dependencies**
Ensure you have **Python** and **Docker** installed. Then, install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔥 Future Enhancements

- Improve feature engineering for better insights.
- Deploy the ETL pipeline and dashboards in a cloud environment (AWS/Azure).
