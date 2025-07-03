# LCSC Part Search
A database search tool for finding LCSC parts, written in python with Streamlit

![screenshot](image.png)

## Features
- Fast, responsive interface for browsing part database (tested to ~7,000,000 parts)
- Filtering by category, part number, description, etc
- Provides cost estimates by quantity, including price breaks (where known)
- Download filtered table results as xlsx files

## Demo
All values (especially prices) are provided for reference and may be outdated. Use with caution.
[Link](https://lcscpartsearchgit.streamlit.app/?embed_options=dark_theme)

## Setup
First, install requirements:
```
pip install -r requirements.txt
```
Note: this includes a custom streamlit table component: [Link](https://github.com/nhansendev/streamlit-sortable-table)

Then, run the app:
```
streamlit run main.py
```
