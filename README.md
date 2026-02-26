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

uvicorn assignment1:app --reload

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

# H3 Geospatial Integration (Detailed Explanation)

The system integrates Uber's H3 geospatial indexing library.

H3 is a hexagonal hierarchical geospatial indexing system.  
Instead of storing raw latitude and longitude coordinates for analytics, the system converts geographic coordinates into a unique H3 hexagonal cell index.

## How H3 Works in This System

When a user registers:

1. The user provides:
   - Latitude
   - Longitude

2. The system converts coordinates into an H3 index using:

   h3.geo_to_h3(lat, lon, 7)

3. Resolution level 7 is used:
   - Medium geographic precision
   - Good balance between detail and performance

4. The generated H3 index is stored in the database inside the `users` table.

## Why H3 Is Used

H3 allows:

  Efficient geographic clustering  
  Fast region-based queries  
  Scalable analytics  
  Grouping users by hexagonal grid instead of raw coordinates  
  Avoiding complex radius-based SQL queries  

## Regional Analytics

Endpoint:

GET /analytics/region/{h3_index}

This endpoint:
- Takes an H3 index as input
- Counts all users stored in that hexagonal cell
- Returns total users in that geographic region

This enables:

- Regional statistics
- Heatmap generation (future extension)
- Identifying high-demand charity areas
- Location-based decision making
  
## Why H3 Is Better Than Raw Coordinates

Without H3:
- Complex distance calculations
- Slower queries
- Harder clustering

With H3:
- Simple string comparison
- Fast SQL filtering
- Hierarchical indexing support
- Easy aggregation

This makes the system scalable and geo-analytics ready.

# System Endpoints

### 1.Register User
POST /users/register

Stores user with H3 index.

### 2.Create Help Request
POST /requests/create

Recipient only.

### 3.Verify Help Request
PATCH /requests/verify/{req_id}

Admin only.

### 4.Regional Analytics
GET /analytics/region/{h3_index}

Returns number of users in region.

### 5.View System Logs
GET /system/logs

Admin only.
