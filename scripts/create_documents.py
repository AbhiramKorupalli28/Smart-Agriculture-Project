from pathlib import Path
import json, os, shutil
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
DOCS = ROOT / 'docs'

metrics = json.loads((OUT / 'metrics.json').read_text())
prod = pd.read_csv(ROOT / 'data/raw/crop_prediction_india.csv')
rec = pd.read_csv(ROOT / 'data/raw/crop_recommendation.csv')

# 1. Dataset Inventory Workbook
wb = Workbook()
ws = wb.active
ws.title = 'Dataset Inventory'
headers = ['Dataset', 'Source URL', 'Access status', 'File size (bytes)', 'Rows', 'Columns', 'Formats', 'License / terms', 'Key attributes', 'Use in project']
rows = [
    ['CATCrops', 'https://www.kaggle.com/datasets/irtaremotesensing/catcrops-dataset', 'Investigated; download requires Kaggle access', 32490000000, 'Reported 332k files', 'Reported 5.64m columns', 'CSV, HDF5, Shapefile', 'Kaggle page exposes metadata; verify terms at download', 'Sentinel-2 L2A parcel time series, parcel boundaries, ancillary metadata', 'Primary satellite source and future distributed ingestion'],
    ['Indian crop prediction', 'https://github.com/AbhishekKandoi/Crop-Yield-Prediction-based-on-Indian-Agriculture', 'Downloaded and executed', os.path.getsize(ROOT / 'data/raw/crop_prediction_india.csv'), len(prod), len(prod.columns), 'CSV', 'Repository-published public source; retain attribution', 'State, district, year, season, crop, temperature, humidity, soil moisture, area, production', 'Yield regression, regional/weather analysis'],
    ['Crop recommendation', 'https://github.com/AbhishekKandoi/Crop-Yield-Prediction-based-on-Indian-Agriculture', 'Downloaded and executed', os.path.getsize(ROOT / 'data/raw/crop_recommendation.csv'), len(rec), len(rec.columns), 'CSV', 'Repository-published public source; retain attribution', 'N, P, K, temperature, humidity, pH, rainfall, crop label', 'K-Means and Random Forest classification'],
    ['Cornell/ICRISAT district database', 'https://tci.cornell.edu/?projects=district-level-database-for-indian-agriculture-and-allied-sectors', 'Investigated; external acquisition', 'N/A', '11m+ data points reported', '1,030 variables reported', 'Multiple downloadable datasets', 'Open-access project portal; check file-specific terms', '571 districts, 20 states, 1966–2020', 'Supplementary district-scale historical data'],
    ['DES APY reports', 'https://data.desagri.gov.in/website/crops-apy-report-web', 'Investigated; official portal', 'N/A', 'Portal-dependent', 'Portal-dependent', 'Web reports / downloads', 'Government of India portal', 'Area, production, yield by crop and year', 'Authoritative validation source'],
    ['FAOSTAT', 'https://www.fao.org/faostat/en/', 'Investigated; official portal', 'N/A', 'Portal-dependent', 'Portal-dependent', 'Bulk downloads / API', 'FAO terms; verify at download', 'International crop production statistics', 'Cross-country benchmark']
]
ws.append(headers)
for r in rows:
    ws.append(r)
for cell in ws[1]:
    cell.font = Font(bold=True, color='FFFFFF')
    cell.fill = PatternFill('solid', fgColor='2F7D32')
    cell.alignment = Alignment(wrap_text=True)

col_widths = {'A': 24, 'B': 52, 'C': 34, 'D': 18, 'E': 22, 'F': 18, 'G': 20, 'H': 32, 'I': 52, 'J': 42}
for col, width in col_widths.items():
    ws.column_dimensions[col].width = width
ws.freeze_panes = 'A2'
ws.auto_filter.ref = ws.dimensions

ws2 = wb.create_sheet('Executed Metrics')
ws2.append(['Experiment', 'Metric', 'Value', 'Notes'])
for exp, vals in [('K-Means', metrics['kmeans']), ('Random Forest', metrics['random_forest']), ('Yield regression', metrics['yield_regression'])]:
    for k, v in vals.items():
        if k not in ['confusion_matrix', 'classes', 'features', 'cluster_sizes']:
            ws2.append([exp, k, str(v), 'Computed on held-out/local run'])
for cell in ws2[1]:
    cell.font = Font(bold=True, color='FFFFFF')
    cell.fill = PatternFill('solid', fgColor='2F7D32')
for c in 'ABCD':
    ws2.column_dimensions[c].width = {'A': 20, 'B': 26, 'C': 24, 'D': 30}[c]
wb.save(ROOT / 'Dataset_Inventory.xlsx')

# 2. Academic Case Study Report
D = Document()
sec = D.sections[0]
sec.top_margin = Inches(0.75)
sec.bottom_margin = Inches(0.7)
sec.left_margin = Inches(0.85)
sec.right_margin = Inches(0.85)

styles = D.styles
styles['Normal'].font.name = 'Calibri'
styles['Normal'].font.size = Pt(11)
styles['Normal'].font.color.rgb = RGBColor(30, 41, 59)

for s in ['Heading 1', 'Heading 2', 'Heading 3']:
    styles[s].font.name = 'Calibri'
    styles[s].font.color.rgb = RGBColor(31, 91, 36)
styles['Heading 1'].font.size = Pt(17)
styles['Heading 2'].font.size = Pt(13.5)
styles['Heading 3'].font.size = Pt(12)

def p(text='', bold=False, align=None):
    q = D.add_paragraph()
    r = q.add_run(text)
    r.bold = bold
    if align is not None:
        q.alignment = align
    q.paragraph_format.space_after = Pt(4)
    q.paragraph_format.line_spacing = 1.15
    return q

def h(text, level=1):
    heading = D.add_heading(text, level=level)
    heading.paragraph_format.space_before = Pt(12)
    heading.paragraph_format.space_after = Pt(4)
    return heading

def page():
    D.add_page_break()

def table(headers, data):
    t = D.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    for i, x in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = str(x)
        p_cell = cell.paragraphs[0]
        p_cell.runs[0].bold = True
    for row in data:
        cells = t.add_row().cells
        for i, x in enumerate(row):
            cells[i].text = str(x)
    return t

# --- Cover Page ---
p('SMART AGRICULTURE DATA ANALYTICS PLATFORM', True, WD_ALIGN_PARAGRAPH.CENTER)
p('(Big Data Analytics Case Study: PySpark Distributed Ingestion, Machine Learning, and Interactive Dashboard)', False, WD_ALIGN_PARAGRAPH.CENTER)
p('\nReport submitted for the degree of\nBACHELOR OF TECHNOLOGY\nIN\nCOMPUTER SCIENCE ENGINEERING (AI & ML)\n', False, WD_ALIGN_PARAGRAPH.CENTER)
p('Submitted by\nKORUPALLI LIKITH SRI SAI ABHIRAM (A23126552281)\n', True, WD_ALIGN_PARAGRAPH.CENTER)
p('DEPARTMENT OF CSE (AI & ML)\nANIL NEERUKONDA INSTITUTE OF TECHNOLOGY AND SCIENCES\n(UGC AUTONOMOUS)\n(Affiliated to Andhra University, Approved by AICTE, Accredited by NBA & NAAC A+)\nSANGIVALASA, VISAKHAPATNAM – 531162\n2023-2027\n', False, WD_ALIGN_PARAGRAPH.CENTER)

D.add_picture(str(ROOT / 'Architecture_Diagram.png'), width=Inches(6.2))
p('Figure 1. End-to-end architecture for the proposed platform.', False, WD_ALIGN_PARAGRAPH.CENTER)
page()

# --- Bonafide Certificate & Acknowledgement ---
h('BONAFIDE CERTIFICATE')
p('This is to certify that this Case Study Report titled “Smart Agriculture Data Analytics Platform” is the bonafide work of KORUPALLI LIKITH SRI SAI ABHIRAM (A23126552281) of Department of CSE (AI & ML), Anil Neerukonda Institute of Technology and Sciences (ANITS), carried out as part of the curriculum requirements in Big Data Analytics.')

h('ACKNOWLEDGEMENT')
p('I express my sincere gratitude to the faculty and mentors of the Department of Computer Science & Engineering (AI & ML) at ANITS for their continuous guidance and encouragement. I also acknowledge the creators of the open-source agricultural datasets, the maintainers of Apache Spark, scikit-learn, Streamlit, and GitHub for providing the software and tools essential for the implementation of this work.')

h('ABSTRACT')
p('This case study presents a smart agriculture analytics platform combining crop production, soil nutrients, weather variables, and distributed Big Data transformations. The implementation ingests curated tables into Parquet format, executes PySpark jobs for distributed aggregations and K-Means feature scaling, and trains Random Forest classification and yield regression models. A local validation run utilized 49,999 raw Indian crop-production records (49,784 regression-eligible after cleaning) and 2,200 soil/weather recommendation records. Random Forest achieved 0.993 accuracy and 0.993 weighted F1 score on held-out evaluation. The PySpark distributed pipeline aggregated 49,784 seasonal records and fitted 5 spatial clusters in local multi-core mode. An interactive Streamlit dashboard enables exploration of agricultural KPIs, weather patterns, clustering, and dynamic crop predictions.')

h('1. Introduction')
p('Agricultural decisions are influenced by heterogeneous observations: crop and production records, soil nutrients, weather variables, remote sensing, irrigation, and geography. These sources differ in scale, format, frequency, and uncertainty. A Big Data architecture separates durable raw storage from distributed transformation and model-serving layers.')

h('2. Problem Statement')
p('Traditional single-node tabular analyses struggle with high-volume data streams and cross-source joins. The project addresses the problem of designing a reproducible platform that ingests agricultural data, processes it with PySpark, identifies soil/weather clusters, classifies crop suitability with machine learning, and exposes interactive insights through a web dashboard.')

h('3. Objectives')
for x in [
    'Create a source-traceable ingestion and dataset inventory process.',
    'Represent raw and curated agricultural data in Parquet format.',
    'Implement distributed preprocessing with PySpark and Spark MLlib.',
    'Perform K-Means clustering, Random Forest classification, and yield regression.',
    'Provide a responsive, high-contrast Streamlit & Plotly dashboard with theme modes.',
    'Document distributed architecture and execution results with full reproducibility.'
]:
    D.add_paragraph(x, style='List Bullet')

h('4. Existing System')
p('Existing agricultural analytics workflows commonly rely on isolated notebooks, manual downloads, or single-machine scripts. They produce standalone models but lack durable raw-zone storage, data lineage, repeatable distributed transformations, and an integrated user interface.')

h('5. Proposed System')
p('The proposed system uses a layered Big Data design: source files enter a raw zone; Spark reads raw datasets to perform schema normalization, feature creation, and columnar Parquet writing; machine learning models generate clusters and class predictions; and Streamlit presents the curated outputs through an interactive interface.')

h('6. Dataset Description')
table(
    ['Executed Source', 'Rows', 'Columns', 'Size (Bytes)', 'Role'],
    [
        ['Indian crop prediction CSV', len(prod), len(prod.columns), os.path.getsize(ROOT / 'data/raw/crop_prediction_india.csv'), 'Yield & regional analysis'],
        ['Crop recommendation CSV', len(rec), len(rec.columns), os.path.getsize(ROOT / 'data/raw/crop_recommendation.csv'), 'Soil/weather classification & clustering']
    ]
)

h('7. Big Data 5 Vs')
table(
    ['Dimension', 'Project Implementation'],
    [
        ['Volume', '49,999 production records and 2,200 soil records; scalable to multi-gigabyte satellite datasets.'],
        ['Velocity', 'Satellite time series and sensor/weather streams ingestible incrementally via Spark.'],
        ['Variety', 'Structured CSV, Snappy-compressed Parquet, vector features, and interactive visualizations.'],
        ['Veracity', 'Exact byte sizes, schema validation, zero-area filtering, and stratified train/test holdouts.'],
        ['Value', 'Actionable crop recommendations, soil clusters, yield predictions, and regional summaries.']
    ]
)

h('8. Apache Spark & Distributed Execution')
p('src/spark_job.py reads raw CSVs via Spark, normalizes schemas, calculates yield per area, aggregates seasonal summaries, scales 7-dimensional soil vectors via VectorAssembler & StandardScaler, fits distributed K-Means, and writes partitioned Parquet outputs to data/processed/spark. In local execution, the Spark master runs on local[*] utilizing all CPU cores with native Hadoop winutils support.')

h('9. Machine Learning Evaluation')
table(
    ['Experiment', 'Metric', 'Executed Value', 'Evaluation Method'],
    [
        ['Random Forest Classifier', 'Accuracy', f"{metrics['random_forest']['accuracy']:.4f}", 'Stratified 80/20 Test Set'],
        ['Random Forest Classifier', 'Weighted F1 Score', f"{metrics['random_forest']['f1_weighted']:.4f}", 'Stratified 80/20 Test Set'],
        ['Random Forest Classifier', 'Weighted Precision', f"{metrics['random_forest']['precision_weighted']:.4f}", 'Stratified 80/20 Test Set'],
        ['Random Forest Classifier', 'Weighted Recall', f"{metrics['random_forest']['recall_weighted']:.4f}", 'Stratified 80/20 Test Set'],
        ['K-Means Clustering', 'Inertia (WCSS)', f"{metrics['kmeans']['inertia']:.3f}", 'k = 5, Scaled Features'],
        ['Yield Regressor', 'MAE', f"{metrics['yield_regression']['mae']:.4f}", 'Random 80/20 Holdout'],
        ['Yield Regressor', 'RMSE', f"{metrics['yield_regression']['rmse']:.4f}", 'Random 80/20 Holdout']
    ]
)

h('10. Interactive Streamlit Dashboard')
p('The web dashboard provides 10 navigable modules: Executive Overview, Soil Analytics, Weather Analytics, Crop Yield Analysis, Crop Distribution, K-Means Clustering, Random Forest Results, Crop Prediction, Regional Analysis, and Hadoop/Spark Monitoring. Both Dark Tech Green and Clean Light Green themes are supported.')

page()

# --- References Section (Matching College Reference Style on Page 34) ---
h('REFERENCES')

refs = [
    '[1] Abhishek Kandoi, “Crop Yield Prediction based on Indian Agriculture Dataset”, GitHub,\nhttps://github.com/AbhishekKandoi/Crop-Yield-Prediction-based-on-Indian-Agriculture',
    '[2] IRTA Remote Sensing, “CATCrops: Sentinel-2 Multi-spectral Time Series Dataset for Crop Classification”, Kaggle,\nhttps://www.kaggle.com/datasets/irtaremotesensing/catcrops-dataset',
    '[3] Tata-Cornell Institute (TCI) and ICRISAT, “District-Level Database for Indian Agriculture and Allied Sectors (1966–2020)”,\nhttps://tci.cornell.edu',
    '[4] Directorate of Economics and Statistics (DES), “Area, Production and Yield (APY) Reports”, Ministry of Agriculture & Farmers Welfare, Govt. of India,\nhttps://data.desagri.gov.in',
    '[5] Food and Agriculture Organization (FAO), “FAOSTAT: Agricultural Production Statistics Database”,\nhttps://www.fao.org/faostat',
    '[6] Apache Spark Documentation, “PySpark and MLlib Distributed Processing Guide”, Apache Software Foundation,\nhttps://spark.apache.org/docs/latest',
    '[7] Scikit-Learn Documentation, “Random Forest Classifier & Regressor User Guide”,\nhttps://scikit-learn.org',
    '[8] Streamlit Documentation, “Interactive Data Applications and Dashboard Framework”,\nhttps://docs.streamlit.io',
    '[9] Python Software Foundation, “Python Language Reference and Standard Library (Version 3.13)”,\nhttps://www.python.org'
]

for ref in refs:
    para = D.add_paragraph(ref)
    para.paragraph_format.space_after = Pt(10)
    para.paragraph_format.line_spacing = 1.15

page()

# --- Appendix Section (Matching College Appendix Style on Page 35) ---
h('APPENDIX')
p('A. Source Code (GitHub Links)', bold=True)
p('The complete source code and materials for the project are available at the following locations:')

links = [
    ('• Smart Agriculture Project Repository', 'https://github.com/AbhiramKorupalli28/Smart-Agriculture-Project'),
    ('• Classification Predictions Output Table', 'https://github.com/AbhiramKorupalli28/Smart-Agriculture-Project/blob/main/outputs/tables/classification_predictions.csv'),
    ('• Spark Distributed Parquet Output Directory', 'https://github.com/AbhiramKorupalli28/Smart-Agriculture-Project/tree/main/data/processed/spark'),
    ('• Interactive Analytics Dashboard (Streamlit Local)', 'http://localhost:8501')
]

for label, url in links:
    para = D.add_paragraph(f"{label}: {url}")
    para.paragraph_format.space_after = Pt(6)

# Footer
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer.add_run('Smart Agriculture Data Analytics Platform | Page ')
run = footer.add_run()
fldChar1 = OxmlElement('w:fldChar')
fldChar1.set(qn('w:fldCharType'), 'begin')
instr = OxmlElement('w:instrText')
instr.set(qn('xml:space'), 'preserve')
instr.text = ' PAGE '
fldChar2 = OxmlElement('w:fldChar')
fldChar2.set(qn('w:fldCharType'), 'end')
run._r.extend([fldChar1, instr, fldChar2])

docx_path = ROOT / 'Mini_Case_Study_Report.docx'
D.save(docx_path)
print(f'Successfully created {docx_path}')

# Convert to PDF using Word COM
try:
    import win32com.client
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(str(docx_path))
    pdf_path = ROOT / 'Mini_Case_Study_Report.pdf'
    doc.SaveAs(str(pdf_path), FileFormat=17)
    doc.Close()
    word.Quit()
    print(f'Successfully converted {pdf_path}')
except Exception as e:
    print('PDF conversion notice:', e)
