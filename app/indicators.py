import pandas as pd

def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()

def crossover(fast: pd.Series, slow: pd.Series) -> pd.Series:
    return ((fast > slow) & (fast.shift(1) <= slow.shift(1))).fillna(False)

def crossunder(fast: pd.Series, slow: pd.Series) -> pd.Series:
    return ((fast < slow) & (fast.shift(1) >= slow.shift(1))).fillna(False)
