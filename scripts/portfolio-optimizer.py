"""
Portfolio Optimization và Risk Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

class PortfolioOptimizer:
    def __init__(self, symbols=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']):
        self.symbols = symbols
        self.returns_data = None
        self.mean_returns = None
        self.cov_matrix = None
        
    def load_data(self):
        """Load price data and calculate returns"""
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
            self.mean_returns = self.returns_data.mean() * 252  # Annualized
            self.cov_matrix = self.returns_data.cov() * 252    # Annualized
            return True
        return False
    
    def portfolio_performance(self, weights):
        """Calculate portfolio return and volatility"""
        portfolio_return = np.sum(self.mean_returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        return portfolio_return, portfolio_volatility
    
    def negative_sharpe_ratio(self, weights, risk_free_rate=0.02):
        """Calculate negative Sharpe ratio for optimization"""
        p_return, p_volatility = self.portfolio_performance(weights)
        return -(p_return - risk_free_rate) / p_volatility
    
    def optimize_portfolio(self, target='sharpe'):
        """Optimize portfolio based on different objectives"""
        num_assets = len(self.symbols)
        
        # Constraints
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(num_assets))
        
        # Initial guess (equal weights)
        initial_guess = np.array([1/num_assets] * num_assets)
        
        if target == 'sharpe':
            # Maximize Sharpe Ratio
            result = minimize(self.negative_sharpe_ratio, initial_guess,
                            method='SLSQP', bounds=bounds, constraints=constraints)
        elif target == 'min_vol':
            # Minimize Volatility
            def portfolio_volatility(weights):
                return self.portfolio_performance(weights)[1]
            
            result = minimize(portfolio_volatility, initial_guess,
                            method='SLSQP', bounds=bounds, constraints=constraints)
        
        return result.x if result.success else None
    
    def efficient_frontier(self, num_portfolios=100):
        """Generate efficient frontier"""
        results = np.zeros((3, num_portfolios))
        
        # Define target returns
        min_ret = self.mean_returns.min()
        max_ret = self.mean_returns.max()
        target_returns = np.linspace(min_ret, max_ret, num_portfolios)
        
        num_assets = len(self.symbols)
        
        for i, target in enumerate(target_returns):
            # Constraints
            constraints = (
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: np.sum(self.mean_returns * x) - target}
            )
            bounds = tuple((0, 1) for _ in range(num_assets))
            
            # Minimize volatility for target return
            def portfolio_volatility(weights):
                return self.portfolio_performance(weights)[1]
            
            initial_guess = np.array([1/num_assets] * num_assets)
            result = minimize(portfolio_volatility, initial_guess,
                            method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                ret, vol = self.portfolio_performance(result.x)
                results[0, i] = ret
                results[1, i] = vol
                results[2, i] = (ret - 0.02) / vol  # Sharpe ratio
        
        return results
    
    def monte_carlo_simulation(self, num_simulations=10000):
        """Monte Carlo simulation for portfolio optimization"""
        num_assets = len(self.symbols)
        results = np.zeros((3, num_simulations))
        
        for i in range(num_simulations):
            # Random weights
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            
            # Calculate performance
            ret, vol = self.portfolio_performance(weights)
            sharpe = (ret - 0.02) / vol
            
            results[0, i] = ret
            results[1, i] = vol
            results[2, i] = sharpe
        
        return results
    
    def generate_report(self):
        """Generate comprehensive portfolio analysis report"""
        if not self.load_data():
            print("Không thể load dữ liệu!")
            return
        
        print("=" * 80)
        print("📊 PORTFOLIO OPTIMIZATION ANALYSIS")
        print("=" * 80)
        
        # Individual asset analysis
        print("\n📈 PHÂN TÍCH CÁC TÀI SẢN:")
        print("-" * 50)
        for symbol in self.symbols:
            annual_return = self.mean_returns[symbol]
            annual_vol = np.sqrt(self.cov_matrix.loc[symbol, symbol])
            sharpe = (annual_return - 0.02) / annual_vol
            
            print(f"{symbol:6} | Return: {annual_return:6.2%} | Vol: {annual_vol:6.2%} | Sharpe: {sharpe:5.2f}")
        
        # Optimal portfolios
        print(f"\n🎯 PORTFOLIO TỐI ƯU:")
        print("-" * 50)
        
        # Maximum Sharpe Ratio Portfolio
        max_sharpe_weights = self.optimize_portfolio('sharpe')
        if max_sharpe_weights is not None:
            ret, vol = self.portfolio_performance(max_sharpe_weights)
            sharpe = (ret - 0.02) / vol
            
            print(f"\n🏆 Maximum Sharpe Ratio Portfolio:")
            print(f"   Expected Return: {ret:.2%}")
            print(f"   Volatility: {vol:.2%}")
            print(f"   Sharpe Ratio: {sharpe:.3f}")
            print(f"   Weights:")
            for i, symbol in enumerate(self.symbols):
                print(f"     {symbol}: {max_sharpe_weights[i]:.1%}")
        
        # Minimum Volatility Portfolio
        min_vol_weights = self.optimize_portfolio('min_vol')
        if min_vol_weights is not None:
            ret, vol = self.portfolio_performance(min_vol_weights)
            sharpe = (ret - 0.02) / vol
            
            print(f"\n🛡️ Minimum Volatility Portfolio:")
            print(f"   Expected Return: {ret:.2%}")
            print(f"   Volatility: {vol:.2%}")
            print(f"   Sharpe Ratio: {sharpe:.3f}")
            print(f"   Weights:")
            for i, symbol in enumerate(self.symbols):
                print(f"     {symbol}: {min_vol_weights[i]:.1%}")
        
        # Equal Weight Portfolio
        equal_weights = np.array([1/len(self.symbols)] * len(self.symbols))
        ret, vol = self.portfolio_performance(equal_weights)
        sharpe = (ret - 0.02) / vol
        
        print(f"\n⚖️ Equal Weight Portfolio:")
        print(f"   Expected Return: {ret:.2%}")
        print(f"   Volatility: {vol:.2%}")
        print(f"   Sharpe Ratio: {sharpe:.3f}")
        print(f"   Weights: {100/len(self.symbols):.1f}% each")
        
        # Correlation Matrix
        print(f"\n🔗 CORRELATION MATRIX:")
        print("-" * 50)
        corr_matrix = self.returns_data.corr()
        print(corr_matrix.round(3))
        
        # Risk Analysis
        print(f"\n⚠️ RISK ANALYSIS:")
        print("-" * 50)
        
        # VaR calculation (95% confidence)
        portfolio_returns = self.returns_data.mean(axis=1)  # Equal weight for simplicity
        var_95 = np.percentile(portfolio_returns, 5)
        var_99 = np.percentile(portfolio_returns, 1)
        
        print(f"Value at Risk (95%): {var_95:.2%}")
        print(f"Value at Risk (99%): {var_99:.2%}")
        print(f"Maximum Drawdown: {portfolio_returns.min():.2%}")
        
        # Save results to Excel
        self.save_results_to_excel(max_sharpe_weights, min_vol_weights, equal_weights)
        
        print(f"\n✅ Kết quả đã được lưu vào Portfolio_Analysis.xlsx")
    
    def save_results_to_excel(self, max_sharpe_weights, min_vol_weights, equal_weights):
        """Save portfolio analysis results to Excel"""
        import xlsxwriter
        
        workbook = xlsxwriter.Workbook('Portfolio_Analysis.xlsx')
        
        # Format
        header_format = workbook.add_format({
            'bold': True, 'fg_color': '#D7E4BC', 'border': 1
        })
        percent_format = workbook.add_format({'num_format': '0.00%'})
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        
        # Portfolio Weights Sheet
        worksheet1 = workbook.add_worksheet('Portfolio Weights')
        
        headers = ['Asset', 'Max Sharpe', 'Min Volatility', 'Equal Weight']
        for col, header in enumerate(headers):
            worksheet1.write(0, col, header, header_format)
        
        for row, symbol in enumerate(self.symbols, 1):
            worksheet1.write(row, 0, symbol)
            worksheet1.write(row, 1, max_sharpe_weights[row-1], percent_format)
            worksheet1.write(row, 2, min_vol_weights[row-1], percent_format)
            worksheet1.write(row, 3, 1/len(self.symbols), percent_format)
        
        # Performance Metrics Sheet
        worksheet2 = workbook.add_worksheet('Performance Metrics')
        
        metrics = ['Expected Return', 'Volatility', 'Sharpe Ratio']
        portfolios = ['Max Sharpe', 'Min Volatility', 'Equal Weight']
        
        # Headers
        worksheet2.write(0, 0, 'Metric', header_format)
        for col, portfolio in enumerate(portfolios, 1):
            worksheet2.write(0, col, portfolio, header_format)
        
        # Calculate metrics for each portfolio
        portfolio_weights = [max_sharpe_weights, min_vol_weights, 
                           np.array([1/len(self.symbols)] * len(self.symbols))]
        
        for row, metric in enumerate(metrics, 1):
            worksheet2.write(row, 0, metric)
            for col, weights in enumerate(portfolio_weights, 1):
                ret, vol = self.portfolio_performance(weights)
                if metric == 'Expected Return':
                    worksheet2.write(row, col, ret, percent_format)
                elif metric == 'Volatility':
                    worksheet2.write(row, col, vol, percent_format)
                elif metric == 'Sharpe Ratio':
                    sharpe = (ret - 0.02) / vol
                    worksheet2.write(row, col, sharpe, number_format)
        
        # Correlation Matrix Sheet
        worksheet3 = workbook.add_worksheet('Correlation Matrix')
        corr_matrix = self.returns_data.corr()
        
        # Headers
        worksheet3.write(0, 0, 'Asset', header_format)
        for col, symbol in enumerate(self.symbols, 1):
            worksheet3.write(0, col, symbol, header_format)
        
        # Data
        for row, symbol in enumerate(self.symbols, 1):
            worksheet3.write(row, 0, symbol, header_format)
            for col, other_symbol in enumerate(self.symbols, 1):
                corr_value = corr_matrix.loc[symbol, other_symbol]
                worksheet3.write(row, col, corr_value, number_format)
        
        workbook.close()

if __name__ == "__main__":
    optimizer = PortfolioOptimizer()
    optimizer.generate_report()