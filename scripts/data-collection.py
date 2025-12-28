"""
Script thu thập dữ liệu tài chính từ các API công khai
Yêu cầu: pip install requests pandas yfinance
"""

import requests
import pandas as pd
import yfinance as yf
import json
from datetime import datetime, timedelta

class FinancialDataCollector:
    def __init__(self, alpha_vantage_key=None):
        self.alpha_vantage_key = alpha_vantage_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_stock_data_yahoo(self, symbol, period="1y"):
        """
        Lấy dữ liệu cổ phiếu từ Yahoo Finance
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            return data
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu {symbol}: {e}")
            return None
    
    def get_company_info_yahoo(self, symbol):
        """Lấy thông tin công ty từ Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return info
        except Exception as e:
            print(f"Lỗi khi lấy thông tin {symbol}: {e}")
            return None
    
    def get_financial_statements_alpha(self, symbol, statement_type="INCOME_STATEMENT"):
        """
        Lấy báo cáo tài chính từ Alpha Vantage
        statement_type: INCOME_STATEMENT, BALANCE_SHEET, CASH_FLOW
        """
        if not self.alpha_vantage_key:
            print("Cần API key Alpha Vantage")
            return None
        
        params = {
            'function': statement_type,
            'symbol': symbol,
            'apikey': self.alpha_vantage_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            return data
        except Exception as e:
            print(f"Lỗi khi lấy báo cáo tài chính {symbol}: {e}")
            return None
    
    def save_to_excel(self, data, filename, sheet_name="Sheet1"):
        """Lưu dữ liệu vào file Excel"""
        try:
            if isinstance(data, pd.DataFrame):
                # Xử lý timezone cho datetime columns
                df_copy = data.copy()
                for col in df_copy.columns:
                    if df_copy[col].dtype == 'datetime64[ns, UTC]' or str(df_copy[col].dtype).startswith('datetime64[ns,'):
                        df_copy[col] = df_copy[col].dt.tz_localize(None)
                df_copy.to_excel(f"data/{filename}", sheet_name=sheet_name)
            else:
                df = pd.DataFrame(data)
                df.to_excel(f"data/{filename}", sheet_name=sheet_name)
            print(f"Đã lưu dữ liệu vào data/{filename}")
        except Exception as e:
            print(f"Lỗi khi lưu file: {e}")

# Ví dụ sử dụng
if __name__ == "__main__":
    # Khởi tạo collector
    collector = FinancialDataCollector()
    
    # Danh sách cổ phiếu để phân tích
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    
    # Thu thập dữ liệu cho từng cổ phiếu
    for symbol in symbols:
        print(f"Đang thu thập dữ liệu cho {symbol}...")
        
        # Lấy dữ liệu giá cổ phiếu
        stock_data = collector.get_stock_data_yahoo(symbol, "1y")
        if stock_data is not None:
            collector.save_to_excel(stock_data, f"{symbol}_price_data.xlsx")
        
        # Lấy thông tin công ty
        company_info = collector.get_company_info_yahoo(symbol)
        if company_info:
            df_info = pd.DataFrame([company_info])
            collector.save_to_excel(df_info, f"{symbol}_company_info.xlsx")
    
    print("Hoàn thành thu thập dữ liệu!")