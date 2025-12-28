"""
Demo hiển thị kết quả phân tích tài chính
"""

import pandas as pd
import numpy as np
from datetime import datetime

def display_analysis_results():
    """Hiển thị kết quả phân tích tài chính"""
    
    print("=" * 80)
    print("🎯 KẾT QUẢ PHÂN TÍCH TÀI CHÍNH - DEMO")
    print("=" * 80)
    print(f"📅 Cập nhật: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Đọc dữ liệu tổng hợp
        summary_df = pd.read_excel('data/all_companies_summary.xlsx')
        
        print("\n📊 TỔNG QUAN CÁC CÔNG TY:")
        print("-" * 80)
        
        # Hiển thị thông tin cơ bản
        for _, company in summary_df.iterrows():
            symbol = company.get('Symbol', 'N/A')
            name = company.get('Company_Name', 'N/A')
            sector = company.get('Sector', 'N/A')
            price = company.get('Current_Price', 0)
            market_cap = company.get('Market_Cap', 0)
            pe_ratio = company.get('PE_Ratio', 0)
            
            print(f"\n🏢 {symbol} - {name}")
            print(f"   Ngành: {sector}")
            print(f"   Giá hiện tại: ${price:.2f}")
            print(f"   Vốn hóa: ${market_cap:,.0f}")
            print(f"   P/E Ratio: {pe_ratio:.2f}")
        
        print("\n" + "=" * 80)
        print("📈 BẢNG SO SÁNH CHỈ SỐ TÀI CHÍNH")
        print("=" * 80)
        
        # Tạo bảng so sánh
        comparison_data = []
        for _, company in summary_df.iterrows():
            comparison_data.append({
                'Symbol': company.get('Symbol', ''),
                'Price': f"${company.get('Current_Price', 0):.2f}",
                'P/E': f"{company.get('PE_Ratio', 0):.1f}",
                'ROE': f"{company.get('ROE', 0)*100:.1f}%",
                'Profit Margin': f"{company.get('Profit_Margin', 0)*100:.1f}%",
                'Beta': f"{company.get('Beta', 0):.2f}"
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        print(comparison_df.to_string(index=False))
        
        print("\n" + "=" * 80)
        print("🎯 KHUYẾN NGHỊ ĐẦU TƯ")
        print("=" * 80)
        
        # Phân tích và khuyến nghị đơn giản
        recommendations = []
        
        for _, company in summary_df.iterrows():
            symbol = company.get('Symbol', '')
            pe_ratio = company.get('PE_Ratio', 0)
            roe = company.get('ROE', 0) * 100
            profit_margin = company.get('Profit_Margin', 0) * 100
            beta = company.get('Beta', 0)
            
            # Logic đánh giá đơn giản
            score = 0
            reasons = []
            
            if roe > 15:
                score += 2
                reasons.append("ROE cao")
            elif roe > 10:
                score += 1
                reasons.append("ROE trung bình")
            
            if 0 < pe_ratio < 20:
                score += 2
                reasons.append("P/E hợp lý")
            elif 20 <= pe_ratio < 30:
                score += 1
                reasons.append("P/E chấp nhận được")
            
            if profit_margin > 15:
                score += 1
                reasons.append("Biên lợi nhuận tốt")
            
            if beta < 1.2:
                score += 1
                reasons.append("Rủi ro thấp")
            
            # Xác định khuyến nghị
            if score >= 5:
                recommendation = "🟢 BUY"
                action = "Mua"
            elif score >= 3:
                recommendation = "🟡 HOLD"
                action = "Nắm giữ"
            else:
                recommendation = "🔴 CAUTION"
                action = "Thận trọng"
            
            recommendations.append({
                'symbol': symbol,
                'recommendation': recommendation,
                'action': action,
                'score': score,
                'reasons': ', '.join(reasons) if reasons else 'Cần phân tích thêm'
            })
        
        # Hiển thị khuyến nghị
        for rec in recommendations:
            print(f"\n{rec['recommendation']} {rec['symbol']} - {rec['action']}")
            print(f"   Điểm số: {rec['score']}/6")
            print(f"   Lý do: {rec['reasons']}")
        
        print("\n" + "=" * 80)
        print("📊 PHÂN TÍCH KỸ THUẬT NHANH - AAPL")
        print("=" * 80)
        
        # Phân tích kỹ thuật cho AAPL
        try:
            aapl_price = pd.read_excel('data/AAPL_price_data.xlsx', index_col=0)
            
            # Tính các chỉ số
            current_price = aapl_price['Close'].iloc[-1]
            ma_20 = aapl_price['Close'].rolling(20).mean().iloc[-1]
            ma_50 = aapl_price['Close'].rolling(50).mean().iloc[-1]
            
            # Tính RSI đơn giản
            delta = aapl_price['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = (100 - (100 / (1 + rs))).iloc[-1]
            
            # Volatility
            daily_returns = aapl_price['Close'].pct_change()
            volatility = daily_returns.std() * np.sqrt(252) * 100
            
            print(f"💰 Giá hiện tại: ${current_price:.2f}")
            print(f"📈 MA20: ${ma_20:.2f} ({'Tích cực' if current_price > ma_20 else 'Tiêu cực'})")
            print(f"📈 MA50: ${ma_50:.2f} ({'Tích cực' if current_price > ma_50 else 'Tiêu cực'})")
            print(f"⚡ RSI: {rsi:.1f} ({'Quá mua' if rsi > 70 else 'Quá bán' if rsi < 30 else 'Trung tính'})")
            print(f"📊 Volatility: {volatility:.1f}%")
            
            # Xu hướng
            if current_price > ma_20 > ma_50:
                trend = "🟢 Xu hướng tăng mạnh"
            elif current_price > ma_20:
                trend = "🟡 Xu hướng tăng nhẹ"
            elif current_price < ma_20 < ma_50:
                trend = "🔴 Xu hướng giảm"
            else:
                trend = "⚪ Xu hướng không rõ ràng"
            
            print(f"📊 Xu hướng: {trend}")
            
        except Exception as e:
            print(f"❌ Không thể phân tích kỹ thuật: {e}")
        
        print("\n" + "=" * 80)
        print("📁 FILES ĐÃ TẠO")
        print("=" * 80)
        
        print("📊 Excel Dashboard: Financial_Analysis_Dashboard.xlsx")
        print("📋 Báo cáo chi tiết: reports/[SYMBOL]_analysis_report.md")
        print("📈 Dữ liệu thô: data/[SYMBOL]_price_data.xlsx")
        print("📄 Thông tin công ty: data/[SYMBOL]_company_info.xlsx")
        
        print("\n" + "=" * 80)
        print("✅ DEMO HOÀN TẤT - DỰ ÁN SẴN SÀNG SỬ DỤNG!")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Lỗi khi hiển thị kết quả: {e}")
        print("Vui lòng chạy lại scripts thu thập dữ liệu.")

if __name__ == "__main__":
    display_analysis_results()