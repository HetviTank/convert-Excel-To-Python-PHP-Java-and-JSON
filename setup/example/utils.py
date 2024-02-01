import os
import pandas as pd

def convert_xlsx_to_json(xlsx_file):
    df = pd.read_excel(xlsx_file)
    json_content = df.to_json(orient='records')
    print(json_content)
    return json_content