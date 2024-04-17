Installation Instructions
=========================

Follow these steps to set up and run the application on your local machine.

Prerequisites
-------------
- **Python**: This project requires Python 3.6 or higher. Download Python from https://www.python.org/downloads/.
- **pip**: Ensure that pip is installed along with Python.

Step 1: Set Up a Virtual Environment
------------------------------------
It's recommended to use a virtual environment. To set up and activate a virtual environment:

For macOS and Linux:
python3 -m venv venv
source venv/bin/activate

For Windows:
python -m venv venv
.\venv\Scripts\activate

Step 2: Install Required Packages
---------------------------------
Install all dependencies listed in the requirements.txt file.

pip install -r requirements.txt
OR
pip install <each of the libraries listed below>

streamlit
pandas
yfinance
psycopg2-binary
plotly
python-dotenv
tensorflow
scikit-learn
matplotlib

Step 3: Run the Application
---------------------------
Finally, run the application using Streamlit. The applications entry point is Landing.py

streamlit run Landing.py

---------------
If the Stock prediction does not work ensure that the path to the loaded model is specified correctly.

For running the models, Please execute all of the commands in models.ipynb from top to bottom sequentially.
