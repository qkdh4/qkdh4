import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = BASE_DIR / "results"

CITY_DATASET_URLS: Dict[str, str] = {
    "Delhi": "https://raw.githubusercontent.com/cp099/India-Air-Quality-Dataset/main/Delhi_AQI_Dataset.csv",
    "Mumbai": "https://raw.githubusercontent.com/cp099/India-Air-Quality-Dataset/main/Mumbai_AQI_Dataset.csv",
    "Bangalore": "https://raw.githubusercontent.com/cp099/India-Air-Quality-Dataset/main/Bangalore_AQI_Dataset.csv",
    "Chennai": "https://raw.githubusercontent.com/cp099/India-Air-Quality-Dataset/main/Chennai_AQI_Dataset.csv",
    "Hyderabad": "https://raw.githubusercontent.com/cp099/India-Air-Quality-Dataset/main/Hyderabad_AQI_Dataset.csv",
}

MODEL_FEATURES: List[str] = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "AQI"]
TARGET_COLUMN = "AQI"


def ensure_directories() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def configure_korean_matplotlib() -> str:
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    font_candidates = [
        "Malgun Gothic",
        "AppleGothic",
        "NanumGothic",
        "Noto Sans CJK KR",
        "DejaVu Sans",
    ]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    selected = next((name for name in font_candidates if name in installed), "DejaVu Sans")
    plt.rcParams["font.family"] = selected
    plt.rcParams["axes.unicode_minus"] = False
    return selected


def save_result_summary(filename: str, payload: dict) -> Path:
    ensure_directories()
    path = RESULTS_DIR / filename
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def download_city_datasets(cities: Iterable[str] | None = None, force: bool = False) -> List[Path]:
    ensure_directories()
    targets = list(cities) if cities else list(CITY_DATASET_URLS.keys())
    saved_files: List[Path] = []

    for city in targets:
        if city not in CITY_DATASET_URLS:
            raise ValueError(f"지원하지 않는 도시입니다: {city}")
        url = CITY_DATASET_URLS[city]
        dest = RAW_DIR / f"{city.lower()}_raw.csv"
        if dest.exists() and not force:
            saved_files.append(dest)
            continue

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        dest.write_text(response.text, encoding="utf-8")
        saved_files.append(dest)

    return saved_files


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().replace("\ufeff", "") for c in df.columns]
    unnamed = [c for c in df.columns if c.lower().startswith("unnamed") or c == ""]
    if unnamed:
        df = df.drop(columns=unnamed)
    return df


def clean_air_quality_dataframe(df: pd.DataFrame, city: str) -> pd.DataFrame:
    df = _clean_columns(df)
    required = {"City", "Date"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{city} 원본 데이터에 필수 컬럼이 없습니다: {sorted(missing)}")

    df = df[df["City"].astype(str).str.strip().str.lower() == city.lower()].copy()
    if df.empty:
        raise ValueError(f"{city} 데이터가 비어 있습니다.")

    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%y", errors="coerce")
    df = df.dropna(subset=["Date"])

    for col in MODEL_FEATURES:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df[["City", "Date"] + MODEL_FEATURES].sort_values("Date").drop_duplicates(subset=["Date"])
    return df


def preprocess_city_data(city: str = "Delhi") -> pd.DataFrame:
    ensure_directories()
    raw_path = RAW_DIR / f"{city.lower()}_raw.csv"
    if not raw_path.exists():
        download_city_datasets([city], force=False)

    raw_df = pd.read_csv(raw_path)
    cleaned = clean_air_quality_dataframe(raw_df, city=city)
    cleaned[MODEL_FEATURES] = cleaned[MODEL_FEATURES].interpolate(method="linear", limit_direction="both")
    cleaned = cleaned.dropna(subset=MODEL_FEATURES)

    processed_path = PROCESSED_DIR / f"{city.lower()}_clean.csv"
    cleaned.to_csv(processed_path, index=False, encoding="utf-8")
    return cleaned


def build_processed_bundle(cities: Iterable[str] | None = None, force_download: bool = False) -> dict:
    ensure_directories()
    targets = list(cities) if cities else list(CITY_DATASET_URLS.keys())
    download_city_datasets(targets, force=force_download)

    stats = {}
    merged = []
    for city in targets:
        cleaned = preprocess_city_data(city)
        merged.append(cleaned.copy())
        stats[city] = {
            "rows": int(len(cleaned)),
            "start_date": cleaned["Date"].min().strftime("%Y-%m-%d"),
            "end_date": cleaned["Date"].max().strftime("%Y-%m-%d"),
            "features": MODEL_FEATURES,
        }

    merged_df = pd.concat(merged, ignore_index=True)
    merged_df.to_csv(PROCESSED_DIR / "all_cities_clean.csv", index=False, encoding="utf-8")

    metadata = {
        "source_urls": {k: CITY_DATASET_URLS[k] for k in targets},
        "cities": stats,
        "target": TARGET_COLUMN,
        "features": MODEL_FEATURES,
    }
    (PROCESSED_DIR / "dataset_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return metadata


def load_prepared_city_data(city: str = "Delhi") -> pd.DataFrame:
    processed_path = PROCESSED_DIR / f"{city.lower()}_clean.csv"
    if not processed_path.exists():
        preprocess_city_data(city)
    df = pd.read_csv(processed_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").set_index("Date")
    return df[MODEL_FEATURES]


def handle_missing_values(df: pd.DataFrame, method: str = "linear") -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    out = df.copy()
    out[numeric_cols] = out[numeric_cols].interpolate(method=method, limit_direction="both")
    out = out.dropna()
    return out


def create_timeseries_windows(data: pd.DataFrame, lookback: int = 7) -> Tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for i in range(len(data) - lookback):
        X.append(data.iloc[i : i + lookback].values)
        y.append(data.iloc[i + lookback][TARGET_COLUMN])
    return np.array(X), np.array(y)


def train_test_split_timeseries(X: np.ndarray, y: np.ndarray, test_size: float = 0.2):
    split_idx = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    return X_train, X_test, y_train, y_test


def normalize_data(X_train: np.ndarray, X_test: np.ndarray):
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X_train_flat = X_train.reshape(-1, X_train.shape[-1])
    scaler.fit(X_train_flat)

    X_train_normalized = np.array([scaler.transform(x) for x in X_train])
    X_test_normalized = np.array([scaler.transform(x) for x in X_test])
    return X_train_normalized, X_test_normalized, scaler
