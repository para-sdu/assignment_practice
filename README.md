# Azhar Charity Platform

## Project Overview
Azhar Charity Platform is a role-based charity management system built with FastAPI and SQLite.  
The system allows users to register, create help requests, verify requests, and analyze regional activity using H3 geospatial indexing.


# How to Run the System

## 1.Install Dependencies

Make sure Python 3.10+ is installed.

Install required packages:

pip install fastapi uvicorn sqlalchemy h3

## 2.Run the Application

uvicorn main:app --reload

## 3.Open API Documentation

Open in browser:

http://127.0.0.1:8000/docs

Swagger UI will allow testing all endpoints.


# Project Structure

main.py  
azhar.db   
README.md  


# Group Member Roles

| Name | Responsibility |
|------|---------------|
| Kystaubay Ayanat| Tester |
| Sultangazyyeva Altynay | Frontend dev |
| Kraman Zhaniya| Backend dev |


# Security Model

The system uses Role-Based Access Control.

Roles:
- admin
- needy
- donor 

Role validation is enforced via HTTP Header:

X-User-Role: admin  
X-User-Role: needy  

Unauthorized access returns HTTP 403.

# How H3 Is Used in the System

The system uses Uber’s H3 geospatial indexing library.

When a user registers:
- Latitude and Longitude are provided.
- They are converted into an H3 index at resolution 7.
- The H3 index is stored in the database.

Example:
h3.geo_to_h3(lat, lon, 7)

This enables:

  Regional clustering  
  Location-based analytics  
  Counting users inside same hexagonal grid  

Endpoint:

GET /analytics/region/{h3_index}

Returns number of users inside that H3 cell.

This allows scalable geographic analytics without storing raw coordinates.
