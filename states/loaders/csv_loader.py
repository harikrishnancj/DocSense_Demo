from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
from llama_index.core import Document


def load_csv(path: str, filename: str, artifacts: Dict[str, List[Any]] | None = None) -> List[Document]:
    try:
        df = pd.read_csv(path)
        txt = df.to_string()
        # Add table to artifacts for visualization
        if artifacts is not None and not df.empty:
            artifacts["extracted_tables"].append({
                "data": df.to_dict(orient='records'),
                "columns": df.columns.tolist(),
                "source": filename,
                "type": "csv"
            })
        return [Document(text=txt, metadata={"filename": filename, "type": "csv"})]
    except Exception as e:
        print(f"Failed to load CSV {filename}: {e}")
        return []
