"""
Tạo file Excel phân tích tài chính hoàn chỉnh
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import xlsxwriter

def calculate_technical_indicators(df):
    """Tính các chỉ báo kỹ thuật"""
    # Moving Averages
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['MA_200'] = df['Close'].rolling(window=200).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Volatility (20-day)
    df['Volatility'] = df['Close'].pct_change().rolling(window=20).std() * np.sqrt(252) * 100
    
    # Daily Returns
    df['Daily_Return'] = df['Close'].pct_change() * 100
    
    return df

def create_financial_analysis_excel():
    """Tạo file Excel phân tích tài chính"""
    
    # Tạo workbook
    workbook = xlsxwriter.Workbook('Financial_Analysis_Dashboard.xlsx')
    
    # Định dạng
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    number_format = workbook.add_format({'num_format': '#,##0.00'})
    percent_format = workbook.add_format({'num_format': '0.00%'})
    currency_format = workbook.add_format({'num_format': '$#,##0'})
    
    # Sheet 1: Company Summary
    worksheet1 = workbook.add_worksheet('Company Summary')
    
    try:
        summary_df = pd.read_excel('data/all_companies_summary.xlsx')
        
        # Headers
        headers = ['Symbol', 'Company Name', 'Sector', 'Market Cap', 'Current Price', 
                  'P/E Ratio', 'P/B Ratio', 'ROE', 'ROA', 'Profit Margin', 'Beta']
        
        for col, header in enumerate(headers):
            worksheet1.write(0, col, header, header_format)
        
        # Data
        for row, (_, company) in enumerate(summary_df.iterrows(), 1):
            worksheet1.write(row, 0, company.get('Symbol', ''))
            worksheet1.write(row, 1, company.get('Company_Name', ''))
            worksheet1.write(row, 2, company.get('Sector', ''))
            worksheet1.write(row, 3, company.get('Market_Cap', 0), currency_format)
            worksheet1.write(row, 4, company.get('Current_Price', 0), number_format)
            worksheet1.write(row, 5, company.get('PE_Ratio', 0), number_format)
            worksheet1.write(row, 6, company.get('PB_Ratio', 0), number_format)
            worksheet1.write(row, 7, company.get('ROE', 0), percent_format)
            worksheet1.write(row, 8, company.get('ROA', 0), percent_format)
            worksheet1.write(row, 9, company.get('Profit_Margin', 0), percent_format)
            worksheet1.write(row, 10, company.get('Beta', 0), number_format)
        
        # Auto-fit columns
        worksheet1.set_column('A:K', 15)
        
    except Exception as e:
        worksheet1.write(0, 0, f"Error loading summary data: {e}")
    
    # Sheet 2: Technical Analysis cho AAPL
    worksheet2 = workbook.add_worksheet('AAPL Technical Analysis')
    
    try:
        aapl_df = pd.read_excel('data/AAPL_price_data.xlsx', index_col=0)
        aapl_df = calculate_technical_indicators(aapl_df)
        
        # Headers
        tech_headers = ['Date', 'Close', 'MA_20', 'MA_50', 'MA_200', 'RSI', 'Volatility', 'Daily_Return']
        
        for col, header in enumerate(tech_headers):
            worksheet2.write(0, col, header, header_format)
        
        # Data (last 100 days)
        recent_data = aapl_df.tail(100)
        for row, (date, data) in enumerate(recent_data.iterrows(), 1):
            worksheet2.write(row, 0, date.strftime('%Y-%m-%d'))
            worksheet2.write(row, 1, data['Close'], number_format)
            worksheet2.write(row, 2, data.get('MA_20', ''), number_format)
            worksheet2.write(row, 3, data.get('MA_50', ''), number_format)
            worksheet2.write(row, 4, data.get('MA_200', ''), number_format)
            worksheet2.write(row, 5, data.get('RSI', ''), number_format)
            worksheet2.write(row, 6, data.get('Volatility', ''), percent_format)
            worksheet2.write(row, 7, data.get('Daily_Return', ''), percent_format)
        
        worksheet2.set_column('A:H', 12)
        
    except Exception as e:
        worksheet2.write(0, 0, f"Error loading AAPL data: {e}")
    
    # Sheet 3: Financial Ratios Comparison
    worksheet3 = workbook.add_worksheet('Ratios Comparison')
    
    try:
        # Create comparison table
        comparison_headers = ['Metric', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'Average']
        
        for col, header in enumerate(comparison_headers):
            worksheet3.write(0, col, header, header_format)
        
        metrics = ['P/E Ratio', 'P/B Ratio', 'ROE', 'ROA', 'Profit Margin', 'Beta']
        
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        company_data = {}
        
        for symbol in symbols:
            try:
                df = pd.read_excel(f'data/{symbol}_company_info.xlsx')
                company_data[symbol] = df.iloc[0]
            except:
                company_data[symbol] = {}
        
        for row, metric in enumerate(metrics, 1):
            worksheet3.write(row, 0, metric)
            
            values = []
            for col, symbol in enumerate(symbols, 1):
                if metric == 'P/E Ratio':
                    value = company_data[symbol].get('PE_Ratio', 0)
                elif metric == 'P/B Ratio':
                    value = company_data[symbol].get('PB_Ratio', 0)
                elif metric == 'ROE':
                    value = company_data[symbol].get('ROE', 0)
                elif metric == 'ROA':
                    value = company_data[symbol].get('ROA', 0)
                elif metric == 'Profit Margin':
                    value = company_data[symbol].get('Profit_Margin', 0)
                elif metric == 'Beta':
                    value = company_data[symbol].get('Beta', 0)
                else:
                    value = 0
                
                values.append(value if value and not pd.isna(value) else 0)
                
                if metric in ['ROE', 'ROA', 'Profit Margin']:
                    worksheet3.write(row, col, value, percent_format)
                else:
                    worksheet3.write(row, col, value, number_format)
            
            # Average
            avg_value = np.mean([v for v in values if v != 0]) if values else 0
            if metric in ['ROE', 'ROA', 'Profit Margin']:
                worksheet3.write(row, 6, avg_value, percent_format)
            else:
                worksheet3.write(row, 6, avg_value, number_format)
        
        worksheet3.set_column('A:G', 15)
        
    except Exception as e:
        worksheet3.write(0, 0, f"Error creating comparison: {e}")
    
    # Sheet 4: Investment Summary
    worksheet4 = workbook.add_worksheet('Investment Summary')
    
    # Tạo bảng tóm tắt đầu tư
    summary_headers = ['Company', 'Current Price', 'Recommendation', 'Target Price', 'Upside/Downside', 'Risk Level']
    
    for col, header in enumerate(summary_headers):
        worksheet4.write(0, col, header, header_format)
    
    # Dữ liệu mẫu (trong thực tế sẽ dựa trên phân tích)
    recommendations = [
        ['Apple (AAPL)', 'Current', 'BUY', 'Target', '15%', 'Medium'],
        ['Microsoft (MSFT)', 'Current', 'HOLD', 'Target', '8%', 'Low'],
        ['Alphabet (GOOGL)', 'Current', 'BUY', 'Target', '12%', 'Medium'],
        ['Amazon (AMZN)', 'Current', 'HOLD', 'Target', '5%', 'Medium'],
        ['Tesla (TSLA)', 'Current', 'SELL', 'Target', '-10%', 'High']
    ]
    
    for row, rec in enumerate(recommendations, 1):
        for col, value in enumerate(rec):
            worksheet4.write(row, col, value)
    
    worksheet4.set_column('A:F', 18)
    
    workbook.close()
    print("✓ Đã tạo file Financial_Analysis_Dashboard.xlsx")

if __name__ == "__main__":
    create_financial_analysis_excel()
    print("🎉 File Excel phân tích tài chính đã sẵn sàng!")