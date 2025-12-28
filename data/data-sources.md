# Nguồn dữ liệu tài chính

## 1. Alpha Vantage API (Khuyến nghị)
- **URL**: https://www.alphavantage.co/
- **Miễn phí**: 5 calls/phút, 500 calls/ngày
- **Dữ liệu**: Giá cổ phiếu, chỉ số kỹ thuật, báo cáo tài chính
- **API Key**: Cần đăng ký miễn phí

### Ví dụ API calls:
```
# Giá cổ phiếu hàng ngày
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=YOUR_API_KEY

# Báo cáo thu nhập
https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=AAPL&apikey=YOUR_API_KEY

# Bảng cân đối kế toán
https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=AAPL&apikey=YOUR_API_KEY
```

## 2. Yahoo Finance (yfinance Python)
- **Miễn phí**: Không giới hạn
- **Dữ liệu**: Giá cổ phiếu, thông tin công ty
- **Sử dụng**: Python library `yfinance`

## 3. FRED (Federal Reserve Economic Data)
- **URL**: https://fred.stlouisfed.org/
- **Miễn phí**: Có
- **Dữ liệu**: Chỉ số kinh tế vĩ mô, lãi suất, GDP

## 4. World Bank Open Data
- **URL**: https://data.worldbank.org/
- **Miễn phí**: Có
- **Dữ liệu**: Chỉ số kinh tế quốc gia, dân số, GDP

## Hướng dẫn lấy API Key Alpha Vantage
1. Truy cập: https://www.alphavantage.co/support/#api-key
2. Nhập email để nhận API key miễn phí
3. Lưu API key vào file `config/api-keys.txt`