"""
프로젝트 1: 다변량 시계열 예측 (Multi-variable Forecasting)
LSTM과 XGBoost를 활용한 AQI 예측
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import warnings
warnings.filterwarnings('ignore')

from utils import (
    load_prepared_city_data, handle_missing_values, ensure_directories,
    create_timeseries_windows, train_test_split_timeseries, normalize_data,
    configure_korean_matplotlib, save_result_summary
)

def build_lstm_model(input_shape):
    """LSTM 모델 구성"""
    model = Sequential([
        LSTM(50, activation='relu', return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, activation='relu'),
        Dropout(0.2),
        Dense(25, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
    return model

def train_lstm_model(X_train, y_train, X_test, y_test):
    """LSTM 모델 학습"""
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
    
    print("[LSTM] 모델 학습 중...")
    history = model.fit(
        X_train, y_train,
        epochs=50, batch_size=32,
        validation_data=(X_test, y_test),
        verbose=0
    )
    
    y_pred = model.predict(X_test, verbose=0).flatten()
    return model, y_pred, history

def train_xgboost_model(X_train, y_train, X_test, y_test):
    """XGBoost 모델 학습"""
    X_train_2d = X_train.reshape(X_train.shape[0], -1)
    X_test_2d = X_test.reshape(X_test.shape[0], -1)
    
    print("[XGBoost] 모델 학습 중...")
    model = xgb.XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1)
    model.fit(X_train_2d, y_train, verbose=False)
    
    y_pred = model.predict(X_test_2d)
    return model, y_pred

def evaluate_model(y_true, y_pred, model_name):
    """모델 성능 평가"""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    print(f"\n[{model_name}] 성능 평가:")
    print(f"  MAE (평균 절대 오차):  {mae:.4f}")
    print(f"  RMSE (평균 제곱근 오차): {rmse:.4f}")
    
    return mae, rmse

def plot_predictions(y_test, lstm_pred, xgb_pred, save_path='results/project1_predictions.png'):
    """예측값 시각화"""
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(y_test, label='실제값', linewidth=2, color='black')
    plt.plot(lstm_pred, label='LSTM 예측', alpha=0.7, color='blue')
    plt.xlabel('시간 (일)')
    plt.ylabel('AQI')
    plt.title('LSTM 모델 - 실제값 vs 예측값')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(y_test, label='실제값', linewidth=2, color='black')
    plt.plot(xgb_pred, label='XGBoost 예측', alpha=0.7, color='red')
    plt.xlabel('시간 (일)')
    plt.ylabel('AQI')
    plt.title('XGBoost 모델 - 실제값 vs 예측값')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n[저장] 그래프가 {save_path}에 저장되었습니다.")
    plt.close()

def main():
    print("="*60)
    print("프로젝트 1: 다변량 시계열 예측 (Multi-variable Forecasting)")
    print("="*60)
    
    ensure_directories()
    selected_font = configure_korean_matplotlib()

    # 1. 데이터 로드 및 전처리
    print("\n[1단계] 데이터 로드 및 전처리...")
    df = load_prepared_city_data(city='Delhi')
    print(f"  원본 데이터 크기: {df.shape}")
    print(f"  피처: {df.columns.tolist()}")
    
    df = handle_missing_values(df, method='linear')
    print(f"  결측치 처리 후: {df.shape}")
    
    # 2. 시계열 윈도우 생성
    print("\n[2단계] 시계열 윈도우 생성 (Lookback=7)...")
    X, y = create_timeseries_windows(df, lookback=7)
    print(f"  X 형태: {X.shape}, y 형태: {y.shape}")
    
    # 3. 시간 기반 분할
    print("\n[3단계] 시간 기반 분할 (80% 학습, 20% 검증)...")
    X_train, X_test, y_train, y_test = train_test_split_timeseries(X, y, test_size=0.2)
    print(f"  X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"  X_test: {X_test.shape}, y_test: {y_test.shape}")
    
    # 정규화
    X_train_norm, X_test_norm, _ = normalize_data(X_train, X_test)
    
    # 4. 모델 학습
    print("\n[4단계] 모델 학습...")
    
    # LSTM 모델
    lstm_model, lstm_pred, lstm_history = train_lstm_model(
        X_train_norm, y_train, X_test_norm, y_test
    )
    lstm_mae, lstm_rmse = evaluate_model(y_test, lstm_pred, "LSTM")
    
    # XGBoost 모델
    xgb_model, xgb_pred = train_xgboost_model(X_train, y_train, X_test, y_test)
    xgb_mae, xgb_rmse = evaluate_model(y_test, xgb_pred, "XGBoost")
    
    # 5. 시각화
    print("\n[5단계] 결과 시각화...")
    plot_predictions(y_test, lstm_pred, xgb_pred)
    
    # 비교 결과
    print("\n" + "="*60)
    print("모델 성능 비교 요약")
    print("="*60)
    comparison_df = pd.DataFrame({
        'Model': ['LSTM', 'XGBoost'],
        'MAE': [lstm_mae, xgb_mae],
        'RMSE': [lstm_rmse, xgb_rmse]
    })
    print(comparison_df.to_string(index=False))

    better_model = "LSTM" if lstm_rmse <= xgb_rmse else "XGBoost"
    interpretation = (
        f"RMSE 기준으로 {better_model} 모델이 더 안정적으로 AQI 변동을 추적했습니다. "
        "예측선이 실제선의 급격한 피크/급락을 얼마나 따라가는지 함께 확인하세요."
    )
    save_result_summary(
        "project1_summary.json",
        {
            "font_used": selected_font,
            "metrics": {
                "LSTM": {"MAE": float(lstm_mae), "RMSE": float(lstm_rmse)},
                "XGBoost": {"MAE": float(xgb_mae), "RMSE": float(xgb_rmse)},
            },
            "best_model_by_rmse": better_model,
            "interpretation": interpretation,
        },
    )
    
    return {
        'lstm_model': lstm_model,
        'xgb_model': xgb_model,
        'X_test': X_test_norm,
        'y_test': y_test
    }

if __name__ == '__main__':
    import os
    os.makedirs('results', exist_ok=True)
    main()
