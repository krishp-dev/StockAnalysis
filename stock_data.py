import numpy as np
from datetime import datetime
class StockData:
    """Handles loading and basic processing of stock data"""
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.dates = None
        self.symbol = file_path.split('/')[-1].split('.')[0]
        
    def load_data(self):
        try:    
            # Load data with explicit dtype specification
            raw_data = np.genfromtxt(self.file_path, 
                                   delimiter=',', 
                                   dtype=None,
                                   names=True,
                                   encoding=None)
            
            # Ensure data is not empty
            if len(raw_data) == 0:
                raise ValueError(f"No data found in {self.file_path}")
                
            # Convert to structured arrays for better handling
            self.dates = np.array([datetime.strptime(str(date), '%Y-%m-%d') 
                                 for date in raw_data['Date']])
            
            # Create price matrix [Open, High, Low, Close, Volume]
            self.data = np.column_stack((
                raw_data['Open'],
                raw_data['High'],
                raw_data['Low'],
                raw_data['Close'],
                raw_data['Volume']
            ))
            
            return True
            
        except Exception as e:
            print(f"Error loading {self.symbol}: {str(e)}")
            return False
    
    def get_closing_prices(self):
        """Return the closing prices"""
        if self.data is not None:
            return self.data[:, 3]  # Close prices
        return np.array([])