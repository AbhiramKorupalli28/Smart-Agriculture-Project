from pathlib import Path
import json
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
DATA = ROOT / 'data/raw'

st.set_page_config(page_title='Smart Agriculture Analytics', page_icon='🌱', layout='wide')

st.sidebar.title('🌱 Smart Agriculture')
theme_choice = st.sidebar.selectbox('Theme Mode', ['Dark Tech Green', 'Clean Light Green'], index=0)

if theme_choice == 'Dark Tech Green':
    bg_gradient = 'linear-gradient(180deg, #0d1510 0%, #0a0f0c 100%)'
    sidebar_bg = '#111a14'
    text_color = '#f1f5f9'
    title_color = '#22c55e'
    caption_color = '#94a3b8'
    kpi_bg = '#14221a'
    kpi_border = 'rgba(34, 197, 94, 0.25)'
    kpi_num = '#ffffff'
    kpi_label = '#94a3b8'
    chart_font = '#e2e8f0'
    plotly_template = 'plotly_dark'
else:
    bg_gradient = '#f4f8f4'
    sidebar_bg = '#e9f1e8'
    text_color = '#1f2937'
    title_color = '#166534'
    caption_color = '#4b5563'
    kpi_bg = '#ffffff'
    kpi_border = '#cbd5e1'
    kpi_num = '#111827'
    kpi_label = '#4b5563'
    chart_font = '#1f2937'
    plotly_template = 'plotly_white'

st.markdown(f'''
<style>
.stApp {{
    background: {bg_gradient} !important;
    color: {text_color} !important;
}}
[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
}}
.main-title {{
    color: {title_color} !important;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.1rem;
}}
.sub-caption {{
    color: {caption_color} !important;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}}
.kpi {{
    background: {kpi_bg} !important;
    border: 1px solid {kpi_border};
    border-left: 5px solid #22c55e !important;
    padding: 16px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    margin-bottom: 12px;
}}
.kpi h2 {{
    color: {kpi_num} !important;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
}}
.kpi div {{
    color: {kpi_label} !important;
    font-size: 0.9rem;
    margin-top: 4px;
}}
</style>
''', unsafe_allow_html=True)

def render_chart(fig):
    fig.update_layout(
        template=plotly_template,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=chart_font),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

prod = pd.read_csv(DATA / 'crop_prediction_india.csv')
rec = pd.read_csv(DATA / 'crop_recommendation.csv')
prod['Yield per Area'] = prod['Production'] / prod['Area'].replace(0, pd.NA)
metrics = json.loads((OUT / 'metrics.json').read_text()) if (OUT / 'metrics.json').exists() else {}

page = st.sidebar.radio(
    'Navigate',
    [
        'Executive Overview',
        'Soil Analytics',
        'Weather Analytics',
        'Crop Yield Analysis',
        'Crop Distribution',
        'K-Means Clustering',
        'Random Forest Results',
        'Crop Prediction',
        'Regional Analysis',
        'Hadoop and Spark Monitoring'
    ]
)

st.markdown('<h1 class="main-title">Smart Agriculture Data Analytics Platform</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub-caption">Real Indian agriculture data • local validated run • green technology theme</div>', unsafe_allow_html=True)

if page == 'Executive Overview':
    c = st.columns(4)
    vals = [
        (f"{len(prod):,}", 'Production records'),
        (f"{len(rec):,}", 'Soil/weather records'),
        (f"{prod['Crop'].nunique()}", 'Crop types'),
        (f"{prod['State_Name'].nunique()}", 'States/regions')
    ]
    for col, (v, l) in zip(c, vals):
        col.markdown(f'<div class="kpi"><h2>{v}</h2><div>{l}</div></div>', unsafe_allow_html=True)
    fig = px.scatter(
        prod.sample(min(3000, len(prod)), random_state=42),
        x='Temperature',
        y='Production',
        color='Season',
        hover_data=['Crop', 'State_Name'],
        title='Production vs temperature'
    )
    render_chart(fig)

elif page == 'Soil Analytics':
    col = st.selectbox('Soil feature', ['N', 'P', 'K', 'ph', 'rainfall', 'humidity', 'temperature'])
    fig = px.histogram(rec, x=col, color='label', nbins=30, title=f'{col} distribution by crop')
    render_chart(fig)

elif page == 'Weather Analytics':
    fig = px.scatter(
        prod.sample(min(4000, len(prod)), random_state=42),
        x='Humidity',
        y='Temperature',
        color='Season',
        size='Area',
        hover_name='Crop',
        title='Temperature and humidity patterns'
    )
    render_chart(fig)

elif page == 'Crop Yield Analysis':
    filtered = prod.dropna(subset=['Yield per Area']).query('`Yield per Area` < `Yield per Area`.quantile(0.98)')
    fig = px.box(filtered, x='Season', y='Yield per Area', color='Season', title='Yield per area by season')
    render_chart(fig)

elif page == 'Crop Distribution':
    x = prod['Crop'].value_counts().head(20).reset_index()
    x.columns = ['Crop', 'Records']
    fig = px.bar(x, x='Records', y='Crop', orientation='h', title='Most represented crops')
    render_chart(fig)

elif page == 'K-Means Clustering':
    f = OUT / 'tables/recommendation_clusters.parquet'
    d = pd.read_parquet(f) if f.exists() else rec
    fig = px.scatter(d, x='rainfall', y='temperature', color='cluster', hover_data=['label'], title='Agricultural pattern clusters')
    render_chart(fig)
    cols = [c for c in ['n', 'p', 'k', 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'] if c in d.columns]
    st.dataframe(d.groupby('cluster')[cols].mean().round(2))

elif page == 'Random Forest Results':
    m = metrics.get('random_forest', {})
    c = st.columns(4)
    for col, k in zip(c, ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted']):
        col.metric(k.replace('_', ' ').title(), f"{m.get(k, 0):.3f}")
    img = OUT / 'figures/confusion_matrix.png'
    if img.exists():
        st.image(str(img), caption='Held-out confusion matrix')

elif page == 'Crop Prediction':
    f_display = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

    def get_default_val(name):
        if name in rec.columns:
            return float(rec[name].median())
        elif name.lower() in rec.columns:
            return float(rec[name.lower()].median())
        return 0.0

    vals = [st.number_input(x, value=get_default_val(x)) for x in f_display]
    if st.button('Predict crop'):
        import joblib
        model_path = OUT / 'models/random_forest.joblib'
        if model_path.exists():
            model = joblib.load(model_path)
            feature_cols = model.get('features', [x.lower() for x in f_display])
            input_df = pd.DataFrame([vals], columns=feature_cols)
            pred = model['model'].predict(input_df)[0]
            st.success(f'Recommended crop: **{pred.capitalize()}**')
        else:
            st.error('Model file not found. Please run the pipeline first.')

elif page == 'Regional Analysis':
    x = prod.groupby('State_Name', as_index=False).agg(
        Records=('Crop', 'size'),
        Production=('Production', 'sum')
    ).sort_values('Production', ascending=False).head(20)
    fig = px.bar(x, x='Production', y='State_Name', orientation='h', title='Top regions by recorded production')
    render_chart(fig)

else:
    spark_out = ROOT / 'data/processed/spark'
    season_path = spark_out / 'season_summary'
    cluster_path = spark_out / 'recommendation_clusters'

    if season_path.exists() and cluster_path.exists():
        st.success('✅ Apache Spark distributed processing job has been executed successfully!')
        c1, c2, c3 = st.columns(3)
        c1.metric('Spark Job Status', 'COMPLETED')
        c1.caption('Master: local[*]')
        df_season = pd.read_parquet(season_path)
        c2.metric('Spark Processed Records', f"{df_season['records'].sum():,}")
        df_clusters = pd.read_parquet(cluster_path)
        c3.metric('Distributed K-Means Clusters', f"{df_clusters['cluster'].nunique()}")

        st.subheader('📊 Season Aggregation from Spark (Parquet)')
        st.dataframe(df_season.style.format({'avg_temperature': '{:.2f}', 'avg_production': '{:,.2f}'}), use_container_width=True)

        st.subheader('🌱 Distributed K-Means Cluster Breakdown')
        cluster_summary = df_clusters.groupby('cluster')[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].mean().round(2)
        st.dataframe(cluster_summary, use_container_width=True)
    else:
        st.info('Spark job output not found. Run spark-submit to generate distributed outputs.')

    st.markdown('---')
    st.subheader('Distributed Architecture & Deployment Notes')
    st.markdown('''
    - **Apache Spark**: Local master `local[*]` executed `src/spark_job.py` using PySpark and native Hadoop winutils binaries, writing Parquet outputs to `data/processed/spark`.
    - **Hadoop HDFS**: In an enterprise/cloud multi-node deployment, HDFS acts as the distributed storage layer. To initialize a full HDFS cluster, run:
    ''')
    st.code('bash scripts/hdfs_setup.sh\nhdfs dfs -ls /smart-agri/raw\nspark-submit --master local[*] src/spark_job.py --input data/raw --output data/processed/spark', language='bash')
