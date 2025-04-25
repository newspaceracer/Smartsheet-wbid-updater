import os
import requests
from dotenv import load_dotenv

load_dotenv()

SMARTSHEET_API_TOKEN = os.getenv("SMARTSHEET_API_TOKEN")
SHEET_ID = os.getenv("SHEET_ID")
LAT_COLUMN_NAME = os.getenv("LAT_COLUMN_NAME", "Latitude")
LON_COLUMN_NAME = os.getenv("LON_COLUMN_NAME", "Longitude")
WBID_COLUMN_NAME = os.getenv("WBID_COLUMN_NAME", "WBID")

base_url = "https://api.smartsheet.com/2.0"
headers = {
    "Authorization": f"Bearer {SMARTSHEET_API_TOKEN}",
    "Content-Type": "application/json"
}

def get_sheet():
    url = f"{base_url}/sheets/{SHEET_ID}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def get_column_map(sheet):
    return {col['title']: col['id'] for col in sheet['columns']}

def get_wbid(lat, lon):
    url = "https://ca.dep.state.fl.us/arcgis/rest/services/OpenData/WBIDS/MapServer/0/query"
    params = {
        "geometry": f"{lon},{lat}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "WBID",
        "returnGeometry": "false",
        "f": "json"
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()
    features = data.get("features", [])
    return features[0]["attributes"].get("WBID") if features else None

def update_wbid(row_id, column_id, wbid):
    url = f"{base_url}/sheets/{SHEET_ID}/rows"
    payload = [{
        "id": row_id,
        "cells": [
            {
                "columnId": column_id,
                "value": wbid
            }
        ]
    }]
    res = requests.put(url, json=payload, headers=headers)
    res.raise_for_status()
    return res.json()

def process_rows_missing_wbid():
    sheet = get_sheet()
    column_map = get_column_map(sheet)

    for row in sheet["rows"]:
        lat = lon = wbid = None

        for cell in row["cells"]:
            col_title = next((k for k, v in column_map.items() if v == cell["columnId"]), None)
            if col_title == LAT_COLUMN_NAME:
                lat = cell.get("value")
            elif col_title == LON_COLUMN_NAME:
                lon = cell.get("value")
            elif col_title == WBID_COLUMN_NAME:
                wbid = cell.get("value")

        if lat and lon and not wbid:
            print(f"Row {row['id']}: lat={lat}, lon={lon} – looking up WBID")
            new_wbid = get_wbid(lat, lon)
            if new_wbid:
                update_wbid(row["id"], column_map[WBID_COLUMN_NAME], new_wbid)
                print(f"✅ WBID updated to {new_wbid}")
            else:
                print(f"⚠️ No WBID found for lat/lon {lat}, {lon}")

if __name__ == "__main__":
    process_rows_missing_wbid()
