from stock_data import StockData
from stock_analyzer import StockAnalyzer
from stock_visualizer import StockVisualizer

def show_stock_options(stocks):
    """Display available stock options and get user's choice."""
    print("\nAvailable Stocks:")
    for i, symbol in enumerate(stocks.keys(), 1):
        print(f"{i}. {symbol}")
    
    while True:
        try:
            choice = int(input("Select a stock by number: "))
            if 1 <= choice <= len(stocks):
                return list(stocks.keys())[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(stocks)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_menu():
    """Display the menu and get user's choice."""
    print("\nStock Analysis System")
    print("1. Moving Averages (Historical Data)")
    print("2. RSI (Historical Data)")
    print("3. MACD (Historical Data)")
    print("4. Bollinger Bands (Historical Data)")
    print("5. Correlation Analysis")
    print("6. Generate Comprehensive Report (PDF)")
    print("7. Exit")
    
    while True:
        try:
            choice = int(input("Select an option (1-7): "))
            if 1 <= choice <= 7:
                return choice
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_multiple_stocks(stocks, min_count=2, max_count=5):
    """Allow user to select multiple stocks for correlation analysis"""
    if len(stocks) < min_count:
        print(f"Need at least {min_count} stocks loaded.")
        return []
    
    print("\nAvailable Stocks:")
    for i, symbol in enumerate(stocks.keys(), 1):
        print(f"{i}. {symbol}")
    
    selected = []
    
    # Improve message for exact number requirements
    if min_count == max_count:
        print(f"\nSelect exactly {min_count} stocks for this analysis (enter stock numbers).")
    else:
        print(f"\nSelect {min_count}-{max_count} stocks as your choice (enter stock numbers).")
    
    print(f"Enter 0 when done (minimum {min_count} stocks required).")
    
    while len(selected) < max_count:
        try:
            choice = int(input(f"Select stock #{len(selected)+1} (0 to finish): "))
            if choice == 0:
                if len(selected) >= min_count:
                    break
                else:
                    print(f"Please select at least {min_count} stocks.")
            elif 1 <= choice <= len(stocks):
                symbol = list(stocks.keys())[choice - 1]
                if symbol not in selected:
                    selected.append(symbol)
                    print(f"Added {symbol}, selected {len(selected)}/{max_count}")
                else:
                    print(f"{symbol} already selected.")
            else:
                print(f"Please enter a number between 0 and {len(stocks)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return selected

def load_multiple_stocks():
    """Load multiple stock CSV files"""
    stock_files = []
    while True:
        try:
            num_files = int(input("\nHow many stock files do you want to load (2-5)? "))
            if 2 <= num_files <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print(f"\nEnter the paths for {num_files} stock CSV files:")
    for i in range(num_files):
        while True:
            file_path = input(f"Enter path for stock {i+1}: ")
            if file_path.endswith('.csv'):
                stock_files.append(file_path)
                break
            else:
                print("Please enter a valid CSV file path.")
    return stock_files

def correlation_analysis_menu(analyzer, visualizer):
    """Handle the correlation analysis sub-menu"""
    print("\n=== Correlation Analysis ===")
    print("1. Correlation Matrix for Multiple Stocks")
    print("2. Correlation Scatter Plot for Two Stocks")
    print("3. Back to Main Menu")
    
    while True:
        try:
            choice = int(input("Select an option (1-3): "))
            if 1 <= choice <= 3:
                break
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    if choice == 3:
        return
    
    if choice == 1:
        # Correlation matrix
        selected_symbols = select_multiple_stocks(analyzer.stocks, min_count=2, max_count=5)
        if selected_symbols:
            print(f"\nCalculating correlation matrix for {', '.join(selected_symbols)}...")
            symbols, corr_matrix = analyzer.calculate_correlation_matrix(selected_symbols)
            if symbols and corr_matrix is not None:
                visualizer.plot_correlation_matrix(symbols, corr_matrix)
    
    elif choice == 2:
        # Correlation scatter plot
        print("\nFor scatter plot analysis, you must select exactly 2 stocks.")
        selected_symbols = select_multiple_stocks(analyzer.stocks, min_count=2, max_count=2)
        if len(selected_symbols) == 2:
            print(f"\nCreating scatter plot for {selected_symbols[0]} vs {selected_symbols[1]}...")
            visualizer.plot_correlation_scatter(analyzer.stocks.keys(), selected_symbols)


def main():
    # Create analyzer
    analyzer = StockAnalyzer()
    
    # Add some stocks (with error handling)
    sample_stocks = ['AAPL.csv', 'GOOGL.csv', 'MSFT.csv', 'META.csv', 'AMZN.csv']
    for stock_file in sample_stocks:
        stock = StockData(f"{stock_file}")
        analyzer.add_stock(stock)
    
    # Check if any stocks were loaded successfully
    if not analyzer.stocks:
        print("Failed to load any sample stocks. Please provide valid stock data files.")
        stock_files = load_multiple_stocks()
        for stock_file in stock_files:
            stock = StockData(stock_file)
            analyzer.add_stock(stock)
        
        if not analyzer.stocks:
            print("Still failed to load any stocks. Exiting program.")
            return
    
    # Create visualizer
    visualizer = StockVisualizer(analyzer)
    
    while True:
        choice = display_menu()
        
        if choice == 1:
            print("\nMoving Averages Analysis")
            selected_symbol = show_stock_options(analyzer.stocks)
            print(f"\nCalculating Moving Averages for {selected_symbol}...")
            
            stock = analyzer.stocks[selected_symbol]
            prices = stock.get_closing_prices()
            sma = analyzer.calculate_sma(prices, window=30)
            ema = analyzer.calculate_ema(prices, window=30)
            visualizer.plot_moving_averages(selected_symbol, prices, sma, ema)

        elif choice == 2:
            print("\nRSI Analysis")
            selected_symbol = show_stock_options(analyzer.stocks)
            print(f"\nCalculating RSI for {selected_symbol}...")
            
            stock = analyzer.stocks[selected_symbol]
            prices = stock.get_closing_prices()
            rsi = analyzer.calculate_rsi(prices)
            visualizer.plot_rsi(selected_symbol, rsi)

        elif choice == 3:
            print("\nMACD Analysis")
            selected_symbol = show_stock_options(analyzer.stocks)
            print(f"\nCalculating MACD for {selected_symbol}...")
            
            stock = analyzer.stocks[selected_symbol]
            prices = stock.get_closing_prices()
            macd, signal = analyzer.calculate_macd(prices)
            visualizer.plot_macd(selected_symbol, macd, signal)

        elif choice == 4:
            print("\nBollinger Bands Analysis")
            selected_symbol = show_stock_options(analyzer.stocks)
            print(f"\nCalculating Bollinger Bands for {selected_symbol}...")
            
            stock = analyzer.stocks[selected_symbol]
            prices = stock.get_closing_prices()
            sma, upper_band, lower_band = analyzer.calculate_bollinger_bands(prices)
            visualizer.plot_bollinger_bands(selected_symbol, prices, sma, upper_band, lower_band)
            
        elif choice == 5:
            print("\nCorrelation Analysis")
            # Check if we have enough stocks
            if len(analyzer.stocks) < 2:
                print("Need at least 2 stocks for correlation analysis. Loading new stocks...")
                new_stock_files = load_multiple_stocks()
                for stock_file in new_stock_files:
                    stock = StockData(stock_file)
                    analyzer.add_stock(stock)
                
                if len(analyzer.stocks) < 2:
                    print("Failed to load enough stocks for correlation analysis.")
                    continue
            
            # Show correlation analysis menu
            correlation_analysis_menu(analyzer, visualizer)

        elif choice == 6:
            print("\nGenerating Comprehensive Report")
            
            # Check if we have any stocks loaded
            if not analyzer.stocks:
                print("No stocks loaded. Loading stocks now...")
                new_stock_files = load_multiple_stocks()
                for stock_file in new_stock_files:
                    stock = StockData(stock_file)
                    analyzer.add_stock(stock)
                
                if not analyzer.stocks:
                    print("Failed to load any stocks. Please try again.")
                    continue
            
            # Let user select which stocks to include in the report
            # Fix: Use select_multiple_stocks instead of the undefined select_stocks_for_report
            selected_symbols = select_multiple_stocks(analyzer.stocks, min_count=1, max_count=5)
            
            if selected_symbols:
                # Ask for PDF output file
                output_pdf = input("\nEnter the output PDF file path (e.g., stock_report.pdf): ")
                if not output_pdf.endswith('.pdf'):
                    output_pdf += '.pdf'
                
                print(f"\nGenerating comprehensive PDF report for {', '.join(selected_symbols)}...")
                visualizer.generate_comprehensive_report(selected_symbols, output_pdf)
                print(f"\nPDF report has been successfully generated: {output_pdf}")
            else:
                print("No stocks were selected for the report.")

        elif choice == 7:
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()