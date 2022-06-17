from datetime import datetime

import numpy as np
from scipy.optimize import curve_fit


class Predictor:

    def __init__(self, func=None):
        self.func = func if func else Predictor.default_func

    # функция по умолчанию используемая для апроксимации влажности
    @staticmethod
    def default_func(x, a, b, c):
        return a * np.exp(-b * x) + c

    def predict(self, datetimes: list[datetime], values: list[float], futures: list[datetime]):
        t0 = min(datetimes)

        x = np.fromiter(((dt-t0).seconds for dt in datetimes), float)
        y = np.asarray(values, float)
        future_x = np.fromiter(((dt-t0).seconds for dt in futures), float)

        return self._inner_predict(x, y, future_x)

    def _inner_predict(self, x: np.ndarray, y: np.ndarray, x1: np.ndarray) -> np.ndarray:
        # scipy отказывается работать, если значения иксов будут сильно отличаться (0, 1000, 2000 ...)
        # поэтому делим все иксы на максимальное значение, что бы они стали (0, 0.1, 0.2 ...),
        coef = max(x)
        x /= coef
        x1 /= coef

        popt, _ = curve_fit(self.func, x, y)
        y1 = self.func(x1, *popt)

        return y1

    def generate_futures(self, datetimes: list[datetime], count_factory=None) -> list[datetime]:
        count: int = int(len(datetimes)/2) if not count_factory else count_factory(datetimes)

        duration = datetimes[-1]-datetimes[0]
        step = duration/len(datetimes)
        return [datetimes[-1] + step * i for i in range(count)]
