from pathlib import Path

import pandas as pd


def save_data_to_csv(data: list[dict], file_name: str) -> None:

    file_path = Path(f"data/{file_name}.csv")
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(data)
    file_exists = file_path.exists()
    df.to_csv(file_path, index=False, mode="a", header=not file_exists)
