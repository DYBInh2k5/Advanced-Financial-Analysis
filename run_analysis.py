"""
Script chính để chạy toàn bộ quy trình phân tích tài chính
"""

import os
import subprocess
import sys
from datetime import datetime

def run_script(script_path, description):
    """Chạy một script Python"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description} - Hoàn thành!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - Lỗi!")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} - Lỗi: {e}")
        return False

def main():
    """Chạy toàn bộ quy trình phân tích"""
    
    print("=" * 60)
    print("🚀 DỰ ÁN PHÂN TÍCH TÀI CHÍNH")
    print("=" * 60)
    print(f"Thời gian bắt đầu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Tạo các thư mục cần thiết
    directories = ['data', 'reports', 'config']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Đã tạo thư mục: {directory}")
    
    # Danh sách các bước thực hiện
    steps = [
        ("scripts/simple-data-collector.py", "Thu thập dữ liệu từ Yahoo Finance"),
        ("scripts/create-analysis-excel.py", "Tạo file Excel phân tích"),
        ("scripts/generate-report.py", "Tạo báo cáo phân tích chi tiết")
    ]
    
    success_count = 0
    
    # Thực hiện từng bước
    for script_path, description in steps:
        if os.path.exists(script_path):
            if run_script(script_path, description):
                success_count += 1
        else:
            print(f"❌ Không tìm thấy file: {script_path}")
    
    # Tổng kết
    print("\n" + "=" * 60)
    print("📊 KẾT QUẢ PHÂN TÍCH")
    print("=" * 60)
    
    print(f"✅ Hoàn thành: {success_count}/{len(steps)} bước")
    
    if success_count == len(steps):
        print("\n🎉 PHÂN TÍCH HOÀN TẤT THÀNH CÔNG!")
        
        print("\n📁 CÁC FILE ĐÃ TẠO:")
        
        # Kiểm tra và liệt kê các file đã tạo
        files_created = []
        
        # File Excel
        if os.path.exists("Financial_Analysis_Dashboard.xlsx"):
            files_created.append("📊 Financial_Analysis_Dashboard.xlsx - Dashboard Excel")
        
        # Dữ liệu
        data_files = [f for f in os.listdir("data") if f.endswith('.xlsx')]
        if data_files:
            files_created.append(f"📈 {len(data_files)} file dữ liệu trong thư mục data/")
        
        # Báo cáo
        if os.path.exists("reports"):
            report_files = [f for f in os.listdir("reports") if f.endswith('.md')]
            if report_files:
                files_created.append(f"📋 {len(report_files)} báo cáo phân tích trong thư mục reports/")
        
        for file_info in files_created:
            print(f"  {file_info}")
        
        print("\n🔍 HƯỚNG DẪN SỬ DỤNG:")
        print("1. Mở file 'Financial_Analysis_Dashboard.xlsx' để xem dashboard")
        print("2. Đọc các báo cáo trong thư mục 'reports/' để có cái nhìn chi tiết")
        print("3. Sử dụng dữ liệu trong thư mục 'data/' cho phân tích thêm")
        print("4. Tham khảo 'documentation/' để hiểu phương pháp phân tích")
        
        print("\n💡 GỢI Ý TIẾP THEO:")
        print("- Import dữ liệu vào Power BI theo hướng dẫn trong powerbi/")
        print("- Tùy chỉnh Excel template theo nhu cầu cụ thể")
        print("- Thiết lập cron job để cập nhật dữ liệu tự động")
        print("- Mở rộng phân tích với thêm nhiều cổ phiếu")
        
    else:
        print(f"\n⚠️  Có {len(steps) - success_count} bước chưa hoàn thành.")
        print("Vui lòng kiểm tra lỗi và chạy lại.")
    
    print(f"\nThời gian kết thúc: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()