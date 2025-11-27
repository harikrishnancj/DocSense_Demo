# backend/states/visualizer.py
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def auto_chart_from_table(table):
    """
    Clean + simplified version of auto chart detection.
    Detects numeric and categorical columns and chooses:
    - Line     (if row count > 8 and numeric)
    - Bar      (if categorical + numeric)
    - Scatter  (if 2 numeric)
    - Histogram (if 1 numeric)
    """
    if not table or not isinstance(table, list):
        return None

    # Convert rows → columns
    columns = {}
    for row in table:
        for k, v in row.items():
            columns.setdefault(k, []).append(v)

    if len(columns) == 0:
        return None

    def is_numeric(val):
        try:
            return float(str(val).replace(",", "").replace("%", "").replace("$", "")) or True
        except:
            return False

    def clean_num(val):
        try:
            return float(str(val).replace(",", "").replace("%", "").replace("$", ""))
        except:
            return 0.0

    numeric_cols = []
    categorical_cols = []

    for col, vals in columns.items():
        if all(is_numeric(v) for v in vals if v not in ["", None]):
            numeric_cols.append(col)
        else:
            categorical_cols.append(col)

    # ----- CHART DECISIONS -----

    # 1) SCATTER → if two numeric columns
    if len(numeric_cols) >= 2:
        x, y = numeric_cols[:2]
        return {
            "type": "scatter",
            "title": f"{y} vs {x}",
            "labels": [clean_num(v) for v in columns[x]],
            "values": [clean_num(v) for v in columns[y]],
        }

    # 2) HISTOGRAM → if one numeric column only
    if len(numeric_cols) == 1 and len(categorical_cols) == 0:
        col = numeric_cols[0]
        return {
            "type": "histogram",
            "title": f"Distribution of {col}",
            "values": [clean_num(v) for v in columns[col]],
        }

    # 3) BAR → category + numeric
    if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
        cat = categorical_cols[0]
        num = numeric_cols[0]

        return {
            "type": "bar",
            "title": f"{num} by {cat}",
            "labels": columns[cat],
            "values": [clean_num(v) for v in columns[num]]
        }

    # 4) LINE → if numeric only and many rows
    if len(numeric_cols) == 1 and len(columns[numeric_cols[0]]) > 8:
        col = numeric_cols[0]
        return {
            "type": "line",
            "title": f"Trend of {col}",
            "labels": list(range(len(columns[col]))),
            "values": [clean_num(v) for v in columns[col]]
        }

    return None


def render_chart(chart, file_path):
    """Simplified chart rendering with clean matplotlib."""
    ctype = chart["type"]
    title = chart["title"]

    plt.figure(figsize=(10, 6))
    plt.title(title, fontsize=14)

    if ctype == "bar":
        labels = chart["labels"]
        values = chart["values"]
        plt.bar(labels, values)
        plt.xticks(rotation=45)

    elif ctype == "line":
        plt.plot(chart["labels"], chart["values"], marker="o")

    elif ctype == "scatter":
        plt.scatter(chart["labels"], chart["values"])

    elif ctype == "histogram":
        plt.hist(chart["values"], bins=10)

    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()


def Visualizer(state):
    """Simple & clean visualizer with auto charts and wordcloud fallback."""
    text = state.summary or state.rag_response or ""
    tables = getattr(state, "extracted_tables", [])

    os.makedirs("visuals", exist_ok=True)
    state.visuals = {"charts": []}

    # 1) Try to generate chart from tables
    for i, table in enumerate(tables, start=1):
        # Extract the actual data from the table dict structure
        table_data = table.get("data", table) if isinstance(table, dict) else table
        chart = auto_chart_from_table(table_data)
        if chart:
            file_path = f"visuals/table_chart_{i}.png"
            render_chart(chart, file_path)
            chart["file"] = file_path
            state.visuals["charts"].append(chart)

    # 2) Fallback: wordcloud
    if not state.visuals["charts"]:
        file_path = "visuals/wordcloud.png"
        wc = WordCloud(width=800, height=400).generate(text)
        plt.imshow(wc)
        plt.axis("off")
        plt.savefig(file_path)
        plt.close()

        state.visuals["charts"].append({
            "type": "wordcloud",
            "file": file_path,
        })

    return state
