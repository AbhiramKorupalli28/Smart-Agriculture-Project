from pathlib import Path
import argparse, json, warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import joblib

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except Exception:
    plt = sns = None


def save_table(df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(path, index=False)
        return str(path)
    except Exception:
        csv = path.with_suffix('.csv')
        df.to_csv(csv, index=False)
        return str(csv)


def main(data_dir, output_dir):
    data_dir, out = Path(data_dir), Path(output_dir)
    (out/'figures').mkdir(parents=True, exist_ok=True); (out/'tables').mkdir(parents=True, exist_ok=True); (out/'models').mkdir(parents=True, exist_ok=True)
    prod = pd.read_csv(data_dir/'crop_prediction_india.csv')
    rec = pd.read_csv(data_dir/'crop_recommendation.csv')
    prod.columns = [c.strip().lower().replace(' ','_') for c in prod.columns]
    rec.columns = [c.strip().lower().replace(' ','_') for c in rec.columns]
    prod['yield_per_area'] = prod['production'] / prod['area'].replace(0, np.nan)
    prod = prod.replace([np.inf,-np.inf], np.nan).dropna(subset=['yield_per_area'])
    metrics = {'data': {'production_rows': int(len(prod)), 'recommendation_rows': int(len(rec)), 'production_columns': list(prod.columns), 'recommendation_columns': list(rec.columns)}}
    save_table(prod, out/'tables/production_clean.parquet'); save_table(rec, out/'tables/recommendation_clean.parquet')

    # K-Means on genuine soil/weather data
    feat = ['n','p','k','temperature','humidity','ph','rainfall']
    Xc = rec[feat].astype(float)
    scaler = StandardScaler(); Xcs = scaler.fit_transform(Xc)
    km = KMeans(n_clusters=5, random_state=42, n_init=10).fit(Xcs)
    rec['cluster'] = km.labels_
    save_table(rec, out/'tables/recommendation_clusters.parquet')
    metrics['kmeans'] = {'k': 5, 'inertia': float(km.inertia_), 'cluster_sizes': rec['cluster'].value_counts().sort_index().to_dict(), 'features': feat}
    joblib.dump({'scaler': scaler, 'model': km, 'features': feat}, out/'models/kmeans.joblib')

    # Random Forest crop classification
    Xtr, Xte, ytr, yte = train_test_split(Xc, rec['label'], test_size=.2, random_state=42, stratify=rec['label'])
    clf = RandomForestClassifier(n_estimators=250, random_state=42, n_jobs=-1, class_weight='balanced_subsample')
    clf.fit(Xtr, ytr); pred = clf.predict(Xte)
    pr, rc, f1, _ = precision_recall_fscore_support(yte, pred, average='weighted', zero_division=0)
    metrics['random_forest'] = {'accuracy': float(accuracy_score(yte,pred)), 'precision_weighted': float(pr), 'recall_weighted': float(rc), 'f1_weighted': float(f1), 'classes': list(clf.classes_), 'features': feat, 'confusion_matrix': confusion_matrix(yte,pred,labels=clf.classes_).tolist()}
    joblib.dump({'model': clf, 'features': feat}, out/'models/random_forest.joblib')
    pd.DataFrame({'actual':yte.values,'predicted':pred}).to_csv(out/'tables/classification_predictions.csv',index=False)

    # Yield regression on genuine production data, with held-out evaluation
    rcols = ['temperature','humidity','soil_moisture','area','crop_year']
    regdf = prod.dropna(subset=rcols+['yield_per_area']).copy()
    Xr, yr = regdf[rcols], regdf['yield_per_area'].clip(lower=0, upper=regdf['yield_per_area'].quantile(.99))
    Xtr, Xte, ytr, yte = train_test_split(Xr, yr, test_size=.2, random_state=42)
    reg = RandomForestRegressor(n_estimators=60, random_state=42, n_jobs=-1, min_samples_leaf=2)
    reg.fit(Xtr,ytr); rpred = reg.predict(Xte)
    metrics['yield_regression'] = {'mae': float(mean_absolute_error(yte,rpred)), 'rmse': float(mean_squared_error(yte,rpred)**0.5), 'r2': float(r2_score(yte,rpred)), 'features': rcols, 'target': 'production / area'}
    joblib.dump({'model':reg,'features':rcols}, out/'models/yield_regressor.joblib')
    pd.DataFrame({'actual_yield':yte.values,'predicted_yield':rpred}).to_csv(out/'tables/yield_predictions.csv',index=False)

    if plt:
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.figure(figsize=(8,5)); rec['label'].value_counts().head(12).sort_values().plot(kind='barh', color='#2f7d32'); plt.title('Top crop classes in recommendation dataset'); plt.xlabel('Records'); plt.tight_layout(); plt.savefig(out/'figures/crop_distribution.png',dpi=160); plt.close()
        plt.figure(figsize=(8,5)); sns.scatterplot(data=rec, x='rainfall', y='temperature', hue='cluster', palette='viridis', s=24, alpha=.65); plt.title('K-Means soil/weather clusters'); plt.tight_layout(); plt.savefig(out/'figures/kmeans_clusters.png',dpi=160); plt.close()
        plt.figure(figsize=(7,6)); cm=np.array(metrics['random_forest']['confusion_matrix']); sns.heatmap(cm, cmap='Greens', cbar=False); plt.title('Random Forest confusion matrix'); plt.xlabel('Predicted'); plt.ylabel('Actual'); plt.tight_layout(); plt.savefig(out/'figures/confusion_matrix.png',dpi=160); plt.close()
        plt.figure(figsize=(7,5)); plt.scatter(yte, rpred, s=8, alpha=.35, color='#1b5e20'); lim=[min(yte.min(),rpred.min()),max(yte.max(),rpred.max())]; plt.plot(lim,lim,'--',color='#d84315'); plt.xlabel('Actual yield per area'); plt.ylabel('Predicted yield per area'); plt.title('Yield regression held-out predictions'); plt.tight_layout(); plt.savefig(out/'figures/yield_regression.png',dpi=160); plt.close()
    (out/'metrics.json').write_text(json.dumps(metrics, indent=2, default=str))
    print(json.dumps(metrics, indent=2, default=str))

if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--data-dir',default='data/raw'); ap.add_argument('--output-dir',default='outputs'); a=ap.parse_args(); main(a.data_dir,a.output_dir)
