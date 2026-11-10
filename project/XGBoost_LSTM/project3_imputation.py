"""
프로젝트 3: 시계열 결측치 보간 (Imputation)
KNN Imputer, MICE, 그리고 시계열 전용 보간 기법 비교
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
import warnings
warnings.filterwarnings('ignore')

from utils import (
    load_prepared_city_data,
    ensure_directories,
    configure_korean_matplotlib,
    save_result_summary,
)

def create_synthetic_missing_values(df, missing_rate=0.1, seed=42):
    """의도적으로 결측치 생성"""
    np.random.seed(seed)
    df_copy = df.copy()
    numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        mask = np.random.random(len(df_copy)) < missing_rate
        df_copy.loc[mask, col] = np.nan
    
    return df_copy

def impute_forward_fill(df):
    """Forward Fill: 이전 값으로 채우기"""
    return df.ffill().bfill()

def impute_backward_fill(df):
    """Backward Fill: 다음 값으로 채우기"""
    return df.bfill().ffill()

def impute_linear_interpolation(df):
    """선형 보간"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_copy = df.copy()
    df_copy[numeric_cols] = df_copy[numeric_cols].interpolate(method='linear')
    df_copy = df_copy.bfill().ffill()
    return df_copy

def impute_polynomial_interpolation(df, order=2):
    """다항식 보간"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_copy = df.copy()
    df_copy[numeric_cols] = df_copy[numeric_cols].interpolate(method='polynomial', order=order)
    df_copy = df_copy.bfill().ffill()
    return df_copy

def impute_knn(df, n_neighbors=5):
    """KNN Imputer: K-최근 이웃을 이용한 보간"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_copy = df.copy()
    
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df_copy[numeric_cols] = imputer.fit_transform(df_copy[numeric_cols])
    
    return df_copy

def impute_spline(df, order=3):
    """Spline 보간"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_copy = df.copy()
    df_copy[numeric_cols] = df_copy[numeric_cols].interpolate(method='spline', order=order)
    df_copy = df_copy.bfill().ffill()
    return df_copy

def calculate_imputation_error(original, imputed, missing_mask):
    """보간 오차 계산"""
    numeric_cols = original.select_dtypes(include=[np.number]).columns
    
    errors = {}
    for col in numeric_cols:
        if missing_mask[col].any():
            mae = np.mean(np.abs(
                original.loc[missing_mask[col], col] - imputed.loc[missing_mask[col], col]
            ))
            rmse = np.sqrt(np.mean((
                original.loc[missing_mask[col], col] - imputed.loc[missing_mask[col], col]
            ) ** 2))
            errors[col] = {'MAE': mae, 'RMSE': rmse}
    
    return errors

def plot_imputation_comparison(original_df, methods_results, feature='PM2.5', 
                               save_path='results/project3_imputation.png'):
    """보간 방법 비교 시각화"""
    methods_count = len(methods_results)
    cols = 2
    rows = int(np.ceil(methods_count / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(16, 5 * rows))
    axes = np.atleast_2d(axes)
    
    methods = list(methods_results.keys())
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown']
    
    # 첫 200개 포인트로 비교 (시각화 명확성)
    sample_range = slice(0, min(200, len(original_df)))
    
    for idx, (method, imputed_df) in enumerate(methods_results.items()):
        ax = axes[idx // 2, idx % 2]
        
        ax.plot(original_df.index[sample_range], original_df[feature][sample_range],
               'ko-', linewidth=2, label='원본 (결측치 제거 전)', markersize=3)
        ax.plot(imputed_df.index[sample_range], imputed_df[feature][sample_range],
               color=colors[idx], linestyle='--', alpha=0.7, linewidth=1.5, label=f'{method} 보간')
        
        ax.set_xlabel('날짜')
        ax.set_ylabel(f'{feature} (μg/m³)')
        ax.set_title(f'{method} 보간 결과')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    total_axes = rows * cols
    for idx in range(methods_count, total_axes):
        axes[idx // 2, idx % 2].axis('off')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\n[저장] 그래프가 {save_path}에 저장되었습니다.")
    plt.close()

def plot_error_comparison(error_results, save_path='results/project3_errors.png'):
    """보간 오차 비교"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # MAE 비교
    ax = axes[0]
    methods = list(error_results.keys())
    mae_values = [np.mean([error_results[m][col]['MAE'] 
                          for col in error_results[m].keys()]) 
                  for m in methods]
    
    bars = ax.bar(methods, mae_values, color=['blue', 'green', 'red', 'purple', 'orange', 'brown'])
    ax.set_ylabel('평균 절대 오차 (MAE)')
    ax.set_title('보간 방법별 MAE 비교')
    ax.grid(True, alpha=0.3, axis='y')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.4f}', ha='center', va='bottom', fontsize=9)
    
    # RMSE 비교
    ax = axes[1]
    rmse_values = [np.mean([error_results[m][col]['RMSE'] 
                           for col in error_results[m].keys()]) 
                   for m in methods]
    
    bars = ax.bar(methods, rmse_values, color=['blue', 'green', 'red', 'purple', 'orange', 'brown'])
    ax.set_ylabel('평균 제곱근 오차 (RMSE)')
    ax.set_title('보간 방법별 RMSE 비교')
    ax.grid(True, alpha=0.3, axis='y')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.4f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[저장] 그래프가 {save_path}에 저장되었습니다.")
    plt.close()

def main():
    print("="*60)
    print("프로젝트 3: 시계열 결측치 보간 (Imputation)")
    print("="*60)
    
    ensure_directories()
    selected_font = configure_korean_matplotlib()

    # 1. 데이터 로드
    print("\n[1단계] 데이터 로드...")
    df_original = load_prepared_city_data(city='Delhi')
    print(f"  원본 데이터 크기: {df_original.shape}")
    
    # 선형 보간으로 기존 결측치 처리
    df_clean = df_original.interpolate(method='linear')
    df_clean = df_clean.dropna()
    print(f"  결측치 처리 후: {df_clean.shape}")
    
    # 2. 의도적 결측치 생성
    print("\n[2단계] 의도적 결측치 생성 (결측률: 10%)...")
    df_with_missing = create_synthetic_missing_values(df_clean, missing_rate=0.1, seed=42)
    missing_mask = df_with_missing.isna()
    print(f"  생성된 NaN 수: {missing_mask.sum().sum()}개")
    
    # 3. 다양한 보간 방법 적용
    print("\n[3단계] 보간 방법 적용...")
    
    methods = {
        'Forward Fill': impute_forward_fill,
        'Linear': impute_linear_interpolation,
        'Polynomial': impute_polynomial_interpolation,
        'KNN (k=5)': impute_knn,
        'Spline': impute_spline
    }
    
    imputed_results = {}
    error_results = {}
    
    for method_name, method_func in methods.items():
        print(f"  - {method_name} 적용 중...")
        imputed_df = method_func(df_with_missing.copy())
        imputed_results[method_name] = imputed_df
        
        # 오차 계산
        errors = calculate_imputation_error(df_clean, imputed_df, missing_mask)
        error_results[method_name] = errors
    
    # 4. 성능 비교
    print("\n[4단계] 성능 비교...")
    print("\n" + "="*60)
    print("보간 방법별 성능 평가 (PM2.5)")
    print("="*60)
    
    summary_data = []
    for method_name in methods.keys():
        if 'PM2.5' in error_results[method_name]:
            mae = error_results[method_name]['PM2.5']['MAE']
            rmse = error_results[method_name]['PM2.5']['RMSE']
            summary_data.append({
                '방법': method_name,
                'MAE': f'{mae:.4f}',
                'RMSE': f'{rmse:.4f}'
            })
    
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))
    
    # 5. 시각화
    print("\n[5단계] 결과 시각화...")
    plot_imputation_comparison(df_clean, imputed_results, feature='PM2.5')
    plot_error_comparison(error_results)
    
    print("\n" + "="*60)
    print("결측치 보간 완료")
    print("="*60)

    pm25_table = []
    for method_name in methods.keys():
        if 'PM2.5' in error_results[method_name]:
            pm25_table.append(
                {
                    "method": method_name,
                    "MAE": float(error_results[method_name]['PM2.5']['MAE']),
                    "RMSE": float(error_results[method_name]['PM2.5']['RMSE']),
                }
            )
    pm25_table_sorted = sorted(pm25_table, key=lambda x: x["RMSE"])
    best_method = pm25_table_sorted[0]["method"] if pm25_table_sorted else None
    interpretation = (
        f"PM2.5 기준 RMSE가 가장 낮은 방법은 {best_method}입니다. "
        "오차 막대그래프에서 MAE/RMSE가 낮을수록 결측값 복원 성능이 좋다고 해석합니다."
    )
    save_result_summary(
        "project3_summary.json",
        {
            "font_used": selected_font,
            "pm25_metrics": pm25_table_sorted,
            "best_method_by_rmse": best_method,
            "interpretation": interpretation,
        },
    )
    
    return {
        'original': df_clean,
        'with_missing': df_with_missing,
        'imputed_results': imputed_results,
        'error_results': error_results
    }

if __name__ == '__main__':
    import os
    os.makedirs('results', exist_ok=True)
    main()
