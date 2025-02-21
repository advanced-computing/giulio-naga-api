import pandas as pd
from giulio_naga_api import employee_mean

df = pd.DataFrame(
    {
        "Employees": [100, 200, 300, 400, 500],
        "Total Interns": [10, 20, 30, 40, 50]
    }
)

# Test function without running the Flask app
result = employee_mean(df)
print(result)
