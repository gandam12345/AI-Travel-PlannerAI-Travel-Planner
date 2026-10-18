# AI Travel Planner — Major Project

## Included
- `AI_Travel_Planner_LangGraph_Major_Project.ipynb`: Google Colab notebook (if included in this package).
- `AI_Travel_Planner_Project_Report.docx`: editable project report.
- `AI_Travel_Planner_Presentation.pptx`: presentation slides.
- `source_code/app.py`: optional Streamlit interface.
- `source_code/requirements.txt`: dependencies for the Streamlit app.

## Run the Colab notebook
1. Open Google Colab.
2. Upload the `.ipynb` notebook.
3. Run cells from top to bottom.
4. Enter a valid Groq API key only when prompted. Do not share or commit the key.

## Run the optional web app locally
1. Install Python 3.10 or newer.
2. Open a terminal in the `source_code` folder.
3. Install dependencies: `pip install -r requirements.txt`
4. Set your API key as an environment variable:
   - Windows PowerShell: `$env:GROQ_API_KEY="YOUR_KEY_HERE"`
   - macOS/Linux: `export GROQ_API_KEY="YOUR_KEY_HERE"`
5. Run: `streamlit run app.py`

If a model is unavailable, set `GROQ_MODEL` to a model currently listed in the official Groq console/docs.

## Important limitations
This is a student prototype. Generated recommendations and costs are estimates and are not live-verified. Check travel time, safety, opening hours, weather, prices, and availability with trusted sources before travelling. The app does not make bookings.
