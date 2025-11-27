from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
from llama_index.core import Document


def load_excel(path: str, filename: str, artifacts: Dict[str, List[Any]] | None = None) -> List[Document]:
    try:
        sheets = pd.read_excel(path, sheet_name=None)
        docs: List[Document] = []
        for sheet_name, df in sheets.items():
            docs.append(
                Document(text=df.to_string(), metadata={"filename": filename, "type": "excel", "sheet": sheet_name})
            )
            # Add table to artifacts for visualization
            if artifacts is not None and not df.empty:
                artifacts["extracted_tables"].append({
                    "data": df.to_dict(orient='records'),
                    "columns": df.columns.tolist(),
                    "source": filename,
                    "sheet": sheet_name,
                    "type": "excel"
                })
        return docs
    
    except Exception as e:
        print(f"Failed to load Excel {filename}: {e}")
        return []
