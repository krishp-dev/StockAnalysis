import numpy as np

class StockAnalyzer:
    """Handles analysis of multiple stocks"""
    def __init__(self):
        self.stocks = {}
        
    def add_stock(self, stock_data):
        """Add a stock to the analyzer"""
        if stock_data.load_data():
            self.stocks[stock_data.symbol] = stock_data

    def calculate_sma(self, prices, window):
        """Calculate Simple Moving Average"""
        if len(prices) < window:
            return np.array([])
        return np.convolve(prices, np.ones(window)/window, 'valid')
    
    def calculate_ema(self, prices, window):
        """Calculate Exponential Moving Average"""
        if len(prices) < window:
            return np.array([])
        ema = np.zeros_like(prices)
        ema[:window] = np.mean(prices[:window])
        alpha = 2 / (window + 1)
        for i in range(window, len(prices)):
            ema[i] = alpha * prices[i] + (1 - alpha) * ema[i-1]
        return ema
    
    def calculate_rsi(self, prices, window=14):
        """Calculate Relative Strength Index (RSI)"""
        if len(prices) < window:
            return np.array([])
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.zeros_like(prices)
        avg_loss = np.zeros_like(prices)
        
        avg_gain[window] = np.mean(gains[:window])
        avg_loss[window] = np.mean(losses[:window])
        
        for i in range(window+1, len(prices)):
            avg_gain[i] = (avg_gain[i-1] * (window-1) + gains[i-1]) / window
            avg_loss[i] = (avg_loss[i-1] * (window-1) + losses[i-1]) / window
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices, short_window=12, long_window=26, signal_window=9):
        """Calculate MACD and Signal Line"""
        ema_short = self.calculate_ema(prices, short_window)
        ema_long = self.calculate_ema(prices, long_window)
        macd = ema_short - ema_long
        signal = self.calculate_ema(macd, signal_window)
        return macd, signal
    
    def calculate_bollinger_bands(self, prices, window=20, num_std=2):
        """Calculate Bollinger Bands"""
        if len(prices) < window:
            return np.array([]), np.array([]), np.array([])
            
        sma = self.calculate_sma(prices, window)
        rolling_std = np.array([np.std(prices[i:i+window]) for i in range(len(prices)-window+1)])
        
        upper_band = sma + (rolling_std * num_std)
        lower_band = sma - (rolling_std * num_std)
        
        return sma, upper_band, lower_band
    
    def calculate_correlation_matrix(self, symbols):
        """Calculate correlation matrix between selected stocks"""
        if len(symbols) < 2:
            print("Need at least 2 stocks to calculate correlation")
            return None
        
        # Get closing prices for all symbols
        price_data = {}
        min_length = float('inf')
        
        # First pass: get lengths to determine the minimum common length
        for symbol in symbols:
            if symbol in self.stocks:
                prices = self.stocks[symbol].get_closing_prices()
                if len(prices) > 0:
                    price_data[symbol] = prices
                    min_length = min(min_length, len(prices))
                else:
                    print(f"No price data available for {symbol}")
                    return None
            else:
                print(f"Stock {symbol} not found")
                return None
        
        # Second pass: trim all arrays to minimum common length and calculate returns
        aligned_returns = {}
        for symbol, prices in price_data.items():
            # Trim to common length (most recent data)
            trimmed_prices = prices[-min_length:]
            # Calculate daily returns
            returns = np.diff(trimmed_prices) / trimmed_prices[:-1]
            aligned_returns[symbol] = returns
        
        # Build correlation matrix
        symbols_list = list(aligned_returns.keys())
        n = len(symbols_list)
        corr_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                sym1 = symbols_list[i]
                sym2 = symbols_list[j]
                # Calculate correlation coefficient
                corr = np.corrcoef(aligned_returns[sym1], aligned_returns[sym2])[0, 1]
                corr_matrix[i, j] = corr
        
        return symbols_list, corr_matrix