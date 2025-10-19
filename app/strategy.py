import pandas as pd
from .indicators import sma, crossover, crossunder

def sma_crossover_signals(df: pd.DataFrame, fast: int, slow: int):
    df = df.copy()
    df['fast'] = sma(df['close'], fast)
    df['slow'] = sma(df['close'], slow)
    df['buy'] = crossover(df['fast'], df['slow'])
    df['sell'] = crossunder(df['fast'], df['slow'])
    return df
