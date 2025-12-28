# Hướng dẫn tạo Dashboard Power BI

## Cấu trúc Dashboard được khuyến nghị

### Page 1: Overview (Tổng quan)
**Visuals:**
- Card: Market Cap, P/E Ratio, Current Price
- Line Chart: Stock Price Trend (6 months)
- Gauge: RSI Current Value
- Table: Top 5 Holdings

### Page 2: Financial Performance
**Visuals:**
- Clustered Column Chart: Revenue vs Net Income (Quarterly)
- Line Chart: Profit Margin Trend
- Waterfall Chart: Revenue Breakdown
- Matrix: Financial Ratios Comparison

### Page 3: Technical Analysis
**Visuals:**
- Line Chart: Price with Moving Averages
- Area Chart: Volume Analysis
- Scatter Plot: Risk vs Return
- Histogram: Daily Returns Distribution

### Page 4: Sector Comparison
**Visuals:**
- Treemap: Market Cap by Company
- Clustered Bar Chart: P/E Ratios Comparison
- Scatter Plot: ROE vs ROA
- Funnel Chart: Revenue Ranking

## Data Model Setup

### Tables cần thiết:
1. **Stock_Prices**
   - Date, Symbol, Open, High, Low, Close, Volume

2. **Company_Info**
   - Symbol, Company_Name, Sector, Industry, Market_Cap

3. **Financial_Ratios**
   - Symbol, Date, PE_Ratio, ROE, ROA, Debt_to_Equity

4. **Date_Table** (Calendar table)
   - Date, Year, Quarter, Month, Week

### Relationships:
- Stock_Prices[Symbol] → Company_Info[Symbol]
- Financial_Ratios[Symbol] → Company_Info[Symbol]
- Stock_Prices[Date] → Date_Table[Date]

## DAX Measures quan trọng

### Price Change
```dax
Price_Change = 
VAR CurrentPrice = SELECTEDVALUE(Stock_Prices[Close])
VAR PreviousPrice = CALCULATE(
    SELECTEDVALUE(Stock_Prices[Close]),
    DATEADD(Date_Table[Date], -1, DAY)
)
RETURN CurrentPrice - PreviousPrice
```

### Price Change %
```dax
Price_Change_Pct = 
DIVIDE([Price_Change], [Previous_Price], 0) * 100
```

### Moving Average 20
```dax
MA_20 = 
CALCULATE(
    AVERAGE(Stock_Prices[Close]),
    DATESINPERIOD(
        Date_Table[Date],
        MAX(Date_Table[Date]),
        -20,
        DAY
    )
)
```

### Volatility
```dax
Volatility = 
VAR DailyReturns = 
    ADDCOLUMNS(
        Stock_Prices,
        "Daily_Return",
        DIVIDE(
            Stock_Prices[Close] - Stock_Prices[Previous_Close],
            Stock_Prices[Previous_Close]
        )
    )
RETURN STDEV.S(DailyReturns[Daily_Return]) * SQRT(252)
```

## Formatting Tips

### Colors:
- Tăng giá: #00B050 (Green)
- Giảm giá: #FF0000 (Red)
- Neutral: #4472C4 (Blue)

### Conditional Formatting:
- RSI > 70: Red background
- RSI < 30: Green background
- P/E > 25: Orange text

## Interactive Features
- Slicer: Date Range, Company Symbol, Sector
- Drill-through: From overview to detailed analysis
- Bookmarks: Save different views
- Tooltips: Custom tooltips with additional metrics