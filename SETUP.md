# Setup Guide - Advanced Financial Analysis

## 🚀 Hướng dẫn Cài đặt Nhanh

### 1. Clone Repository
```bash
git clone https://github.com/DYBInh2k5/Advanced-Financial-Analysis.git
cd Advanced-Financial-Analysis
```

### 2. Cài đặt Python Dependencies
```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt packages
pip install -r config/requirements.txt
```

### 3. Chạy Phân tích Đầu tiên
```bash
# Phân tích cơ bản
python scripts/simple-data-collector.py
python demo_analysis.py

# Phân tích nâng cao (TẤT CẢ)
python run_advanced_analysis.py
```

## 📋 Requirements

### System Requirements
- **Python**: 3.8 trở lên
- **RAM**: Tối thiểu 4GB (khuyến nghị 8GB)
- **Storage**: 1GB trống
- **Internet**: Để tải dữ liệu từ APIs

### Python Packages
```
pandas>=1.5.0
numpy>=1.24.0
yfinance>=0.2.0
matplotlib>=3.6.0
seaborn>=0.12.0
scipy>=1.10.0
xlsxwriter>=3.0.0
openpyxl>=3.0.0
requests>=2.28.0
plotly>=5.15.0
```

## 🔧 Cấu hình Tùy chọn

### API Keys (Tùy chọn)
1. Copy file template:
```bash
cp config/api-keys-template.txt config/api-keys.txt
```

2. Đăng ký API keys miễn phí:
   - **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
   - **FRED**: https://fred.stlouisfed.org/docs/api/api_key.html

3. Điền API keys vào `config/api-keys.txt`

### Tùy chỉnh Danh sách Cổ phiếu
Sửa file `scripts/simple-data-collector.py`:
```python
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # Thay đổi ở đây
```

## 📊 Cách Sử dụng

### Phân tích Nhanh
```bash
python demo_analysis.py
```

### Phân tích Từng Module
```bash
# Portfolio Optimization
python scripts/portfolio-optimizer.py

# Sector Analysis  
python scripts/sector-analysis.py

# Technical Analysis
python scripts/advanced-technical-analysis.py

# Risk Management
python scripts/risk-management.py
```

### Cập nhật Dữ liệu
```bash
# Hàng ngày
python scripts/simple-data-collector.py

# Hàng tuần (phân tích đầy đủ)
python run_advanced_analysis.py
```

## 📁 Kết quả Output

Sau khi chạy, bạn sẽ có:

```
├── Financial_Analysis_Dashboard.xlsx    # Dashboard chính
├── Portfolio_Analysis.xlsx             # Tối ưu hóa danh mục
├── Sector_Analysis.xlsx               # Phân tích ngành
├── Technical_Analysis_*.xlsx          # Phân tích kỹ thuật
├── Risk_Analysis.xlsx                 # Quản lý rủi ro
├── data/                             # Dữ liệu thô
└── reports/                          # Báo cáo markdown
```

## 🐛 Troubleshooting

### Lỗi thường gặp

**1. ModuleNotFoundError**
```bash
pip install -r config/requirements.txt
```

**2. Lỗi kết nối API**
- Kiểm tra internet connection
- Đợi vài phút rồi thử lại (rate limiting)

**3. Lỗi Excel file**
- Đóng tất cả file Excel đang mở
- Xóa file cũ và chạy lại

**4. Lỗi encoding trên Windows**
```bash
set PYTHONIOENCODING=utf-8
python script.py
```

### Performance Tips

**Tăng tốc độ:**
- Sử dụng SSD
- Tăng RAM available
- Chạy trên Python 3.9+

**Giảm memory usage:**
- Giảm số lượng cổ phiếu phân tích
- Giảm historical data period

## 🆘 Hỗ trợ

### Báo cáo lỗi
- **GitHub Issues**: https://github.com/DYBInh2k5/Advanced-Financial-Analysis/issues
- **Email**: binh.vd01500@sinhvien.hoasen.edu.vn

### Đóng góp
Xem file `CONTRIBUTING.md` để biết cách đóng góp.

### Documentation
- **README.md**: Tổng quan dự án
- **documentation/**: Phương pháp phân tích chi tiết
- **templates/**: Mẫu báo cáo

---

**🎉 Chúc bạn phân tích thành công!**