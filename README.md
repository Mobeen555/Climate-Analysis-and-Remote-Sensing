# EcoScope AI — deployment and user guide

EcoScope AI is a Streamlit environmental research MVP with satellite processing,
climate/weather analysis, modelled air quality, river-flow outlooks, earthquake
catalogue maps, biodiversity records, field-observation uploads and report exports.

The midnight-indigo, teal and violet interface includes all eight supplied images.
The provided satellite/GIS concept pictures are labelled as illustrations. Actual
analysis maps are generated from retrieved satellite data and show acquisition dates.

**Use the complete ZIP for deployment.** Uploading only app.py and requirements.txt
will omit the artwork and theme configuration. Missing artwork will not crash the app.

## What is included

| File / folder | Purpose |
|---|---|
| `app.py` | Complete Streamlit application, analytical functions and exports |
| `requirements.txt` | Exact dependency versions tested with Python 3.12 |
| `.streamlit/config.toml` | Dark theme and upload configuration |
| `.streamlit/secrets.toml.example` | Optional AI configuration; contains no real credentials |
| `assets/` | All eight supplied JPG images, preserved as provided |
| `examples/field_samples_template.csv` | Blank measurement template with explicit units |
| `METHODS.md` | Data sources, equations, scope and scientific limitations |
| `VALIDATION.md` | Checks performed and remaining validation limits |
| `.gitignore` | Keeps local API keys and temporary files out of GitHub |

## Deploy on Streamlit Community Cloud — step by step

### 1. Extract the ZIP

Download `EcoScope_AI_Streamlit.zip`. Right-click it in Windows and select **Extract
All**. Open the extracted `ecoscope_ai` folder. You should see `app.py`,
`requirements.txt`, `assets`, and `.streamlit`.

Do not upload the ZIP itself to Streamlit. Streamlit runs the extracted source files.

### 2. Create a GitHub repository

1. Open https://github.com and sign in.
2. Choose **New repository**.
3. Enter a name such as `ecoscope-ai`.
4. Choose public or private according to your sharing needs.
5. Click **Create repository**.

The images were supplied by the project owner. Confirm that you have the rights to
publish them before making a public repository.

### 3. Upload the extracted files

1. In your repository, choose **Add file → Upload files**. A new empty repository may
   show an **uploading an existing file** link instead.
2. Drag the contents of `ecoscope_ai` into the upload area, including the `assets`
   folder and `.streamlit` folder.
3. Commit the upload to your main branch.
4. Verify these paths in GitHub:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `assets/VvwKz.jpg` (and the other seven images)

If `.streamlit/config.toml` did not upload, choose **Add file → Create new file**, use
that exact path as the filename, and copy the configuration from the extracted file.
Do not upload a real `.streamlit/secrets.toml` file or API key.

Keep `app.py` and `requirements.txt` at the repository root. If you intentionally
upload a parent folder, use its full entrypoint path when deploying.

### 4. Create the Streamlit app

1. Open https://share.streamlit.io and sign in with GitHub.
2. Grant Streamlit access to the selected repository when requested by the service.
3. Click **Create app**.
   If asked whether you already have an app, select **Yup, I have an app**.
4. Select your repository and branch (usually `main`).
5. Set **Main file path** to `app.py`.
6. Optionally choose an available app URL/subdomain.

### 5. Choose Python 3.12

Open **Advanced settings** and select **Python 3.12**. These package pins were tested
on Python 3.12. Do not silently switch to an older Python version: geospatial wheel
compatibility can differ.

### 6. Optional: enable the AI analyst

Core analysis and PDF/HTML/Excel/GIS reports require no API key.

To enable the conversational analyst:

1. Open https://console.groq.com/keys and create your own API key.
2. In Streamlit's **Advanced settings → Secrets**, paste:

```toml
GROQ_API_KEY = "YOUR_REAL_GROQ_KEY"
GROQ_MODEL = "openai/gpt-oss-120b"
```

3. Keep the double quotes. Replace only the key value.
4. If already deployed, open **Manage app → Settings → Secrets** to add these values.

Put the key in **Streamlit secrets**, not GitHub repository secrets. GitHub secrets
are not automatically passed to a Streamlit Community Cloud app. You may also enter
a private session-only key in the AI page. Do not put keys in `app.py`.

The default model is configurable because model availability and account limits
can change. Check your Groq account's supported models if it returns a model-access
error. The app uses direct, bounded API calls; it does not require CrewAI or LiteLLM.

### 7. Deploy

Click **Deploy**. Streamlit installs the packages and starts the app. Initial
installation may take several minutes because Rasterio and the plotting libraries
are included. Open the deployment logs if installation fails.

The delivered application is ready to deploy, but has not been published to your
Streamlit or GitHub account by this package.

### 8. Run your first analysis

1. Open **Study & analysis**.
2. Keep the Rawal Lake example or search for a location.
3. Check the coordinates and visible boundary. City search is the default; enable
   the OpenStreetMap landmark option for lake/river names, or enter coordinates.
4. Select historical dates. Forecasts start today and are labelled separately.
5. For a quick connection check, select **Climate** and **Air quality** and click
   **Run environmental analysis**.
6. Add **Satellite** after the first check. Start with a small area, two or three
   scenes, and a period of one to three months. Satellite processing can take longer.
7. Open **Satellite & water**, **Climate & air**, or **Hazards** to inspect results.
8. Add **Biodiversity** to inspect a capped subset of occurrence records.
9. Enable **River outlook** only when the modelled river cell can be checked for
   the river you intend to study. It is not a reservoir-level forecast.

An unavailable module shows its error and remains unavailable. The application
does not insert demonstration numbers to make a failed analysis appear successful.

### 9. Use your own boundary

Either upload a WGS84 GeoJSON Polygon/MultiPolygon or draw a polygon/rectangle on
the setup map and click **Use the drawn boundary**. Enable **Use uploaded / drawn
boundary**. A drawn polygon defines a study region; it does not calculate an upstream
catchment. To revert to a radius, clear that checkbox.

Satellite analysis is capped at **250 km²**, **six selected scenes**, and a maximum
working grid of approximately 600,000 pixels per scene. Large boundaries should
be split into smaller studies. The full historical study can span up to ten years;
satellite runs are limited to three years. These are compute guardrails, not claims
that every date in the interval was observed.

### 10. Add water samples / citizen observations

1. Open **Ecology & field** after running an analysis.
2. Download the blank field CSV template.
3. Fill it in using decimal coordinates and `YYYY-MM-DD` dates.
4. Retain exact column names because units are part of the schema:

| Column | Meaning / unit |
|---|---|
| `site` | Sampling-site identifier |
| `date` | Observation date |
| `latitude`, `longitude` | Decimal WGS84 coordinates |
| `chlorophyll_ug_l` | Chlorophyll-a, µg/L |
| `secchi_m` | Secchi transparency depth, metres |
| `total_phosphorus_ug_l` | Total phosphorus, µg/L |
| `dissolved_oxygen_mg_l` | Dissolved oxygen, mg/L |
| `ph` | Measured pH |
| `temperature_c` | Water temperature, °C |
| `turbidity_ntu` | Measured turbidity, NTU |
| `notes` | Optional method / observation notes |

5. Leave missing measurements blank; do not replace them with zero.
6. Upload the CSV and click **Validate and attach observations**.
7. Optionally enable separate Carlson indices for appropriate lake/reservoir samples.

The app checks coordinates, dates, numeric values and basic physical bounds. Rows
outside the saved study area or period stay in an audit table and do not enter the
study analysis. Samples remain user-supplied and unverified. No data are published
to GBIF or any other external citizen-science service by the upload action.

### 11. Ask the AI analyst

Open **AI analyst**, enable the data-sharing checkbox, and ask a question such as:

- “Summarise the findings and explain the strongest limitations.”
- “What is the maximum modelled PM2.5 in the available window?”
- “Which satellite dates have usable coverage?”
- “What should I measure to validate the water-screening result?”

The optional AI receives run summaries, study coordinates and requested statistics.
It can call only evidence-reading and numeric-summary tools. It cannot execute
arbitrary code or retrieve new unapproved data. The UI shows its tool activity.
AI interpretations are downloaded separately and are not silently inserted into
the deterministic PDF report.

### 12. Download the complete report

1. Open **Reports & sources**.
2. Click **Generate report & export package**.
3. Download the **Complete ZIP**, or select PDF, HTML or Excel separately.

The complete results ZIP contains:

- `report.pdf` and a standalone `report.html` with embedded figures;
- `analysis.xlsx`, including an index and source records;
- `data/` with all returned table rows as CSV;
- `figures/` with exportable PNG maps/charts;
- `maps/study_and_observations.geojson`;
- `maps/satellite_indices.tif` when satellite analysis succeeded;
- `metadata.json` with the boundary, settings, source dates and limitations.

PDF tables preview up to 10 rows and 6 columns; HTML previews up to 20 rows.
The workbook and CSV files contain the full retrieved tables. GBIF and earthquake
API retrieval caps still apply; “full export” does not mean an uncapped catalogue.

Download before ending your browser session. The MVP has no persistent project
database. Streamlit Community Cloud can hibernate inactive apps, so it is not a
continuous monitoring service.

## Optional: run locally on your Windows computer

Install Python 3.12, open PowerShell in the extracted `ecoscope_ai` directory, and run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local address printed by Streamlit, usually http://localhost:8501.
These commands use the virtual environment directly and do not require changing
PowerShell's script execution policy.

For optional local AI access, copy `.streamlit/secrets.toml.example` to
`.streamlit/secrets.toml` and enter your key. `.gitignore` excludes that file.

## Troubleshooting

| Symptom | Action |
|---|---|
| Images are missing | Check the `assets/` folder and exact filenames/capitalisation. Upload the complete package. |
| Theme looks wrong | Verify `.streamlit/config.toml` is at the repository root, then reboot the app. |
| Package installation fails | Confirm Python 3.12 and the supplied requirements. Check the first actual error in deployment logs. |
| Satellite run is slow | Reduce the boundary, select one or two scenes, or shorten the dates. |
| No usable satellite scene | Increase the date window or scene-cloud limit; check the AOI location. Clouds, shadows and unsuitable pixels are masked. |
| SSL/certificate error on a university network | Ask IT to install the organisation's trusted CA correctly. The app honours standard CA-bundle environment variables; do not disable certificate verification. |
| No water pixels | Verify the boundary covers water. Narrow rivers, glint, cloud and classification errors can prevent screening. Do not interpret missing pixels as no water. |
| River result seems wrong | Check the returned model-cell coordinates. The coarse grid may select a different river. |
| Empty biodiversity results | Broaden dates or area. This does not establish absence of wildlife. |
| API HTTP 429 | The provider's quota was reached; wait and use fewer requests. Repeated automatic retries are limited. |
| AI HTTP 401/403 | Check your Groq key/account permissions and Streamlit secrets. |
| AI HTTP 400/404 | Check that your selected Groq model supports chat completions/tool calls and is available to the account. |
| AI HTTP 413/429 | Ask a narrower question or use fewer modules; check token/rate limits. Core analysis remains available. |
| Report generation fails | Individual tables and satellite GeoTIFF can still be downloaded. Check logs for the export error; use a smaller run if memory is exhausted. |
| Changes do not appear after uploading code | Wait for Streamlit's rebuild, then reboot from Manage app if needed. |
| Your session's results disappeared | Rerun the analysis. Add durable storage/background jobs before using this as a production monitoring system. |

## Cost and production planning

The selected core endpoints do not require paid API keys for this prototype, but
their terms, quotas and availability still apply. Open-Meteo's hosted free tier is
for non-commercial use; its data licensing and hosted-service terms are distinct.
Government or organisational deployment should review applicable service terms
and reliability requirements rather than assume unlimited free production use.

Keep Streamlit as the interface when scaling. Add durable storage, a background
job queue, authentication, provider monitoring and validated regional models.
Calibrated chlorophyll/turbidity concentrations, site-specific flood forecasts,
radar flood mapping and long-term climate scenario analysis are future extensions.
Reliable earthquake prediction is not a supported future capability.

## Official documentation

- Streamlit deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Streamlit secrets: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- Groq API: https://console.groq.com/docs/api-reference
- Open-Meteo access terms: https://open-meteo.com/en/pricing
- Earth Search: https://github.com/Element84/earth-search
- Nominatim policy: https://operations.osmfoundation.org/policies/nominatim/

See `METHODS.md` for the scientific sources and complete analytical scope.
