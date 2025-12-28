"""
Advanced Technical Analysis với nhiều chỉ báo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class AdvancedTechnicalAnalyzer:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        
    def load_data(self):
        """Load price data"""
        try:
            self.data = pd.read_excel(f'data/{self.symbol}_price_data.xlsx', index_col=0)
            return True
        except Exception as e:
            print(f"Không thể load dữ liệu cho {self.symbol}: {e}")
            return False
    
    def calculate_sma(self, period):
        """Simple Moving Average"""
        return self.data['Close'].rolling(window=period).mean()
    
    def calculate_ema(self, period):
        """Exponential Moving Average"""
        return self.data['Close'].ewm(span=period).mean()
    
    def calculate_bollinger_bands(self, period=20, std_dev=2):
        """Bollinger Bands"""
        sma = self.calculate_sma(period)
        std = self.data['Close'].rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        return upper_band, sma, lower_band
    
    def calculate_rsi(self, period=14):
        """Relative Strength Index"""
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, fast=12, slow=26, signal=9):
        """MACD (Moving Average Convergence Divergence)"""
        ema_fast = self.calculate_ema(fast)
        ema_slow = self.calculate_ema(slow)
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def calculate_stochastic(self, k_period=14, d_period=3):
        """Stochastic Oscillator"""
        low_min = self.data['Low'].rolling(window=k_period).min()
        high_max = self.data['High'].rolling(window=k_period).max()
        
        k_percent = 100 * ((self.data['Close'] - low_min) / (high_max - low_min))
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return k_percent, d_percent
    
    def calculate_williams_r(self, period=14):
        """Williams %R"""
        high_max = self.data['High'].rolling(window=period).max()
        low_min = self.data['Low'].rolling(window=period).min()
        
        williams_r = -100 * ((high_max - self.data['Close']) / (high_max - low_min))
        return williams_r
    
    def calculate_atr(self, period=14):
        """Average True Range"""
        high_low = self.data['High'] - self.data['Low']
        high_close = np.abs(self.data['High'] - self.data['Close'].shift())
        low_close = np.abs(self.data['Low'] - self.data['Close'].shift())
        
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(window=period).mean()
        
        return atr
    
    def calculate_adx(self, period=14):
        """Average Directional Index"""
        high_diff = self.data['High'].diff()
        low_diff = -self.data['Low'].diff()
        
        plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
        minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)
        
        atr = self.calculate_atr(period)
        
        plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).mean() / atr)
        minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).mean() / atr)
        
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        
        return adx, plus_di, minus_di
    
    def calculate_obv(self):
        """On-Balance Volume"""
        obv = []
        obv_value = 0
        
        for i in range(len(self.data)):
            if i == 0:
                obv.append(self.data['Volume'].iloc[i])
            else:
                if self.data['Close'].iloc[i] > self.data['Close'].iloc[i-1]:
                    obv_value += self.data['Volume'].iloc[i]
                elif self.data['Close'].iloc[i] < self.data['Close'].iloc[i-1]:
                    obv_value -= self.data['Volume'].iloc[i]
                obv.append(obv_value)
        
        return pd.Series(obv, index=self.data.index)
    
    def identify_patterns(self):
        """Identify chart patterns"""
        patterns = []
        
        # Calculate moving averages
        ma20 = self.calculate_sma(20)
        ma50 = self.calculate_sma(50)
        ma200 = self.calculate_sma(200)
        
        current_price = self.data['Close'].iloc[-1]
        
        # Golden Cross
        if (ma20.iloc[-1] > ma50.iloc[-1] and 
            ma20.iloc[-2] <= ma50.iloc[-2]):
            patterns.append("🟡 Golden Cross (MA20 > MA50)")
        
        # Death Cross
        if (ma20.iloc[-1] < ma50.iloc[-1] and 
            ma20.iloc[-2] >= ma50.iloc[-2]):
            patterns.append("🔴 Death Cross (MA20 < MA50)")
        
        # Price above/below key MAs
        if current_price > ma200.iloc[-1]:
            patterns.append("🟢 Giá trên MA200 (Bullish)")
        else:
            patterns.append("🔴 Giá dưới MA200 (Bearish)")
        
        # Bollinger Bands squeeze
        upper_bb, middle_bb, lower_bb = self.calculate_bollinger_bands()
        bb_width = (upper_bb - lower_bb) / middle_bb
        
        if bb_width.iloc[-1] < bb_width.rolling(20).mean().iloc[-1] * 0.8:
            patterns.append("⚡ Bollinger Bands Squeeze")
        
        # RSI conditions
        rsi = self.calculate_rsi()
        if rsi.iloc[-1] > 70:
            patterns.append("⚠️ RSI Overbought (>70)")
        elif rsi.iloc[-1] < 30:
            patterns.append("💡 RSI Oversold (<30)")
        
        return patterns
    
    def generate_signals(self):
        """Generate trading signals"""
        signals = []
        
        # Calculate indicators
        rsi = self.calculate_rsi()
        macd_line, signal_line, histogram = self.calculate_macd()
        k_percent, d_percent = self.calculate_stochastic()
        williams_r = self.calculate_williams_r()
        
        # RSI Signals
        if rsi.iloc[-1] < 30 and rsi.iloc[-2] >= 30:
            signals.append("🟢 BUY: RSI từ oversold")
        elif rsi.iloc[-1] > 70 and rsi.iloc[-2] <= 70:
            signals.append("🔴 SELL: RSI vào overbought")
        
        # MACD Signals
        if (macd_line.iloc[-1] > signal_line.iloc[-1] and 
            macd_line.iloc[-2] <= signal_line.iloc[-2]):
            signals.append("🟢 BUY: MACD Bullish Crossover")
        elif (macd_line.iloc[-1] < signal_line.iloc[-1] and 
              macd_line.iloc[-2] >= signal_line.iloc[-2]):
            signals.append("🔴 SELL: MACD Bearish Crossover")
        
        # Stochastic Signals
        if (k_percent.iloc[-1] > d_percent.iloc[-1] and 
            k_percent.iloc[-2] <= d_percent.iloc[-2] and 
            k_percent.iloc[-1] < 20):
            signals.append("🟢 BUY: Stochastic Bullish từ oversold")
        
        # Williams %R Signals
        if williams_r.iloc[-1] > -20:
            signals.append("⚠️ CAUTION: Williams %R overbought")
        elif williams_r.iloc[-1] < -80:
            signals.append("💡 OPPORTUNITY: Williams %R oversold")
        
        return signals
    
    def calculate_support_resistance(self):
        """Calculate support and resistance levels"""
        # Pivot Points
        high = self.data['High'].iloc[-1]
        low = self.data['Low'].iloc[-1]
        close = self.data['Close'].iloc[-1]
        
        pivot = (high + low + close) / 3
        
        # Support and Resistance levels
        r1 = 2 * pivot - low
        s1 = 2 * pivot - high
        r2 = pivot + (high - low)
        s2 = pivot - (high - low)
        r3 = high + 2 * (pivot - low)
        s3 = low - 2 * (high - pivot)
        
        return {
            'Pivot': pivot,
            'R1': r1, 'R2': r2, 'R3': r3,
            'S1': s1, 'S2': s2, 'S3': s3
        }
    
    def generate_comprehensive_report(self):
        """Generate comprehensive technical analysis report"""
        if not self.load_data():
            return
        
        print("=" * 80)
        print(f"📊 ADVANCED TECHNICAL ANALYSIS - {self.symbol}")
        print("=" * 80)
        
        current_price = self.data['Close'].iloc[-1]
        print(f"💰 Giá hiện tại: ${current_price:.2f}")
        print(f"📅 Dữ liệu từ: {self.data.index[0].strftime('%d/%m/%Y')} đến {self.data.index[-1].strftime('%d/%m/%Y')}")
        
        # Moving Averages
        print(f"\n📈 MOVING AVERAGES:")
        print("-" * 40)
        
        ma_periods = [5, 10, 20, 50, 100, 200]
        for period in ma_periods:
            if len(self.data) >= period:
                ma = self.calculate_sma(period)
                ma_value = ma.iloc[-1]
                trend = "🟢" if current_price > ma_value else "🔴"
                print(f"MA{period:3d}: ${ma_value:7.2f} {trend}")
        
        # Technical Indicators
        print(f"\n⚡ TECHNICAL INDICATORS:")
        print("-" * 40)
        
        # RSI
        rsi = self.calculate_rsi()
        rsi_status = "Overbought" if rsi.iloc[-1] > 70 else "Oversold" if rsi.iloc[-1] < 30 else "Neutral"
        print(f"RSI (14):     {rsi.iloc[-1]:6.1f} ({rsi_status})")
        
        # MACD
        macd_line, signal_line, histogram = self.calculate_macd()
        macd_trend = "Bullish" if macd_line.iloc[-1] > signal_line.iloc[-1] else "Bearish"
        print(f"MACD:         {macd_line.iloc[-1]:6.3f} ({macd_trend})")
        print(f"MACD Signal:  {signal_line.iloc[-1]:6.3f}")
        print(f"MACD Hist:    {histogram.iloc[-1]:6.3f}")
        
        # Stochastic
        k_percent, d_percent = self.calculate_stochastic()
        stoch_status = "Overbought" if k_percent.iloc[-1] > 80 else "Oversold" if k_percent.iloc[-1] < 20 else "Neutral"
        print(f"Stoch %K:     {k_percent.iloc[-1]:6.1f} ({stoch_status})")
        print(f"Stoch %D:     {d_percent.iloc[-1]:6.1f}")
        
        # Williams %R
        williams_r = self.calculate_williams_r()
        williams_status = "Overbought" if williams_r.iloc[-1] > -20 else "Oversold" if williams_r.iloc[-1] < -80 else "Neutral"
        print(f"Williams %R:  {williams_r.iloc[-1]:6.1f} ({williams_status})")
        
        # ATR
        atr = self.calculate_atr()
        print(f"ATR (14):     {atr.iloc[-1]:6.2f}")
        
        # ADX
        adx, plus_di, minus_di = self.calculate_adx()
        trend_strength = "Strong" if adx.iloc[-1] > 25 else "Weak" if adx.iloc[-1] < 20 else "Moderate"
        print(f"ADX:          {adx.iloc[-1]:6.1f} ({trend_strength} trend)")
        
        # Bollinger Bands
        print(f"\n📊 BOLLINGER BANDS:")
        print("-" * 40)
        
        upper_bb, middle_bb, lower_bb = self.calculate_bollinger_bands()
        bb_position = ((current_price - lower_bb.iloc[-1]) / 
                      (upper_bb.iloc[-1] - lower_bb.iloc[-1]) * 100)
        
        print(f"Upper Band:   ${upper_bb.iloc[-1]:7.2f}")
        print(f"Middle Band:  ${middle_bb.iloc[-1]:7.2f}")
        print(f"Lower Band:   ${lower_bb.iloc[-1]:7.2f}")
        print(f"BB Position:  {bb_position:6.1f}%")
        
        # Support and Resistance
        print(f"\n🎯 SUPPORT & RESISTANCE:")
        print("-" * 40)
        
        levels = self.calculate_support_resistance()
        for level, value in levels.items():
            print(f"{level:6}: ${value:7.2f}")
        
        # Chart Patterns
        print(f"\n📈 CHART PATTERNS:")
        print("-" * 40)
        
        patterns = self.identify_patterns()
        if patterns:
            for pattern in patterns:
                print(f"  {pattern}")
        else:
            print("  Không phát hiện pattern đặc biệt")
        
        # Trading Signals
        print(f"\n🚨 TRADING SIGNALS:")
        print("-" * 40)
        
        signals = self.generate_signals()
        if signals:
            for signal in signals:
                print(f"  {signal}")
        else:
            print("  Không có signal rõ ràng")
        
        # Overall Assessment
        print(f"\n🎯 ĐÁNH GIÁ TỔNG QUAN:")
        print("-" * 40)
        
        bullish_signals = 0
        bearish_signals = 0
        
        # Count bullish/bearish indicators
        if rsi.iloc[-1] < 50:
            bearish_signals += 1
        else:
            bullish_signals += 1
            
        if macd_line.iloc[-1] > signal_line.iloc[-1]:
            bullish_signals += 1
        else:
            bearish_signals += 1
            
        if current_price > self.calculate_sma(20).iloc[-1]:
            bullish_signals += 1
        else:
            bearish_signals += 1
        
        if bullish_signals > bearish_signals:
            overall_trend = "🟢 BULLISH"
        elif bearish_signals > bullish_signals:
            overall_trend = "🔴 BEARISH"
        else:
            overall_trend = "🟡 NEUTRAL"
        
        print(f"Xu hướng tổng quan: {overall_trend}")
        print(f"Tín hiệu tích cực: {bullish_signals}")
        print(f"Tín hiệu tiêu cực: {bearish_signals}")
        
        # Save to Excel
        self.save_technical_analysis()
        
        print(f"\n✅ Phân tích kỹ thuật hoàn tất!")
        print(f"📁 Kết quả đã lưu vào Technical_Analysis_{self.symbol}.xlsx")
    
    def save_technical_analysis(self):
        """Save technical analysis to Excel"""
        import xlsxwriter
        
        # Calculate all indicators
        indicators_data = []
        
        for i in range(len(self.data)):
            date = self.data.index[i]
            
            # Basic data
            row_data = {
                'Date': date,
                'Open': self.data['Open'].iloc[i],
                'High': self.data['High'].iloc[i],
                'Low': self.data['Low'].iloc[i],
                'Close': self.data['Close'].iloc[i],
                'Volume': self.data['Volume'].iloc[i]
            }
            
            # Moving averages
            if i >= 19:
                row_data['SMA_20'] = self.calculate_sma(20).iloc[i]
            if i >= 49:
                row_data['SMA_50'] = self.calculate_sma(50).iloc[i]
            
            # RSI
            if i >= 13:
                row_data['RSI'] = self.calculate_rsi().iloc[i]
            
            # MACD
            if i >= 25:
                macd_line, signal_line, histogram = self.calculate_macd()
                row_data['MACD'] = macd_line.iloc[i]
                row_data['MACD_Signal'] = signal_line.iloc[i]
                row_data['MACD_Histogram'] = histogram.iloc[i]
            
            # Bollinger Bands
            if i >= 19:
                upper_bb, middle_bb, lower_bb = self.calculate_bollinger_bands()
                row_data['BB_Upper'] = upper_bb.iloc[i]
                row_data['BB_Middle'] = middle_bb.iloc[i]
                row_data['BB_Lower'] = lower_bb.iloc[i]
            
            indicators_data.append(row_data)
        
        # Create DataFrame
        df = pd.DataFrame(indicators_data)
        
        # Save to Excel
        with pd.ExcelWriter(f'Technical_Analysis_{self.symbol}.xlsx', engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Technical Indicators', index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Technical Indicators']
            
            # Format
            header_format = workbook.add_format({
                'bold': True, 'fg_color': '#D7E4BC', 'border': 1
            })
            
            # Apply header format
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

def analyze_all_stocks():
    """Analyze all stocks in portfolio"""
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    print("🚀 Bắt đầu phân tích kỹ thuật cho tất cả cổ phiếu...")
    
    for symbol in symbols:
        print(f"\n{'='*20} {symbol} {'='*20}")
        analyzer = AdvancedTechnicalAnalyzer(symbol)
        analyzer.generate_comprehensive_report()
    
    print(f"\n🎉 Hoàn thành phân tích kỹ thuật cho {len(symbols)} cổ phiếu!")

if __name__ == "__main__":
    analyze_all_stocks()