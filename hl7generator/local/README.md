# Local HL7 Generator

## Overview
This script, `generate.py`, is designed for local development. It generates ELR (Electronic Laboratory Report) files based on specified parameters.

## Prerequisites
- Python 3.x installed on your machine: https://www.python.org/downloads/
- Homebrew : https://brew.sh/

- **For Microsoft SQL Server database connections:**
  - Python library: `pyodbc`
  ```bash
    brew install pyodbc
  ```
  - System dependency: Microsoft ODBC Driver for SQL Server.

### Install System Dependencies
#### macOS
Install `unixODBC` and the Microsoft ODBC Driver for SQL Server:
```bash
brew install unixodbc
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install --no-sandbox msodbcsql17
```

## Setup Instructions
### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone <repository-url>
cd hl7generator/local
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```
#### Activate the virtual environment
#### On macOS/Linux:
```bash
source venv/bin/activate
```
#### On Windows:
```bash
venv\Scripts\activate
```
#### Install libraries
Install the required Python packages using [`requirements.txt`](requirements.txt):
```bash
pip install -r requirements.txt
```

### 3. Update Connection Details
Edit the [`generate.py`](generate.py) file to update the connection details:
    Replace user and password in the file (line 29, 30) with your specific credentials.
    By default, the host is set to DTS1. Update this value if necessary.

### 4. Run the script
Run the script to generate ELRs. Run the following command with the following parameters:
    10: Number of ELRs to generate.
    10101: Condition code.
    34703-9: Disease code (e.g., Hepatitis)
The following command, when run, will create 10 ELRs with the above condition code and LOINC code for Hepatitis.
```bash
python3 gennerate.py 10 10101 34703-9
```
