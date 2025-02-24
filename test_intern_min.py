import pandas as pd
from giulio_naga_api import calculate_intern_min


def test_calculate_intern_min():
    df = pd.DataFrame(
        {
            "Total Interns": [10, 20, 30, 40, 50]
        }
    )

    result = calculate_intern_min(df)
    expected = 10

    assert result == expected