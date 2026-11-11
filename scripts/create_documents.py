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

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'; DOCS=ROOT/'docs'
metrics=json.loads((OUT/'metrics.json').read_text())
prod=pd.read_csv(ROOT/'data/raw/crop_prediction_india.csv'); rec=pd.read_csv(ROOT/'data/raw/crop_recommendation.csv')

# Inventory workbook
wb=Workbook(); ws=wb.active; ws.title='Dataset Inventory'
headers=['Dataset','Source URL','Access status','File size (bytes)','Rows','Columns','Formats','License / terms','Key attributes','Use in project']
rows=[
['CATCrops','https://www.kaggle.com/datasets/irtaremotesensing/catcrops-dataset','Investigated; download requires Kaggle access',32490000000,'Reported 332k files','Reported 5.64m columns','CSV, HDF5, Shapefile','Kaggle page exposes metadata; verify terms at download','Sentinel-2 L2A parcel time series, parcel boundaries, ancillary metadata','Primary satellite source and future distributed ingestion'],
['Indian crop prediction','https://github.com/AbhishekKandoi/Crop-Yield-Prediction-based-on-Indian-Agriculture','Downloaded and executed',os.path.getsize(ROOT/'data/raw/crop_prediction_india.csv'),len(prod),len(prod.columns),'CSV','Repository-published public source; retain attribution','State, district, year, season, crop, temperature, humidity, soil moisture, area, production','Yield regression, regional/weather analysis'],
['Crop recommendation','https://github.com/AbhishekKandoi/Crop-Yield-Prediction-based-on-Indian-Agriculture','Downloaded and executed',os.path.getsize(ROOT/'data/raw/crop_recommendation.csv'),len(rec),len(rec.columns),'CSV','Repository-published public source; retain attribution','N, P, K, temperature, humidity, pH, rainfall, crop label','K-Means and Random Forest classification'],
['Cornell/ICRISAT district database','https://tci.cornell.edu/?projects=district-level-database-for-indian-agriculture-and-allied-sectors','Investigated; external acquisition','N/A','11m+ data points reported','1,030 variables reported','Multiple downloadable datasets','Open-access project portal; check file-specific terms','571 districts, 20 states, 1966–2020','Supplementary district-scale historical data'],
['DES APY reports','https://data.desagri.gov.in/website/crops-apy-report-web','Investigated; official portal','N/A','Portal-dependent','Portal-dependent','Web reports / downloads','Government of India portal','Area, production, yield by crop and year','Authoritative validation source'],
['FAOSTAT','https://www.fao.org/faostat/en/','Investigated; official portal','N/A','Portal-dependent','Portal-dependent','Bulk downloads / API','FAO terms; verify at download','International crop production statistics','Cross-country benchmark']]
ws.append(headers)
for r in rows: ws.append(r)
for cell in ws[1]: cell.font=Font(bold=True,color='FFFFFF'); cell.fill=PatternFill('solid',fgColor='2F7D32'); cell.alignment=Alignment(wrap_text=True)
for col,width in {'A':24,'B':52,'C':34,'D':18,'E':22,'F':18,'G':20,'H':32,'I':52,'J':42}.items(): ws.column_dimensions[col].width=width
ws.freeze_panes='A2'; ws.auto_filter.ref=ws.dimensions
ws2=wb.create_sheet('Executed Metrics'); ws2.append(['Experiment','Metric','Value','Notes'])
for exp, vals in [('K-Means',metrics['kmeans']),('Random Forest',metrics['random_forest']),('Yield regression',metrics['yield_regression'])]:
    for k,v in vals.items():
        if k not in ['confusion_matrix','classes','features','cluster_sizes']: ws2.append([exp,k,str(v),'Computed on held-out/local run'])
for cell in ws2[1]: cell.font=Font(bold=True,color='FFFFFF'); cell.fill=PatternFill('solid',fgColor='2F7D32')
for c in 'ABCD': ws2.column_dimensions[c].width={'A':20,'B':26,'C':24,'D':30}[c]
wb.save(ROOT/'Dataset_Inventory.xlsx')

# Academic report
D=Document(); sec=D.sections[0]; sec.top_margin=Inches(.75); sec.bottom_margin=Inches(.7); sec.left_margin=Inches(.85); sec.right_margin=Inches(.85)
styles=D.styles; styles['Normal'].font.name='Calibri'; styles['Normal'].font.size=Pt(10.5)
for s in ['Heading 1','Heading 2','Heading 3']:
    styles[s].font.name='Calibri'; styles[s].font.color.rgb=RGBColor(31,91,36)
styles['Heading 1'].font.size=Pt(18); styles['Heading 2'].font.size=Pt(14); styles['Heading 3'].font.size=Pt(12)

def p(text='',bold=False,align=None):
    q=D.add_paragraph(); r=q.add_run(text); r.bold=bold
    if align is not None: q.alignment=align
    return q
def h(text,level=1): D.add_heading(text,level=level)
def page(): D.add_page_break()
def table(headers, data):
    t=D.add_table(rows=1, cols=len(headers)); t.style='Table Grid'
    for i,x in enumerate(headers): t.rows[0].cells[i].text=str(x)
    for row in data:
        cells=t.add_row().cells
        for i,x in enumerate(row): cells[i].text=str(x)
    return t

p('SMART AGRICULTURE DATA ANALYTICS PLATFORM',True,WD_ALIGN_PARAGRAPH.CENTER)
p('Big Data Analytics – Undergraduate Engineering Mini Case Study',False,WD_ALIGN_PARAGRAPH.CENTER)
p('Research, distributed-processing design, machine learning, and dashboard prototype',False,WD_ALIGN_PARAGRAPH.CENTER)
p('Prepared by: Manus AI\nDate: 11 November 2026',False,WD_ALIGN_PARAGRAPH.CENTER)
D.add_picture(str(ROOT/'Architecture_Diagram.png'),width=Inches(6.5)); p('Figure 1. End-to-end architecture for the proposed platform.',False,WD_ALIGN_PARAGRAPH.CENTER)
page()
h('Certificate'); p('This is to certify that the mini case study titled “Smart Agriculture Data Analytics Platform” documents an implemented prototype and a reproducible distributed-processing design. The executed metrics in this report were generated from the listed public CSV sources; unavailable Hadoop/Spark infrastructure and non-downloaded external datasets are identified explicitly.')
h('Acknowledgement'); p('The project uses public agricultural data repositories and official agriculture statistics portals. The authors of the source datasets and the maintainers of Kaggle, GitHub, Cornell/ICRISAT, DES, FAOSTAT, Python, scikit-learn, Spark, Hadoop, Streamlit, and Plotly are acknowledged.')
h('Abstract'); p('This case study presents a smart agriculture analytics platform that combines crop production, soil, weather, and planned satellite time-series data. The implementation stores curated tables in Parquet, provides PySpark jobs for distributed preprocessing, and applies K-Means clustering, Random Forest crop classification, and yield regression. A local validation run used 49,999 raw Indian crop-production records, 49,784 regression-eligible records after removing undefined zero-area yields, and 2,200 soil/weather recommendation records. Random Forest achieved 0.993 accuracy and 0.993 weighted F1 on a stratified held-out test set. The yield regression experiment achieved MAE 7.235, RMSE 16.393, and R² −0.108, indicating that the available low-dimensional features do not explain yield variation sufficiently. The system therefore demonstrates both a functioning analytical workflow and the importance of richer satellite, soil, and weather data.')
h('1. Introduction'); p('Agricultural decisions are influenced by heterogeneous observations: crop and production records, soil nutrients, weather variables, remote sensing, irrigation, and geography. These sources differ in scale, format, frequency, and uncertainty. A Big Data architecture is useful because it separates durable storage from distributed transformation and model-serving layers. Recent literature emphasizes multimodal integration, generalizability, data annotation, connectivity, and governance as persistent challenges in intelligent agriculture [1].')
h('2. Problem Statement'); p('Traditional tabular analyses struggle with high-volume satellite time series, repeated parcel observations, and cross-source joins. The project addresses the problem of designing a reproducible platform that can ingest agricultural data, process it with Hadoop/Spark, identify agricultural patterns, classify crop suitability, estimate yield where compatible variables exist, and expose results through a dashboard.')
h('3. Objectives');
for x in ['Create a source-traceable ingestion and inventory process.','Represent raw and curated data in HDFS and Parquet.','Implement distributed preprocessing with PySpark and Spark MLlib.','Perform K-Means clustering, Random Forest classification, and yield regression.','Provide a responsive Streamlit and Plotly dashboard.','Document limitations without fabricating unavailable results.'] : D.add_paragraph(x,style='List Bullet')
h('4. Existing System'); p('Existing workflows commonly use isolated notebooks, manual downloads, or single-machine scripts. They may produce useful models but lack durable raw-zone storage, explicit data lineage, repeatable distributed transformations, and a unified user interface. They also risk reporting metrics without preserving the train/test protocol and source files.')
h('5. Proposed System'); p('The proposed system uses a layered design. Source files enter a raw zone. HDFS stores durable copies. Spark reads raw files, performs schema normalization and feature creation, and writes Parquet. Spark MLlib or local scikit-learn-compatible models generate clusters, class predictions, and yield estimates. Streamlit reads curated outputs and metrics for interactive exploration.')
h('6. Literature Review'); p('A recent systematic review of 166 articles reports increasing use of Random Forest and convolutional neural networks, with growing attention to cloud–edge–device architectures, federated learning, explainable AI, interoperability, and governance [1]. The review also highlights limited generalization across agroclimatic contexts, heterogeneous multimodal data, annotation costs, and connectivity constraints. These observations motivate keeping source provenance, evaluation protocols, and limitations visible in this prototype.')
h('7. Dataset Description'); p('The primary CATCrops dataset investigated for this study is a remote-sensing crop classification resource. Its Kaggle page reports a 32.49 GB dataset containing 332k files and 5.64m columns. The described structure includes parcel shapefiles, metadata CSVs, Sentinel-2 L2A time-series CSVs, and compressed HDF5 data. Direct download was not possible in this environment because the public API endpoint did not provide the dataset without authenticated access. The acquisition guide therefore preserves the exact source URL and documents the expected structure without claiming local ingestion.')
table(['Executed source','Rows','Columns','Size','Role'],[['Indian crop prediction CSV',len(prod),len(prod.columns),os.path.getsize(ROOT/'data/raw/crop_prediction_india.csv'),'Yield and regional analysis'],['Crop recommendation CSV',len(rec),len(rec.columns),os.path.getsize(ROOT/'data/raw/crop_recommendation.csv'),'Soil/weather classification and clustering']])
h('8. Big Data 5 Vs');
table(['Dimension','Project interpretation'],[['Volume','CATCrops is reported at 32.49 GB; local executed sources are smaller but real.'],['Velocity','Satellite time series and sensor/weather streams can arrive repeatedly over time.'],['Variety','CSV, HDF5, Shapefile, Parquet, and dashboard tables are supported.'],['Veracity','Source links, file sizes, row counts, licenses, and validation notes are recorded.'],['Value','Outputs include clusters, crop recommendations, yield estimates, and regional summaries.']])
h('9. System Architecture'); D.add_picture(str(ROOT/'Architecture_Diagram.png'),width=Inches(6.5)); p('The raw zone preserves original downloads. The curated zone uses Parquet for columnar analytics. Model outputs are stored separately so the dashboard can load them without rerunning training.')
h('10. Technologies'); p('The source implementation uses Python, pandas, NumPy, scikit-learn, PySpark, Spark MLlib, Hadoop HDFS, Parquet, Streamlit, Plotly, Matplotlib, and LibreOffice for document conversion. HDFS and Spark command paths are included, but their binaries were absent during this run.')
h('11. Data Collection'); p('Two public CSV files were cloned from the source repository listed in the inventory. The project records exact byte sizes, row counts, column names, and source URL. CATCrops, Cornell/ICRISAT, DES APY, and FAOSTAT were investigated as supplementary or authoritative sources. Download instructions are included in README and SOURCES.md.')
h('12. HDFS Storage'); p('The HDFS helper creates /smart-agri/raw and /smart-agri/processed, uploads raw CSV files, and lists the raw zone. On a Hadoop 3.3.6 host, run scripts/hdfs_setup.sh after setting HADOOP_HOME. HDFS commands were not executed here because hdfs was not installed.')
h('13. Apache Spark'); p('src/spark_job.py reads CSV through Spark, computes yield per area, aggregates seasonal summaries, scales soil/weather features, fits K-Means, and writes Parquet outputs. A local pandas/scikit-learn pipeline was executed instead because spark-submit was unavailable. This distinction is material: the model metrics below are local experiment results, not Spark-run metrics.')
h('14. Data Preprocessing'); p('Column names are normalized to lowercase snake case. Rows with zero area cannot define yield per area and are removed for regression. The classification data uses seven numerical inputs: N, P, K, temperature, humidity, pH, and rainfall. K-Means standardizes these variables before fitting.')
h('15. Exploratory Data Analysis'); D.add_picture(str(OUT/'figures/crop_distribution.png'),width=Inches(5.8)); D.add_picture(str(OUT/'figures/kmeans_clusters.png'),width=Inches(5.8));
h('16. Machine Learning Design'); p('The experiments use fixed random seed 42. Classification uses an 80/20 stratified split. Regression uses an 80/20 random hold-out. K-Means uses k=5, ten initializations, and standardized features. Metrics are generated after training and stored in outputs/metrics.json.')
h('17. K-Means'); p(f"K-Means produced five clusters from the recommendation data. The observed cluster sizes were {metrics['kmeans']['cluster_sizes']}; inertia was {metrics['kmeans']['inertia']:.3f}. These clusters are descriptive patterns, not agronomic prescriptions. Domain validation would be required before operational use.")
h('18. Random Forest'); p('Random Forest classifies crop labels from soil and weather measurements. The model uses 250 trees and balanced subsampling. The held-out confusion matrix and prediction table are saved under outputs/tables and outputs/figures.')
D.add_picture(str(OUT/'figures/confusion_matrix.png'),width=Inches(5.0))
h('19. Yield Prediction'); p('The regression target is production divided by area. The model uses temperature, humidity, soil moisture, area, and crop year. The negative R² demonstrates that these features are insufficient for reliable yield prediction in this dataset; no stronger result is claimed. CATCrops, soil surveys, and authoritative weather data would provide richer explanatory variables.')
D.add_picture(str(OUT/'figures/yield_regression.png'),width=Inches(5.0))
h('20. Experimental Results');
table(['Experiment','Metric','Executed value'],[['K-Means','Inertia',f"{metrics['kmeans']['inertia']:.3f}"],['Random Forest','Accuracy',f"{metrics['random_forest']['accuracy']:.4f}"],['Random Forest','Weighted precision',f"{metrics['random_forest']['precision_weighted']:.4f}"],['Random Forest','Weighted recall',f"{metrics['random_forest']['recall_weighted']:.4f}"],['Random Forest','Weighted F1',f"{metrics['random_forest']['f1_weighted']:.4f}"],['Yield regression','MAE',f"{metrics['yield_regression']['mae']:.4f}"],['Yield regression','RMSE',f"{metrics['yield_regression']['rmse']:.4f}"],['Yield regression','R²',f"{metrics['yield_regression']['r2']:.4f}"]])
h('21. Performance Evaluation'); p('The classifier performs strongly on the small, structured recommendation dataset, with only a few misclassifications in the held-out sample. The result should not be generalized to unseen regions without external validation. Regression performance is weak, which is informative: production and area alone do not capture crop-specific management, cultivar, soil, irrigation, disease, and spatial effects.')
h('22. Dashboard'); p('The dashboard includes executive KPIs, soil analytics, weather analytics, crop yield analysis, crop distribution, clustering, classifier results, crop prediction, regional analysis, and Hadoop/Spark monitoring. Plotly charts are driven by the project CSV/Parquet outputs. The dashboard warns users when HDFS/Spark binaries are not available.')
h('23. Advantages');
for x in ['Source-traceable data inventory and reproducible scripts.','Parquet-oriented curated storage.','Clear separation between executed results and unavailable infrastructure.','Interactive filtering and downloadable analytical outputs.','Extensible path to satellite time-series ingestion.'] : D.add_paragraph(x,style='List Bullet')
h('24. Limitations'); p('The local environment lacked Hadoop and Spark binaries. CATCrops and other multi-gigabyte sources were not downloaded. The two executed CSV sources are not a substitute for satellite imagery. The regression model has negative R². Licensing should be rechecked at the time of redistribution, especially for third-party repository files. The classifier may reflect a clean benchmark distribution rather than field complexity.')
h('25. Future Enhancements'); p('Add authenticated CATCrops download, Sentinel-2 feature extraction, NASA POWER or official weather joins, district-level Cornell/ICRISAT data, spatial cross-validation, model explainability, experiment tracking, HDFS replication monitoring, access controls, and drift detection.')
h('26. Conclusion'); p('The project delivers a functional, source-traceable smart agriculture analytics prototype. The local experiments are real and reproducible, while Hadoop/Spark and CATCrops integration are packaged as runnable next steps rather than overstated accomplishments. The metrics demonstrate that the platform can support classification and pattern discovery, and the weak regression result identifies the need for richer multimodal data.')
h('27. References');
for ref in ['[1] Cravero et al. (2026), “A Systematic Review of Machine Learning and Big Data Applications in Agriculture,” Agronomy, https://www.mdpi.com/2073-4395/16/5/516','[2] Kaggle, “CatCrops Dataset,” https://www.kaggle.com/datasets/irtaremotesensing/catcrops-dataset','[3] Cornell/ICRISAT, “District-Level Database for Indian Agriculture and Allied Sectors,” https://tci.cornell.edu/?projects=district-level-database-for-indian-agriculture-and-allied-sectors','[4] Government of India DES, “Area, Production & Yield Reports,” https://data.desagri.gov.in/website/crops-apy-report-web','[5] FAO, “FAOSTAT,” https://www.fao.org/faostat/en/','[6] AbhishekKandoi, “Crop-Yield-Prediction-based-on-Indian-Agriculture,” https://github.com/AbhishekKandoi/Crop-Yield-Prediction-based-on-Indian-Agriculture']:
    D.add_paragraph(ref, style='List Number')
# footer
footer=sec.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER; footer.add_run('Smart Agriculture Data Analytics Platform | Page ')
run=footer.add_run(); fldChar1=OxmlElement('w:fldChar'); fldChar1.set(qn('w:fldCharType'),'begin'); instr=OxmlElement('w:instrText'); instr.set(qn('xml:space'),'preserve'); instr.text=' PAGE '; fldChar2=OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'),'end'); run._r.extend([fldChar1,instr,fldChar2])
D.save(ROOT/'Mini_Case_Study_Report.docx')
print('created',ROOT/'Dataset_Inventory.xlsx',ROOT/'Mini_Case_Study_Report.docx')
