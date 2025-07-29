# 🧪 Excel Test Data Generator (FastAPI + Render)

This project is a web-based tool that allows users to generate customized Excel test data files by filtering and modifying a base dataset. It is built using **FastAPI** and hosted on **Render**, with a user-friendly HTML form interface.

---

## 🚀 Live Demo

👉 Open the Excel Generator Form

---

## 📦 Features

- ✅ Uploads and processes a base Excel file (`Test_Data_Table.xlsx`)
- ✅ Filters rows based on a user-specified division
- ✅ Duplicates rows to match a desired count
- ✅ Updates date fields to 2 months ago
- ✅ Resets index values
- ✅ Returns a downloadable Excel file via a public link
- ✅ Accessible via a simple web form

---

## 🛠️ Tech Stack

| Tool        | Purpose                                                                 |
|-------------|-------------------------------------------------------------------------|
| **FastAPI** | Backend API framework for handling form submissions and file processing |
| **pandas**  | Data manipulation and Excel file handling                               |
| **openpyxl**| Excel engine used by pandas to read/write `.xlsx` files                 |
| **Render**  | Cloud platform used to host the FastAPI app                             |
| **Copilot Studio** | AI agent that guides users to the form and explains how to use it |

---

## 🧰 How It Works

1. User visits the hosted form on Render.
2. They enter:
   - A **division name** (e.g., "CAI", "CCI", "CEI")
   - A **row count** (e.g., 10)
3. The form submits a `POST` request to the FastAPI `/process` endpoint.
4. The backend:
   - Loads and filters the Excel file
   - Modifies the data as needed
   - Saves the result to a `downloads/` folder
5. A public download link is returned to the user.

---

## 📁 Project Structure

