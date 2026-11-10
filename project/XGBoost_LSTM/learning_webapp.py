"""
Deprecated launcher.

이 파일은 기존 Streamlit 기반 학습 웹앱의 호환용 진입점입니다.
현재 학습 페이지는 Flask + HTML/CSS/JS 기반으로 /learning 경로에서 제공됩니다.
"""

from __future__ import annotations

import webbrowser


def main() -> None:
    url = "http://127.0.0.1:8600/learning"
    print("[안내] Streamlit 버전은 사용하지 않습니다.")
    print(f"[안내] 학습 페이지: {url}")
    print("[안내] 먼저 `python web_server.py` 로 서버를 실행하세요.")
    try:
        webbrowser.open(url)
    except Exception:
        pass


if __name__ == "__main__":
    main()
