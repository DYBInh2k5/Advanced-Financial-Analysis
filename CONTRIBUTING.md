# Contributing to Advanced Financial Analysis

Cảm ơn bạn quan tâm đến việc đóng góp cho dự án! 

## Cách đóng góp

### 1. Báo cáo lỗi (Bug Reports)
- Sử dụng GitHub Issues để báo cáo lỗi
- Mô tả chi tiết lỗi và cách tái tạo
- Bao gồm thông tin về môi trường (OS, Python version, etc.)

### 2. Đề xuất tính năng (Feature Requests)
- Mở GitHub Issue với label "enhancement"
- Mô tả rõ tính năng và lý do cần thiết
- Thảo luận trước khi bắt đầu implement

### 3. Pull Requests
- Fork repository
- Tạo branch mới cho feature/bugfix
- Viết code theo coding standards
- Thêm tests nếu có thể
- Cập nhật documentation
- Tạo Pull Request với mô tả chi tiết

## Coding Standards

### Python
- Tuân theo PEP 8
- Sử dụng docstrings cho functions và classes
- Tên biến và function rõ ràng, có ý nghĩa
- Comments bằng tiếng Việt hoặc tiếng Anh

### Git Commit Messages
- Sử dụng tiếng Anh
- Format: `type: description`
- Types: feat, fix, docs, style, refactor, test, chore

Ví dụ:
```
feat: add portfolio optimization module
fix: resolve data loading issue in sector analysis
docs: update README with new features
```

## Development Setup

1. Clone repository:
```bash
git clone https://github.com/DYBInh2k5/Advanced-Financial-Analysis.git
cd Advanced-Financial-Analysis
```

2. Cài đặt dependencies:
```bash
pip install -r config/requirements.txt
```

3. Chạy tests:
```bash
python -m pytest tests/
```

## Cấu trúc dự án

```
├── scripts/           # Core analysis modules
├── data/             # Data storage (gitignored)
├── documentation/    # Analysis methodology
├── templates/        # Report templates
├── config/          # Configuration files
└── tests/           # Unit tests (future)
```

## Liên hệ

- Email: binh.vd01500@sinhvien.hoasen.edu.vn
- GitHub Issues: https://github.com/DYBInh2k5/Advanced-Financial-Analysis/issues

Cảm ơn bạn đã đóng góp! 🚀