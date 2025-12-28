# Dự án Phân tích Tài chính Nâng cao (Advanced Financial Analysis)

## Mô tả dự án
Hệ thống phân tích tài chính toàn diện sử dụng dữ liệu công khai để thực hiện:

### 📊 Phân tích Cơ bản
- Hiệu suất tài chính của công ty
- So sánh các chỉ số tài chính
- Phân tích fundamental và valuation

### 📈 Phân tích Nâng cao
- **Portfolio Optimization**: Tối ưu hóa danh mục đầu tư với Sharpe Ratio
- **Sector Analysis**: Phân tích ngành và so sánh hiệu suất
- **Advanced Technical Analysis**: 15+ chỉ báo kỹ thuật chuyên sâu
- **Risk Management**: VaR, CVaR, Stress Testing, Drawdown Analysis

## Công nghệ sử dụng
- **Python**: Pandas, NumPy, SciPy, Matplotlib cho phân tích
- **Excel**: Dashboard và báo cáo tương tác
- **Power BI**: Visualization nâng cao
- **APIs**: Yahoo Finance, Alpha Vantage

## Nguồn dữ liệu
- **Yahoo Finance**: Dữ liệu giá và thông tin công ty (miễn phí)
- **Alpha Vantage API**: Báo cáo tài chính chi tiết
- **Federal Reserve Economic Data (FRED)**: Dữ liệu kinh tế vĩ mô
- **World Bank Open Data**: Chỉ số kinh tế quốc gia

## Cấu trúc dự án
```
financial-analysis/
├── data/                    # Dữ liệu thô và đã xử lý
├── reports/                 # Báo cáo phân tích tự động
├── scripts/                 # Scripts phân tích nâng cao
│   ├── portfolio-optimizer.py
│   ├── sector-analysis.py
│   ├── advanced-technical-analysis.py
│   └── risk-management.py
├── excel/                   # Templates Excel
├── powerbi/                 # Hướng dẫn Power BI
├── documentation/           # Tài liệu phương pháp
└── templates/              # Mẫu báo cáo

# Files kết quả
├── Financial_Analysis_Dashboard.xlsx
├── Portfolio_Analysis.xlsx
├── Sector_Analysis.xlsx
├── Technical_Analysis_*.xlsx
└── Risk_Analysis.xlsx
```

## 🚀 Bắt đầu nhanh
```bash
# 1. Cài đặt dependencies
pip install -r config/requirements.txt

# 2. Thu thập dữ liệu cơ bản
python scripts/simple-data-collector.py

# 3. Chạy phân tích cơ bản
python scripts/create-analysis-excel.py
python scripts/generate-report.py

# 4. Chạy phân tích nâng cao (TẤT CẢ)
python run_advanced_analysis.py

# 5. Xem tổng quan
python demo_analysis.py
```
#
# 📊 Kết quả Phân tích Mới nhất

### 🏆 Portfolio Optimization
- **Tối ưu Sharpe Ratio**: 100% GOOGL (Sharpe: 1.63)
- **Tối ưu Rủi ro thấp**: 65.4% MSFT + 20.5% GOOGL + 14.1% AAPL
- **Equal Weight**: Sharpe Ratio 0.76, Volatility 29.81%

### 🏭 Sector Analysis
- **Ngành tốt nhất**: Communication Services (ROE: 35.4%, Profit Margin: 32.2%)
- **Khuyến nghị**: 🟢 STRONG BUY Communication Services & Technology
- **Tránh**: 🔴 Consumer Cyclical (rủi ro cao, lợi nhuận thấp)

### 📈 Technical Analysis Highlights
- **MSFT**: 🟢 BULLISH - Giá trên MA200, MACD tích cực
- **AMZN**: 🟢 BULLISH - Nhưng Williams %R overbought
- **TSLA**: 🟢 BULLISH - Xu hướng tăng mạnh
- **AAPL**: 🔴 BEARISH - Dưới MA20, MACD tiêu cực
- **GOOGL**: 🔴 BEARISH - Mặc dù trên MA200

### ⚠️ Risk Management
- **Portfolio VaR (95%)**: -2.74% ($2,737 loss/day)
- **Max Drawdown**: -29.16%
- **Cảnh báo**: Volatility cao (29.81%), cần stop-loss strategy
- **Stress Test**: Market crash có thể gây loss 32.7%

## 🎯 Insights Chính

1. **GOOGL dominates**: Hiệu suất vượt trội với Sharpe ratio 1.63
2. **Technology sector**: Tốt nhất về ROE (101.8%) và growth potential
3. **Risk concentration**: Portfolio cần diversify hơn để giảm correlation
4. **Technical signals**: Mixed signals, cần theo dõi sát

## 💡 Khuyến nghị Đầu tư

### Ngắn hạn (1-3 tháng)
- **Tăng tỷ trọng**: MSFT, AMZN (technical bullish)
- **Giảm tỷ trọng**: AAPL (technical bearish)
- **Theo dõi**: GOOGL (fundamental tốt nhưng technical mixed)

### Dài hạn (6-12 tháng)
- **Core holding**: Technology sector (MSFT, GOOGL)
- **Satellite**: Communication Services
- **Avoid**: Consumer Cyclical cho đến khi cải thiện fundamentals

### Risk Management
- **Stop-loss**: 15-20% cho individual positions
- **Portfolio limit**: VaR không vượt quá 3%
- **Rebalancing**: Hàng tháng dựa trên technical signals

## 🔄 Cập nhật & Monitoring

### Hàng tuần
```bash
python run_advanced_analysis.py  # Cập nhật tất cả phân tích
```

### Hàng ngày
```bash
python demo_analysis.py  # Quick overview
```

### Theo dõi chỉ số
- RSI < 30 (oversold opportunities)
- VaR > 3% (risk warning)
- Correlation > 0.8 (diversification needed)
- Sharpe ratio changes (performance monitoring)

## 🚀 Tính năng Tiếp theo

### Đang phát triển
- [ ] Real-time alerts system
- [ ] Backtesting framework
- [ ] Machine learning predictions
- [ ] ESG scoring integration
- [ ] Crypto portfolio analysis

### Mở rộng
- [ ] More asset classes (bonds, commodities)
- [ ] International markets
- [ ] Options strategies analysis
- [ ] Fundamental screening tools

---

**⚠️ Disclaimer**: Đây là công cụ phân tích, không phải lời khuyên đầu tư. Luôn tham khảo chuyên gia tài chính và đánh giá rủi ro cá nhân trước khi đầu tư.