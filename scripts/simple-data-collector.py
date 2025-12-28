"""
Script đơn giản thu thập dữ liệu tài chính
"""

import yfinance as yf
import pandas as pd
import os

# Tạo thư mục data nếu chưa có
if not os.path.exists('data'):
    os.makedirs('data')

# Danh sách cổ phiếu để phân tích
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

print("Bắt đầu thu thập dữ liệu tài chính...")

for symbol in symbols:
    print(f"\nĐang xử lý {symbol}...")
    
    try:
        # Lấy dữ liệu cổ phiếu
        stock = yf.Ticker(symbol)
        
        # Lấy dữ liệu giá 1 năm
        hist = stock.history(period="1y")
        
        # Xử lý timezone
        if hasattr(hist.index, 'tz_localize'):
            hist.index = hist.index.tz_localize(None)
        
        # Lưu dữ liệu giá
        hist.to_excel(f"data/{symbol}_price_data.xlsx")
        print(f"✓ Đã lưu dữ liệu giá {symbol}")
        
        # Lấy thông tin công ty
        info = stock.info
        
        # Chọn các thông tin quan trọng
        key_info = {
            'Symbol': symbol,
            'Company_Name': info.get('longName', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Industry': info.get('industry', 'N/A'),
            'Market_Cap': info.get('marketCap', 0),
            'Current_Price': info.get('currentPrice', 0),
            'PE_Ratio': info.get('trailingPE', 0),
            'Forward_PE': info.get('forwardPE', 0),
            'PB_Ratio': info.get('priceToBook', 0),
            'Dividend_Yield': info.get('dividendYield', 0),
            'ROE': info.get('returnOnEquity', 0),
            'ROA': info.get('returnOnAssets', 0),
            'Profit_Margin': info.get('profitMargins', 0),
            'Debt_to_Equity': info.get('debtToEquity', 0),
            'Revenue': info.get('totalRevenue', 0),
            'Net_Income': info.get('netIncomeToCommon', 0),
            'Beta': info.get('beta', 0),
            '52_Week_High': info.get('fiftyTwoWeekHigh', 0),
            '52_Week_Low': info.get('fiftyTwoWeekLow', 0)
        }
        
        # Tạo DataFrame và lưu
        df_info = pd.DataFrame([key_info])
        df_info.to_excel(f"data/{symbol}_company_info.xlsx", index=False)
        print(f"✓ Đã lưu thông tin công ty {symbol}")
        
    except Exception as e:
        print(f"✗ Lỗi khi xử lý {symbol}: {e}")

# Tạo file tổng hợp
print("\nTạo file tổng hợp...")

try:
    # Đọc tất cả thông tin công ty
    all_companies = []
    for symbol in symbols:
        try:
            df = pd.read_excel(f"data/{symbol}_company_info.xlsx")
            all_companies.append(df)
        except:
            pass
    
    if all_companies:
        combined_df = pd.concat(all_companies, ignore_index=True)
        combined_df.to_excel("data/all_companies_summary.xlsx", index=False)
        print("✓ Đã tạo file tổng hợp all_companies_summary.xlsx")
    
    print(f"\n🎉 Hoàn thành! Đã thu thập dữ liệu cho {len(symbols)} cổ phiếu.")
    print("📁 Kiểm tra thư mục 'data/' để xem các file đã tạo.")
    
except Exception as e:
    print(f"Lỗi khi tạo file tổng hợp: {e}")