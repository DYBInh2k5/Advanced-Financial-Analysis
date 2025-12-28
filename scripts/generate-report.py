"""
Tạo báo cáo phân tích tài chính chi tiết
"""

import pandas as pd
import numpy as np
from datetime import datetime

def generate_company_report(symbol):
    """Tạo báo cáo phân tích cho một công ty"""
    
    try:
        # Đọc dữ liệu
        company_info = pd.read_excel(f'data/{symbol}_company_info.xlsx').iloc[0]
        price_data = pd.read_excel(f'data/{symbol}_price_data.xlsx', index_col=0)
        
        # Tính toán các chỉ số
        current_price = company_info.get('Current_Price', 0)
        pe_ratio = company_info.get('PE_Ratio', 0)
        market_cap = company_info.get('Market_Cap', 0)
        
        # Tính performance
        price_1m_ago = price_data['Close'].iloc[-22] if len(price_data) > 22 else price_data['Close'].iloc[0]
        price_3m_ago = price_data['Close'].iloc[-66] if len(price_data) > 66 else price_data['Close'].iloc[0]
        price_1y_ago = price_data['Close'].iloc[0]
        
        perf_1m = ((current_price - price_1m_ago) / price_1m_ago * 100) if price_1m_ago > 0 else 0
        perf_3m = ((current_price - price_3m_ago) / price_3m_ago * 100) if price_3m_ago > 0 else 0
        perf_1y = ((current_price - price_1y_ago) / price_1y_ago * 100) if price_1y_ago > 0 else 0
        
        # Volatility
        daily_returns = price_data['Close'].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(252) * 100
        
        # Tạo báo cáo
        report = f"""
# Báo cáo Phân tích Tài chính - {company_info.get('Company_Name', symbol)}

## Thông tin Cơ bản
- **Mã cổ phiếu**: {symbol}
- **Tên công ty**: {company_info.get('Company_Name', 'N/A')}
- **Ngành**: {company_info.get('Sector', 'N/A')}
- **Lĩnh vực**: {company_info.get('Industry', 'N/A')}
- **Ngày phân tích**: {datetime.now().strftime('%d/%m/%Y')}

## Thông tin Tài chính Cơ bản
- **Giá hiện tại**: ${current_price:.2f}
- **Vốn hóa thị trường**: ${market_cap:,.0f}
- **P/E Ratio**: {pe_ratio:.2f}
- **P/B Ratio**: {company_info.get('PB_Ratio', 0):.2f}
- **Beta**: {company_info.get('Beta', 0):.2f}
- **Dividend Yield**: {company_info.get('Dividend_Yield', 0)*100:.2f}%

## Hiệu suất Giá (Performance)
- **1 tháng**: {perf_1m:+.2f}%
- **3 tháng**: {perf_3m:+.2f}%
- **1 năm**: {perf_1y:+.2f}%
- **52-week High**: ${company_info.get('52_Week_High', 0):.2f}
- **52-week Low**: ${company_info.get('52_Week_Low', 0):.2f}

## Chỉ số Tài chính
- **ROE (Return on Equity)**: {company_info.get('ROE', 0)*100:.2f}%
- **ROA (Return on Assets)**: {company_info.get('ROA', 0)*100:.2f}%
- **Profit Margin**: {company_info.get('Profit_Margin', 0)*100:.2f}%
- **Debt-to-Equity**: {company_info.get('Debt_to_Equity', 0):.2f}

## Phân tích Rủi ro
- **Volatility (1 năm)**: {volatility:.2f}%
- **Beta**: {company_info.get('Beta', 0):.2f} ({'Cao' if company_info.get('Beta', 0) > 1.2 else 'Thấp' if company_info.get('Beta', 0) < 0.8 else 'Trung bình'} so với thị trường)

## Đánh giá Định giá
"""
        
        # Đánh giá P/E
        if pe_ratio > 0:
            if pe_ratio < 15:
                pe_assessment = "Định giá hấp dẫn (P/E thấp)"
            elif pe_ratio < 25:
                pe_assessment = "Định giá hợp lý"
            else:
                pe_assessment = "Có thể định giá cao (P/E cao)"
        else:
            pe_assessment = "Không có lãi hoặc dữ liệu không đầy đủ"
        
        report += f"- **P/E Assessment**: {pe_assessment}\n"
        
        # Đánh giá ROE
        roe = company_info.get('ROE', 0) * 100
        if roe > 15:
            roe_assessment = "Hiệu quả sử dụng vốn tốt"
        elif roe > 10:
            roe_assessment = "Hiệu quả sử dụng vốn trung bình"
        else:
            roe_assessment = "Hiệu quả sử dụng vốn thấp"
        
        report += f"- **ROE Assessment**: {roe_assessment}\n"
        
        # Khuyến nghị đầu tư
        report += f"""
## Khuyến nghị Đầu tư

### Điểm mạnh:
"""
        
        strengths = []
        if roe > 15:
            strengths.append("ROE cao, hiệu quả sử dụng vốn tốt")
        if company_info.get('Profit_Margin', 0) > 0.1:
            strengths.append("Biên lợi nhuận tốt")
        if perf_1y > 0:
            strengths.append("Tăng trưởng giá tích cực trong năm qua")
        if company_info.get('Beta', 0) < 1:
            strengths.append("Rủi ro thấp hơn thị trường")
        
        if not strengths:
            strengths.append("Cần phân tích thêm dữ liệu")
        
        for strength in strengths:
            report += f"- {strength}\n"
        
        report += f"""
### Điểm yếu:
"""
        
        weaknesses = []
        if pe_ratio > 30:
            weaknesses.append("P/E cao, có thể định giá quá mức")
        if roe < 10:
            weaknesses.append("ROE thấp, hiệu quả sử dụng vốn kém")
        if perf_1y < -10:
            weaknesses.append("Giá giảm mạnh trong năm qua")
        if volatility > 40:
            weaknesses.append("Biến động giá cao, rủi ro lớn")
        
        if not weaknesses:
            weaknesses.append("Không có điểm yếu đáng kể")
        
        for weakness in weaknesses:
            report += f"- {weakness}\n"
        
        # Khuyến nghị cuối cùng
        report += f"""
### Khuyến nghị:
"""
        
        # Logic đơn giản cho khuyến nghị
        score = 0
        if roe > 15: score += 1
        if pe_ratio > 0 and pe_ratio < 25: score += 1
        if perf_1y > 0: score += 1
        if volatility < 30: score += 1
        if company_info.get('Profit_Margin', 0) > 0.1: score += 1
        
        if score >= 4:
            recommendation = "**BUY** - Cổ phiếu có triển vọng tốt"
        elif score >= 2:
            recommendation = "**HOLD** - Theo dõi thêm trước khi quyết định"
        else:
            recommendation = "**CAUTION** - Cần nghiên cứu kỹ trước khi đầu tư"
        
        report += f"{recommendation}\n"
        
        report += f"""
---
**Lưu ý**: Đây là báo cáo phân tích tự động dựa trên dữ liệu công khai. 
Nhà đầu tư nên tham khảo thêm ý kiến chuyên gia và nghiên cứu kỹ trước khi đưa ra quyết định đầu tư.
"""
        
        # Lưu báo cáo
        with open(f'reports/{symbol}_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ Đã tạo báo cáo phân tích cho {symbol}")
        return report
        
    except Exception as e:
        print(f"✗ Lỗi khi tạo báo cáo cho {symbol}: {e}")
        return None

if __name__ == "__main__":
    # Tạo thư mục reports
    import os
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Tạo báo cáo cho tất cả các công ty
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    print("Tạo báo cáo phân tích chi tiết...")
    
    for symbol in symbols:
        generate_company_report(symbol)
    
    print(f"\n🎉 Đã tạo xong {len(symbols)} báo cáo phân tích!")
    print("📁 Kiểm tra thư mục 'reports/' để xem các báo cáo.")