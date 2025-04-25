# Smartsheet WBID Updater

This script looks up Water Body ID (WBID) values for coordinates listed in a Smartsheet and updates the corresponding rows with the correct WBID.

It uses:

- Latitude and Longitude columns in a Smartsheet sheet
- A public ArcGIS REST API provided by the Florida DEP
- The Smartsheet API to read/write values

---

## 🚀 What It Does

For each row in your Smartsheet:

- If the `Latitude` and `Longitude` columns are filled
- And the `WBID` column is **blank**
- ➡️ The script sends the coordinates to the Florida ArcGIS API
- ✅ It gets the intersecting WBID and writes it back to Smartsheet

---

## 🛠 Prerequisites

- Python 3.7 or newer
- A Smartsheet API Token (get it from your [Smartsheet Account > API Access](https://app.smartsheet.com))
- Your Sheet ID and column names
- Basic comfort running a terminal command

---

## 📦 Setup Instructions

1. **Clone or download this repository**
   git clone https://github.com/YOUR-USERNAME/smartsheet-wbid-updater.git cd smartsheet-wbid-updater

2. **Create a virtual environment** (optional but recommended)
   python3 -m venv venv source venv/bin/activate

3. **Install dependencies**
   pip install -r requirements.txt

4. **Configure your settings**

- Copy the example config file:
  ```
  cp .env.example .env
  ```
- Open `.env` and add your API token, sheet ID, and column names.

---

## ▶️ Running the Script

Once everything is set up:
python smartsheet_wbid_updater.py

You’ll see messages in your terminal for each row it processes.

---

## 🧪 Example Column Setup

Your Smartsheet must include at least these columns:

| Latitude | Longitude | WBID |
| -------- | --------- | ---- |
| 30.3     | -84.8     |      |

Rows with both coordinates but no WBID will be automatically updated.

---

## ✅ What Gets Updated

Only rows with:

- A value in both `Latitude` and `Longitude`
- An empty cell in `WBID`

No other rows are touched.

---

## Other notes

- This repo includes `.gitignore` for `.env` if you initialize Git here.
