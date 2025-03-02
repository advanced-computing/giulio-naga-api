import pandas as pd
from giulio_naga_api import calculate_intern_max


def test_calculate_intern_max():
    df = pd.DataFrame(
        {
            "Total Interns": [10, 20, 30, 40, 50]
        }
    )

    result = calculate_intern_max(df)
    expected = 50

    assert result == expected