# Devot-challange
My solution for the Devot Home Budget App challange.
# Run instructions
## 1. Create python environment
```bash
conda env create -f environment.yml
```
or
```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
#.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```
## 2. Create .env file
This file should have the following variables (values can be changed) and be in the root directory:
```ini
DATABASE_URL=sqlite:///data.db
JWT_SECRET=CHANGE_THIS_TO_A_STRONG_SECRET
JWT_ALGORITHM=HS256
ACCESS_EXPIRES_MINUTES=30
```
## 3. Using the API
### 3.1 Running the application
Use the following command:
```bash
python -m uvicorn app.main:app --reload
```
### 3.2 Docs
You can check API functionalities easily from the docs page:
```
http://127.0.0.1:8000/docs
```
### 3.3 Build database
Use the rebuild_database functionality to create a database with a few users, categories, and expenses. N.B.: Each user only sees their own categories and expenses.
### 3.4 Authorise
In order to use API functionalities you need to authorise. To do that click on "Authorise" button at the top of the docs page where you will need to enter user email in the "username" field and user password in the "password" field.
### 3.5 Use the API
