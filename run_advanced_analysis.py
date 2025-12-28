"""
Master Script để chạy tất cả phân tích nâng cao
"""

import os
import subprocess
import sys
from datetime import datetime

def run_script(script_path, description):
    """Chạy một script Python"""
    print(f"\n🔄 {description}...")
    print("-" * 60)
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Hoàn thành!")
            return True
        else:
            print(f"❌ {description} - Có lỗi xảy ra!")
            return False
    except Exception as e:
        print(f"❌ {description} - Lỗi: {e}")
        return False

def main():
    """Chạy toàn bộ phân tích nâng cao"""
    
    print("=" * 80)
    print("🚀 PHÂN TÍCH TÀI CHÍNH NÂNG CAO")
    print("=" * 80)
    print(f"⏰ Thời gian bắt đầu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Kiểm tra dữ liệu cơ bản
    if not os.path.exists('data/all_companies_summary.xlsx'):
        print("\n⚠️ Chưa có dữ liệu cơ bản. Đang thu thập...")
        run_script('scripts/simple-data-collector.py', 'Thu thập dữ liệu cơ bản')
    
    # Danh sách các phân tích nâng cao
    advanced_analyses = [
        {
            'script': 'scripts/portfolio-optimizer.py',
            'name': 'Portfolio Optimization',
            'description': 'Tối ưu hóa danh mục đầu tư và phân tích hiệu quả',
            'output': 'Portfolio_Analysis.xlsx'
        },
        {
            'script': 'scripts/sector-analysis.py',
            'name': 'Sector Analysis',
            'description': 'Phân tích ngành và so sánh hiệu suất',
            'output': 'Sector_Analysis.xlsx'
        },
        {
            'script': 'scripts/advanced-technical-analysis.py',
            'name': 'Advanced Technical Analysis',
            'description': 'Phân tích kỹ thuật nâng cao với nhiều chỉ báo',
            'output': 'Technical_Analysis_*.xlsx'
        },
        {
            'script': 'scripts/risk-management.py',
            'name': 'Risk Management',
            'description': 'Quản lý rủi ro và Value at Risk',
            'output': 'Risk_Analysis.xlsx'
        }
    ]
    
    print(f"\n📋 DANH SÁCH PHÂN TÍCH SẼ THỰC HIỆN:")
    for i, analysis in enumerate(advanced_analyses, 1):
        print(f"  {i}. {analysis['name']} - {analysis['description']}")
    
    # Thực hiện từng phân tích
    success_count = 0
    completed_analyses = []
    
    for analysis in advanced_analyses:
        script_path = analysis['script']
        
        if os.path.exists(script_path):
            print(f"\n{'='*20} {analysis['name'].upper()} {'='*20}")
            
            if run_script(script_path, analysis['name']):
                success_count += 1
                completed_analyses.append(analysis)
            else:
                print(f"⚠️ Bỏ qua {analysis['name']} do lỗi")
        else:
            print(f"❌ Không tìm thấy script: {script_path}")
    
    # Tổng kết kết quả
    print("\n" + "=" * 80)
    print("📊 KẾT QUẢ PHÂN TÍCH NÂNG CAO")
    print("=" * 80)
    
    print(f"✅ Hoàn thành: {success_count}/{len(advanced_analyses)} phân tích")
    
    if success_count > 0:
        print(f"\n🎉 PHÂN TÍCH THÀNH CÔNG!")
        
        print(f"\n📁 CÁC FILE KẾT QUẢ:")
        
        # Kiểm tra các file output
        output_files = []
        
        for analysis in completed_analyses:
            output_pattern = analysis['output']
            
            if '*' in output_pattern:
                # Tìm files matching pattern
                import glob
                matching_files = glob.glob(output_pattern)
                for file in matching_files:
                    if os.path.exists(file):
                        output_files.append(f"📊 {file} - {analysis['name']}")
            else:
                if os.path.exists(output_pattern):
                    output_files.append(f"📊 {output_pattern} - {analysis['name']}")
        
        # Hiển thị files
        for file_info in output_files:
            print(f"  {file_info}")
        
        # Tổng kết insights
        print(f"\n🔍 INSIGHTS CHÍNH:")
        print("-" * 50)
        
        insights = []
        
        # Portfolio Optimization insights
        if os.path.exists('Portfolio_Analysis.xlsx'):
            insights.append("📈 Tối ưu hóa danh mục: Xem tỷ trọng tối ưu trong Portfolio_Analysis.xlsx")
        
        # Sector Analysis insights
        if os.path.exists('Sector_Analysis.xlsx'):
            insights.append("🏭 Phân tích ngành: So sánh hiệu suất các ngành trong Sector_Analysis.xlsx")
        
        # Technical Analysis insights
        technical_files = [f for f in os.listdir('.') if f.startswith('Technical_Analysis_') and f.endswith('.xlsx')]
        if technical_files:
            insights.append(f"📊 Phân tích kỹ thuật: {len(technical_files)} file với chỉ báo chi tiết")
        
        # Risk Management insights
        if os.path.exists('Risk_Analysis.xlsx'):
            insights.append("⚠️ Quản lý rủi ro: VaR và stress testing trong Risk_Analysis.xlsx")
        
        for insight in insights:
            print(f"  {insight}")
        
        print(f"\n💡 HƯỚNG DẪN SỬ DỤNG:")
        print("-" * 50)
        print("1. 📊 Mở các file Excel để xem phân tích chi tiết")
        print("2. 📈 Sử dụng kết quả Portfolio Optimization để điều chỉnh tỷ trọng")
        print("3. 🏭 Tham khảo Sector Analysis để chọn ngành đầu tư")
        print("4. 📊 Theo dõi Technical Analysis để timing entry/exit")
        print("5. ⚠️ Áp dụng Risk Management để kiểm soát rủi ro")
        
        print(f"\n🔄 CẬP NHẬT DỮ LIỆU:")
        print("-" * 50)
        print("• Chạy lại script này hàng tuần để cập nhật phân tích")
        print("• Theo dõi thay đổi trong risk metrics")
        print("• Điều chỉnh portfolio dựa trên kết quả mới")
        
        print(f"\n🚀 MỞ RỘNG THÊM:")
        print("-" * 50)
        print("• Thêm nhiều cổ phiếu vào danh sách phân tích")
        print("• Tích hợp với Power BI để tạo dashboard real-time")
        print("• Thiết lập alerts cho risk thresholds")
        print("• Backtest các chiến lược đầu tư")
        
    else:
        print(f"\n⚠️ Không có phân tích nào hoàn thành thành công.")
        print("Vui lòng kiểm tra:")
        print("• Dữ liệu cơ bản đã được thu thập chưa")
        print("• Các package Python cần thiết đã cài đặt chưa")
        print("• Kết nối internet để tải dữ liệu")
    
    print(f"\n⏰ Thời gian kết thúc: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    main()