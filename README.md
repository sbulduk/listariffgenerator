# LIS Tariff Generator Application
## Endpoints
### 1. File Upload Endpoint
URL: /upload
Method: POST
Description: This endpoint allows the user to upload an Excel file to the backend. The file will be saved in the App/Files folder, and the filename (including extension) will be returned if the upload is successful.
### 2. Generate Target File Endpoint
URL: /generatetargetfile
Method: POST
Description: This endpoint takes the filename from the uploaded file and processes it to generate the target Excel file.
Frontend Overview
The frontend consists of a form where the user can:

Select an Excel file to upload.
Specify additional options like sheet names and output file names.
Submit the form to trigger the file conversion process.
The frontend communicates with the backend to:

Upload the file.
Trigger the generatetargetfile endpoint to handle the processing.

## Overview
This application is a simple Flask-based tool designed to handle Excel file conversions. It processes an uploaded Excel file and generates a target file based on predefined rules. The application consists of two main parts: 
1. Backend (built with Python/Flask)
2. Frontend (built with HTML, CSS, Vanilla JS)

## Basic Prerequisites
- Python 3.x (At least 3.11 is recommended.)
- Flask
- Pandas
- Openpyxl

Ensure you have the necessary packages installed by running:

```bash
pip install -r requirements.txt
