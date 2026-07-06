# ✈️ Flight Monitoring ETL Pipeline

## 📌 Project Overview
This project implements an automated **Data Engineering ETL pipeline** that retrieves real-time flight departure data from the AviationStack API, transforms the raw JSON response into a structured tabular format, and loads the data into a Dockerized PostgreSQL database.

The project focuses on departures from **Athens International Airport (ATH)** and demonstrates a complete workflow using **Python, Docker, PostgreSQL, SQL, environment variables, logging, and Cron-based automation**.

The pipeline is designed to monitor scheduled flight departures from Athens International Airport and store them in a relational database for further SQL analysis.

The project includes:

* API data extraction
* JSON transformation
* PostgreSQL loading
* Dockerized services
* Environment-based configuration
* Cron-based scheduling
* ETL logging
* SQL analysis queries

---

## 🎯 Project Objectives

The main objectives of this project are to:

* Build a reproducible ETL pipeline using Python
* Extract flight departure data from a public API
* Transform nested JSON data into a clean tabular structure
* Load transformed records into PostgreSQL
* Run the database and ETL pipeline inside Docker containers
* Automate the pipeline with Cron
* Store execution logs
* Provide SQL queries for flight monitoring analysis
* Follow good project practices using `.env`, `.gitignore`, and `.gitattributes`

---

## 📊 Data Source & API Limitations

The data is extracted from the **AviationStack API** using the `/flights` endpoint.

The main API filter used is:

```text
dep_iata=ATH
```

This means the pipeline collects flights departing from:

```text
Athens International Airport
```

### API Limitations

This project uses the AviationStack free plan, which has request limits and limited data availability.

In the collected sample, many operational fields such as:

* `actual_departure`
* `actual_arrival`
* `departure_delay`

may be unavailable or frequently null.

Because of this, the current project focuses mainly on:

* flight schedule monitoring
* airline activity
* destination activity
* ETL automation
* database loading
* SQL-based reporting

The database schema still includes actual-time and delay-related fields so that the pipeline can support future delay analysis if more complete data becomes available.

---

## 🏗️ ETL Pipeline Architecture

The ETL pipeline follows this flow:

```text
AviationStack API
        ↓
extract.py
        ↓
transform.py
        ↓
load.py
        ↓
PostgreSQL Database
        ↓
analysis.sql
```

The full architecture diagram is available here:

```text
documentation/architecture.png
```


---

## ⚙️ ETL Components

### 1. Extract Layer

File:

```text
src/extract.py
```

The extract layer sends a request to the AviationStack API and retrieves flight departure data for Athens International Airport.

The raw response contains nested JSON objects related to:

* flight details
* airline details
* departure airport details
* arrival airport details
* scheduled timestamps
* estimated timestamps
* actual timestamps
* flight status

---

### 2. Transformation Layer

File:

```text
src/transform.py
```

The transformation layer converts the nested JSON response into a clean Pandas DataFrame.

The transformed dataset includes fields such as:

* flight date
* flight status
* airline name
* airline IATA and ICAO codes
* flight number
* flight IATA and ICAO codes
* departure airport
* departure IATA and ICAO codes
* arrival airport
* arrival IATA and ICAO codes
* scheduled departure
* estimated departure
* actual departure
* scheduled arrival
* estimated arrival
* actual arrival
* ETL load timestamp

Timestamp fields are converted into timezone-aware datetime values.

---

### 3. Load Layer

File:

```text
src/load.py
```

The load layer inserts the transformed records into a PostgreSQL table named:

```text
flights
```

The database table is created automatically from:

```text
sql_scripts/init.sql
```

---

### 4. Pipeline Orchestration

File:

```text
src/etl_pipeline.py
```

This file orchestrates the full ETL process:

```text
Extract → Transform → Load
```

It is used both by Cron automation and for manual ETL execution.

---

## 🧱 Database & Environment Configuration

The PostgreSQL database runs inside Docker.

Database configuration:

```text
Database: flights_db
User: postgres
Internal Docker port: 5432
Local machine port: 5433
```

The ETL container connects to PostgreSQL using the Docker service name:

```text
postgres
```

From DBeaver or another local database client, connect using:

```text
Host: localhost
Port: 5433
Database: flights_db
User: postgres
```

Sensitive credentials are stored in a local `.env` file and are not committed to GitHub.

A template is provided in:

```text
.env.example
```

For this project setup, the real `.env` file should be created inside the `docker/` folder.

---

## 📁 Project Structure

```text
flight-monitoring-etl-pipeline/
├── data/
│   └── logs/
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── cron_job
│   └── entrypoint.sh
├── documentation/
│   └── architecture.png
├── sql_scripts/
│   ├── init.sql
│   └── analysis.sql
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── etl_pipeline.py
├── .env.example
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd flight-monitoring-etl-pipeline
```

---

### 2. Create the environment file

Create a `.env` file inside the `docker/` folder.

You can use `.env.example` as a guide.

Example:

```bash
cp .env.example docker/.env
```

Then edit:

```text
docker/.env
```

and add your real AviationStack API key and PostgreSQL password.

---

### 3. Start the Docker containers

From the `docker/` folder, run:

```bash
docker compose up --build
```

This starts:

* the PostgreSQL container
* the ETL container
* the Cron scheduler inside the ETL container

---

### 4. Stop the Docker containers

From the `docker/` folder, run:

```bash
docker compose down
```

This stops the containers but keeps the PostgreSQL Docker volume.

To reset the database completely, run:

```bash
docker compose down -v
```

Use `-v` only when you intentionally want to delete and recreate the database volume.

---

## ⏰ Cron Automation & Logging

The ETL pipeline is automated using Cron inside the ETL container.

Current schedule:

```cron
0 8 * * *
```

This means the pipeline runs once per day at:

```text
08:00 UTC
```

The Cron job runs:

```bash
python src/etl_pipeline.py
```

ETL execution logs are written to:

```text
data/logs/etl_cron.log
```

Log files are excluded from Git tracking.

---

## 🧪 Running the ETL Manually

The ETL pipeline can also be executed manually from inside the running ETL container:

```bash
docker exec -it flight_etl sh -c "cd /app && python src/etl_pipeline.py"
```

This is useful for testing or debugging.

Important note: each manual execution consumes one AviationStack API request.

---

## 📈 SQL Analysis

SQL analysis queries are stored in:

```text
sql_scripts/analysis.sql
```

The analysis queries cover topics such as:

* total records loaded
* records loaded per ETL execution
* flights by status
* flights by airline
* top 10 destinations from Athens
* scheduled departures by hour
* UTC vs Athens local scheduled departure hour

These queries help validate that the ETL pipeline is loading usable data into PostgreSQL.

---

## 🛠️ Tech Stack

| Category         | Tools                  |
| ---------------- | ---------------------- |
| Programming      | Python                 |
| Data Processing  | Pandas                 |
| API Requests     | Requests               |
| Database         | PostgreSQL             |
| Database Driver  | Psycopg2               |
| Containerization | Docker, Docker Compose |
| Automation       | Cron                   |
| Querying         | SQL                    |
| Version Control  | Git, GitHub            |

---

## ✅ Current Status

Completed features:

* AviationStack API extraction
* JSON transformation with Pandas
* PostgreSQL loading
* Dockerized PostgreSQL database
* Dockerized ETL container
* Cron-based scheduling
* ETL logging
* SQL analysis queries
* Environment variable template
* Line-ending rules for Docker/Linux files using `.gitattributes`

---

## 🔮 Future Improvements

Possible future improvements include:

* adding more departure airports
* adding incremental deduplication logic
* creating dimension and fact tables
* adding a data dictionary
* adding data quality documentation
* building a dashboard in Metabase or Power BI
* adding more advanced delay analysis
* improving error handling and monitoring
* adding automated tests

---


## 👤 Author

**Built by:** Sotiris Dimakis  
Project developed as part of Data Engineering Bootcamp at Big Blue Data Academy 