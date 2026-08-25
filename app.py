"""
AcheiMeuCliente — Inteligência de Mercado B2B (Beleza)
app.py — Streamlit single-file. Responsivo (mobile-first), triagem persistente.

Design: neutro quente (Notion/Claude), um único acento, sem cor decorativa.
"""

import json
import math
import os
import re
from datetime import datetime, date, timedelta
from html import escape
from io import BytesIO
from urllib.parse import quote_plus

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="AcheiMeuCliente",
    page_icon="◍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════
# 1. DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
  --bg:#faf9f7; --surface:#ffffff; --sunk:#f4f2ef; --sunk-2:#efece7;
  --border:#e8e5df; --border-2:#d9d4cb;
  --text:#1f1e1c; --text-2:#6b6862; --muted:#9a958c;
  --accent:#b8562f; --accent-soft:#fbf1ec; --accent-line:#eccfc0;
  --ok:#3f7d58; --ok-soft:#f0f6f2; --ok-line:#cadfd2;
  --no:#a8443a; --no-soft:#faf0ef;
  --star:#a97417; --star-soft:#fbf4e6; --star-line:#e8d5ac;
  --r:10px; --r-sm:7px;
  --sh:0 1px 2px rgba(31,30,28,.04);
  --sh-2:0 2px 10px rgba(31,30,28,.07);
  --font:"DM Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --mono:"JetBrains Mono",ui-monospace,Menlo,monospace;
}

html,body,[data-testid="stAppViewContainer"],[data-testid="stSidebar"]{
  font-family:var(--font)!important; color:var(--text);
}
[data-testid="stAppViewContainer"]{ background:var(--bg); }
[data-testid="stHeader"]{ background:transparent; height:0; }
[data-testid="stToolbar"]{ right:8px; }
.block-container{ max-width:1220px; padding:1.1rem 1.15rem 4rem; }
h1,h2,h3,h4{ font-family:var(--font)!important; color:var(--text)!important; letter-spacing:-.02em; }
hr{ border-color:var(--border)!important; margin:1rem 0!important; }
a{ color:var(--accent); }
a:hover{ color:#8f421f; }
*{ -webkit-tap-highlight-color:transparent; }

.appbar{ display:flex; align-items:center; gap:11px; padding:2px 0 14px; }
.mark{ width:34px; height:34px; border-radius:9px; background:var(--text); color:#fff;
  display:flex; align-items:center; justify-content:center; font-size:15px; font-weight:600; flex-shrink:0; }
.appname{ font-size:16px; font-weight:600; letter-spacing:-.02em; line-height:1.15; }
.appsub{ font-size:12px; color:var(--text-2); margin-top:1px; }
.chip-plan{ margin-left:auto; font-size:11px; font-weight:600; color:var(--text-2);
  border:1px solid var(--border); background:var(--surface); border-radius:20px; padding:4px 11px;
  display:inline-flex; align-items:center; gap:6px; white-space:nowrap; }
.chip-plan i{ width:6px; height:6px; border-radius:50%; background:var(--ok); display:block; }

.stTextInput input, .stNumberInput input{
  background:var(--surface)!important; border-radius:var(--r)!important;
  border:1px solid var(--border-2)!important; font-size:14.5px!important;
  padding:10px 12px!important; color:var(--text)!important;
}
.stTextInput input:focus{ border-color:var(--accent)!important; box-shadow:0 0 0 3px var(--accent-soft)!important; }
.stTextInput input::placeholder{ color:var(--muted)!important; }
[data-baseweb="select"]>div{ background:var(--surface)!important; border-color:var(--border-2)!important;
  border-radius:var(--r-sm)!important; font-size:13.5px!important; }
[data-baseweb="tag"]{ background:var(--text)!important; border-radius:5px!important; }
label p{ font-size:12.5px!important; font-weight:500!important; color:var(--text-2)!important; }

.stButton>button, .stDownloadButton>button{
  border-radius:var(--r-sm)!important; border:1px solid var(--border-2)!important;
  background:var(--surface)!important; color:var(--text)!important;
  font-size:13.5px!important; font-weight:600!important; min-height:44px!important;
  box-shadow:var(--sh)!important; transition:background .12s ease,border-color .12s ease;
}
.stButton>button:hover, .stDownloadButton>button:hover{ background:var(--sunk)!important; color:var(--text)!important; }
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"]{
  background:var(--text)!important; border-color:var(--text)!important; color:#fff!important; }
.stButton>button[kind="primary"]:hover{ background:#000!important; }

.stTabs [data-baseweb="tab-list"]{ gap:2px; border-bottom:1px solid var(--border); overflow-x:auto;
  flex-wrap:nowrap; -webkit-overflow-scrolling:touch; scrollbar-width:none; }
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar{ display:none; }
.stTabs [data-baseweb="tab"]{ height:42px; padding:0 14px; background:transparent; font-size:14px;
  font-weight:600; color:var(--text-2); white-space:nowrap; flex-shrink:0; }
.stTabs [aria-selected="true"]{ color:var(--text)!important; border-bottom:2px solid var(--text); }
.stTabs [data-baseweb="tab-highlight"]{ display:none; }

[data-testid="stExpander"]{ border:1px solid var(--border)!important; border-radius:var(--r)!important;
  background:var(--surface)!important; box-shadow:var(--sh)!important; overflow:hidden!important; }
[data-testid="stExpander"] summary{ padding:12px 14px!important; }
[data-testid="stExpander"] summary p{ font-size:14px!important; font-weight:600!important; color:var(--text)!important; }
[data-testid="stExpander"] summary:hover{ background:var(--sunk)!important; }

.kpis{ display:grid; grid-template-columns:repeat(auto-fit,minmax(148px,1fr)); gap:10px; margin:2px 0 4px; }
.kpi{ background:var(--surface); border:1px solid var(--border); border-radius:var(--r); padding:13px 15px; box-shadow:var(--sh); }
.kpi-l{ font-size:11.5px; font-weight:600; color:var(--muted); }
.kpi-v{ font-size:26px; font-weight:600; letter-spacing:-.035em; margin-top:5px; line-height:1; font-variant-numeric:tabular-nums; }
.kpi-s{ font-size:11.5px; color:var(--text-2); margin-top:5px; }

.chips{ display:flex; flex-wrap:wrap; gap:6px; margin:10px 0 2px; }
.chip{ display:inline-flex; align-items:center; gap:6px; font-size:12.5px; font-weight:500;
  background:var(--surface); border:1px solid var(--border-2); border-radius:20px;
  padding:6px 10px 6px 12px; color:var(--text)!important; text-decoration:none!important; }
.chip:hover{ background:var(--no-soft); border-color:#e2c3bf; color:var(--no)!important; }
.chip b{ font-weight:600; }
.chip span{ color:var(--muted); font-size:13px; line-height:1; }

.section-l{ font-size:12px; font-weight:600; color:var(--muted); margin:18px 0 8px; }
.count-line{ font-size:13px; color:var(--text-2); margin:14px 0 10px; display:flex; align-items:baseline; gap:8px; flex-wrap:wrap; }
.count-line b{ color:var(--text); font-weight:600; }
.f-group{ font-size:11px; font-weight:600; letter-spacing:.06em; color:var(--muted); margin:4px 0 2px; }

/* ══════════════ GRID DE LEADS ══════════════ */
.leads{ display:grid; grid-template-columns:repeat(auto-fill,minmax(360px,1fr)); gap:12px; align-items:start; }
.lead{ background:var(--surface); border:1px solid var(--border); border-radius:12px; box-shadow:var(--sh);
  display:flex; flex-direction:column; overflow:hidden; transition:box-shadow .14s ease,border-color .14s ease; }
.lead:hover{ box-shadow:var(--sh-2); border-color:var(--border-2); }
.lead.is-ok{ border-color:var(--ok-line); box-shadow:inset 3px 0 0 var(--ok),var(--sh); }
.lead.is-star{ border-color:var(--star-line); box-shadow:inset 3px 0 0 var(--star),var(--sh); }
.lead.is-no{ opacity:.5; box-shadow:inset 3px 0 0 var(--border-2),var(--sh); }
.lead.is-no:hover{ opacity:.95; }

.l-head{ padding:14px 15px 0; }
.l-name{ font-size:15.5px; font-weight:600; letter-spacing:-.015em; line-height:1.28; }
.l-legal{ font-size:12px; color:var(--muted); margin-top:2px; }
.l-cnpj{ font-family:var(--mono); font-size:11.5px; color:var(--text-2); margin-top:6px;
  display:flex; align-items:center; gap:6px; }
.l-addr{ font-size:12.5px; color:var(--text-2); margin-top:6px; line-height:1.45; display:flex; gap:6px; }
.l-addr svg{ margin-top:2px; }

/* Contatos: só ícones + número miúdo */
.l-contacts{ margin:12px 15px 0; background:var(--sunk); border:1px solid var(--border);
  border-radius:var(--r-sm); padding:7px 8px; display:flex; flex-direction:column; gap:5px; }
.c-row{ display:flex; align-items:center; gap:6px; }
.c-num{ font-family:var(--mono); font-size:11.5px; font-weight:500; color:var(--text-2);
  letter-spacing:-.02em; flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.c-mail{ font-size:11px; color:var(--text-2); flex:1; min-width:0; overflow:hidden;
  text-overflow:ellipsis; white-space:nowrap; }
.ic{ width:30px; height:30px; border-radius:6px; border:1px solid var(--border-2); background:var(--surface);
  color:var(--text-2)!important; display:inline-flex; align-items:center; justify-content:center;
  text-decoration:none!important; flex-shrink:0; }
.ic:hover{ background:var(--sunk-2); color:var(--text)!important; }
.ic-wa:hover{ background:var(--ok-soft); border-color:var(--ok-line); color:var(--ok)!important; }
.c-none{ font-size:11.5px; color:var(--muted); padding:3px 2px; }

/* CNAE */
.l-cnae{ padding:12px 15px 0; }
.cn-flag{ display:inline-flex; align-items:center; gap:6px; font-size:11px; font-weight:600;
  letter-spacing:.02em; padding:3px 8px; border-radius:5px; margin-bottom:7px; }
.cn-flag-ok{ background:var(--ok-soft); border:1px solid var(--ok-line); color:var(--ok); }
.cn-flag-no{ background:var(--star-soft); border:1px solid var(--star-line); color:var(--star); }
.cn-line{ display:flex; gap:7px; font-size:12px; line-height:1.5; color:var(--text-2);
  white-space:nowrap; overflow:hidden; }
.cn-line b{ font-family:var(--mono); font-size:11px; font-weight:500; color:var(--text); flex-shrink:0; }
.cn-line i{ overflow:hidden; text-overflow:ellipsis; font-style:normal; }
.cn-line-ok b, .cn-line-ok i{ color:var(--ok); }
.cn-main{ font-size:12.5px; line-height:1.45; color:var(--text); display:flex; gap:7px; }
.cn-sub-h{ font-size:10.5px; font-weight:600; letter-spacing:.05em; color:var(--muted); margin:9px 0 4px; }

.l-badges{ display:flex; flex-wrap:wrap; gap:5px; padding:12px 15px 0; }
.bdg{ font-size:11.5px; font-weight:500; padding:3px 8px; border-radius:5px;
  background:var(--sunk); border:1px solid var(--border); color:var(--text-2); }
.bdg-warn{ background:var(--star-soft); border-color:var(--star-line); color:var(--star); }

.l-links{ display:flex; gap:6px; padding:13px 15px; flex-wrap:wrap; }
.lk{ flex:1 1 0; min-width:72px; min-height:38px; display:inline-flex; align-items:center; justify-content:center;
  gap:5px; font-size:12px; font-weight:500; border:1px solid var(--border); border-radius:var(--r-sm);
  background:var(--surface); color:var(--text-2)!important; text-decoration:none!important; }
.lk:hover{ background:var(--sunk); color:var(--text)!important; border-color:var(--border-2); }
.lk.dis{ opacity:.38; pointer-events:none; }

.l-triage{ display:grid; grid-template-columns:1fr 1fr 1fr; border-top:1px solid var(--border); margin-top:auto; }
.tg{ min-height:46px; display:inline-flex; align-items:center; justify-content:center; gap:6px;
  font-size:12.5px; font-weight:600; text-decoration:none!important; color:var(--text-2)!important;
  border-right:1px solid var(--border); background:var(--surface); }
.tg:last-child{ border-right:none; }
.tg:hover{ background:var(--sunk); color:var(--text)!important; }
.tg-on-ok{ background:var(--ok-soft)!important; color:var(--ok)!important; }
.tg-on-star{ background:var(--star-soft)!important; color:var(--star)!important; }
.tg-on-no{ background:var(--no-soft)!important; color:var(--no)!important; }

.exp-card{ background:var(--surface); border:1px solid var(--border); border-radius:var(--r);
  padding:16px 17px; box-shadow:var(--sh); height:100%; }
.exp-card h4{ font-size:15px; font-weight:600; margin:0 0 5px; }
.exp-card p{ font-size:13px; color:var(--text-2); margin:0; line-height:1.5; }
.note{ background:var(--surface); border:1px solid var(--border); border-left:2px solid var(--accent);
  border-radius:var(--r-sm); padding:13px 15px; font-size:13.5px; color:var(--text-2); line-height:1.5; }
.empty{ text-align:center; padding:44px 20px; border:1px dashed var(--border-2); border-radius:var(--r);
  background:var(--surface); color:var(--text-2); font-size:14px; }
.empty b{ display:block; color:var(--text); font-size:15px; font-weight:600; margin-bottom:5px; }

[data-testid="stSidebar"]{ background:var(--surface)!important; border-right:1px solid var(--border)!important; }
[data-testid="stFileUploader"]{ background:var(--sunk); border:1px dashed var(--border-2); border-radius:var(--r); padding:8px; }
[data-testid="stFileUploader"] section{ background:transparent!important; }

@media (max-width:640px){
  .block-container{ padding:.7rem .8rem 3.5rem; }
  .leads{ grid-template-columns:1fr; gap:10px; }
  .kpis{ grid-template-columns:1fr 1fr; }
  .kpi-v{ font-size:22px; }
  .stTextInput input{ font-size:16px!important; }
  .l-name{ font-size:15px; }
  .l-links .lk{ flex:1 1 calc(50% - 3px); }
  .stTabs [data-baseweb="tab"]{ font-size:13.5px; padding:0 11px; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# 2. CONSTANTES
# ══════════════════════════════════════════════════════════════════════════
BEAUTY_CNAES = {
    "9602501": "Salões e Barbearias",
    "9602502": "Clínicas de Estética",
    "4772500": "Lojas e Pontos de Venda",
    "4646001": "Distribuidores Atacadistas",
    "4646002": "Distribuidores Atacadistas",
    "4618401": "Representantes e Agentes",
    "4644301": "Distribuidores Atacadistas",
    "2063100": "Fábricas e Marcas",
    "8593700": "Ensino e Cursos de Beleza",
}
SEGMENTOS = list(dict.fromkeys(BEAUTY_CNAES.values()))

CNAE_BASE = {
    "9602501": "CABELEIREIROS, BARBEARIAS, MANICURE E PEDICURE",
    "9602502": "ATIVIDADES DE ESTÉTICA E OUTROS SERVIÇOS DE CUIDADOS COM A BELEZA",
    "4772500": "COMÉRCIO VAREJISTA DE COSMÉTICOS, PRODUTOS DE PERFUMARIA E DE HIGIENE PESSOAL",
    "4646001": "COMÉRCIO ATACADISTA DE COSMÉTICOS E PRODUTOS DE PERFUMARIA",
    "4646002": "COMÉRCIO ATACADISTA DE PRODUTOS DE HIGIENE PESSOAL",
    "4618401": "REPRESENTANTES COMERCIAIS DE COSMÉTICOS E PRODUTOS DE PERFUMARIA",
    "4644301": "COMÉRCIO ATACADISTA DE MEDICAMENTOS E DROGAS DE USO HUMANO",
    "2063100": "FABRICAÇÃO DE COSMÉTICOS, PRODUTOS DE PERFUMARIA E DE HIGIENE PESSOAL",
    "8593700": "ENSINO DE IDIOMAS",
    "4781400": "COMÉRCIO VAREJISTA DE ARTIGOS DO VESTUÁRIO E ACESSÓRIOS",
    "4789005": "COMÉRCIO VAREJISTA DE PRODUTOS SANEANTES DOMISSANITÁRIOS",
    "4789002": "COMÉRCIO VAREJISTA DE PLANTAS E FLORES NATURAIS",
    "4639701": "COMÉRCIO ATACADISTA DE PRODUTOS ALIMENTÍCIOS EM GERAL",
    "4642701": "COMÉRCIO ATACADISTA DE ARTIGOS DO VESTUÁRIO E ACESSÓRIOS",
    "4649408": "COMÉRCIO ATACADISTA DE PRODUTOS DE HIGIENE, LIMPEZA E CONSERVAÇÃO DOMICILIAR",
    "4729699": "COMÉRCIO VAREJISTA DE PRODUTOS ALIMENTÍCIOS EM GERAL",
    "8690999": "OUTRAS ATIVIDADES DE ATENÇÃO À SAÚDE HUMANA",
}

TIER_CFG = {
    "explorador": {"label": "Explorador", "limit": 0},
    "operacional": {"label": "Operacional", "limit": 300},
    "regional": {"label": "Regional", "limit": 1000},
    "nacional": {"label": "Nacional", "limit": 999999},
}
PERFIS = {
    "pro@achei.com": {"nome": "Amanda Consultora", "tier": "regional"},
    "demo@achei.com": {"nome": "Rafael Consultor", "tier": "operacional"},
    "admin@achei.com": {"nome": "Admin Geral", "tier": "nacional"},
    "explorador@achei.com": {"nome": "Explorador Free", "tier": "explorador"},
}

TRIAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".triagem.json")
TRIAGE_META = {
    "ok": {"label": "Serve", "icon": "✓", "cls": "is-ok", "btn": "tg-on-ok"},
    "star": {"label": "Prioridade", "icon": "★", "cls": "is-star", "btn": "tg-on-star"},
    "no": {"label": "Não serve", "icon": "✕", "cls": "is-no", "btn": "tg-on-no"},
}

_SVG = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"'
I_PIN = f'<svg width="13" height="13" {_SVG} style="flex-shrink:0"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
I_WA = f'<svg width="15" height="15" {_SVG}><path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20.5l1.7-5.2A8.5 8.5 0 1 1 21 11.5z"/><path d="M8.8 9.2c0 3 2.4 5.4 5.4 5.4"/></svg>'
I_TEL = f'<svg width="14" height="14" {_SVG}><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
I_COPY = f'<svg width="13" height="13" {_SVG}><rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>'
I_MAIL = f'<svg width="14" height="14" {_SVG}><rect x="2" y="4.5" width="20" height="15" rx="2.5"/><path d="m2.5 6 9.5 7 9.5-7"/></svg>'
I_GLOBE = f'<svg width="13" height="13" {_SVG}><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18z"/></svg>'
I_CAM = f'<svg width="13" height="13" {_SVG}><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.6"/><path d="M17.5 6.5h.01"/></svg>'
I_DOC = f'<svg width="13" height="13" {_SVG}><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/></svg>'
I_SPARK = f'<svg width="13" height="13" {_SVG}><path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/></svg>'

# ══════════════════════════════════════════════════════════════════════════
# 3. DADOS
# ══════════════════════════════════════════════════════════════════════════
EXPECTED_STR = ["RAZÃO SOCIAL", "NOME FANTASIA", "CNPJ", "MUNICIPIO", "ESTADO", "BAIRRO", "CEP",
                "ORIGEM_CNAE", "E-MAIL", "ENDERECO MAPA", "NATUREZA_JURIDICA", "MATRIZ FILIAL",
                "PORTE", "CNAE_PRINCIPAL_CODIGO", "CNAE_PRINCIPAL_NOME", "CNAE_SECUNDARIO_CODIGO",
                "CNAE_SECUNDARIO_NOME", "SITE", "MAPS", "RECEITA FEDERAL",
                "TELEFONE_1", "TELEFONE_2", "TELEFONE_3", "WHATSAPP_1", "WHATSAPP_2", "WHATSAPP_3"]
EXPECTED_BOOL = ["TEM_EMAIL", "TEM_TELEFONE", "EMAIL_CONTABILIDADE", "MEI", "SIMPLES"]


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    # Garante o esquema: qualquer base enviada pelo usuário passa a ter todas as
    # colunas esperadas (vazias quando não existem), então nada mais quebra depois.
    for c in EXPECTED_STR:
        if c not in df.columns:
            df[c] = ""
    for c in EXPECTED_BOOL:
        if c not in df.columns:
            df[c] = False
    if "CAPITAL SOCIAL" not in df.columns:
        df["CAPITAL SOCIAL"] = 0
    if "INICIO ATIVIDADE" not in df.columns:
        df["INICIO ATIVIDADE"] = pd.NaT
    for c in ["RAZÃO SOCIAL", "NOME FANTASIA", "MUNICIPIO", "ESTADO", "BAIRRO", "CEP", "ORIGEM_CNAE",
              "SEGMENTO", "E-MAIL", "ENDERECO MAPA", "NATUREZA_JURIDICA", "MATRIZ FILIAL",
              "CNAE_PRINCIPAL_NOME", "CNAE_SECUNDARIO_CODIGO", "CNAE_SECUNDARIO_NOME", "SITE"]:
        if c in df.columns:
            df[c] = df[c].fillna("").astype(str).str.strip()

    if "CNPJ" in df.columns:
        def _cnpj(v):
            d = re.sub(r"\D", "", str(v))
            return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:14]}" if len(d) == 14 else str(v).strip()
        df["CNPJ"] = df["CNPJ"].apply(_cnpj)

    for c in ["TEM_EMAIL", "TEM_TELEFONE", "EMAIL_CONTABILIDADE", "MEI", "SIMPLES"]:
        if c in df.columns:
            df[c] = df[c].apply(lambda v: v is True or str(v).strip().upper() in ("SIM", "TRUE", "1", "S"))

    porte_map = {"MICRO EMPRESA": "ME", "EMPRESA DE PEQUENO PORTE": "EPP", "DEMAIS": "Grande",
                 "MEI": "MEI", "ME": "ME", "EPP": "EPP", "GRANDE": "Grande"}
    if "PORTE" in df.columns:
        df["PORTE"] = df["PORTE"].apply(lambda v: porte_map.get(str(v).strip().upper(), str(v).strip()))
    if "MATRIZ FILIAL" in df.columns:
        df["MATRIZ FILIAL"] = df["MATRIZ FILIAL"].str.title()
    if "ORIGEM_CNAE" in df.columns:
        df["ORIGEM_CNAE"] = df["ORIGEM_CNAE"].str.upper()

    df["CNAE_PRINCIPAL_CODIGO"] = df["CNAE_PRINCIPAL_CODIGO"].apply(lambda v: re.sub(r"\D", "", str(v)))
    df["_CNAE_P_LABEL"] = df["CNAE_PRINCIPAL_CODIGO"] + " — " + df["CNAE_PRINCIPAL_NOME"].astype(str).str.slice(0, 46)
    if "SEGMENTO" not in df.columns or df["SEGMENTO"].astype(str).str.strip().eq("").all():
        df["SEGMENTO"] = df["CNAE_PRINCIPAL_CODIGO"].map(lambda c: BEAUTY_CNAES.get(c, "Outros ramos"))

    df["INICIO ATIVIDADE"] = pd.to_datetime(df["INICIO ATIVIDADE"], errors="coerce")
    df["ANOS_ATIVIDADE"] = ((datetime.now() - df["INICIO ATIVIDADE"]).dt.days / 365.25).fillna(0).round(1)
    df["CAPITAL SOCIAL"] = pd.to_numeric(df["CAPITAL SOCIAL"], errors="coerce").fillna(0)

    for i in range(1, 4):
        for col in (f"WHATSAPP_{i}", f"TELEFONE_{i}"):
            df[col] = df[col].fillna("").astype(str).str.strip().replace("nan", "")
    return df


def _mock() -> pd.DataFrame:
    rows = [
        {"NOME FANTASIA": "ATACADAO DA BELEZA", "RAZÃO SOCIAL": "ATACADAO DA BELEZA AMAPA LTDA",
         "CNPJ": "62891615000102", "CNAE_PRINCIPAL_CODIGO": "4772500",
         "CNAE_PRINCIPAL_NOME": CNAE_BASE["4772500"],
         "CNAE_SECUNDARIO_CODIGO": "4639701,4642701,4646001,4649408,4781400,4789005,9602501",
         "CNAE_SECUNDARIO_NOME": "", "TELEFONE_1": "+559681430456", "TELEFONE_2": "+5596991234567", "TELEFONE_3": "",
         "WHATSAPP_1": "https://wa.me/559681430456", "WHATSAPP_2": "", "WHATSAPP_3": "",
         "E-MAIL": "ATACADAODOSCOSMETICOSMCP@GMAIL.COM", "TEM_EMAIL": "SIM", "TEM_TELEFONE": "SIM",
         "EMAIL_CONTABILIDADE": "NÃO", "BAIRRO": "CENTRAL", "CEP": "68900030", "MUNICIPIO": "MACAPA",
         "ESTADO": "AP", "ENDERECO MAPA": "AVENIDA PADRE JULIO MARIA LOMBAERD, 564 - CENTRAL",
         "MATRIZ FILIAL": "MATRIZ", "PORTE": "MICRO EMPRESA", "CAPITAL SOCIAL": 150000.0, "MEI": "NÃO",
         "SIMPLES": "SIM", "INICIO ATIVIDADE": "2017-08-02", "ORIGEM_CNAE": "SECUNDARIO",
         "NATUREZA_JURIDICA": "SOCIEDADE EMPRESÁRIA LIMITADA", "MAPS": "", "RECEITA FEDERAL": ""},
        {"NOME FANTASIA": "IVY BELEZA NATURAL", "RAZÃO SOCIAL": "IVANESSA S E SILVA",
         "CNPJ": "26538973000172", "CNAE_PRINCIPAL_CODIGO": "9602501",
         "CNAE_PRINCIPAL_NOME": CNAE_BASE["9602501"],
         "CNAE_SECUNDARIO_CODIGO": "4789002,4781400,4772500,9602502", "CNAE_SECUNDARIO_NOME": "",
         "TELEFONE_1": "+556184963319", "TELEFONE_2": "", "TELEFONE_3": "",
         "WHATSAPP_1": "https://wa.me/556184963319", "WHATSAPP_2": "", "WHATSAPP_3": "",
         "E-MAIL": "INEYCY@YAHOO.COM.BR", "TEM_EMAIL": "SIM", "TEM_TELEFONE": "SIM",
         "EMAIL_CONTABILIDADE": "NÃO", "BAIRRO": "FONTE NOVA", "CEP": "68928241", "MUNICIPIO": "SANTANA",
         "ESTADO": "AP", "ENDERECO MAPA": "RUA DAS ROSAS, 203 - FONTE NOVA", "MATRIZ FILIAL": "MATRIZ",
         "PORTE": "MICRO EMPRESA", "CAPITAL SOCIAL": 5000.0, "MEI": "SIM", "SIMPLES": "NÃO",
         "INICIO ATIVIDADE": "2016-11-15", "ORIGEM_CNAE": "PRINCIPAL",
         "NATUREZA_JURIDICA": "EMPRESÁRIO (INDIVIDUAL)", "MAPS": "", "RECEITA FEDERAL": ""},
        {"NOME FANTASIA": "", "RAZÃO SOCIAL": "DISTRIBUIDORA BELEZAMIX LTDA", "CNPJ": "44333222000199",
         "CNAE_PRINCIPAL_CODIGO": "4646001", "CNAE_PRINCIPAL_NOME": CNAE_BASE["4646001"],
         "CNAE_SECUNDARIO_CODIGO": "4772500,4644301", "CNAE_SECUNDARIO_NOME": "",
         "TELEFONE_1": "+553134445555", "TELEFONE_2": "+5531984445555", "TELEFONE_3": "+553134446666",
         "WHATSAPP_1": "https://wa.me/5531984445555", "WHATSAPP_2": "", "WHATSAPP_3": "",
         "E-MAIL": "contato@contabilmg.com.br", "TEM_EMAIL": "SIM", "TEM_TELEFONE": "SIM",
         "EMAIL_CONTABILIDADE": "SIM", "BAIRRO": "CENTRO", "CEP": "30110000", "MUNICIPIO": "BELO HORIZONTE",
         "ESTADO": "MG", "ENDERECO MAPA": "AVENIDA AFONSO PENA, 1500 - CENTRO", "MATRIZ FILIAL": "MATRIZ",
         "PORTE": "EMPRESA DE PEQUENO PORTE", "CAPITAL SOCIAL": 500000.0, "MEI": "NÃO", "SIMPLES": "NÃO",
         "INICIO ATIVIDADE": "2012-05-10", "ORIGEM_CNAE": "PRINCIPAL",
         "NATUREZA_JURIDICA": "SOCIEDADE EMPRESÁRIA LIMITADA", "MAPS": "", "RECEITA FEDERAL": ""},
    ]
    return normalize_df(pd.DataFrame(rows))


@st.cache_data(show_spinner=False)
def load_repo_csv():
    for path in ("plano/bd_teste/9602501_AP.csv", "dados.csv"):
        if os.path.exists(path):
            for sep in (";", ","):
                try:
                    df = pd.read_csv(path, sep=sep, encoding="utf-8", dtype=str)
                    if df.shape[1] > 3:
                        return normalize_df(df)
                except Exception:
                    continue
    return None


@st.cache_data(show_spinner=False)
def load_upload(file_bytes: bytes, name: str) -> pd.DataFrame:
    buf = BytesIO(file_bytes)
    if name.lower().endswith((".xlsx", ".xls")):
        return normalize_df(pd.read_excel(buf, dtype=str))
    for sep in (";", ","):
        buf.seek(0)
        try:
            df = pd.read_csv(buf, sep=sep, encoding="utf-8", dtype=str)
            if df.shape[1] > 3:
                return normalize_df(df)
        except Exception:
            continue
    raise ValueError("formato não reconhecido")


@st.cache_data(show_spinner=False)
def cnae_names(df: pd.DataFrame) -> dict:
    """code → nome. Aprende com os pares principais da própria base (confiáveis)."""
    m = dict(CNAE_BASE)
    if {"CNAE_PRINCIPAL_CODIGO", "CNAE_PRINCIPAL_NOME"} <= set(df.columns):
        for cod, nome in df[["CNAE_PRINCIPAL_CODIGO", "CNAE_PRINCIPAL_NOME"]].dropna().values:
            c, n = re.sub(r"\D", "", str(cod)), str(nome).strip()
            if c and n and c not in m:
                m[c] = n
    return m

# ══════════════════════════════════════════════════════════════════════════
# 4. TRIAGEM PERSISTENTE
# ══════════════════════════════════════════════════════════════════════════
def load_triage() -> dict:
    if "triagem" not in st.session_state:
        data = {}
        if os.path.exists(TRIAGE_PATH):
            try:
                with open(TRIAGE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        st.session_state.triagem = data if isinstance(data, dict) else {}
    return st.session_state.triagem


def save_triage() -> None:
    try:
        with open(TRIAGE_PATH, "w", encoding="utf-8") as f:
            json.dump(st.session_state.triagem, f, ensure_ascii=False, indent=1)
    except Exception:
        st.session_state.triagem_ro = True


def set_triage(cnpj: str, status: str) -> None:
    t = load_triage()
    if t.get(cnpj, {}).get("status") == status:
        t.pop(cnpj, None)
    else:
        t[cnpj] = {"status": status, "em": datetime.now().strftime("%Y-%m-%d %H:%M")}
    save_triage()

# ══════════════════════════════════════════════════════════════════════════
# 5. HELPERS
# ══════════════════════════════════════════════════════════════════════════
def minify(html: str) -> str:
    return re.sub(r"\n[ \t]*", " ", html).strip()


def txt(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    s = str(v).strip()
    return "" if s.lower() in ("nan", "none", "nat") else s


def digits(v) -> str:
    return re.sub(r"\D", "", str(v))


def fmt_phone(v) -> str:
    d = digits(txt(v))
    if not d or d.count("0") >= len(d) - 1:
        return ""
    if d.startswith("55") and len(d) in (12, 13):
        d = d[2:]
    if len(d) == 11:
        return f"({d[:2]}) {d[2:7]}-{d[7:]}"
    if len(d) == 10:
        return f"({d[:2]}) {d[2:6]}-{d[6:]}"
    return ""


def all_phones(row) -> list[tuple[str, str]]:
    """[(formatado, só dígitos com 55)] — telefones e whatsapps, sem repetição."""
    out, seen = [], set()
    for col in [f"TELEFONE_{i}" for i in range(1, 4)] + [f"WHATSAPP_{i}" for i in range(1, 4)]:
        f = fmt_phone(row.get(col))
        if f and f not in seen:
            seen.add(f)
            d = digits(f)
            out.append((f, d if d.startswith("55") else f"55{d}"))
    return out


def fmt_capital(v) -> str:
    try:
        n = float(v)
    except Exception:
        return "—"
    if n >= 1_000_000:
        return f"R$ {n/1_000_000:.1f}M".replace(".", ",")
    if n >= 1_000:
        return f"R$ {n/1_000:.0f} mil"
    return f"R$ {n:.0f}"


def display_names(row) -> tuple[str, str]:
    nf, rs = txt(row.get("NOME FANTASIA")), txt(row.get("RAZÃO SOCIAL"))
    return (nf, rs if rs and rs != nf else "") if nf else (rs or "Sem nome cadastrado", "")


def sec_cnaes(row, nomes: dict) -> list[tuple[str, str, bool]]:
    cods = [re.sub(r"\D", "", c) for c in txt(row.get("CNAE_SECUNDARIO_CODIGO")).split(",")]
    cods = [c for c in cods if c]
    fallback = [n.strip() for n in txt(row.get("CNAE_SECUNDARIO_NOME")).split("|") if n.strip()]
    out = []
    for i, c in enumerate(cods):
        nome = nomes.get(c) or (fallback[i] if i < len(fallback) and len(cods) == len(fallback) else "")
        out.append((c, nome or "Atividade não catalogada", c in BEAUTY_CNAES))
    return out


def wa_link(digits55: str, nome: str) -> str:
    msg = f"Olá! Falo com o {nome}? Sou consultor(a) e trabalho com produtos para o seu segmento — posso enviar a tabela?"
    return f"https://wa.me/{digits55}?text={quote_plus(msg)}"


def smart_search_url(row) -> str:
    nome = txt(row.get("NOME FANTASIA")) or txt(row.get("RAZÃO SOCIAL"))
    if not nome:
        return ""
    p = [nome]
    cnpj = digits(txt(row.get("CNPJ")))
    if cnpj:
        p.append(f'"{cnpj}"')
    for c in ("BAIRRO", "MUNICIPIO", "ESTADO"):
        if txt(row.get(c)):
            p.append(txt(row.get(c)))
    tels = all_phones(row)
    if tels:
        p.append(f'"{tels[0][1][2:]}"')
    if not row.get("EMAIL_CONTABILIDADE") and txt(row.get("E-MAIL")):
        p.append(f'"{txt(row.get("E-MAIL"))}"')
    p.append("instagram site google maps whatsapp listar links oficiais e resumo da atividade")
    return "https://www.google.com/search?q=" + quote_plus(" ".join(p)) + "&udm=50&hl=pt-BR&gl=br"

# ══════════════════════════════════════════════════════════════════════════
# 6. FILTROS
# ══════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    # contato
    "email_f": "Todos", "sem_contador": False, "tel_f": "Todos", "wa": False,
    # ramo
    "cnae_p": [], "origem": "Todos", "segmentos": [], "cnae_sec": "",
    # localização
    "endereco": "", "bairros": [], "municipios": [], "cep": "", "estados": [],
    # identificação
    "cnpj": "", "razao": "", "fantasia": "",
    # características
    "matriz": "Todos", "mei": "Todos", "simples": "Todos", "natureza": [],
    "portes": [], "cap_min": 0, "cap_max": 0, "idade": (0, 70), "abertura": (),
    # visão
    "triagem_view": "Todos (não descartados)", "ordem": "Mais completos",
}


def init_state():
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(f"f_{k}", v)
    st.session_state.setdefault("q", "")
    st.session_state.setdefault("limite", 20)
    st.session_state.setdefault("perfil", "pro@achei.com")


def read_filters() -> dict:
    f = {k: st.session_state.get(f"f_{k}", v) for k, v in DEFAULTS.items()}
    f["q"] = st.session_state.get("q", "")
    return f


def reset_filters():
    for k, v in DEFAULTS.items():
        st.session_state[f"f_{k}"] = v
    st.session_state["q"] = ""


def _contains(df, col, term):
    return df[col].astype(str).str.upper().str.contains(term.upper(), na=False, regex=False) \
        if col in df.columns else pd.Series(True, index=df.index)


def apply_filters(df: pd.DataFrame, f: dict, triagem: dict) -> pd.DataFrame:
    m = pd.Series(True, index=df.index)

    if f["q"]:
        sub = pd.Series(False, index=df.index)
        for c in ["NOME FANTASIA", "RAZÃO SOCIAL", "CNPJ", "BAIRRO", "MUNICIPIO", "ENDERECO MAPA"]:
            if c in df.columns:
                sub |= _contains(df, c, f["q"])
        m &= sub

    if f["email_f"] == "Sim":
        m &= df.get("TEM_EMAIL", pd.Series(False, index=df.index))
    elif f["email_f"] == "Não":
        m &= ~df.get("TEM_EMAIL", pd.Series(False, index=df.index))
    if f["sem_contador"] and "EMAIL_CONTABILIDADE" in df.columns:
        m &= ~df["EMAIL_CONTABILIDADE"]
    if f["tel_f"] == "Sim":
        m &= df.get("TEM_TELEFONE", pd.Series(False, index=df.index))
    elif f["tel_f"] == "Não":
        m &= ~df.get("TEM_TELEFONE", pd.Series(False, index=df.index))
    if f["wa"]:
        m &= df["WHATSAPP_1"].astype(str).str.len().gt(0)

    if f["cnae_p"] and "_CNAE_P_LABEL" in df.columns:
        m &= df["_CNAE_P_LABEL"].isin(f["cnae_p"])
    if f["origem"] != "Todos" and "ORIGEM_CNAE" in df.columns:
        m &= df["ORIGEM_CNAE"].eq(f["origem"])
    if f["segmentos"]:
        m &= df["SEGMENTO"].isin(f["segmentos"])
    if f["cnae_sec"]:
        m &= _contains(df, "CNAE_SECUNDARIO_CODIGO", digits(f["cnae_sec"]) or f["cnae_sec"])

    if f["endereco"]:
        m &= _contains(df, "ENDERECO MAPA", f["endereco"])
    if f["cep"]:
        m &= _contains(df, "CEP", digits(f["cep"]))
    for key, col in (("bairros", "BAIRRO"), ("municipios", "MUNICIPIO"), ("estados", "ESTADO"),
                     ("portes", "PORTE"), ("natureza", "NATUREZA_JURIDICA")):
        if f[key] and col in df.columns:
            m &= df[col].isin(f[key])

    if f["cnpj"]:
        m &= _contains(df, "CNPJ", f["cnpj"])
    if f["razao"]:
        m &= _contains(df, "RAZÃO SOCIAL", f["razao"])
    if f["fantasia"]:
        m &= _contains(df, "NOME FANTASIA", f["fantasia"])

    if f["matriz"] != "Todos" and "MATRIZ FILIAL" in df.columns:
        m &= df["MATRIZ FILIAL"].str.upper().eq(f["matriz"].upper())
    for key, col in (("mei", "MEI"), ("simples", "SIMPLES")):
        if f[key] != "Todos" and col in df.columns:
            m &= df[col] if f[key] == "Sim" else ~df[col]

    if "CAPITAL SOCIAL" in df.columns:
        if f["cap_min"]:
            m &= df["CAPITAL SOCIAL"] >= f["cap_min"]
        if f["cap_max"]:
            m &= df["CAPITAL SOCIAL"] <= f["cap_max"]
    if "ANOS_ATIVIDADE" in df.columns:
        a0, a1 = f["idade"]
        m &= df["ANOS_ATIVIDADE"].between(a0, a1)
    if f["abertura"] and len(f["abertura"]) == 2 and "INICIO ATIVIDADE" in df.columns:
        d0, d1 = f["abertura"]
        m &= df["INICIO ATIVIDADE"].between(pd.Timestamp(d0), pd.Timestamp(d1))

    out = df[m].copy()
    out["_TRIAGEM"] = out["CNPJ"].astype(str).map(lambda c: triagem.get(c, {}).get("status", ""))
    view = f["triagem_view"]
    if view == "Todos (não descartados)":
        out = out[out["_TRIAGEM"] != "no"]
    elif view == "Só os que servem":
        out = out[out["_TRIAGEM"].isin(["ok", "star"])]
    elif view == "Só prioridade":
        out = out[out["_TRIAGEM"] == "star"]
    elif view == "Só descartados":
        out = out[out["_TRIAGEM"] == "no"]
    elif view == "Ainda não avaliados":
        out = out[out["_TRIAGEM"] == ""]

    o = f["ordem"]
    if o == "Mais completos" and len(out):
        score = (out["WHATSAPP_1"].astype(str).str.len().gt(0).astype(int) * 3
                 + out.get("TEM_EMAIL", pd.Series(False, index=out.index)).astype(int) * 2
                 + out.get("ORIGEM_CNAE", pd.Series("", index=out.index)).eq("PRINCIPAL").astype(int))
        out = out.assign(_S=score).sort_values("_S", ascending=False).drop(columns="_S")
    elif o == "Maior capital social" and "CAPITAL SOCIAL" in out.columns:
        out = out.sort_values("CAPITAL SOCIAL", ascending=False)
    elif o == "Mais antigas" and "INICIO ATIVIDADE" in out.columns:
        out = out.sort_values("INICIO ATIVIDADE")
    elif o == "Abertas mais recentemente" and "INICIO ATIVIDADE" in out.columns:
        out = out.sort_values("INICIO ATIVIDADE", ascending=False)
    elif o == "Nome (A–Z)":
        out = out.sort_values("RAZÃO SOCIAL")
    return out


def active_chips(f: dict) -> list[tuple[str, str, str]]:
    c = []
    if f["q"]:
        c.append((f'Busca: “{f["q"]}”', "q", ""))
    for key, pref in (("segmentos", ""), ("estados", ""), ("municipios", ""), ("bairros", ""),
                      ("portes", "Porte "), ("natureza", ""), ("cnae_p", "CNAE ")):
        for v in f[key]:
            c.append((f"{pref}{v[:38]}", key, v))
    for key, lab in (("cnpj", "CNPJ"), ("razao", "Razão social"), ("fantasia", "Nome fantasia"),
                     ("endereco", "Endereço"), ("cep", "CEP"), ("cnae_sec", "CNAE secundário")):
        if f[key]:
            c.append((f"{lab}: {f[key]}", key, ""))
    for key, lab in (("email_f", "E-mail"), ("tel_f", "Telefone"), ("origem", "Origem CNAE"),
                     ("matriz", "Matriz/Filial"), ("mei", "MEI"), ("simples", "Simples")):
        if f[key] not in ("Todos",):
            c.append((f"{lab}: {f[key]}", key, ""))
    if f["sem_contador"]:
        c.append(("Sem e-mail de contador", "sem_contador", ""))
    if f["wa"]:
        c.append(("Com WhatsApp", "wa", ""))
    if f["cap_min"]:
        c.append((f'Capital ≥ {fmt_capital(f["cap_min"])}', "cap_min", ""))
    if f["cap_max"]:
        c.append((f'Capital ≤ {fmt_capital(f["cap_max"])}', "cap_max", ""))
    if tuple(f["idade"]) != DEFAULTS["idade"]:
        c.append((f'{f["idade"][0]}–{f["idade"][1]} anos', "idade", ""))
    if f["abertura"] and len(f["abertura"]) == 2:
        c.append((f'Abertura {f["abertura"][0]:%d/%m/%Y}–{f["abertura"][1]:%d/%m/%Y}', "abertura", ""))
    return c

# ══════════════════════════════════════════════════════════════════════════
# 7. CARD DE LEAD
# ══════════════════════════════════════════════════════════════════════════
def card_html(row, status: str, nomes: dict) -> str:
    nome, legal = display_names(row)
    nome_e, legal_e = escape(nome), escape(legal)
    cnpj = txt(row.get("CNPJ"))
    cnpj_d = digits(cnpj)

    end = escape(txt(row.get("ENDERECO MAPA")) or "Endereço não informado")
    bairro, mun, uf = txt(row.get("BAIRRO")), txt(row.get("MUNICIPIO")), txt(row.get("ESTADO"))
    cep = txt(row.get("CEP"))
    cep_f = f"{cep[:5]}-{cep[5:]}" if len(digits(cep)) == 8 else cep
    linha2 = escape(" · ".join(p for p in [f"{mun} — {uf}" if mun else uf, f"CEP {cep_f}" if cep else ""] if p))

    # Contatos: ícones para cada telefone + e-mail miúdo
    rows_c = ""
    for fmt, d55 in all_phones(row):
        rows_c += (
            f'<div class="c-row"><span class="c-num">{fmt}</span>'
            f'<a class="ic ic-wa" href="{wa_link(d55, nome_e)}" target="_blank" title="Abrir WhatsApp com mensagem pronta">{I_WA}</a>'
            f'<a class="ic" href="tel:+{d55}" title="Ligar para {fmt}">{I_TEL}</a>'
            f'<a class="ic" href="javascript:void(0)" onclick="navigator.clipboard.writeText(\'{fmt}\')" title="Copiar {fmt}">{I_COPY}</a>'
            f'</div>')
    email = txt(row.get("E-MAIL"))
    if email:
        contab = bool(row.get("EMAIL_CONTABILIDADE"))
        rows_c += (
            f'<div class="c-row"><span class="c-mail" title="{escape(email)}'
            f'{" (e-mail do escritório de contabilidade)" if contab else ""}">{escape(email.lower())}</span>'
            f'<a class="ic" href="mailto:{escape(email)}" title="Enviar e-mail">{I_MAIL}</a>'
            f'<a class="ic" href="javascript:void(0)" onclick="navigator.clipboard.writeText(\'{escape(email)}\')" title="Copiar e-mail">{I_COPY}</a>'
            f'</div>')
    if not rows_c:
        rows_c = '<div class="c-none">Nenhum telefone ou e-mail neste cadastro</div>'

    # CNAE principal + label de beleza + todos os secundários
    cp = txt(row.get("CNAE_PRINCIPAL_CODIGO"))
    nome_p = escape(nomes.get(cp) or txt(row.get("CNAE_PRINCIPAL_NOME")) or "Atividade não identificada")
    is_b = cp in BEAUTY_CNAES
    flag = (f'<div class="cn-flag cn-flag-ok">✓ Beleza no CNAE principal · {BEAUTY_CNAES[cp]}</div>'
            if is_b else '<div class="cn-flag cn-flag-no">CNAE principal fora da beleza</div>')
    secs = sec_cnaes(row, nomes)
    n_b_sec = sum(1 for _, _, b in secs if b)
    if not is_b and n_b_sec:
        flag += f'<div class="cn-flag cn-flag-ok">✓ Beleza em {n_b_sec} CNAE secundário(s)</div>'
    sec_html = ""
    if secs:
        sec_html = f'<div class="cn-sub-h">ATIVIDADES SECUNDÁRIAS ({len(secs)})</div>' + "".join(
            f'<div class="cn-line {"cn-line-ok" if b else ""}"><b>{c}</b><i title="{escape(n)}">{escape(n)}</i></div>'
            for c, n, b in secs)

    # Badges factuais
    dt = row.get("INICIO ATIVIDADE")
    anos = row.get("ANOS_ATIVIDADE")
    abertura = (f'{pd.to_datetime(dt):%d/%m/%Y} ({int(anos)} anos)'
                if pd.notna(dt) and pd.notna(anos) else "Abertura não informada")
    bdgs = [f'<span class="bdg" title="Data de abertura na Receita Federal">Abertura: {abertura}</span>',
            f'<span class="bdg" title="Porte">{escape(txt(row.get("PORTE")) or "—")}</span>',
            f'<span class="bdg" title="Capital social declarado">Capital {fmt_capital(row.get("CAPITAL SOCIAL", 0))}</span>']
    if txt(row.get("MATRIZ FILIAL")):
        bdgs.append(f'<span class="bdg" title="Matriz ou filial">{escape(txt(row.get("MATRIZ FILIAL")))}</span>')
    if row.get("SIMPLES"):
        bdgs.append('<span class="bdg" title="Optante pelo Simples Nacional">Simples</span>')
    if row.get("MEI"):
        bdgs.append('<span class="bdg" title="Microempreendedor individual">MEI</span>')
    if txt(row.get("NATUREZA_JURIDICA")):
        bdgs.append(f'<span class="bdg" title="Natureza jurídica">{escape(txt(row.get("NATUREZA_JURIDICA")).title())}</span>')
    if row.get("EMAIL_CONTABILIDADE"):
        bdgs.append('<span class="bdg bdg-warn" title="O e-mail cadastrado é do escritório de contabilidade">E-mail do contador</span>')

    maps = txt(row.get("MAPS")) or ("https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{end} {mun} {uf}"))
    rf = txt(row.get("RECEITA FEDERAL")) or (
        f"http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/Cnpjreva_Solicitacao.asp?cnpj={cnpj_d}" if cnpj_d else "")
    ia = smart_search_url(row)
    ig = txt(row.get("SITE")) or ("https://www.google.com/search?q=" + quote_plus(f"{nome} {mun} instagram"))
    links = (
        f'<a class="lk" href="{escape(ia, True)}" target="_blank" title="Busca com IA do Google: site, redes e dono">{I_SPARK} Busca IA</a>'
        f'<a class="lk" href="{escape(ig, True)}" target="_blank" title="Procurar o perfil no Instagram">{I_CAM} Instagram</a>'
        f'<a class="lk" href="{escape(maps, True)}" target="_blank" title="Ver no Google Maps">{I_PIN} Maps</a>'
        + (f'<a class="lk" href="{escape(rf, True)}" target="_blank" title="Consultar cadastro na Receita Federal">{I_DOC} Receita</a>'
           if rf else f'<span class="lk dis">{I_DOC} Receita</span>'))

    tg = ""
    for key in ("ok", "star", "no"):
        meta = TRIAGE_META[key]
        on = f' {meta["btn"]}' if status == key else ""
        tg += (f'<a class="tg{on}" href="?t={key}&c={quote_plus(cnpj)}" '
               f'title="Marcar como {meta["label"].lower()}">{meta["icon"]} {meta["label"]}</a>')

    cls = TRIAGE_META.get(status, {}).get("cls", "")
    return f"""
<div class="lead {cls}">
  <div class="l-head">
    <div class="l-name">{nome_e}</div>
    {f'<div class="l-legal">{legal_e}</div>' if legal_e else ''}
    <div class="l-cnpj">{escape(cnpj)}
      <a class="ic" style="width:22px;height:22px" href="javascript:void(0)"
         onclick="navigator.clipboard.writeText('{escape(cnpj)}')" title="Copiar CNPJ">{I_COPY}</a></div>
    <div class="l-addr">{I_PIN}<span>{end}<br>{linha2}</span></div>
  </div>
  <div class="l-contacts">{rows_c}</div>
  <div class="l-cnae">{flag}<div class="cn-main"><b style="font-family:var(--mono);font-size:11px;flex-shrink:0">{escape(cp)}</b><span>{nome_p}</span></div>{sec_html}</div>
  <div class="l-badges">{''.join(bdgs)}</div>
  <div class="l-links">{links}</div>
  <div class="l-triage">{tg}</div>
</div>"""


def render_leads(df: pd.DataFrame, nomes: dict, limite: int | None = None):
    if df.empty:
        st.markdown('<div class="empty"><b>Nenhum lead com esses filtros</b>'
                    'Remova um filtro nos chips acima ou amplie a busca.</div>', unsafe_allow_html=True)
        return
    triagem = load_triage()
    page = df if limite is None else df.head(limite)
    cards = "".join(card_html(r, triagem.get(str(r.get("CNPJ")), {}).get("status", ""), nomes)
                    for _, r in page.iterrows())
    st.markdown(minify(f'<div class="leads">{cards}</div>'), unsafe_allow_html=True)
    if limite is not None and len(df) > limite:
        rest = len(df) - limite
        if st.button(f"Carregar mais {min(20, rest)} de {rest} restantes", use_container_width=True, key="more"):
            st.session_state.limite += 20
            st.rerun()


def bar(series, color="#1f1e1c", height=None):
    s = series[::-1]
    fig = go.Figure(go.Bar(x=s.values, y=[str(i)[:38] for i in s.index], orientation="h",
                           marker_color=color, text=s.values, textposition="outside",
                           hovertemplate="%{y}: %{x}<extra></extra>"))
    fig.update_layout(margin=dict(l=0, r=34, t=6, b=6), height=height or max(200, len(s) * 30),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="DM Sans", size=11.5, color="#6b6862"),
                      xaxis=dict(visible=False), yaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════════════════
# 8. APP
# ══════════════════════════════════════════════════════════════════════════
def main():
    init_state()
    triagem = load_triage()

    qp = st.query_params
    if "t" in qp and "c" in qp:
        set_triage(qp["c"], qp["t"])
        st.query_params.clear()
        st.rerun()
    if "rm" in qp:
        key, _, val = qp["rm"].partition("|")
        if key == "q":
            st.session_state["q"] = ""
        elif key in DEFAULTS:
            if val and isinstance(DEFAULTS[key], list):
                st.session_state[f"f_{key}"] = [v for v in st.session_state.get(f"f_{key}", []) if v != val]
            else:
                st.session_state[f"f_{key}"] = DEFAULTS[key]
        st.query_params.clear()
        st.rerun()

    with st.sidebar:
        st.markdown('<div style="font-size:14px;font-weight:600;margin-bottom:10px;">Conta e base de dados</div>',
                    unsafe_allow_html=True)
        perfil = st.selectbox("Perfil (simulação de plano)", list(PERFIS.keys()),
                              format_func=lambda e: f"{PERFIS[e]['nome']} · {TIER_CFG[PERFIS[e]['tier']]['label']}",
                              index=list(PERFIS.keys()).index(st.session_state.perfil),
                              help="Troca o plano simulado — muda o limite de exportação.")
        if perfil != st.session_state.perfil:
            st.session_state.perfil = perfil
            st.rerun()
        st.divider()
        up = st.file_uploader("Enviar sua base (CSV ou Excel)", type=["csv", "xlsx", "xls"],
                             help="Exportação da Receita Federal / AcheiMeuCliente. Sem arquivo, uso a base do projeto.")
        if up is not None:
            try:
                st.session_state.df_up = load_upload(up.getvalue(), up.name)
                st.caption(f"{len(st.session_state.df_up)} registros de {up.name}")
            except Exception as e:
                st.error(f"Não consegui ler o arquivo: {e}")
        if st.session_state.get("triagem_ro"):
            st.warning("A triagem não pôde ser gravada em disco — use o download na aba Triagem.")

    df_full = st.session_state.get("df_up")
    fonte = "sua base enviada"
    if df_full is None:
        df_full, fonte = load_repo_csv(), "base do projeto"
    if df_full is None:
        df_full, fonte = _mock(), "base de demonstração"
    nomes = cnae_names(df_full)

    user = PERFIS[st.session_state.perfil]
    tier = TIER_CFG[user["tier"]]

    st.markdown(
        f'<div class="appbar"><div class="mark">◍</div>'
        f'<div><div class="appname">AcheiMeuCliente</div>'
        f'<div class="appsub">{escape(user["nome"])} · {len(df_full)} empresas na {fonte}</div></div>'
        f'<span class="chip-plan"><i></i>Plano {tier["label"]}</span></div>', unsafe_allow_html=True)

    st.text_input("Buscar", key="q", label_visibility="collapsed",
                  placeholder="Buscar por nome, CNPJ, endereço, bairro ou cidade",
                  help="Busca livre em nome fantasia, razão social, CNPJ, endereço, bairro e cidade.")

    f_prev = read_filters()
    n_ativos = len(active_chips(f_prev))
    with st.expander(f"Filtros{f'  ·  {n_ativos} ativos' if n_ativos else '  ·  todos os campos da base'}",
                     expanded=False):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('<div class="f-group">CONTATO</div>', unsafe_allow_html=True)
            st.selectbox("Empresas com e-mail?", ["Todos", "Sim", "Não"], key="f_email_f",
                         help="Sim = só quem tem e-mail cadastrado na Receita.")
            st.selectbox("Empresas com telefone?", ["Todos", "Sim", "Não"], key="f_tel_f",
                         help="Sim = só quem tem pelo menos um telefone.")
            st.checkbox("Só com WhatsApp", key="f_wa", help="Deixa apenas quem tem número de WhatsApp identificado.")
            st.checkbox("Excluir e-mail de contadores", key="f_sem_contador",
                        help="O e-mail do escritório de contabilidade não chega ao dono do negócio.")

            st.markdown('<div class="f-group">RAMO DE ATIVIDADE</div>', unsafe_allow_html=True)
            cnae_opts = sorted(df_full["_CNAE_P_LABEL"].dropna().unique()) if "_CNAE_P_LABEL" in df_full else []
            st.multiselect("Atividade principal (CNAE)", cnae_opts, key="f_cnae_p",
                           help="CNAE principal registrado — a atividade central da empresa.")
            st.selectbox("Origem do CNAE de beleza", ["Todos", "PRINCIPAL", "SECUNDARIO"], key="f_origem",
                         help="PRINCIPAL = beleza é o negócio central. SECUNDARIO = beleza é atividade extra.")
            st.multiselect("Segmento de beleza", SEGMENTOS, key="f_segmentos",
                           help="Agrupamento do CNAE principal: salão, clínica, loja, distribuidor, fábrica.")
            st.text_input("CNAE secundário contém", key="f_cnae_sec", placeholder="ex: 9602501",
                          help="Filtra pelo código dentro da lista de atividades secundárias.")

        with c2:
            st.markdown('<div class="f-group">LOCALIZAÇÃO</div>', unsafe_allow_html=True)
            ufs = sorted(x for x in df_full.get("ESTADO", pd.Series(dtype=str)).dropna().unique() if x)
            st.multiselect("Estado (UF)", ufs, key="f_estados")
            base_m = df_full[df_full["ESTADO"].isin(st.session_state.f_estados)] if st.session_state.f_estados else df_full
            muns = sorted(x for x in base_m.get("MUNICIPIO", pd.Series(dtype=str)).dropna().unique() if x)
            st.session_state.f_municipios = [m for m in st.session_state.f_municipios if m in muns]
            st.multiselect("Município", muns, key="f_municipios", help="Escolha o estado primeiro para encurtar a lista.")
            base_b = df_full[df_full["MUNICIPIO"].isin(st.session_state.f_municipios)] if st.session_state.f_municipios else base_m
            bais = sorted(x for x in base_b.get("BAIRRO", pd.Series(dtype=str)).dropna().unique() if x)
            st.session_state.f_bairros = [b for b in st.session_state.f_bairros if b in bais]
            st.multiselect("Bairro", bais, key="f_bairros", help="Útil para montar rota de visita a pé.")
            st.text_input("Endereço contém", key="f_endereco", placeholder="ex: AVENIDA PADRE JULIO",
                          help="Busca dentro do endereço cadastrado — rua, avenida, número.")
            st.text_input("CEP", key="f_cep", placeholder="ex: 68900", help="Aceita CEP parcial.")

            st.markdown('<div class="f-group">IDENTIFICAÇÃO</div>', unsafe_allow_html=True)
            st.text_input("CNPJ", key="f_cnpj", placeholder="com ou sem pontuação")
            st.text_input("Razão social contém", key="f_razao")
            st.text_input("Nome fantasia contém", key="f_fantasia")

        with c3:
            st.markdown('<div class="f-group">CARACTERÍSTICAS</div>', unsafe_allow_html=True)
            st.multiselect("Porte", ["MEI", "ME", "EPP", "Grande"], key="f_portes",
                           help="MEI e ME são os menores; EPP e Grande têm mais estrutura de compra.")
            mfs = sorted(x for x in df_full.get("MATRIZ FILIAL", pd.Series(dtype=str)).dropna().unique() if x)
            st.selectbox("Matriz ou filial", ["Todos"] + mfs, key="f_matriz")
            st.selectbox("MEI?", ["Todos", "Sim", "Não"], key="f_mei",
                         help="Não = tira os microempreendedores individuais da lista.")
            st.selectbox("Simples Nacional?", ["Todos", "Sim", "Não"], key="f_simples")
            nats = sorted(x for x in df_full.get("NATUREZA_JURIDICA", pd.Series(dtype=str)).dropna().unique() if x)
            st.multiselect("Natureza jurídica", nats, key="f_natureza",
                           help="Ltda, empresário individual, S/A — indica o tamanho da estrutura societária.")
            cc1, cc2 = st.columns(2)
            cc1.number_input("Capital social mínimo", min_value=0, step=1000, key="f_cap_min")
            cc2.number_input("Capital social máximo", min_value=0, step=1000, key="f_cap_max",
                             help="Deixe 0 para não limitar.")
            st.slider("Idade da empresa (anos)", 0, 70, key="f_idade",
                      help="Muito nova ainda está montando; muito antiga já tem fornecedor fixo.")
            if "INICIO ATIVIDADE" in df_full.columns and df_full["INICIO ATIVIDADE"].notna().any():
                st.date_input("Data de abertura (intervalo)", key="f_abertura",
                              min_value=date(1900, 1, 1), max_value=date.today(),
                              help="Vazio = sem filtro. Escolha duas datas para limitar o período.")

        st.divider()
        c4, c5, c6 = st.columns([1, 1, 1])
        with c4:
            st.selectbox("Mostrar", ["Todos (não descartados)", "Só os que servem", "Só prioridade",
                                     "Ainda não avaliados", "Só descartados", "Tudo, inclusive descartados"],
                         key="f_triagem_view", help="Filtra pela sua triagem (✓ serve, ★ prioridade, ✕ não serve).")
        with c5:
            st.selectbox("Ordenar por", ["Mais completos", "Maior capital social", "Abertas mais recentemente",
                                         "Mais antigas", "Nome (A–Z)"], key="f_ordem",
                         help="“Mais completos” põe primeiro quem tem WhatsApp, e-mail e CNAE principal de beleza.")
        with c6:
            st.markdown('<div style="height:26px"></div>', unsafe_allow_html=True)
            if st.button("Limpar todos os filtros", use_container_width=True):
                reset_filters()
                st.session_state.limite = 20
                st.rerun()

    filters = read_filters()
    df = apply_filters(df_full, filters, triagem)

    chips = active_chips(filters)
    if chips:
        html = "".join(
            f'<a class="chip" href="?rm={quote_plus(k)}{"|" + quote_plus(str(v)) if v else ""}" '
            f'title="Remover este filtro"><b>{escape(str(l))}</b><span>×</span></a>' for l, k, v in chips)
        st.markdown(minify(f'<div class="chips">{html}</div>'), unsafe_allow_html=True)

    total = len(df)
    n_wa = int(df["WHATSAPP_1"].astype(str).str.len().gt(0).sum()) if total else 0
    n_mail = int(df.get("TEM_EMAIL", pd.Series(dtype=bool)).sum()) if total else 0
    n_ok = int(df["_TRIAGEM"].isin(["ok", "star"]).sum()) if total else 0
    idade_media = df["ANOS_ATIVIDADE"].mean() if total and "ANOS_ATIVIDADE" in df else 0
    st.markdown(minify(f"""
    <div class="kpis">
      <div class="kpi"><div class="kpi-l">Leads no filtro</div><div class="kpi-v">{total}</div>
        <div class="kpi-s">de {len(df_full)} na base</div></div>
      <div class="kpi"><div class="kpi-l">Com WhatsApp</div><div class="kpi-v">{n_wa}</div>
        <div class="kpi-s">{(n_wa/total*100 if total else 0):.0f}% abordáveis hoje</div></div>
      <div class="kpi"><div class="kpi-l">Com e-mail</div><div class="kpi-v">{n_mail}</div>
        <div class="kpi-s">{(n_mail/total*100 if total else 0):.0f}% do filtro</div></div>
      <div class="kpi"><div class="kpi-l">Idade média</div><div class="kpi-v">{idade_media:.0f}</div>
        <div class="kpi-s">anos de atividade</div></div>
      <div class="kpi"><div class="kpi-l">Aprovados por você</div><div class="kpi-v">{n_ok}</div>
        <div class="kpi-s">✓ serve ou ★ prioridade</div></div>
    </div>"""), unsafe_allow_html=True)

    t_leads, t_triagem, t_resumo, t_export = st.tabs(["Leads", "Minha triagem", "Resumo", "Exportar"])

    with t_leads:
        st.markdown(f'<div class="count-line"><b>{total} leads</b> · ordenados por {filters["ordem"].lower()} · '
                    f'avalie com ✓ / ★ / ✕ no fim de cada card</div>', unsafe_allow_html=True)
        render_leads(df, nomes, st.session_state.limite)

    with t_triagem:
        marcados = df_full[df_full["CNPJ"].astype(str).isin(triagem.keys())].copy()
        if marcados.empty:
            st.markdown('<div class="empty"><b>Nada avaliado ainda</b>'
                        'Use ✓ Serve · ★ Prioridade · ✕ Não serve no rodapé de cada card.</div>',
                        unsafe_allow_html=True)
        else:
            marcados["_TRIAGEM"] = marcados["CNPJ"].astype(str).map(lambda c: triagem[c]["status"])
            n = marcados["_TRIAGEM"].value_counts()
            st.markdown(f'<div class="count-line"><b>{len(marcados)} avaliados</b> · '
                        f'{int(n.get("star",0))} prioridade · {int(n.get("ok",0))} servem · '
                        f'{int(n.get("no",0))} descartados · gravado no servidor</div>', unsafe_allow_html=True)
            escolha = st.radio("Ver", ["Prioridade", "Servem", "Descartados"], horizontal=True,
                               label_visibility="collapsed")
            alvo = {"Prioridade": "star", "Servem": "ok", "Descartados": "no"}[escolha]
            render_leads(marcados[marcados["_TRIAGEM"] == alvo], nomes)
            st.download_button("Baixar minha triagem (CSV)",
                               marcados.assign(TRIAGEM=marcados["_TRIAGEM"]).to_csv(sep=";", index=False).encode("utf-8-sig"),
                               file_name=f"triagem_{datetime.now():%Y%m%d}.csv", mime="text/csv")

    with t_resumo:
        if total == 0:
            st.markdown('<div class="empty"><b>Sem dados no filtro atual</b>Limpe os filtros para ver o resumo.</div>',
                        unsafe_allow_html=True)
        else:
            r1, r2 = st.columns(2)
            with r1:
                st.markdown('<div class="section-l">ATIVIDADE PRINCIPAL (CNAE)</div>', unsafe_allow_html=True)
                bar(df["_CNAE_P_LABEL"].value_counts().head(8) if "_CNAE_P_LABEL" in df
                    else df["CNAE_PRINCIPAL_CODIGO"].value_counts().head(8))
            with r2:
                st.markdown('<div class="section-l">ATIVIDADE SECUNDÁRIA (CNAE)</div>', unsafe_allow_html=True)
                sec_all = []
                for _, r in df.iterrows():
                    sec_all += [f"{c} — {n[:34]}" for c, n, _ in sec_cnaes(r, nomes)]
                if sec_all:
                    bar(pd.Series(sec_all).value_counts().head(8), color="#3f7d58")
                else:
                    st.markdown('<div class="note">Nenhuma atividade secundária nesta seleção.</div>',
                                unsafe_allow_html=True)
            r3, r4 = st.columns(2)
            with r3:
                st.markdown('<div class="section-l">EMPRESAS POR MUNICÍPIO</div>', unsafe_allow_html=True)
                bar(df["MUNICIPIO"].replace("", "Não informado").value_counts().head(10), color="#b8562f")
            with r4:
                st.markdown('<div class="section-l">EMPRESAS POR BAIRRO</div>', unsafe_allow_html=True)
                bar(df["BAIRRO"].replace("", "Não informado").value_counts().head(10))

            st.markdown('<div class="section-l">TABELA COMPLETA</div>', unsafe_allow_html=True)
            tabela = pd.DataFrame({
                "Estabelecimento": [display_names(r)[0] for _, r in df.iterrows()],
                "CNPJ": df["CNPJ"],
                "Endereço": df.get("ENDERECO MAPA", ""),
                "Cidade/UF": df["MUNICIPIO"].astype(str) + "/" + df["ESTADO"].astype(str),
                "Telefones": [" · ".join(p for p, _ in all_phones(r)) for _, r in df.iterrows()],
                "E-mail": df.get("E-MAIL", ""),
                "Porte": df.get("PORTE", ""),
                "Capital": [fmt_capital(v) for v in df.get("CAPITAL SOCIAL", pd.Series(0, index=df.index))],
                "Idade": [f"{v:.0f} anos" for v in df.get("ANOS_ATIVIDADE", pd.Series(0, index=df.index))],
                "Triagem": df["_TRIAGEM"].map({"ok": "✓ Serve", "star": "★ Prioridade", "no": "✕ Não"}).fillna("—"),
            })
            st.dataframe(tabela, use_container_width=True, hide_index=True, height=430)

    with t_export:
        limite_plano = tier["limit"]
        if limite_plano == 0:
            st.markdown('<div class="note">O plano <b>Explorador</b> não permite download. '
                        'Troque o perfil na barra lateral para testar a exportação.</div>', unsafe_allow_html=True)
        else:
            qtd = min(total, limite_plano)
            st.markdown(f'<div class="count-line">Vai baixar <b>{qtd} leads</b> — exatamente os que estão no '
                        f'filtro atual. Seu plano {tier["label"]} permite até {limite_plano} por arquivo.</div>',
                        unsafe_allow_html=True)
            df_exp = df.drop(columns=[c for c in ("_TRIAGEM", "_CNAE_P_LABEL") if c in df.columns]).head(limite_plano)
            e1, e2 = st.columns(2)
            with e1:
                st.markdown('<div class="exp-card"><h4>Planilha Excel</h4><p>Abre direto no Excel ou Google '
                            'Planilhas, colunas já formatadas. Use se vai trabalhar a lista na mão.</p></div>',
                            unsafe_allow_html=True)
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as w:
                    df_exp.to_excel(w, index=False, sheet_name="Leads")
                st.download_button("Baixar .xlsx", buf.getvalue(), file_name=f"leads_{datetime.now():%Y%m%d}.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True, type="primary")
            with e2:
                st.markdown('<div class="exp-card"><h4>Arquivo CSV</h4><p>Formato de importação: use para subir a '
                            'lista em CRM, discador ou ferramenta de disparo. Separador ponto e vírgula.</p></div>',
                            unsafe_allow_html=True)
                st.download_button("Baixar .csv", df_exp.to_csv(sep=";", index=False).encode("utf-8-sig"),
                                   file_name=f"leads_{datetime.now():%Y%m%d}.csv", mime="text/csv",
                                   use_container_width=True)


if __name__ == "__main__":
    main()
