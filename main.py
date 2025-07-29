import os
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
from datetime import datetime, timedelta

# Ensure the downloads folder exists before mounting
os.makedirs("downloads", exist_ok=True)

app = FastAPI()
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def serve_form():
    return """
    <html>
        <head>
            <title>Excel Agent</title>
        </head>
        <body>
            <h2>Generate Filtered Excel File</h2>
            <form action="/process" method="post">
                <label for="division">Division:</label>
                <input type="text" id="division" name="division" required><br><br>
                <label for="count">Count:</label>
                <input type="number" id="count" name="count" required><br><br>
                <input type="submit" value="Generate File">
            </form>
        </body>
    </html>
    """

@app.post("/process")
async def process_file(
    division: str = Form(...),
    count: int = Form(default=0)
):
    # Load the Excel file
    file_path = "Test_Data_Table.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")
    df.columns = df.columns.str.strip().str.lower()

    # Select only the first 16 columns
    df = df.iloc[:, :16].copy()

    # Columns to fill with topmost value
    fill_cols = ['index', 'gen_eve_subcat_id', 'job_posting_title', 'job_desc',
                 'worker_type_id', 'employee_type_id', 'country_reference']

    for col in fill_cols:
        if col in df.columns:
            df[col] = df[col].iloc[0]

    # Filter rows based on division
    filtered = df[df.apply(lambda row: row.astype(str).str.contains(division, case=False).any(), axis=1)].copy()

    # Duplicate rows if count is specified and greater than current number of rows
    if count > 0 and len(filtered) > 0 and count > len(filtered):
        multiplier = (count + len(filtered) - 1) // len(filtered)
        filtered = pd.concat([filtered] * multiplier, ignore_index=True).iloc[:count]

    # Set Availability_Date and Earliest_Hire_Date to 2 months prior to today
    past_date = "'" + (datetime.today() - timedelta(days=60)).strftime('%Y-%m-%d')
    for date_col in ['availability_date', 'earliest_hire_date']:
        if date_col in filtered.columns:
            filtered[date_col] = past_date

    # Reset Index column
    filtered['index'] = range(1, len(filtered) + 1)

    # Save the processed file
    output_filename = f"{division.lower()}_filtered.xlsx"
    output_path = os.path.join("downloads", output_filename)
    filtered.to_excel(output_path, index=False)

    # Return a download URL
    download_url = f"http://localhost:8000/downloads/{output_filename}"
    return JSONResponse(content={"download_url": download_url})
