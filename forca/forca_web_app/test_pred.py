import pytest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import numpy as np
import pandas as pd

# Mocking the external dependencies
@pytest.fixture
def mock_external_dependencies():
    with patch('yfinance.download') as mock_yf_download, \
         patch('tensorflow.keras.models.load_model') as mock_load_model, \
         patch('sklearn.preprocessing.MinMaxScaler.fit_transform') as mock_fit_transform, \
         patch('sklearn.preprocessing.MinMaxScaler.inverse_transform') as mock_inverse_transform:
        
        # Mock the return value of yfinance's download function
        mock_yf_download.return_value = pd.DataFrame({
            'Open': [100, 102, 101, 103, 104],
            'High': [105, 107, 106, 108, 109],
            'Low': [95, 97, 96, 98, 99],
            'Close': [102, 104, 103, 105, 106],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })

        # Mock the model's predict method to return a numpy array
        mock_model = mock_load_model.return_value
        mock_model.predict.return_value = np.array([[105], [107]])

        # Mock the data preprocessing and inverse transformations
        mock_fit_transform.return_value = np.array([[0.5], [0.6], [0.7], [0.8], [0.9]])
        mock_inverse_transform.return_value = np.array([[105], [107]])

        yield  # This provides control to the test function


def test_show_stock_prediction(mock_external_dependencies):
    at = AppTest.from_file("pages/2_StockPrediction.py").run()
    
    # Assuming you have a way to authenticate or bypass authentication in testing
    # For example, setting a session state variable directly
    at.session_state['user_authenticated'] = True
    at.session_state['current_page'] = 'stock_prediction'
    
    
    
    
    # Fill in the required inputs for stock prediction
    at.text_input("ticker_symbol_input").input("AAPL").run()
    at.date_input("Start Date").input("2022-01-01")
    at.number_input("Number of days to predict:").input(2)
    
    # Trigger the prediction
    at.button("Predict").click()

    # Re-run the app to reflect the changes
    at.run()

    # Assertions to verify that predictions are displayed correctly
    # These assertions will depend on how your app displays the predictions
    assert "AAPL Candlestick Chart" in at.markdown
    assert "Predicted Future Price" in at.markdown
