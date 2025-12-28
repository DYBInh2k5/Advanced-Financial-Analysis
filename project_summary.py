"""
Tổng kết dự án phân tích tài chính
"""

import os
from datetime import datetime

def check_project_status():
    """Kiểm tra trạng thái dự án"""
    
    print("=" * 60)
    print("📊 TỔNG KẾT DỰ ÁN PHÂN TÍCH TÀI CHÍNH")
    print("=" * 60)
    print(f"Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Kiểm tra các thư mục
    directories = {
        'data': 'Dữ liệu tài chính',
        'reports': 'Báo cáo phân tích',
        'scripts': 'Scripts thu thập và xử lý',
        'documentation': 'Tài liệu hướng dẫn',
        'excel': 'Templates Excel',
        'powerbi': 'Hướng dẫn Power BI',
        'templates': 'Mẫu báo cáo',
        'config': 'Cấu hình'
    }
    
    print("\n📁 CẤU TRÚC DỰ ÁN:")
    for directory, description in directories.items():
        if os.path.exists(directory):
            files = os.listdir(directory)
            print(f"✅ {directory}/ - {description} ({len(files)} files)")
        else:
            print(f"❌ {directory}/ - Chưa tạo")
    
    # Kiểm tra các file quan trọng
    important_files = {
        'Financial_Analysis_Dashboard.xlsx': 'Dashboard Excel chính',
        'README.md': 'Hướng dẫn dự án',
        '.gitignore': 'Git ignore file'
    }
    
    print("\n📄 CÁC FILE QUAN TRỌNG:")
    for file, description in important_files.items():
        if os.path.exists(file):
            print(f"✅ {file} - {description}")
        else:
            print(f"❌ {file} - Chưa có")
    
    # Kiểm tra dữ liệu
    if os.path.exists('data'):
        data_files = [f for f in os.listdir('data') if f.endswith('.xlsx')]
        print(f"\n📈 DỮ LIỆU: {len(data_files)} file Excel")
        for file in data_files[:5]:  # Hiển thị 5 file đầu
            print(f"  - {file}")
        if len(data_files) > 5:
            print(f"  ... và {len(data_files) - 5} file khác")
    
    # Kiểm tra báo cáo
    if os.path.exists('reports'):
        report_files = [f for f in os.listdir('reports') if f.endswith('.md')]
        print(f"\n📋 BÁO CÁO: {len(report_files)} báo cáo phân tích")
        for file in report_files:
            print(f"  - {file}")
    
    # Hướng dẫn sử dụng
    print("\n" + "=" * 60)
    print("🚀 HƯỚNG DẪN SỬ DỤNG")
    print("=" * 60)
    
    print("\n1. 📊 PHÂN TÍCH EXCEL:")
    print("   - Mở 'Financial_Analysis_Dashboard.xlsx'")
    print("   - Xem các sheet: Company Summary, Technical Analysis, Ratios Comparison")
    
    print("\n2. 📋 ĐỌC BÁO CÁO:")
    print("   - Vào thư mục 'reports/'")
    print("   - Đọc các file .md để có phân tích chi tiết từng công ty")
    
    print("\n3. 🔄 CẬP NHẬT DỮ LIỆU:")
    print("   - Chạy: python scripts/simple-data-collector.py")
    print("   - Chạy: python scripts/create-analysis-excel.py")
    print("   - Chạy: python scripts/generate-report.py")
    
    print("\n4. 📚 TÀI LIỆU THAM KHẢO:")
    print("   - documentation/analysis-methodology.md - Phương pháp phân tích")
    print("   - powerbi/dashboard-guide.md - Hướng dẫn Power BI")
    print("   - excel/financial-analysis-template.md - Template Excel")
    
    print("\n5. 🔧 MỞ RỘNG DỰ ÁN:")
    print("   - Thêm cổ phiếu mới vào danh sách symbols")
    print("   - Tùy chỉnh các chỉ số phân tích")
    print("   - Tích hợp với Power BI để tạo dashboard tương tác")
    print("   - Thiết lập cập nhật dữ liệu tự động")
    
    print("\n" + "=" * 60)
    print("✅ DỰ ÁN ĐÃ SẴN SÀNG SỬ DỤNG!")
    print("=" * 60)

if __name__ == "__main__":
    check_project_status()