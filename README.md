# Data-Driven Recruitment Process Optimization

## Overview
Big data is transforming industries globally, and the recruitment process is no exception. This project utilizes data from various sources to analyze job metrics, applicant details, and organizational information. The goal is to adapt to a data-driven recruitment process, providing benefits for both companies and candidates.

## Project Goals and Objectives
- Understand candidate personality traits before interviews.
- Assist recruiters in tracking potential candidates and improving the hiring process.
- Provide candidates with insights into skills needed for specific roles.
- Help organizations identify skill gaps and transform the recruitment process efficiently.
- Deliver an application to actively recruit candidates, ranking them based on various criteria.

## Data Description
![image](https://github.com/Lohitha-Vanteru/Data-Driven-Analysis-on-Job-Portals/assets/113141006/70871cf8-3c1b-4dfe-b59b-076889709575)

- Collected from LinkedIn, Glassdoor, Dice, Stack Overflow, Indeed, and Zip Recruiter.
- Total dataset size: 13GB with 2.5M records.
- Attributes include job title, company, salary, job description, reviews, survey results, and location.

## Architecture and High-Level Design
![image](https://github.com/Lohitha-Vanteru/Data-Driven-Analysis-on-Job-Portals/assets/113141006/94c60f2b-b9cd-455e-963d-9514d2b6842f)
![image](https://github.com/Lohitha-Vanteru/Data-Driven-Analysis-on-Job-Portals/assets/113141006/ee9078ca-747c-4890-87c7-18e370f1592d)

### ETL Pipeline
![image](https://github.com/Lohitha-Vanteru/Data-Driven-Analysis-on-Job-Portals/assets/113141006/8d91cc42-eca4-4966-8ce5-304dea15dd87)

- Data collected from various sources in CSV and JSON formats.
- Raw data stored in an AWS S3 bucket.
- ETL performed using AWS Glue for JSON and PySpark scripts for CSV data.
- Transformed data stored in S3.
- Data transferred to AWS Redshift using Apache Airflow.
- Connection established from Redshift to Tableau for visualizations.

### Web Integration
Login Page : 
![image](https://github.com/Lohitha-Vanteru/Data-Driven-Analysis-on-Job-Portals/assets/113141006/a76fa65c-b36e-40e8-a1b0-a8c8907f4051)
Home Page:
![image](https://github.com/Lohitha-Vanteru/Data-Driven-Analysis-on-Job-Portals/assets/113141006/e0efc832-c6bd-47b1-878f-d6faab33530b)

- Tableau desktop used for creating dashboards.
- Dashboards hosted on Tableau Cloud Server.
- Flask application created with Tableau Public URL embedded.
- Google OAuth implemented for single sign-on.
- Deployed on Heroku cloud platform.

## Data Cleaning and Transformation
- PySpark scripts used to clean and transform data.
- Handled null values, outliers, and removed unnecessary columns.
- Converted job titles to lowercase.
- Extracted city, state, and country from the location column.
- Added columns for max rating and source portal details.

## Website
- Flask application with embedded Tableau Public URL.
- Google OAuth for single sign-on.
- Deployed on Heroku at [https://theinsightco.herokuapp.com/](https://theinsightco.herokuapp.com/).

## References
- [GitHub - Medium API Docs](https://github.com/Medium/medium-api-docs)
- [Choosing the Right Cloud Service Provider](https://medium.com/futuremind/how-to-choose-the-right-cloud-service-provider-79c82b01642e)
- [Building a Data Pipeline with PySpark and AWS](https://www.analyticsvidhya.com/blog/2021/08/building-a-data-pipeline-with-pyspark-and-aws/)
- [AWS IAM Documentation](https://docs.aws.amazon.com/iam/index.html)
- [Simplify Querying Nested JSON with AWS Glue](https://aws.amazon.com/blogs/big-data/simplify-querying-nested-json-with-the-aws-glue-relationalize-transform/)
