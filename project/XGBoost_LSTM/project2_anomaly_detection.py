"""
프로젝트 2: 시계열 이상 징후 감지 (Anomaly Detection)
Autoencoder와 Isolation Forest를 활용한 이상치 탐지
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
import warnings
warnings.filterwarnings('ignore')

from utils import (
    load_prepared_city_data, handle_missing_values, create_timeseries_windows, ensure_directories,
    configure_korean_matplotlib, save_result_summary
)

def build_autoencoder(input_shape):
    """Autoencoder 모델 구성"""
    inputs = Input(shape=input_shape)
    
    # Encoder
    encoded = Dense(32, activation='relu')(inputs)
    encoded = Dense(16, activation='relu')(encoded)
    
    # Decoder
    decoded = Dense(32, activation='relu')(encoded)
    decoded = Dense(input_shape[0], activation='relu')(decoded)
    
    autoencoder = Model(inputs, decoded)
    autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    
    return autoencoder

def train_autoencoder(X_train, X_test):
    """Autoencoder 학습"""
    print("[Autoencoder] 모델 학습 중...")
    
    X_train_2d = X_train.reshape(X_train.shape[0], -1)
    X_test_2d = X_test.reshape(X_test.shape[0], -1)
    
    model = build_autoencoder((X_train_2d.shape[1],))
    
    history = model.fit(
        X_train_2d, X_train_2d,
        epochs=30, batch_size=32,
        validation_data=(X_test_2d, X_test_2d),
        verbose=0
    )
    
    return model, history

def detect_anomalies_autoencoder(model, X_test, threshold_percentile=95):
    """Autoencoder 기반 이상치 탐지"""
    X_test_2d = X_test.reshape(X_test.shape[0], -1)
    predictions = model.predict(X_test_2d, verbose=0)
    
    mse = np.mean(np.square(X_test_2d - predictions), axis=1)
    threshold = np.percentile(mse, threshold_percentile)
    
    anomalies = mse > threshold
    anomaly_scores = mse
    
    return anomalies, anomaly_scores, threshold

def detect_anomalies_isolation_forest(X_data, contamination=0.05):
    """Isolation Forest 기반 이상치 탐지"""
    print("[Isolation Forest] 모델 학습 중...")
    
    X_2d = X_data.reshape(X_data.shape[0], -1)
    
    model = IsolationForest(contamination=contamination, random_state=42)
    predictions = model.fit_predict(X_2d)
    
    anomalies = predictions == -1
    anomaly_scores = -model.score_samples(X_2d)
    
    return model, anomalies, anomaly_scores

def plot_anomaly_detection(y_test, anomaly_ae, scores_ae, anomaly_if, scores_if, 
                          save_path='results/project2_anomalies.png'):
    """이상치 탐지 결과 시각화"""
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))
    
    # Autoencoder - 이상도 점수
    ax = axes[0, 0]
    ax.plot(scores_ae, linewidth=1, color='blue', alpha=0.7)
    threshold_ae = np.percentile(scores_ae, 95)
    ax.axhline(y=threshold_ae, color='red', linestyle='--', label=f'Threshold: {threshold_ae:.2f}')
    ax.scatter(np.where(anomaly_ae)[0], scores_ae[anomaly_ae], 
              color='red', s=100, marker='x', linewidths=2, label='이상치')
    ax.set_xlabel('시간 (일)')
    ax.set_ylabel('재구성 오차 (MSE)')
    ax.set_title('Autoencoder - 이상도 점수')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Autoencoder - 이상치 표시
    ax = axes[0, 1]
    colors = ['red' if a else 'blue' for a in anomaly_ae]
    ax.scatter(range(len(anomaly_ae)), y_test, c=colors, s=30, alpha=0.6)
    ax.set_xlabel('시간 (일)')
    ax.set_ylabel('AQI')
    ax.set_title('Autoencoder - 실제값에 표시된 이상치')
    ax.grid(True, alpha=0.3)
    
    # Isolation Forest - 이상도 점수
    ax = axes[1, 0]
    ax.plot(scores_if, linewidth=1, color='green', alpha=0.7)
    ax.scatter(np.where(anomaly_if)[0], scores_if[anomaly_if], 
              color='red', s=100, marker='x', linewidths=2, label='이상치')
    ax.set_xlabel('시간 (일)')
    ax.set_ylabel('이상도 점수')
    ax.set_title('Isolation Forest - 이상도 점수')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Isolation Forest - 이상치 표시
    ax = axes[1, 1]
    colors = ['red' if a else 'green' for a in anomaly_if]
    ax.scatter(range(len(anomaly_if)), y_test, c=colors, s=30, alpha=0.6)
    ax.set_xlabel('시간 (일)')
    ax.set_ylabel('AQI')
    ax.set_title('Isolation Forest - 실제값에 표시된 이상치')
    ax.grid(True, alpha=0.3)
    
    # 비교: 두 방법이 모두 감지한 이상치
    ax = axes[2, 0]
    consensus_anomalies = anomaly_ae & anomaly_if
    ax.plot(y_test, linewidth=1.5, color='black', label='실제값', alpha=0.7)
    ax.scatter(np.where(consensus_anomalies)[0], y_test[consensus_anomalies],
              color='red', s=100, marker='o', label='공통 이상치 (두 방법 모두)', linewidths=2)
    ax.set_xlabel('시간 (일)')
    ax.set_ylabel('AQI')
    ax.set_title('합의 이상치 (Consensus Anomalies)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 요약 통계
    ax = axes[2, 1]
    ax.axis('off')
    summary_text = f"""
    이상치 탐지 요약
    
    Autoencoder:
      - 탐지된 이상치: {np.sum(anomaly_ae)}개 ({100*np.sum(anomaly_ae)/len(anomaly_ae):.1f}%)
      - 평균 이상도 점수: {np.mean(scores_ae):.4f}
    
    Isolation Forest:
      - 탐지된 이상치: {np.sum(anomaly_if)}개 ({100*np.sum(anomaly_if)/len(anomaly_if):.1f}%)
      - 평균 이상도 점수: {np.mean(scores_if):.4f}
    
    합의 이상치:
      - 두 방법 모두 이상으로 판정: {np.sum(consensus_anomalies)}개
    """
    ax.text(0.1, 0.5, summary_text, fontsize=11,
           verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n[저장] 그래프가 {save_path}에 저장되었습니다.")
    plt.close()

def main():
    print("="*60)
    print("프로젝트 2: 시계열 이상 징후 감지 (Anomaly Detection)")
    print("="*60)
    
    ensure_directories()
    selected_font = configure_korean_matplotlib()

    # 1. 데이터 로드 및 전처리
    print("\n[1단계] 데이터 로드 및 전처리...")
    df = load_prepared_city_data(city='Delhi')
    print(f"  원본 데이터 크기: {df.shape}")
    
    df = handle_missing_values(df, method='linear')
    print(f"  결측치 처리 후: {df.shape}")
    
    # 2. 시계열 윈도우 생성
    print("\n[2단계] 시계열 윈도우 생성...")
    X, y = create_timeseries_windows(df, lookback=7)
    print(f"  X 형태: {X.shape}, y 형태: {y.shape}")
    
    # 정규화
    from sklearn.preprocessing import StandardScaler
    X_2d = X.reshape(X.shape[0], -1)
    scaler = StandardScaler()
    X_2d_normalized = scaler.fit_transform(X_2d)
    X_normalized = X_2d_normalized.reshape(X.shape)
    
    # 3. Autoencoder 학습
    print("\n[3단계] Autoencoder 모델 학습...")
    split_idx = int(len(X_normalized) * 0.8)
    X_train = X_normalized[:split_idx]
    X_test = X_normalized[split_idx:]
    
    ae_model, ae_history = train_autoencoder(X_train, X_test)
    anomaly_ae, scores_ae, threshold_ae = detect_anomalies_autoencoder(ae_model, X_test)
    print(f"  Autoencoder 이상치 탐지: {np.sum(anomaly_ae)}개 ({100*np.sum(anomaly_ae)/len(anomaly_ae):.1f}%)")
    
    # 4. Isolation Forest 학습
    print("\n[4단계] Isolation Forest 모델 학습...")
    if_model, anomaly_if, scores_if = detect_anomalies_isolation_forest(X_test, contamination=0.05)
    print(f"  Isolation Forest 이상치 탐지: {np.sum(anomaly_if)}개 ({100*np.sum(anomaly_if)/len(anomaly_if):.1f}%)")
    
    # 5. 시각화
    print("\n[5단계] 결과 시각화...")
    y_test = y[split_idx:]
    plot_anomaly_detection(y_test, anomaly_ae, scores_ae, anomaly_if, scores_if)

    ae_count = int(np.sum(anomaly_ae))
    if_count = int(np.sum(anomaly_if))
    consensus = int(np.sum(anomaly_ae & anomaly_if))
    interpretation = (
        "두 모델이 동시에 탐지한 구간(합의 이상치)은 신뢰도가 높은 이벤트로 볼 수 있습니다. "
        "한쪽 모델만 탐지한 경우는 센서 노이즈 또는 경계 사례일 수 있어 추가 확인이 필요합니다."
    )
    save_result_summary(
        "project2_summary.json",
        {
            "font_used": selected_font,
            "anomaly_counts": {
                "autoencoder": ae_count,
                "isolation_forest": if_count,
                "consensus": consensus,
            },
            "ratios": {
                "autoencoder_pct": float(100 * ae_count / len(anomaly_ae)),
                "isolation_forest_pct": float(100 * if_count / len(anomaly_if)),
                "consensus_pct_of_test": float(100 * consensus / len(anomaly_if)),
            },
            "interpretation": interpretation,
        },
    )
    
    print("\n" + "="*60)
    print("이상 징후 감지 완료")
    print("="*60)
    
    return {
        'ae_model': ae_model,
        'if_model': if_model,
        'anomaly_ae': anomaly_ae,
        'anomaly_if': anomaly_if
    }

if __name__ == '__main__':
    import os
    os.makedirs('results', exist_ok=True)
    main()
