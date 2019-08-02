# Data Processing with Airflow
### Data Engineering Capstone Project 

#### Project Summary

The project follows the follow steps:
* Step 1: Scope the Project and Gather Data
* Step 2: Explore and Assess the Data
* Step 3: Define the Data Model
* Step 4: Run ETL to Model the Data
* Step 5: Complete Project Write Up

### Step 1: Scope the Project and Gather Data

#### Scope 
Explain what you plan to do in the project in more detail. What data do you use? What is your end solution look like? What tools did you use? etc>

The aim of the project is to process data from a S3 bucket in csv format into tables in Redshift. This tables could be useful for the operation team of the company that demands this system. Examples of case uses are defined in the appropriate section.

Technologies that are involved in this project are:
* Amazon S3: storage system from AWS.
* Airflow: orchestrator of ETL processes.
* Redshift: distributed SQL database from AWS.


#### Describe and Gather Data 
Describe the data sets you're using. Where did it come from? What type of information is included?

* Rides data: collected from rides in Capital Bikeshare System (Washington DC). Available in their [S3 bucket](https://s3.amazonaws.com/capitalbikeshare-data/index.html).
* Weather data: collected from meteo station at Reagan Airport (Washington DC). Provided by [NOAA](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets).

### Step 2: Explore and Assess the Data
#### Explore the Data 

Data is provided in plain csv files. In order to ease ingestion and extract valuable data afterwards, two staging tables are crated only with type definition for each column.


#### Cleaning Steps
Document steps necessary to clean the data
* Rides table: since all fields come with double quote sign ("), it must be removed before processing. Afterwards, every fields is casted to the proper type: integers or timestamps.
* Weather table: every field is casted to the proper type: floats or timestamps.

### Step 3: Define the Data Model
#### 3.1 Conceptual Data Model
Map out the conceptual data model and explain why you chose that model

#### 3.2 Mapping Out Data Pipelines
List the steps necessary to pipeline the data into the chosen data model

### Step 4: Run Pipelines to Model the Data 
#### 4.1 Create the data model
Build the data pipelines to create the data model.

#### 4.2 Data Quality Checks
Explain the data quality checks you'll perform to ensure the pipeline ran as expected. These could include:
 * Integrity constraints on the relational database (e.g., unique key, data type, etc.)
 * Unit tests for the scripts to ensure they are doing the right thing
 * Source/Count checks to ensure completeness
 
Run Quality Checks

#### 4.3 Data dictionary 
Create a data dictionary for your data model. For each field, provide a brief description of what the data is and where it came from. You can include the data dictionary in the notebook or in a separate file.

### Step 5: Complete Project Write Up
* Clearly state the rationale for the choice of tools and technologies for the project.
* Propose how often the data should be updated and why.
* Write a description of how you would approach the problem differently under the following scenarios:
 * The data was increased by 100x.
 * The data populates a dashboard that must be updated on a daily basis by 7am every day.
 * The database needed to be accessed by 100+ people.



 ![DAG](../images/DAG.PNG)


 ![gant](../images/gant.PNG)


 ![tree](../images/tree.PNG)