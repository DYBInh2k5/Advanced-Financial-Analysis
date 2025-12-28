# Phương pháp Phân tích Tài chính

## 1. Phân tích Cơ bản (Fundamental Analysis)

### A. Phân tích Báo cáo Tài chính
**Bảng Cân đối Kế toán:**
- Tài sản (Assets): Current Assets, Fixed Assets
- Nợ phải trả (Liabilities): Current Liabilities, Long-term Debt
- Vốn chủ sở hữu (Equity): Shareholders' Equity

**Báo cáo Kết quả Kinh doanh:**
- Doanh thu (Revenue/Sales)
- Chi phí hoạt động (Operating Expenses)
- Lợi nhuận ròng (Net Income)

**Báo cáo Lưu chuyển Tiền tệ:**
- Hoạt động kinh doanh (Operating Activities)
- Hoạt động đầu tư (Investing Activities)
- Hoạt động tài chính (Financing Activities)

### B. Chỉ số Tài chính Quan trọng

**Chỉ số Thanh khoản:**
- Current Ratio = Tài sản ngắn hạn / Nợ ngắn hạn
- Quick Ratio = (Tài sản ngắn hạn - Hàng tồn kho) / Nợ ngắn hạn
- Cash Ratio = Tiền mặt / Nợ ngắn hạn

**Chỉ số Hiệu quả:**
- ROE = Lợi nhuận ròng / Vốn chủ sở hữu
- ROA = Lợi nhuận ròng / Tổng tài sản
- Profit Margin = Lợi nhuận ròng / Doanh thu

**Chỉ số Đòn bẩy:**
- Debt-to-Equity = Tổng nợ / Vốn chủ sở hữu
- Interest Coverage = EBIT / Chi phí lãi vay

**Chỉ số Định giá:**
- P/E Ratio = Giá cổ phiếu / EPS
- P/B Ratio = Giá cổ phiếu / Book Value per Share
- EV/EBITDA = Enterprise Value / EBITDA

## 2. Phân tích Kỹ thuật (Technical Analysis)

### A. Chỉ báo Xu hướng
**Moving Averages:**
- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- Tín hiệu: Golden Cross, Death Cross

**MACD (Moving Average Convergence Divergence):**
- MACD Line = EMA12 - EMA26
- Signal Line = EMA9 của MACD Line
- Histogram = MACD Line - Signal Line

### B. Chỉ báo Momentum
**RSI (Relative Strength Index):**
- Công thức: RSI = 100 - (100 / (1 + RS))
- RS = Average Gain / Average Loss
- Overbought: RSI > 70
- Oversold: RSI < 30

**Stochastic Oscillator:**
- %K = (Close - Low14) / (High14 - Low14) × 100
- %D = SMA3 của %K

### C. Chỉ báo Khối lượng
**Volume Analysis:**
- On-Balance Volume (OBV)
- Volume Price Trend (VPT)
- Accumulation/Distribution Line

## 3. Phân tích Rủi ro

### A. Volatility
**Historical Volatility:**
- Standard deviation của daily returns
- Annualized: σ_daily × √252

**Beta:**
- Correlation với thị trường
- β > 1: Riskier than market
- β < 1: Less risky than market

### B. Value at Risk (VaR)
**Parametric VaR:**
- VaR = μ - (z × σ) × Portfolio Value
- Confidence levels: 95%, 99%

**Monte Carlo Simulation:**
- Simulate thousands of scenarios
- Calculate potential losses

## 4. Quy trình Phân tích

### Bước 1: Thu thập Dữ liệu
1. Tải dữ liệu từ API
2. Làm sạch và chuẩn hóa dữ liệu
3. Tính toán các chỉ số cần thiết

### Bước 2: Phân tích Định lượng
1. Tính toán financial ratios
2. So sánh với industry averages
3. Phân tích xu hướng theo thời gian

### Bước 3: Phân tích Kỹ thuật
1. Vẽ charts với indicators
2. Xác định support/resistance levels
3. Tìm patterns và signals

### Bước 4: Đánh giá Rủi ro
1. Tính volatility và beta
2. Stress testing scenarios
3. Portfolio optimization

### Bước 5: Kết luận và Khuyến nghị
1. Tổng hợp findings
2. Investment recommendation
3. Risk assessment summary