import pandas as pd


def pareto_flags(
    df: pd.DataFrame, score: str = "f1_macro", cost: str = "fit_median_s"
) -> list[bool]:
    """Calcula las soluciones no dominadas en la frontera de Pareto multiobjetivo.

    Un modelo es dominado si existe otro con mayor o igual score y menor o
    igual costo, con al menos una desigualdad estricta.
    """
    flags = []
    for _, row in df.iterrows():
        dominated = (
            (df[score] >= row[score])
            & (df[cost] <= row[cost])
            & ((df[score] > row[score]) | (df[cost] < row[cost]))
        ).any()
        flags.append(not bool(dominated))
    return flags