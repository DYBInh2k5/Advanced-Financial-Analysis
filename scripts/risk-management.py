"""
Risk Management và Value at Risk Analysis
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class RiskManager:
    def __init__(self, symbols=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']):
        self.symbols = symbols
        self.returns_data = None
        self.portfolio_value = 100000  # Default $100k portfolio
        
    def load_data(self):
        """Load returns data for all symbols"""
        returns_list = []
        
        for symbol in self.symbols:
            try:
                df = pd.read_excel(f'data/{symbol}_price_data.xlsx', index_col=0)
                returns = df['Close'].pct_change().dropna()
                returns.name = symbol
                returns_list.append(returns)
            except Exception as e:
                print(f"Không thể load dữ liệu cho {symbol}: {e}")
        
        if returns_list:
            self.returns_data = pd.concat(returns_list, axis=1).dropna()
            return True
        return False
    
    def calculate_var(self, returns, confidence_level=0.05, method='historical'):
        """Calculate Value at Risk"""
        if method == 'historical':
            # Historical VaR
            var = np.percentile(returns, confidence_level * 100)
        elif method == 'parametric':
            # Parametric VaR (assuming normal distribution)
            mean = returns.mean()
            std = returns.std()
            var = stats.norm.ppf(confidence_level, mean, std)
        elif method == 'monte_carlo':
            # Monte Carlo VaR
            mean = returns.mean()
            std = returns.std()
            simulated_returns = np.random.normal(mean, std, 10000)
            var = np.percentile(simulated_returns, confidence_level * 100)
        
        return var
    
    def calculate_cvar(self, returns, confidence_level=0.05):
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        var = self.calculate_var(returns, confidence_level, 'historical')
        cvar = returns[returns <= var].mean()
        return cvar
    
    def calculate_maximum_drawdown(self, prices):
        """Calculate Maximum Drawdown"""
        cumulative = (1 + prices.pct_change()).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        return max_drawdown, drawdown
    
    def calculate_beta(self, stock_returns, market_returns):
        """Calculate Beta coefficient"""
        covariance = np.cov(stock_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        beta = covariance / market_variance
        return beta
    
    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """Calculate Sharpe Ratio"""
        excess_returns = returns.mean() * 252 - risk_free_rate
        volatility = returns.std() * np.sqrt(252)
        sharpe = excess_returns / volatility
        return sharpe
    
    def calculate_sortino_ratio(self, returns, risk_free_rate=0.02):
        """Calculate Sortino Ratio"""
        excess_returns = returns.mean() * 252 - risk_free_rate
        downside_returns = returns[returns < 0]
        downside_deviation = downside_returns.std() * np.sqrt(252)
        sortino = excess_returns / downside_deviation if downside_deviation > 0 else 0
        return sortino
    
    def calculate_calmar_ratio(self, returns, prices):
        """Calculate Calmar Ratio"""
        annual_return = returns.mean() * 252
        max_dd, _ = self.calculate_maximum_drawdown(prices)
        calmar = annual_return / abs(max_dd) if max_dd != 0 else 0
        return calmar
    
    def stress_testing(self, returns, scenarios):
        """Perform stress testing"""
        results = {}
        
        for scenario_name, scenario_params in scenarios.items():
            if scenario_name == "market_crash":
                # Simulate market crash (30% drop)
                stressed_returns = returns - 0.30
            elif scenario_name == "high_volatility":
                # Double the volatility
                mean_return = returns.mean()
                stressed_returns = np.random.normal(mean_return, returns.std() * 2, len(returns))
            elif scenario_name == "recession":
                # Simulate recession (negative returns for extended period)
                stressed_returns = returns - 0.02  # 2% additional negative return
            elif scenario_name == "interest_rate_shock":
                # Simulate interest rate shock (affects growth stocks more)
                stressed_returns = returns * 0.8  # 20% reduction in returns
            
            # Calculate metrics for stressed scenario
            stressed_var_95 = self.calculate_var(stressed_returns, 0.05)
            stressed_var_99 = self.calculate_var(stressed_returns, 0.01)
            stressed_cvar = self.calculate_cvar(stressed_returns, 0.05)
            
            results[scenario_name] = {
                'VaR_95': stressed_var_95,
                'VaR_99': stressed_var_99,
                'CVaR': stressed_cvar,
                'Expected_Loss': stressed_var_95 * self.portfolio_value
            }
        
        return results
    
    def portfolio_risk_analysis(self, weights=None):
        """Comprehensive portfolio risk analysis"""
        if weights is None:
            # Equal weights
            weights = np.array([1/len(self.symbols)] * len(self.symbols))
        
        # Portfolio returns
        portfolio_returns = (self.returns_data * weights).sum(axis=1)
        
        # Risk metrics
        var_95_hist = self.calculate_var(portfolio_returns, 0.05, 'historical')
        var_99_hist = self.calculate_var(portfolio_returns, 0.01, 'historical')
        var_95_param = self.calculate_var(portfolio_returns, 0.05, 'parametric')
        var_95_mc = self.calculate_var(portfolio_returns, 0.05, 'monte_carlo')
        
        cvar_95 = self.calculate_cvar(portfolio_returns, 0.05)
        cvar_99 = self.calculate_cvar(portfolio_returns, 0.01)
        
        # Portfolio prices for drawdown calculation
        portfolio_prices = (1 + portfolio_returns).cumprod()
        max_dd, drawdown_series = self.calculate_maximum_drawdown(portfolio_prices)
        
        # Risk-adjusted returns
        sharpe = self.calculate_sharpe_ratio(portfolio_returns)
        sortino = self.calculate_sortino_ratio(portfolio_returns)
        calmar = self.calculate_calmar_ratio(portfolio_returns, portfolio_prices)
        
        # Volatility
        daily_vol = portfolio_returns.std()
        annual_vol = daily_vol * np.sqrt(252)
        
        return {
            'portfolio_returns': portfolio_returns,
            'var_95_hist': var_95_hist,
            'var_99_hist': var_99_hist,
            'var_95_param': var_95_param,
            'var_95_mc': var_95_mc,
            'cvar_95': cvar_95,
            'cvar_99': cvar_99,
            'max_drawdown': max_dd,
            'annual_volatility': annual_vol,
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'calmar_ratio': calmar
        }
    
    def individual_stock_risk(self):
        """Risk analysis for individual stocks"""
        results = {}
        
        for symbol in self.symbols:
            returns = self.returns_data[symbol]
            
            # Load price data for drawdown calculation
            try:
                price_data = pd.read_excel(f'data/{symbol}_price_data.xlsx', index_col=0)
                prices = price_data['Close']
            except:
                continue
            
            var_95 = self.calculate_var(returns, 0.05)
            var_99 = self.calculate_var(returns, 0.01)
            cvar_95 = self.calculate_cvar(returns, 0.05)
            
            max_dd, _ = self.calculate_maximum_drawdown(prices)
            
            sharpe = self.calculate_sharpe_ratio(returns)
            sortino = self.calculate_sortino_ratio(returns)
            calmar = self.calculate_calmar_ratio(returns, prices)
            
            annual_vol = returns.std() * np.sqrt(252)
            
            results[symbol] = {
                'VaR_95': var_95,
                'VaR_99': var_99,
                'CVaR_95': cvar_95,
                'Max_Drawdown': max_dd,
                'Annual_Volatility': annual_vol,
                'Sharpe_Ratio': sharpe,
                'Sortino_Ratio': sortino,
                'Calmar_Ratio': calmar
            }
        
        return results
    
    def generate_risk_report(self):
        """Generate comprehensive risk management report"""
        if not self.load_data():
            print("Không thể load dữ liệu!")
            return
        
        print("=" * 80)
        print("⚠️ RISK MANAGEMENT ANALYSIS")
        print("=" * 80)
        
        # Portfolio Risk Analysis
        print(f"\n📊 PORTFOLIO RISK ANALYSIS (Equal Weight):")
        print("-" * 60)
        
        portfolio_risk = self.portfolio_risk_analysis()
        
        print(f"Value at Risk (95%):      {portfolio_risk['var_95_hist']:8.2%}")
        print(f"Value at Risk (99%):      {portfolio_risk['var_99_hist']:8.2%}")
        print(f"Conditional VaR (95%):    {portfolio_risk['cvar_95']:8.2%}")
        print(f"Conditional VaR (99%):    {portfolio_risk['cvar_99']:8.2%}")
        print(f"Maximum Drawdown:         {portfolio_risk['max_drawdown']:8.2%}")
        print(f"Annual Volatility:        {portfolio_risk['annual_volatility']:8.2%}")
        
        print(f"\n📈 RISK-ADJUSTED RETURNS:")
        print("-" * 40)
        print(f"Sharpe Ratio:             {portfolio_risk['sharpe_ratio']:8.3f}")
        print(f"Sortino Ratio:            {portfolio_risk['sortino_ratio']:8.3f}")
        print(f"Calmar Ratio:             {portfolio_risk['calmar_ratio']:8.3f}")
        
        # VaR in dollar terms
        var_95_dollar = portfolio_risk['var_95_hist'] * self.portfolio_value
        var_99_dollar = portfolio_risk['var_99_hist'] * self.portfolio_value
        
        print(f"\n💰 VaR IN DOLLAR TERMS (Portfolio: ${self.portfolio_value:,}):")
        print("-" * 60)
        print(f"1-day VaR (95%):          ${var_95_dollar:,.0f}")
        print(f"1-day VaR (99%):          ${var_99_dollar:,.0f}")
        
        # Individual Stock Risk
        print(f"\n📋 INDIVIDUAL STOCK RISK ANALYSIS:")
        print("-" * 80)
        
        stock_risks = self.individual_stock_risk()
        
        print(f"{'Stock':<6} {'VaR95%':<8} {'VaR99%':<8} {'MaxDD':<8} {'Vol':<8} {'Sharpe':<8}")
        print("-" * 60)
        
        for symbol, metrics in stock_risks.items():
            print(f"{symbol:<6} {metrics['VaR_95']:>6.2%} {metrics['VaR_99']:>6.2%} "
                  f"{metrics['Max_Drawdown']:>6.2%} {metrics['Annual_Volatility']:>6.2%} "
                  f"{metrics['Sharpe_Ratio']:>6.2f}")
        
        # Stress Testing
        print(f"\n🚨 STRESS TESTING:")
        print("-" * 60)
        
        stress_scenarios = {
            "market_crash": "Market Crash (-30%)",
            "high_volatility": "High Volatility (2x)",
            "recession": "Recession Scenario",
            "interest_rate_shock": "Interest Rate Shock"
        }
        
        portfolio_returns = portfolio_risk['portfolio_returns']
        stress_results = self.stress_testing(portfolio_returns, stress_scenarios)
        
        for scenario, description in stress_scenarios.items():
            if scenario in stress_results:
                result = stress_results[scenario]
                print(f"\n{description}:")
                print(f"  VaR (95%): {result['VaR_95']:6.2%} | Loss: ${result['Expected_Loss']:,.0f}")
                print(f"  VaR (99%): {result['VaR_99']:6.2%}")
                print(f"  CVaR:      {result['CVaR']:6.2%}")
        
        # Risk Recommendations
        print(f"\n🎯 RISK MANAGEMENT RECOMMENDATIONS:")
        print("-" * 60)
        
        recommendations = []
        
        if portfolio_risk['annual_volatility'] > 0.25:
            recommendations.append("⚠️ Volatility cao (>25%) - Cân nhắc giảm position size")
        
        if abs(portfolio_risk['max_drawdown']) > 0.20:
            recommendations.append("🔴 Max Drawdown lớn (>20%) - Cần stop-loss strategy")
        
        if portfolio_risk['sharpe_ratio'] < 1.0:
            recommendations.append("📉 Sharpe Ratio thấp (<1.0) - Tối ưu hóa portfolio")
        
        if abs(var_95_dollar) > self.portfolio_value * 0.05:
            recommendations.append("💰 VaR cao (>5% portfolio) - Diversify thêm")
        
        # Correlation risk
        corr_matrix = self.returns_data.corr()
        avg_correlation = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()
        
        if avg_correlation > 0.7:
            recommendations.append("🔗 Correlation cao (>0.7) - Cần diversify sang asset class khác")
        
        if not recommendations:
            recommendations.append("✅ Portfolio có risk profile hợp lý")
        
        for rec in recommendations:
            print(f"  {rec}")
        
        # Save results
        self.save_risk_analysis(portfolio_risk, stock_risks, stress_results)
        
        print(f"\n✅ Risk analysis hoàn tất!")
        print(f"📁 Kết quả đã lưu vào Risk_Analysis.xlsx")
    
    def save_risk_analysis(self, portfolio_risk, stock_risks, stress_results):
        """Save risk analysis to Excel"""
        import xlsxwriter
        
        workbook = xlsxwriter.Workbook('Risk_Analysis.xlsx')
        
        # Formats
        header_format = workbook.add_format({
            'bold': True, 'fg_color': '#D7E4BC', 'border': 1
        })
        percent_format = workbook.add_format({'num_format': '0.00%'})
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        currency_format = workbook.add_format({'num_format': '$#,##0'})
        
        # Portfolio Risk Sheet
        worksheet1 = workbook.add_worksheet('Portfolio Risk')
        
        metrics = [
            ('VaR (95%) Historical', portfolio_risk['var_95_hist']),
            ('VaR (99%) Historical', portfolio_risk['var_99_hist']),
            ('VaR (95%) Parametric', portfolio_risk['var_95_param']),
            ('VaR (95%) Monte Carlo', portfolio_risk['var_95_mc']),
            ('CVaR (95%)', portfolio_risk['cvar_95']),
            ('CVaR (99%)', portfolio_risk['cvar_99']),
            ('Maximum Drawdown', portfolio_risk['max_drawdown']),
            ('Annual Volatility', portfolio_risk['annual_volatility']),
            ('Sharpe Ratio', portfolio_risk['sharpe_ratio']),
            ('Sortino Ratio', portfolio_risk['sortino_ratio']),
            ('Calmar Ratio', portfolio_risk['calmar_ratio'])
        ]
        
        worksheet1.write(0, 0, 'Metric', header_format)
        worksheet1.write(0, 1, 'Value', header_format)
        
        for row, (metric, value) in enumerate(metrics, 1):
            worksheet1.write(row, 0, metric)
            if 'Ratio' in metric:
                worksheet1.write(row, 1, value, number_format)
            else:
                worksheet1.write(row, 1, value, percent_format)
        
        # Individual Stock Risk Sheet
        worksheet2 = workbook.add_worksheet('Individual Stock Risk')
        
        headers = ['Symbol', 'VaR 95%', 'VaR 99%', 'CVaR 95%', 'Max Drawdown', 
                  'Annual Volatility', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio']
        
        for col, header in enumerate(headers):
            worksheet2.write(0, col, header, header_format)
        
        for row, (symbol, metrics) in enumerate(stock_risks.items(), 1):
            worksheet2.write(row, 0, symbol)
            worksheet2.write(row, 1, metrics['VaR_95'], percent_format)
            worksheet2.write(row, 2, metrics['VaR_99'], percent_format)
            worksheet2.write(row, 3, metrics['CVaR_95'], percent_format)
            worksheet2.write(row, 4, metrics['Max_Drawdown'], percent_format)
            worksheet2.write(row, 5, metrics['Annual_Volatility'], percent_format)
            worksheet2.write(row, 6, metrics['Sharpe_Ratio'], number_format)
            worksheet2.write(row, 7, metrics['Sortino_Ratio'], number_format)
            worksheet2.write(row, 8, metrics['Calmar_Ratio'], number_format)
        
        # Stress Testing Sheet
        worksheet3 = workbook.add_worksheet('Stress Testing')
        
        headers = ['Scenario', 'VaR 95%', 'VaR 99%', 'CVaR', 'Expected Loss ($)']
        
        for col, header in enumerate(headers):
            worksheet3.write(0, col, header, header_format)
        
        scenario_names = {
            "market_crash": "Market Crash",
            "high_volatility": "High Volatility",
            "recession": "Recession",
            "interest_rate_shock": "Interest Rate Shock"
        }
        
        for row, (scenario_key, result) in enumerate(stress_results.items(), 1):
            worksheet3.write(row, 0, scenario_names.get(scenario_key, scenario_key))
            worksheet3.write(row, 1, result['VaR_95'], percent_format)
            worksheet3.write(row, 2, result['VaR_99'], percent_format)
            worksheet3.write(row, 3, result['CVaR'], percent_format)
            worksheet3.write(row, 4, result['Expected_Loss'], currency_format)
        
        workbook.close()

if __name__ == "__main__":
    risk_manager = RiskManager()
    risk_manager.generate_risk_report()