# Template Excel cho Phân tích Tài chính

## Cấu trúc file Excel được khuyến nghị

### Sheet 1: Raw Data
- Dữ liệu thô từ API
- Giá cổ phiếu hàng ngày
- Khối lượng giao dịch

### Sheet 2: Company Info
- Thông tin cơ bản công ty
- Market Cap, P/E Ratio, EPS
- Sector, Industry

### Sheet 3: Financial Ratios
**Chỉ số thanh khoản:**
- Current Ratio = Current Assets / Current Liabilities
- Quick Ratio = (Current Assets - Inventory) / Current Liabilities

**Chỉ số hiệu quả:**
- ROE = Net Income / Shareholders' Equity
- ROA = Net Income / Total Assets
- Profit Margin = Net Income / Revenue

**Chỉ số đòn bẩy:**
- Debt-to-Equity = Total Debt / Total Equity
- Interest Coverage = EBIT / Interest Expense

### Sheet 4: Technical Analysis
- Moving Averages (MA20, MA50, MA200)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)

### Sheet 5: Comparison
- So sánh các công ty trong cùng ngành
- Benchmarking với chỉ số thị trường

### Sheet 6: Dashboard
- Charts và graphs tổng hợp
- Key Performance Indicators (KPIs)

## Công thức Excel hữu ích

### Tính toán Moving Average
```excel
=AVERAGE(B2:B21)  // MA20
=AVERAGE(B2:B51)  // MA50
```

### Tính RSI
```excel
// Gain/Loss columns first
=IF(B3>B2,B3-B2,0)  // Gain
=IF(B3<B2,B2-B3,0)  // Loss

// RSI calculation
=100-(100/(1+(AVERAGE(gain_range)/AVERAGE(loss_range))))
```

### Volatility (Standard Deviation)
```excel
=STDEV(B2:B252)*SQRT(252)  // Annualized volatility
```

## Conditional Formatting
- Màu xanh: Tăng giá
- Màu đỏ: Giảm giá
- Màu vàng: Cảnh báo (RSI > 70 hoặc < 30)