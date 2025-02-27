import matplotlib.pyplot as plt
import numpy as np
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class StockVisualizer:
    """Handles visualization of stock analysis"""
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def plot_moving_averages(self, symbol, prices, sma, ema, save_to_buffer=False):
        """Plot Moving Averages"""
        plt.figure(figsize=(10, 6))
        plt.plot(prices, label='Close Prices', color='blue')
        plt.plot(range(len(prices)-len(sma), len(prices)), sma, label='SMA', color='orange')
        plt.plot(ema, label='EMA', color='green')
        plt.title(f'{symbol} - Moving Averages')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_to_buffer:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()
            return buffer
        else:
            plt.show()

    def plot_rsi(self, symbol, rsi, save_to_buffer=False):
        """Plot RSI"""
        plt.figure(figsize=(10, 4))
        plt.plot(rsi, label='RSI', color='purple')
        plt.axhline(70, color='red', linestyle='--', label='Overbought')
        plt.axhline(30, color='green', linestyle='--', label='Oversold')
        plt.title(f'{symbol} - RSI')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_to_buffer:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()
            return buffer
        else:
            plt.show()

    def plot_macd(self, symbol, macd, signal, save_to_buffer=False):
        """Plot MACD and Signal Line"""
        plt.figure(figsize=(10, 6))
        plt.plot(macd, label='MACD', color='blue')
        plt.plot(signal, label='Signal Line', color='red')
        plt.title(f'{symbol} - MACD')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_to_buffer:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()
            return buffer
        else:
            plt.show()
        
    def plot_bollinger_bands(self, symbol, prices, sma, upper_band, lower_band, save_to_buffer=False):
        """Plot Bollinger Bands"""
        plt.figure(figsize=(10, 6))
        plt.plot(prices, label='Close Prices', color='blue')
        plt.plot(range(len(prices)-len(sma), len(prices)), sma, label='SMA', color='red')
        plt.plot(range(len(prices)-len(upper_band), len(prices)), upper_band, label='Upper Band', color='gray')
        plt.plot(range(len(prices)-len(lower_band), len(prices)), lower_band, label='Lower Band', color='gray')
        plt.title(f'{symbol} - Bollinger Bands')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_to_buffer:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()
            return buffer
        else:
            plt.show()
    
    def plot_correlation_matrix(self, symbols, corr_matrix, save_to_buffer=False):
        """Plot correlation matrix as a heatmap"""
        plt.figure(figsize=(10, 8))
        # Create the heatmap
        plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
        
        # Add colorbar
        plt.colorbar(label='Correlation Coefficient')
        
        # Add labels and ticks
        plt.title('Stock Return Correlation Matrix')
        plt.xticks(np.arange(len(symbols)), symbols, rotation=45)
        plt.yticks(np.arange(len(symbols)), symbols)
        
        # Add text annotations
        for i in range(len(symbols)):
            for j in range(len(symbols)):
                plt.text(j, i, f'{corr_matrix[i, j]:.2f}', 
                         ha='center', va='center', 
                         color='white' if abs(corr_matrix[i, j]) > 0.5 else 'black')
        
        plt.tight_layout()
        
        if save_to_buffer:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()
            return buffer
        else:
            plt.show()
        
    def plot_correlation_scatter(self, symbols, selected_symbols, save_to_buffer=False):
        """Plot scatter plots of returns for selected pairs of stocks"""
        if len(selected_symbols) != 2:
            print("Need exactly 2 symbols for scatter plot")
            return None
            
        sym1, sym2 = selected_symbols
        if sym1 not in self.analyzer.stocks or sym2 not in self.analyzer.stocks:
            print("One or both symbols not found")
            return None
            
        # Get price data
        prices1 = self.analyzer.stocks[sym1].get_closing_prices()
        prices2 = self.analyzer.stocks[sym2].get_closing_prices()
        
        # Ensure same length (use the shorter one)
        min_length = min(len(prices1), len(prices2))
        prices1 = prices1[-min_length:]
        prices2 = prices2[-min_length:]
        
        # Calculate returns
        returns1 = np.diff(prices1) / prices1[:-1]
        returns2 = np.diff(prices2) / prices2[:-1]
        
        # Calculate correlation
        corr = np.corrcoef(returns1, returns2)[0, 1]
        
        # Create scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(returns1, returns2, alpha=0.5)
        plt.title(f'Return Correlation: {sym1} vs {sym2} (r = {corr:.2f})')
        plt.xlabel(f'{sym1} Daily Returns')
        plt.ylabel(f'{sym2} Daily Returns')
        plt.grid(True, alpha=0.3)
        
        # Add regression line
        if len(returns1) > 1:
            m, b = np.polyfit(returns1, returns2, 1)
            plt.plot(returns1, m*returns1 + b, 'r-', alpha=0.7)
            
        plt.tight_layout()
        
        if save_to_buffer:
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()
            return buffer
        else:
            plt.show()
            return None

    def generate_comprehensive_report(self, symbols, output_pdf=None):
        """Generate a comprehensive report for multiple stocks"""
        report_data = {}
        
        print("\n=== Generating Comprehensive Stock Analysis Report ===")
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

        for symbol in symbols:
            if symbol not in self.analyzer.stocks:
                print(f"Stock {symbol} not found. Skipping...")
                continue
                
            stock = self.analyzer.stocks[symbol]
            prices = stock.get_closing_prices()
            
            # Calculate all indicators
            rsi = self.analyzer.calculate_rsi(prices)
            macd, signal = self.analyzer.calculate_macd(prices)
            sma, upper_band, lower_band = self.analyzer.calculate_bollinger_bands(prices)
            
            # Get latest values
            current_rsi = rsi[-1] if len(rsi) > 0 else None
            current_macd = macd[-1] if len(macd) > 0 else None
            current_signal = signal[-1] if len(signal) > 0 else None
            current_price = prices[-1] if len(prices) > 0 else None
            
            # Save data for PDF report
            stock_data = {
                "symbol": symbol,
                "price": current_price,
                "rsi": {
                    "value": current_rsi,
                    "status": "Overbought" if current_rsi and current_rsi > 70 else
                              "Oversold" if current_rsi and current_rsi < 30 else "Neutral"
                },
                "macd": {
                    "value": current_macd,
                    "signal": current_signal,
                    "trend": "Bullish" if current_macd and current_signal and current_macd > current_signal else "Bearish"
                },
                "bollinger": {
                    "upper": upper_band[-1] if len(upper_band) > 0 else None,
                    "lower": lower_band[-1] if len(lower_band) > 0 else None,
                    "status": "Price above upper band (Potential overbought)" if current_price and len(upper_band) > 0 and current_price > upper_band[-1] else
                              "Price below lower band (Potential oversold)" if current_price and len(lower_band) > 0 and current_price < lower_band[-1] else
                              "Price within bands"
                }
            }
            
            # Generate trading recommendation based on indicators
            bullish_signals = 0
            bearish_signals = 0
            
            if current_rsi is not None:
                if current_rsi < 30:
                    bullish_signals += 1
                elif current_rsi > 70:
                    bearish_signals += 1
            
            if current_macd is not None and current_signal is not None:
                if current_macd > current_signal:
                    bullish_signals += 1
                else:
                    bearish_signals += 1
            
            if len(upper_band) > 0 and len(lower_band) > 0:
                if current_price < lower_band[-1]:
                    bullish_signals += 1
                elif current_price > upper_band[-1]:
                    bearish_signals += 1
            
            if bullish_signals > bearish_signals:
                recommendation = "Bullish - Consider buying/holding"
            elif bearish_signals > bullish_signals:
                recommendation = "Bearish - Consider selling/waiting"
            else:
                recommendation = "Neutral - Monitor for clearer signals"
            
            stock_data["recommendation"] = recommendation
            
            # Generate charts
            if output_pdf:
                ema = self.analyzer.calculate_ema(prices, window=30)
                stock_data["charts"] = {
                    "ma": self.plot_moving_averages(symbol, prices, sma, ema[-len(prices):] if len(ema) > 0 else np.array([]), save_to_buffer=True),
                    "rsi": self.plot_rsi(symbol, rsi, save_to_buffer=True),
                    "macd": self.plot_macd(symbol, macd, signal, save_to_buffer=True),
                    "bollinger": self.plot_bollinger_bands(symbol, prices, sma, upper_band, lower_band, save_to_buffer=True)
                }
            
            report_data[symbol] = stock_data
            
            # Print a summary to the console
            print(f"\nStock: {symbol}")
            print("-" * 30)
            print(f"Current Price: ₹{current_price:.2f}" if current_price else "Current Price: N/A")            
            # RSI Analysis
            print("\nRSI Analysis:")
            if current_rsi is not None:
                print(f"Current RSI: {current_rsi:.2f}")
                print(f"Status: {stock_data['rsi']['status']}")
            else:
                print("RSI data not available")
            
            # MACD Analysis
            print("\nMACD Analysis:")
            if current_macd is not None and current_signal is not None:
                print(f"MACD: {current_macd:.4f}")
                print(f"Signal Line: {current_signal:.4f}")
                print(f"Signal: {stock_data['macd']['trend']}")
            else:
                print("MACD data not available")
            
            # Bollinger Bands Analysis
            print("\nBollinger Bands Analysis:")
            if len(upper_band) > 0 and len(lower_band) > 0:
                print(f"Upper Band: ₹{upper_band[-1]:.2f}")
                print(f"Lower Band: ₹{lower_band[-1]:.2f}")
                print(f"Status: {stock_data['bollinger']['status']}")
            else:
                print("Bollinger Bands data not available")
            
            print("\nRecommendation:")
            print(f"Overall: {recommendation}")
            print("=" * 50)
        
        # If PDF output is requested, generate the PDF
        if output_pdf:
            self.create_pdf_report(report_data, output_pdf)
            print(f"\nPDF report has been generated: {output_pdf}")
        
        return report_data

    def create_pdf_report(self, report_data, output_path):
        """Create a PDF report from the analysis data"""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title
        title_style = styles["Title"]
        elements.append(Paragraph("Stock Market Analysis Report", title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
        elements.append(Spacer(1, 12))
        
        # Create a section for each stock
        for symbol, data in report_data.items():
            # Add stock title
            elements.append(Paragraph(f"{symbol} Analysis", styles["Heading1"]))
            elements.append(Spacer(1, 12))
            
            # Add price information
            price_text = f"Current Price: ₹{data['price']:.2f}" if data['price'] is not None else "Current Price: N/A"
            elements.append(Paragraph(price_text, styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            # Add indicator analysis sections
            elements.append(Paragraph("Technical Indicators", styles["Heading2"]))
            
            # Create table for indicator data
            indicators_data = [
                ["Indicator", "Value", "Status/Signal"],
                ["RSI", f"{data['rsi']['value']:.2f}" if data['rsi']['value'] is not None else "N/A", data['rsi']['status']],
                ["MACD", f"{data['macd']['value']:.4f}" if data['macd']['value'] is not None else "N/A", 
                  f"Signal: {data['macd']['signal']:.4f}" if data['macd']['signal'] is not None else "N/A"],
                ["MACD Trend", "", data['macd']['trend']],
                ["Bollinger Bands", f"Upper: ₹{data['bollinger']['upper']:.2f}\nLower: ₹{data['bollinger']['lower']:.2f}" 
                  if data['bollinger']['upper'] is not None and data['bollinger']['lower'] is not None 
                  else "N/A", data['bollinger']['status']]
            ]
            
            t = Table(indicators_data, colWidths=[100, 150, 250])
            t.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 12))
            
            # Add recommendation
            elements.append(Paragraph("Recommendation:", styles["Heading3"]))
            elements.append(Paragraph(data["recommendation"], styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            # Add charts if available
            if "charts" in data:
                elements.append(Paragraph("Technical Charts", styles["Heading2"]))
                elements.append(Spacer(1, 8))
                
                # Add Moving Averages chart
                if data["charts"]["ma"]:
                    elements.append(Paragraph("Moving Averages", styles["Heading3"]))
                    elements.append(Image(data["charts"]["ma"], width=500, height=300))
                    elements.append(Spacer(1, 8))
                
                # Add RSI chart
                if data["charts"]["rsi"]:
                    elements.append(Paragraph("Relative Strength Index (RSI)", styles["Heading3"]))
                    elements.append(Image(data["charts"]["rsi"], width=500, height=200))
                    elements.append(Spacer(1, 8))
                
                # Add MACD chart
                if data["charts"]["macd"]:
                    elements.append(Paragraph("MACD", styles["Heading3"]))
                    elements.append(Image(data["charts"]["macd"], width=500, height=300))
                    elements.append(Spacer(1, 8))
                
                # Add Bollinger Bands chart
                if data["charts"]["bollinger"]:
                    elements.append(Paragraph("Bollinger Bands", styles["Heading3"]))
                    elements.append(Image(data["charts"]["bollinger"], width=500, height=300))
                    elements.append(Spacer(1, 8))
            
            # Add page break between stocks
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("_" * 65, styles["Normal"]))
            elements.append(Spacer(1, 20))
        
        # Add disclaimer
        elements.append(Paragraph("DISCLAIMER:", styles["Heading3"]))
        elements.append(Paragraph("This report is for informational purposes only and does not constitute financial advice. "
                                 "Past performance is not indicative of future results. Always conduct your own research or "
                                 "consult with a financial advisor before making investment decisions.", styles["Normal"]))
        
        # Build PDF
        doc.build(elements)