"""
Sector Analysis và Industry Comparison
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

class SectorAnalyzer:
    def __init__(self):
        self.companies_data = None
        self.sector_performance = {}
        
    def load_data(self):
        """Load company data"""
        try:
            self.companies_data = pd.read_excel('data/all_companies_summary.xlsx')
            return True
        except Exception as e:
            print(f"Không thể load dữ liệu: {e}")
            return False
    
    def analyze_sectors(self):
        """Analyze performance by sector"""
        if not self.load_data():
            return
        
        print("=" * 80)
        print("🏭 SECTOR ANALYSIS")
        print("=" * 80)
        
        # Group by sector
        sectors = self.companies_data.groupby('Sector')
        
        print(f"\n📊 TỔNG QUAN THEO NGÀNH:")
        print("-" * 60)
        
        sector_stats = []
        
        for sector_name, sector_data in sectors:
            num_companies = len(sector_data)
            avg_market_cap = sector_data['Market_Cap'].mean()
            avg_pe = sector_data['PE_Ratio'].mean()
            avg_roe = sector_data['ROE'].mean() * 100
            avg_profit_margin = sector_data['Profit_Margin'].mean() * 100
            avg_beta = sector_data['Beta'].mean()
            
            sector_stats.append({
                'Sector': sector_name,
                'Companies': num_companies,
                'Avg_Market_Cap': avg_market_cap,
                'Avg_PE': avg_pe,
                'Avg_ROE': avg_roe,
                'Avg_Profit_Margin': avg_profit_margin,
                'Avg_Beta': avg_beta
            })
            
            print(f"\n🏢 {sector_name}")
            print(f"   Số công ty: {num_companies}")
            print(f"   Vốn hóa TB: ${avg_market_cap:,.0f}")
            print(f"   P/E TB: {avg_pe:.1f}")
            print(f"   ROE TB: {avg_roe:.1f}%")
            print(f"   Profit Margin TB: {avg_profit_margin:.1f}%")
            print(f"   Beta TB: {avg_beta:.2f}")
        
        # Sector comparison
        print(f"\n📈 SO SÁNH HIỆU SUẤT NGÀNH:")
        print("-" * 80)
        
        sector_df = pd.DataFrame(sector_stats)
        
        # Best performing sectors
        best_roe_sector = sector_df.loc[sector_df['Avg_ROE'].idxmax()]
        best_margin_sector = sector_df.loc[sector_df['Avg_Profit_Margin'].idxmax()]
        lowest_risk_sector = sector_df.loc[sector_df['Avg_Beta'].idxmin()]
        
        print(f"🏆 Ngành có ROE cao nhất: {best_roe_sector['Sector']} ({best_roe_sector['Avg_ROE']:.1f}%)")
        print(f"💰 Ngành có Profit Margin cao nhất: {best_margin_sector['Sector']} ({best_margin_sector['Avg_Profit_Margin']:.1f}%)")
        print(f"🛡️ Ngành có rủi ro thấp nhất: {lowest_risk_sector['Sector']} (Beta: {lowest_risk_sector['Avg_Beta']:.2f})")
        
        return sector_df
    
    def calculate_sector_performance(self):
        """Calculate historical performance by sector"""
        sector_returns = {}
        
        for _, company in self.companies_data.iterrows():
            symbol = company['Symbol']
            sector = company['Sector']
            
            try:
                # Load price data
                price_data = pd.read_excel(f'data/{symbol}_price_data.xlsx', index_col=0)
                
                # Calculate returns
                returns_1m = ((price_data['Close'].iloc[-1] - price_data['Close'].iloc[-22]) / 
                             price_data['Close'].iloc[-22] * 100) if len(price_data) > 22 else 0
                returns_3m = ((price_data['Close'].iloc[-1] - price_data['Close'].iloc[-66]) / 
                             price_data['Close'].iloc[-66] * 100) if len(price_data) > 66 else 0
                returns_1y = ((price_data['Close'].iloc[-1] - price_data['Close'].iloc[0]) / 
                             price_data['Close'].iloc[0] * 100)
                
                if sector not in sector_returns:
                    sector_returns[sector] = {'1M': [], '3M': [], '1Y': [], 'companies': []}
                
                sector_returns[sector]['1M'].append(returns_1m)
                sector_returns[sector]['3M'].append(returns_3m)
                sector_returns[sector]['1Y'].append(returns_1y)
                sector_returns[sector]['companies'].append(symbol)
                
            except Exception as e:
                print(f"Lỗi khi tính toán cho {symbol}: {e}")
        
        # Calculate average returns by sector
        print(f"\n📊 HIỆU SUẤT THEO THỜI GIAN:")
        print("-" * 60)
        print(f"{'Sector':<20} {'1M':<8} {'3M':<8} {'1Y':<8}")
        print("-" * 60)
        
        for sector, data in sector_returns.items():
            avg_1m = np.mean(data['1M']) if data['1M'] else 0
            avg_3m = np.mean(data['3M']) if data['3M'] else 0
            avg_1y = np.mean(data['1Y']) if data['1Y'] else 0
            
            print(f"{sector:<20} {avg_1m:>6.1f}% {avg_3m:>6.1f}% {avg_1y:>6.1f}%")
        
        return sector_returns
    
    def risk_return_analysis(self):
        """Analyze risk-return profile by sector"""
        print(f"\n⚠️ PHÂN TÍCH RỦI RO - LỢi NHUẬN:")
        print("-" * 60)
        
        risk_return_data = []
        
        for _, company in self.companies_data.iterrows():
            symbol = company['Symbol']
            sector = company['Sector']
            
            try:
                price_data = pd.read_excel(f'data/{symbol}_price_data.xlsx', index_col=0)
                daily_returns = price_data['Close'].pct_change().dropna()
                
                # Calculate metrics
                annual_return = daily_returns.mean() * 252 * 100
                annual_volatility = daily_returns.std() * np.sqrt(252) * 100
                sharpe_ratio = (annual_return - 2) / annual_volatility if annual_volatility > 0 else 0
                max_drawdown = ((price_data['Close'] / price_data['Close'].expanding().max() - 1).min()) * 100
                
                risk_return_data.append({
                    'Symbol': symbol,
                    'Sector': sector,
                    'Annual_Return': annual_return,
                    'Volatility': annual_volatility,
                    'Sharpe_Ratio': sharpe_ratio,
                    'Max_Drawdown': max_drawdown
                })
                
            except Exception as e:
                print(f"Lỗi khi phân tích {symbol}: {e}")
        
        if risk_return_data:
            risk_df = pd.DataFrame(risk_return_data)
            
            # Group by sector
            sector_risk = risk_df.groupby('Sector').agg({
                'Annual_Return': 'mean',
                'Volatility': 'mean',
                'Sharpe_Ratio': 'mean',
                'Max_Drawdown': 'mean'
            }).round(2)
            
            print(sector_risk)
            
            return risk_df
        
        return None
    
    def generate_investment_recommendations(self):
        """Generate sector-based investment recommendations"""
        print(f"\n🎯 KHUYẾN NGHỊ ĐẦU TƯ THEO NGÀNH:")
        print("-" * 60)
        
        sector_scores = {}
        
        # Score each sector based on multiple criteria
        for _, company in self.companies_data.iterrows():
            sector = company['Sector']
            
            if sector not in sector_scores:
                sector_scores[sector] = {
                    'growth_score': 0,
                    'value_score': 0,
                    'quality_score': 0,
                    'risk_score': 0,
                    'count': 0
                }
            
            # Growth Score (based on ROE)
            roe = company.get('ROE', 0) * 100
            if roe > 20:
                sector_scores[sector]['growth_score'] += 3
            elif roe > 15:
                sector_scores[sector]['growth_score'] += 2
            elif roe > 10:
                sector_scores[sector]['growth_score'] += 1
            
            # Value Score (based on P/E)
            pe = company.get('PE_Ratio', 0)
            if 0 < pe < 15:
                sector_scores[sector]['value_score'] += 3
            elif 15 <= pe < 25:
                sector_scores[sector]['value_score'] += 2
            elif 25 <= pe < 35:
                sector_scores[sector]['value_score'] += 1
            
            # Quality Score (based on Profit Margin)
            margin = company.get('Profit_Margin', 0) * 100
            if margin > 20:
                sector_scores[sector]['quality_score'] += 3
            elif margin > 15:
                sector_scores[sector]['quality_score'] += 2
            elif margin > 10:
                sector_scores[sector]['quality_score'] += 1
            
            # Risk Score (based on Beta - lower is better)
            beta = company.get('Beta', 1)
            if beta < 0.8:
                sector_scores[sector]['risk_score'] += 3
            elif beta < 1.2:
                sector_scores[sector]['risk_score'] += 2
            elif beta < 1.5:
                sector_scores[sector]['risk_score'] += 1
            
            sector_scores[sector]['count'] += 1
        
        # Calculate average scores and recommendations
        recommendations = []
        
        for sector, scores in sector_scores.items():
            count = scores['count']
            if count > 0:
                avg_growth = scores['growth_score'] / count
                avg_value = scores['value_score'] / count
                avg_quality = scores['quality_score'] / count
                avg_risk = scores['risk_score'] / count
                
                total_score = avg_growth + avg_value + avg_quality + avg_risk
                
                # Determine recommendation
                if total_score >= 8:
                    recommendation = "🟢 STRONG BUY"
                elif total_score >= 6:
                    recommendation = "🟡 BUY"
                elif total_score >= 4:
                    recommendation = "⚪ HOLD"
                else:
                    recommendation = "🔴 AVOID"
                
                recommendations.append({
                    'Sector': sector,
                    'Total_Score': total_score,
                    'Growth': avg_growth,
                    'Value': avg_value,
                    'Quality': avg_quality,
                    'Risk': avg_risk,
                    'Recommendation': recommendation
                })
        
        # Sort by total score
        recommendations.sort(key=lambda x: x['Total_Score'], reverse=True)
        
        print(f"{'Ngành':<20} {'Điểm':<6} {'Khuyến nghị':<15}")
        print("-" * 50)
        
        for rec in recommendations:
            print(f"{rec['Sector']:<20} {rec['Total_Score']:<6.1f} {rec['Recommendation']}")
        
        return recommendations
    
    def save_sector_analysis(self, sector_df, risk_df, recommendations):
        """Save sector analysis to Excel"""
        import xlsxwriter
        
        workbook = xlsxwriter.Workbook('Sector_Analysis.xlsx')
        
        # Formats
        header_format = workbook.add_format({
            'bold': True, 'fg_color': '#D7E4BC', 'border': 1
        })
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        percent_format = workbook.add_format({'num_format': '0.00%'})
        
        # Sector Overview Sheet
        worksheet1 = workbook.add_worksheet('Sector Overview')
        
        headers = ['Sector', 'Companies', 'Avg Market Cap', 'Avg P/E', 'Avg ROE', 'Avg Profit Margin', 'Avg Beta']
        for col, header in enumerate(headers):
            worksheet1.write(0, col, header, header_format)
        
        for row, (_, data) in enumerate(sector_df.iterrows(), 1):
            worksheet1.write(row, 0, data['Sector'])
            worksheet1.write(row, 1, data['Companies'])
            worksheet1.write(row, 2, data['Avg_Market_Cap'], number_format)
            worksheet1.write(row, 3, data['Avg_PE'], number_format)
            worksheet1.write(row, 4, data['Avg_ROE']/100, percent_format)
            worksheet1.write(row, 5, data['Avg_Profit_Margin']/100, percent_format)
            worksheet1.write(row, 6, data['Avg_Beta'], number_format)
        
        # Risk-Return Sheet
        if risk_df is not None:
            worksheet2 = workbook.add_worksheet('Risk Return Analysis')
            
            headers = ['Symbol', 'Sector', 'Annual Return', 'Volatility', 'Sharpe Ratio', 'Max Drawdown']
            for col, header in enumerate(headers):
                worksheet2.write(0, col, header, header_format)
            
            for row, (_, data) in enumerate(risk_df.iterrows(), 1):
                worksheet2.write(row, 0, data['Symbol'])
                worksheet2.write(row, 1, data['Sector'])
                worksheet2.write(row, 2, data['Annual_Return']/100, percent_format)
                worksheet2.write(row, 3, data['Volatility']/100, percent_format)
                worksheet2.write(row, 4, data['Sharpe_Ratio'], number_format)
                worksheet2.write(row, 5, data['Max_Drawdown']/100, percent_format)
        
        # Recommendations Sheet
        worksheet3 = workbook.add_worksheet('Recommendations')
        
        headers = ['Sector', 'Total Score', 'Growth Score', 'Value Score', 'Quality Score', 'Risk Score', 'Recommendation']
        for col, header in enumerate(headers):
            worksheet3.write(0, col, header, header_format)
        
        for row, rec in enumerate(recommendations, 1):
            worksheet3.write(row, 0, rec['Sector'])
            worksheet3.write(row, 1, rec['Total_Score'], number_format)
            worksheet3.write(row, 2, rec['Growth'], number_format)
            worksheet3.write(row, 3, rec['Value'], number_format)
            worksheet3.write(row, 4, rec['Quality'], number_format)
            worksheet3.write(row, 5, rec['Risk'], number_format)
            worksheet3.write(row, 6, rec['Recommendation'])
        
        workbook.close()
    
    def run_full_analysis(self):
        """Run complete sector analysis"""
        print("Bắt đầu phân tích ngành...")
        
        sector_df = self.analyze_sectors()
        if sector_df is None:
            return
        
        sector_performance = self.calculate_sector_performance()
        risk_df = self.risk_return_analysis()
        recommendations = self.generate_investment_recommendations()
        
        # Save results
        self.save_sector_analysis(sector_df, risk_df, recommendations)
        
        print(f"\n✅ Phân tích ngành hoàn tất!")
        print(f"📁 Kết quả đã lưu vào Sector_Analysis.xlsx")

if __name__ == "__main__":
    analyzer = SectorAnalyzer()
    analyzer.run_full_analysis()