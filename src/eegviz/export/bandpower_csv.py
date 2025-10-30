from __future__ import annotations
import pandas as pd
from typing import Sequence

def bandpower_to_csv_bytes(ch_names: Sequence[str], band_name: str, power):
    df = pd.DataFrame({"channel": list(ch_names), "band": band_name, "power": power})
    return df.to_csv(index=False).encode("utf-8")
