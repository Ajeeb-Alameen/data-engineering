# 🚀 Data Engineering ETL Project

📌 Project Overview

Milestone 2 automates the ETL pipeline established in Milestone 1, ensuring a scalable, efficient, and reproducible data workflow for seamless analysis and visualization. The goal is to transition from manual data preprocessing to an automated ETL pipeline, where Apache **Airflow** orchestrates workflows, **PostgreSQL** handles data storage, and **Superset** enables visualization—all running as containerized services using Docker.

---

## 📚 **Table of Contents**

- [Prerequisites](#prerequisites)
- [Folder Structure](#folder-structure)
- [Running the Project](#running-the-project)
  - [1️⃣ Create the Docker Network](#1️⃣-create-the-docker-network)
  - [2️⃣ Start PostgreSQL](#2️⃣-start-postgresql)
  - [3️⃣ Start Airflow (Task Orchestration)](#3️⃣-start-airflow-task-orchestration)
  - [4️⃣ Verify Data in PostgreSQL](#4️⃣-verify-data-in-postgresql)
   - [🛠️ Viewing Data with Adminer](#%F0%9F%9B%A0%EF%B8%8F-viewing-data-with-adminer)
  - [5️⃣ Start Superset (Dashboarding)](#5️⃣-start-superset-dashboarding)

---



🔹 **Note:** The web interfaces for Airflow, Superset, and PostgreSQL may take a few minutes to become accessible. If they are not immediately available, please wait and refresh the page.

---

##  Folder Structure (milestone2)

- [README.md](README.md) - Milestone 2 documentation
- [milestone2_description.pdf](milestone2_description.pdf) - Milestone 2 requirements
- [dag_graph_screenshot.png](dag_graph_screenshot.png) - DAG workflow screenshot
- [fintech_dashboard.pdf](fintech_dashboard.pdf) - Superset Dashboard report
- **[docker/](docker/)** - Containerized services setup
   - **[airflow/](docker/airflow/)** - Airflow setup
      - [docker-compose.yml](docker/airflow/docker-compose.yml) - Docker config for ETL automation
      - **[data/](docker/airflow/data/)** - Raw & processed data for ETL process
      - **[dags/](docker/airflow/dags/)** - Airflow DAG scripts
      - [data_cleaning_dag.py](docker/airflow/dags/data_cleaning_dag.py) - DAG scripts for ETl
      - **[_functions/](docker/airflow/dags/_functions/)** - ETL functions
         - [cleaning1.py](docker/airflow/dags/_functions/cleaning1.py) - DAG functions used in ETL
   - **[postgres/](docker/postgres/)** - PostgreSQL and pgAdmin setup
      - [docker-compose.yml](docker/postgres/docker-compose.yml) - PostgreSQL setup
   - **[superset/](docker/superset/)** - Superset setup
      - [docker-compose.yml](docker/superset/docker-compose.yml) - Superset configuration
      
---

##  Prerequisites

Before running the project, make sure you have:
- **[Docker](https://www.docker.com/)** installed and **running**

**Set up your environment:** Install dependencies using:
   ```bash
   pip install -r ../requirements.txt
   ```

---

##  Running the Project

⏳ **Startup Delay Notice:** Some services (Airflow, Superset, and PostgreSQL) **may take 1-2 minutes to fully initialize**. If a web interface is not immediately accessible, **wait and refresh the page**.

**🔹 Steps to Start the Project**  
Before running these commands, ensure:  
✅ **Docker** is installed and **running**  
✅ You are inside the `milestone2/` folder  

Run the following commands in order:

### 1️⃣ Create the Docker Network

```bash
docker network create data_engineering || echo "Network already exists"
```

This ensures all services can communicate within the same network.


### 2️⃣ Start PostgreSQL

This starts the PostgreSQL database, which stores the data for Airflow and Superset.

```bash
docker compose -f docker/postgres/docker-compose.yml up -d
```


### 3️⃣ Start Airflow (Task Orchestration)

Airflow is used for automating data pipelines.
Use the `--build` option before `-d` if this is your first time creating the image.

```bash
docker compose -f docker/airflow/docker-compose.yml up -d
```

Once Airflow is running, go to **[Airflow](http://localhost:8080)** and trigger the DAG manually.

🔹 Pipeline Triggering: The DAG is manually triggered through the Airflow UI. There is no scheduled execution.
   - **Username**: `airflow`.
   - **Password**: `airflow`.

🔹 Note: If the web interface is not immediately accessible, wait a few seconds and refresh the page.

#### 📄 DAG Workflow Overview

This **Airflow DAG** (`data_cleaning_dag.py`) automates fintech data processing with the following tasks:

1️⃣ **Extract & Clean Data** → Loads raw data, standardizes formats, and handles missing values.  
2️⃣ **Extract State Data** → Reads and saves state information for merging.  
3️⃣ **Combine Data Sources** → Merges fintech data with state details.  
4️⃣ **Load to PostgreSQL** → Stores the cleaned dataset in a database.  
5️⃣ **Handle Outliers** → Detects and adjusts extreme values using log transformation.  
6️⃣ **Encode Categorical Features** → Applies encoding techniques for categorical data.  



### 4️⃣ Verify Data in PostgreSQL

Once the Airflow tasks run successfully, check the data in the PostgreSQL database:
- **pgAdmin**: [http://localhost:5050](http://localhost:5050)

   #### 🛠️ **Connecting pgAdmin to PostgreSQL (`data_engineering` Database)**

   Since your `POSTGRES_DB` is set to `data_engineering`, the database **already exists**, and you just need to connect to it in pgAdmin.

   1️⃣ **Open pgAdmin** at [http://localhost:5050](http://localhost:5050).

   2️⃣ **Log in** with the following credentials:
      - **Email**: `root@root.com`
      - **Password**: `root`

   3️⃣ In the **pgAdmin interface**, right-click on the **"Servers"** node and select **"Create" → "Server..."**.

   4️⃣ In the **"Create - Server"** dialog, enter the following details:
      - **Name**: `PostgreSQL`  # This is just a label
      - **Host name/address**: `pgdatabase`  # Matches the service name in `docker-compose.yml`
      - **Port**: `5432`
      - **Username**: `root`
      - **Password**: `root`

   5️⃣ Click **"Save"** to create the server connection.

   6️⃣ Expand the **"Servers"** node, and you should see `data_engineering` under **Databases**.

   🔹 The `fintech_clean` table is now created and can be accessed in **pgAdmin** under `data_engineering` > `Schemas` > `public` > `Tables`.



   #### 🛠️ Viewing Data with Adminer

   Adminer is a lightweight alternative to pgAdmin.

   - **Access Adminer at**: [http://localhost:5051](http://localhost:5051)
   - **Login Credentials**:
   - **System**: PostgreSQL
   - **Server**: `pgdatabase`
   - **Username**: `root`
   - **Password**: `root`
   - **Database**: `data_engineering`



### 5️⃣ Start Superset (Dashboarding)

Superset is used to visualize and explore data.

```bash
docker compose -f docker/superset/docker-compose.yml up -d
```

🔹 **Note:** Superset and Airflow may take a few minutes to start. If the UI is not immediately accessible, wait a few minutes and try again. If your system has limited processing power, consider stopping the **Airflow** container after running the DAGs. Running Airflow and Superset together may slow performance.


#### 📊 Connecting Superset to PostgreSQL

To visualize the data in Superset, follow these steps:

1️⃣ Open Superset at [http://localhost:8088](http://localhost:8088).

   - **Username**: `admin`
   - **Password**: `admin`

2️⃣ Go to **Settings (⚙️) → Database Connections**.

3️⃣ Click **+ Database** and enter:
   - **System**: PostgreSQL
   - **Host name**: `pgdatabase`
   - **Port**: `5432`
   - **Database**: `data_engineering`
   - **Username**: `root`
   - **Password**: `root`

4️⃣ Click **Save**.

5️⃣ Navigate to **Data → Datasets**, select the `public` schema, and add the `fintech_clean` table.

6️⃣ You can now create visualizations in Superset.

🔹 **Note:** Superset may take a few minutes to initialize. If the UI does not load immediately, wait and refresh.

📊 **Dashboard Availability**: The Superset dashboard was developed locally and is not included in this setup by default. However, I have provided a PDF version of the [fintech_dashboard.pdf](milestone2/fintech_dashboard.pdf) for reference.
To recreate the dashboard, follow the "Creating a New Superset Dashboard from Scratch" section.

#### 📊 Creating a New Superset Dashboard from Scratch

If you need to create a new dashboard:

1️⃣ Ensure Superset is running at [http://localhost:8088](http://localhost:8088).

2️⃣ Navigate to **Charts → + New Chart**.

3️⃣ Select `fintech_clean` as the dataset.

4️⃣ Choose a visualization type (e.g., Bar Chart, Pie Chart, Table, etc.).

5️⃣ Configure your metrics and dimensions.

6️⃣ Click **Run Query** to preview the data.

7️⃣ Click **Save** and add it to a new or existing dashboard.

8️⃣ Navigate to **Dashboards → + New Dashboard**.

9️⃣ Add the saved charts to the dashboard and adjust layouts as needed.

🔟 Click **Save** and start analyzing your data!


---


🏁 **Milestone 2** successfully transitions the project from manual data preprocessing to a fully automated ETL pipeline using Apache Airflow, PostgreSQL, and Superset. This milestone ensures that data workflows are scalable, reproducible, and ready for advanced analytics and business intelligence applications.

---
