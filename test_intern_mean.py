import pandas as pd
from giulio_naga_api import calculate_intern_mean


def test_calculate_intern_mean():
    df = pd.DataFrame(
        {
            "Total Interns": [10, 20, 30, 40, 50]
        }
    )

    result = calculate_intern_mean(df)
    expected = 30.0  # (10+20+30+40+50) / 5 = 30.0

    assert result == expected, f"Expected {expected}, but got {result}"