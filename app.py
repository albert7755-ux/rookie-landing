# -*- coding: utf-8 -*-
"""
回收吧！債券火箭 — Streamlit 外殼
- 遊戲本體在 game.html（同一個資料夾）
- 排行榜存在 Supabase 的 rocket_scores 表
- Supabase 網址和金鑰放在 Streamlit Cloud 的 Secrets，不要寫進程式碼
"""
import pathlib

import streamlit as st
import streamlit.components.v1 as components

# ====== 換期時改這裡：改成新的名稱，排行榜就從零開始（舊成績還在資料庫，只是不顯示）======
BOARD_ID = "rocket-2026-11"

st.set_page_config(
    page_title="回收吧！債券火箭",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def read_secret(name: str) -> str:
    """讀 Secrets；本機沒有設定 secrets 時回傳空字串，遊戲會自動變成單機版。"""
    try:
        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""


supabase_url = read_secret("SUPABASE_URL").rstrip("/")
# 注意：這裡一定要用 anon（public）金鑰，不能用 service_role 金鑰，因為它會送到玩家的瀏覽器
supabase_key = read_secret("SUPABASE_ANON_KEY")

html = (pathlib.Path(__file__).parent / "game.html").read_text(encoding="utf-8")
html = (
    html.replace("__SUPABASE_URL__", supabase_url or "__SUPABASE_URL__")
    .replace("__SUPABASE_KEY__", supabase_key or "__SUPABASE_KEY__")
    .replace("__BOARD_ID__", BOARD_ID)
)

# 把 Streamlit 的標題列、邊距藏起來，讓遊戲佔滿整個畫面
st.markdown(
    """
    <style>
      header[data-testid="stHeader"], footer, #MainMenu,
      [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display:none !important;}
      .block-container, [data-testid="stMainBlockContainer"] {padding:0 !important; max-width:100% !important;}
      [data-testid="stAppViewContainer"], .stApp {background:#07101f;}
      iframe {position:fixed; inset:0; width:100vw !important; height:100vh !important; height:100dvh !important;
              border:0; z-index:1000; background:#07101f;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 新版 Streamlit 用 st.iframe；舊版沒有的話改用 components.html
if hasattr(st, "iframe"):
    st.iframe(html, height=900)
else:
    components.html(html, height=900, scrolling=False)
