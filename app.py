"""EcoScope AI 1.0 — an evidence-first environmental research workbench.

Run: python -m streamlit run app.py
Python 3.12. All eight supplied artworks live in assets/. No key is needed
for the environmental adapters; Groq is an optional, bounded analysis agent.
See README.md and METHODS.md for coverage, attribution and scientific limits.
"""
from __future__ import annotations

import base64
import calendar
import hashlib
import html
import io
import json
import math
import os
import re
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

import folium
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from pyproj import Geod, Transformer
from requests.adapters import HTTPAdapter
from shapely.geometry import Point, Polygon, mapping, shape
from shapely.geometry.polygon import orient
from shapely.ops import transform as shape_transform, unary_union
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parent
VERSION = "1.0.0"
GEOD = Geod(ellps="WGS84")
TEAL, VIOLET, GOLD = "#5FE1C3", "#A78BFA", "#F4C97A"
COLORS = [TEAL, VIOLET, GOLD, "#76B8FF", "#F18BB8"]
MAX_SAT_KM2, MAX_SAT_PIXELS = 250.0, 600_000
SAT_COLLECTION = "sentinel-2-c1-l2a"
MODULES = ["Climate", "Air quality", "Satellite", "River outlook", "Earthquakes", "Biodiversity", "US weather alerts"]
PAGES = ["Overview", "Study & analysis", "Satellite & water", "Climate & air", "Hazards", "Ecology & field", "AI analyst", "Reports & sources"]
FIELD_COLUMNS = ["site", "date", "latitude", "longitude", "chlorophyll_ug_l", "secchi_m", "total_phosphorus_ug_l", "dissolved_oxygen_mg_l", "ph", "temperature_c", "turbidity_ntu", "notes"]
SOURCES = {
    "Climate": "https://open-meteo.com/en/docs/historical-weather-api",
    "Weather forecast": "https://open-meteo.com/en/docs",
    "Air quality": "https://open-meteo.com/en/docs/air-quality-api",
    "Satellite": "https://github.com/Element84/earth-search",
    "River outlook": "https://open-meteo.com/en/docs/flood-api",
    "Earthquakes": "https://earthquake.usgs.gov/fdsnws/event/1/",
    "Biodiversity": "https://techdocs.gbif.org/en/openapi/v1/occurrence",
    "US weather alerts": "https://www.weather.gov/documentation/services-web-api",
    "Field observations": "https://www.nalms.org/secchidipin/monitoring-methods/trophic-state-equations/",
}


class DataError(Exception):
    """A user-readable validation or provider failure."""


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def secret(name, default=""):
    try:
        return str(st.secrets.get(name, os.getenv(name, default)))
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return os.getenv(name, default)


def request_json(url, params=None, payload=None):
    """Two attempts at most; API credentials never appear in errors/logs."""
    retry = Retry(total=0 if urlparse(url).hostname == "nominatim.openstreetmap.org" else 1, connect=1, read=0, backoff_factor=0.4,
                  status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=frozenset(["GET"]), respect_retry_after_header=False)
    with requests.Session() as session:
        session.mount("https://", HTTPAdapter(max_retries=retry))
        headers = {"User-Agent": "EcoScopeAI/1.0 environmental research dashboard",
                   "Accept": "application/json"}
        try:
            response = session.request("POST" if payload is not None else "GET", url,
                                       params=params, json=payload, headers=headers,
                                       timeout=(15, 45))
            if response.status_code >= 400:
                try:
