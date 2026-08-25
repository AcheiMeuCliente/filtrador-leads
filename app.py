"""
AcheiMeuCliente — Plataforma de Inteligência de Mercado para Beleza
app.py — dashboard Streamlit de arquivo único (Streamlit Community Cloud / Local)
Versão Consolidada: Agregação Completa de Todas as Funcionalidades + Visual Moderno
"""

import os
import re
import math
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from io import BytesIO
from html import escape

# ══════════════════════════════════════════════════════════════
# 1. CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AcheiMeuCliente · Inteligência de Mercado",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# 2. DESIGN SYSTEM (Slate + Indigo + Notion / Linear)
# ══════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root{
  --bg:#f8fafc;
  --bg-tint:#f1f5f9;
  --surface:#ffffff;
  --surface-2:#fafaf9;
  --surface-sunk:#f1f5f9;
  --border:#e2e8f0;
  --border-strong:#cbd5e1;
  --text:#0f172a;
  --text-2:#475569;
  --muted:#94a3b8;

  --navy:#1e1b4b;
  --navy-2:#312e81;
  --purple:#4f46e5;
  --purple-dark:#4338ca;
  --purple-soft:#eeeffd;
  --coral:#e2603f;
  --coral-dark:#c74d2f;
  --coral-soft:#fdece6;
  --gold:#c98a1c;
  --gold-soft:#faf1de;

  --accent:#4f46e5;
  --accent-soft:#eeeffd;
  --green:#047857;
  --green-soft:#ecfdf5;
  --amber:#b45309;
  --amber-soft:#fef3c7;
  --red:#c23b2e;
  --red-soft:#fcebe8;

  --radius:12px;
  --radius-sm:8px;
  --shadow-sm:0 1px 2px rgba(15,23,42,.04), 0 1px 1px rgba(15,23,42,.03);
  --shadow-md:0 4px 14px rgba(15,23,42,.07), 0 1px 3px rgba(15,23,42,.05);
  --shadow-lg:0 12px 28px rgba(15,23,42,.12), 0 2px 6px rgba(15,23,42,.06);
  --font:"Plus Jakarta Sans", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --mono:ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"]{
  font-family:var(--font) !important;
  color:var(--text);
}
[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1100px 420px at 100% -8%, rgba(79,70,229,.05), transparent 60%),
    radial-gradient(900px 380px at -6% 0%, rgba(30,27,75,.04), transparent 55%),
    var(--bg);
}
[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:1.6rem; padding-bottom:4rem; max-width:1400px; }

h1,h2,h3,h4,h5{ font-family:var(--font) !important; color:var(--text) !important; letter-spacing:-0.02em; }
hr{ border-color:var(--border) !important; margin:1.1rem 0 !important; }
p, span, div, label{ letter-spacing:-0.005em; }

/* ══════════════════════ SIDEBAR (White/Light Benchmark Theme) ══════════════════════ */
[data-testid="stSidebar"]{
  background:#ffffff !important;
  border-right:1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] .block-container{ padding-top:1.2rem; padding-left:1rem; padding-right:1rem; }
[data-testid="stSidebar"] *{ color:#1e293b; }
[data-testid="stSidebar"] .sec-label{
  color:#6366f1 !important; font-size:11px !important; font-weight:700 !important;
  letter-spacing:.06em !important; text-transform:uppercase; margin:14px 0 8px !important;
  display:flex; align-items:center; gap:6px;
}

/* Sidebar Expanders */
[data-testid="stSidebar"] [data-testid="stExpander"]{
  border:1px solid #e2e8f0 !important;
  border-radius:12px !important;
  background:#ffffff !important;
  margin-bottom:10px !important;
  box-shadow:0 1px 3px rgba(0,0,0,0.02) !important;
  overflow:hidden !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary{
  padding:10px 14px !important;
  background:#f8fafc !important;
  border-bottom:1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover{
  background:#f1f5f9 !important;
}
[data-testid="stSidebar"] summary p{
  font-size:13px !important;
  font-weight:700 !important;
  color:#0f172a !important;
}
[data-testid="stSidebar"] label p{
  font-size:12.5px !important;
  color:#334155 !important;
}

/* Sidebar Inputs & Selects */
[data-testid="stSidebar"] [data-baseweb="select"] > div{
  background:#f8fafc !important;
  border:1px solid #e2e8f0 !important;
  color:#0f172a !important;
  border-radius:8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div{
  color:#0f172a !important;
}
[data-testid="stSidebar"] [data-baseweb="input"]{
  background:#f8fafc !important;
  border:1px solid #e2e8f0 !important;
  border-radius:8px !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input{
  color:#0f172a !important;
  background:transparent !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input::placeholder{
  color:#94a3b8 !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"]{
  background:#4f46e5 !important;
  color:#ffffff !important;
  border-radius:6px !important;
}

/* Sidebar File Uploader */
[data-testid="stSidebar"] [data-testid="stFileUploader"]{
  background:#f8fafc;
  border:1px dashed #cbd5e1;
  border-radius:10px;
  padding:8px;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] section{
  background:transparent !important;
  padding:4px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] span,
[data-testid="stSidebar"] [data-testid="stFileUploader"] small{
  color:#64748b !important;
}

/* Sidebar Buttons & Reset */
[data-testid="stSidebar"] .stButton > button{
  background:#f8fafc !important;
  border:1px solid #e2e8f0 !important;
  color:#334155 !important;
  border-radius:8px !important;
  font-size:12px !important;
  font-weight:600 !important;
  padding:6px 12px !important;
  transition:all .12s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover{
  background:#eef2ff !important;
  border-color:#c7d2fe !important;
  color:#4338ca !important;
}
[data-testid="stSidebar"] hr{ border-color:#e2e8f0 !important; margin:12px 0 !important; }

/* Preset Card Styling */
.preset-card-item{
  background:#f8fafc;
  border:1px solid #e2e8f0;
  border-radius:10px;
  padding:9px 12px;
  margin-bottom:7px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  transition:all .12s ease;
}
.preset-card-item:hover{
  background:#f1f5f9;
  border-color:#cbd5e1;
}

/* Sidebar Header Bar */
.sidebar-header-bar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding-bottom:10px;
  margin-bottom:12px;
  border-bottom:1px solid #e2e8f0;
}
.sidebar-title{
  font-size:15px;
  font-weight:800;
  color:#0f172a;
  display:flex;
  align-items:center;
  gap:8px;
}
.sidebar-counter{
  background:#4f46e5;
  color:#ffffff;
  font-size:11px;
  font-weight:700;
  width:20px;
  height:20px;
  border-radius:50%;
  display:inline-flex;
  align-items:center;
  justify-content:center;
}

/* ── Botões Globais ── */
.stButton>button, .stDownloadButton>button{
  border-radius:var(--radius-sm); border:1px solid var(--border-strong); background:var(--surface);
  color:var(--text); font-size:12.5px; font-weight:600; box-shadow:var(--shadow-sm);
  transition:all .12s ease;
}
.stButton>button:hover, .stDownloadButton>button:hover{
  background:var(--surface-2); border-color:var(--muted); color:var(--text);
}
.stButton>button:active{ transform:scale(.98); }
.stButton>button[kind="primary"], .stDownloadButton>button{
  background:var(--purple); border-color:var(--purple); color:#fff;
}
.stButton>button[kind="primary"]:hover, .stDownloadButton>button:hover{
  background:var(--purple-dark); border-color:var(--purple-dark); color:#fff;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid var(--border); }
.stTabs [data-baseweb="tab"]{
  height:38px; padding:0 14px; background:transparent; font-size:13px;
  font-weight:600; color:var(--text-2); border-radius:8px 8px 0 0;
}
.stTabs [data-baseweb="tab"]:hover{ background:var(--surface-2); }
.stTabs [aria-selected="true"]{ color:var(--purple) !important; border-bottom:2.5px solid var(--purple); background:var(--surface-2); }

/* ── Topbar ── */
.topbar{ display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:2px; }
.brand{ display:flex; align-items:center; gap:12px; }
.brand-mark{
  width:38px; height:38px; border-radius:10px; color:#fff;
  background:linear-gradient(135deg, var(--navy) 0%, var(--purple) 100%);
  display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:800;
  box-shadow:var(--shadow-md);
}
.brand-name{ font-size:20px; font-weight:800; letter-spacing:-0.02em; color:var(--text); }
.brand-sub{ font-size:12.5px; color:var(--text-2); margin-top:1px; }
.plan-chip{
  display:inline-flex; align-items:center; gap:6px; font-size:11px; font-weight:700;
  padding:4px 10px; border-radius:20px; border:1px solid #c7d2fe;
  background:var(--purple-soft); color:var(--purple-dark); margin-left:10px; vertical-align:middle;
  text-transform:uppercase; letter-spacing:.04em;
}
.plan-dot{ width:6px; height:6px; border-radius:50%; background:var(--green); box-shadow:0 0 0 3px var(--green-soft); }

.sec-label{
  font-size:10.5px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
  color:var(--muted); margin:6px 0 10px;
}

/* ══════════════════════ KPIs ══════════════════════ */
.kpi{
  background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--kpi-c, var(--navy));
  border-radius:var(--radius); padding:15px 17px; height:100%; box-shadow:var(--shadow-sm);
  transition:box-shadow .15s ease, transform .15s ease;
}
.kpi:hover{ box-shadow:var(--shadow-md); transform:translateY(-1px); }
.kpi-top{ display:flex; align-items:center; justify-content:space-between; }
.kpi-label{ font-size:11px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; color:var(--muted); }
.kpi-icon{ width:26px; height:26px; border-radius:7px; display:flex; align-items:center; justify-content:center;
  background:var(--kpi-soft, var(--purple-soft)); color:var(--kpi-c, var(--purple)); flex-shrink:0; }
.kpi-value{ font-size:28px; font-weight:800; letter-spacing:-0.03em; color:var(--text); margin-top:8px; line-height:1.05; }
.kpi-sub{ font-size:11.5px; color:var(--text-2); margin-top:5px; font-weight:500; }
.kpi-accent{ color:var(--green); }

.mini-strip{ display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
.mini{
  flex:1 1 200px; border:1px solid var(--border); border-radius:var(--radius);
  background:var(--surface-2); padding:10px 14px; display:flex;
  align-items:center; justify-content:space-between; gap:10px;
}
.mini-k{ font-size:11.5px; color:var(--text-2); font-weight:500; }
.mini-v{ font-size:14px; font-weight:700; color:var(--navy); }

/* ══════════════════════ CARD DE LEAD (GEOMETRIC + NOTION) ══════════════════════ */
.lead-card{
  background:var(--surface); border:1px solid var(--border); border-radius:14px;
  overflow:hidden; margin-bottom:16px; box-shadow:var(--shadow-sm);
  transition:border-color .12s ease, box-shadow .15s ease, transform .12s ease;
}
.lead-card:hover{ border-color:var(--border-strong); box-shadow:var(--shadow-lg); transform:translateY(-2px); }
.card-top{ padding:16px 18px 12px; }
.card-header-flex{ display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:11px; }
.card-identity{ display:flex; gap:12px; align-items:flex-start; flex:1; min-width:0; }
.card-meta-panel{
  background:var(--surface-2); border:1px solid var(--border); border-radius:8px;
  padding:7px 10px; font-size:11px; line-height:1.45; min-width:210px; flex-shrink:0; text-align:right;
}
.meta-cnpj{ font-family:var(--mono); font-weight:700; color:var(--purple-dark); font-size:11.5px; }
.meta-capital{ font-weight:700; color:var(--green); margin-top:1px; }
.meta-pills{ display:flex; gap:3px; justify-content:flex-end; margin:3px 0 2px; flex-wrap:wrap; }
.meta-pill{ font-size:9.5px; font-weight:700; padding:1px 6px; border-radius:4px; background:var(--surface-sunk); border:1px solid var(--border); color:var(--text-2); }
.meta-pill-mei{ background:#fef3c7; border-color:#fde047; color:#92400e; }
.meta-pill-simples{ background:#dcfce7; border-color:#86efac; color:#166534; }
.meta-pill-porte{ background:#e0f2fe; border-color:#7dd3fc; color:#075985; }
.meta-sub{ font-size:10.5px; color:var(--text-2); margin-top:2px; }

.card-avatar-purple{
  width:42px; height:42px; border-radius:10px; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  font-size:14px; font-weight:800; background:linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color:#fff; box-shadow:0 2px 6px rgba(99, 102, 241, 0.25);
}
.name-block{ flex:1; min-width:0; }
.company-main{ font-size:15px; font-weight:700; color:var(--text); line-height:1.3; }
.company-sub{ font-size:11.5px; color:var(--muted); margin-top:2px; }
.tag{
  display:inline-flex; align-items:center; gap:5px; font-size:10.5px; font-weight:600;
  padding:3px 9px; border-radius:6px; border:1px solid var(--border);
  background:var(--surface-sunk); color:var(--text-2); margin-top:7px; margin-right:4px;
}
.tag-new{ background:var(--green-soft); border-color:#bfe4d1; color:var(--green); }
.tag-warn{ background:var(--amber-soft); border-color:#eed6a6; color:var(--amber); }

.card-info{ display:flex; flex-direction:column; gap:5px; font-size:11.5px; color:var(--text-2); margin-bottom:11px; font-weight:500; }
.info-row{ display:flex; align-items:center; gap:7px; }

.cnae-strip-highlight{
  background:#ecfdf5; border:1px solid #a7f3d0; border-radius:8px;
  padding:9px 12px; font-size:11.5px; color:#065f46; margin:10px 0;
}
.cnae-strip-title{
  font-size:10.5px; font-weight:800; letter-spacing:.04em;
  text-transform:uppercase; color:#047857; margin-bottom:3px;
  display:flex; align-items:center; gap:5px;
}
.cnae-code{ font-family:var(--mono); font-size:11px; color:var(--text); line-height:1.45; }

/* ── Contatos Pílulas ── */
.contact-pill-box{ display:flex; flex-direction:column; gap:7px; padding:10px 17px; background:var(--surface-2); border-top:1px solid var(--border); }
.contact-pill-wa{
  display:flex; align-items:center; justify-content:space-between;
  background:#ecfdf5; border:1px solid #a7f3d0; border-radius:8px;
  padding:6px 10px; font-size:12px;
}
.contact-pill-mail{
  display:flex; align-items:center; justify-content:space-between;
  background:#fff7ed; border:1px solid #fed7aa; border-radius:8px;
  padding:6px 10px; font-size:12px;
}
.btn-abordar{
  background:#4f46e5; color:#fff !important; border-radius:7px;
  padding:4px 12px; font-size:11.5px; font-weight:700; text-decoration:none;
  display:inline-flex; align-items:center; gap:5px; box-shadow:0 1px 3px rgba(79,70,229,.3);
  transition:background .12s ease;
}
.btn-abordar:hover{ background:#4338ca; }
.btn-email{
  background:#fff; border:1px solid #e2e8f0; color:#475569 !important; border-radius:7px;
  padding:4px 12px; font-size:11.5px; font-weight:600; text-decoration:none;
}
.btn-email:hover{ background:#f8fafc; }

/* ── Ações no Card ── */
.action-buttons{ display:flex; gap:7px; padding:9px 17px; background:var(--surface); border-top:1px solid var(--border); }
.act-btn{
  flex:1; padding:6px 8px; border-radius:7px; border:1px solid var(--border);
  font-size:11.5px; font-weight:600; text-align:center; text-decoration:none;
  display:inline-flex; align-items:center; justify-content:center; gap:6px;
  background:var(--surface); color:var(--navy); transition:all .12s ease;
}
.act-btn:hover{ background:var(--purple-soft); border-color:var(--border-strong); color:var(--purple-dark); }
.act-btn-rf{ color:#475569; background:#f8fafc; border-color:#e2e8f0; }
.act-btn-maps{ color:#b91c1c; background:#fef2f2; border-color:#fecaca; }
.act-btn-ig{ color:#c13584; background:#fdf2f8; border-color:#f9a8d4; }
.act-btn-web{ color:#2563eb; background:#eff6ff; border-color:#bfdbfe; }
.act-btn-off{ opacity:.4; }

details.card-expand{ border-top:1px solid var(--border); }
details.card-expand summary{
  padding:10px 17px; font-size:11.5px; color:var(--text-2); cursor:pointer;
  list-style:none; display:flex; align-items:center; gap:6px; font-weight:600;
}
details.card-expand summary:hover{ color:var(--purple); }
.expand-body{ padding:13px 17px; border-top:1px solid var(--border); background:var(--surface-2); }
.exp-card{
  background:#fff; border:1px solid var(--border); border-radius:8px;
  padding:10px 12px; margin-bottom:10px; font-size:12px;
}
.exp-card-title{
  font-size:10px; font-weight:800; letter-spacing:.06em;
  text-transform:uppercase; color:var(--muted); margin-bottom:6px;
}
.cnae-list-box{ display:flex; flex-direction:column; gap:8px; }
.cnae-item-row{
  display:flex; align-items:flex-start; gap:10px; padding:8px 10px;
  background:#fff; border:1px solid var(--border); border-radius:6px; font-size:11.5px;
}
.cnae-item-row-beauty{ border-color:#bfe4d1; background:var(--green-soft); }
.cnae-type-badge{
  font-size:9.5px; font-weight:700; padding:2px 6px; border-radius:4px; text-transform:uppercase; flex-shrink:0; margin-top:1px;
}
.cnae-type-principal{ background:var(--navy); color:#fff; }
.cnae-type-secundario{ background:var(--surface-sunk); color:var(--text-2); border:1px solid var(--border); }

/* ── Avisos e Notificações ── */
.notice{
  border:1px solid var(--border); border-left:3px solid var(--purple); border-radius:8px;
  background:var(--purple-soft); padding:12px 15px; font-size:12.5px; color:var(--text-2);
}
.notice-lock{ border-left-color:var(--coral); background:var(--coral-soft); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. CONSTANTES
# ══════════════════════════════════════════════════════════════
BEAUTY_CNAES = {
    "9602501": "Salões e Barbearias",
    "9602-5/01": "Salões e Barbearias",
    "9602502": "Clínicas de Estética",
    "9602-5/02": "Clínicas de Estética",
    "4772500": "Lojas e Pontos de Venda",
    "4772-5/00": "Lojas e Pontos de Venda",
    "4646001": "Distribuidores Atacadistas",
    "4646-0/01": "Distribuidores Atacadistas",
    "4618401": "Representantes e Agentes",
    "4618-4/01": "Representantes e Agentes",
    "2063100": "Fábricas e Marcas",
    "2063-1/00": "Fábricas e Marcas",
}

SEG_CFG = {
    "Salões e Barbearias": {"e": "✂"},
    "Clínicas de Estética": {"e": "✦"},
    "Distribuidores Atacadistas": {"e": "📦"},
    "Lojas e Pontos de Venda": {"e": "🛍️"},
    "Fábricas e Marcas": {"e": "🏭"},
    "Representantes e Agentes": {"e": "💼"},
}

TIER_CFG = {
    "explorador":  {"label": "Explorador",  "limit": 0,      "states": 1},
    "operacional": {"label": "Operacional", "limit": 300,    "states": 1},
    "regional":    {"label": "Regional",    "limit": 1000,   "states": 5},
    "nacional":    {"label": "Nacional",    "limit": 999999, "states": 27},
}

MOCK_USERS = {
    "pro@achei.com":        {"nome": "Amanda Consultora", "senha": "pro123",  "tier": "regional",    "exports_used": 45},
    "demo@achei.com":       {"nome": "Rafael Consultor",  "senha": "demo123", "tier": "operacional", "exports_used": 253},
    "admin@achei.com":      {"nome": "Admin Geral",       "senha": "admin123","tier": "nacional",    "exports_used": 0},
    "explorador@achei.com": {"nome": "Explorador Free",    "senha": "demo",    "tier": "explorador",  "exports_used": 0},
}

PROFILE_LABELS = {
    "pro@achei.com": "Amanda · Regional",
    "demo@achei.com": "Rafael · Operacional",
    "admin@achei.com": "Admin · Nacional",
    "explorador@achei.com": "Explorador · Gratuito",
}

KNOWN_CNAES = {
    "9602501": "Cabeleireiros, barbearias, manicure e pedicure",
    "9602502": "Atividades de estética e outros serviços de cuidados com a beleza",
    "4772500": "Comércio varejista de cosméticos, produtos de perfumaria e de higiene pessoal",
    "4646001": "Comércio atacadista de cosméticos e produtos de perfumaria",
    "4618401": "Representantes comerciais e agentes do comércio de cosméticos",
    "2063100": "Fabricação de cosméticos, produtos de perfumaria e de higiene pessoal",
    "4781400": "Comércio varejista de artigos do vestuário e acessórios",
    "8690999": "Outras atividades de atenção à saúde humana",
    "4789002": "Comércio varejista de plantas e flores naturais",
    "4729699": "Comércio varejista de produtos alimentícios em geral",
}

SVG_WHATSAPP = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:-2px"><path d="M12.012 2c-5.506 0-9.989 4.478-9.99 9.984 0 1.764.459 3.487 1.334 5.006l-1.417 5.176 5.297-1.389c1.464.798 3.116 1.218 4.774 1.219h.004c5.507 0 9.991-4.479 9.991-9.986 0-2.668-1.038-5.177-2.924-7.062a9.924 9.924 0 0 0-7.063-2.948zm5.952 14.183c-.252.71-1.464 1.348-2.016 1.408-.504.055-1.156.079-3.704-.972-3.08-1.272-5.074-4.423-5.228-4.63-.151-.205-1.246-1.657-1.246-3.161 0-1.503.785-2.241 1.063-2.548.277-.307.605-.383.807-.383.202 0 .404.001.58.01.187.008.439-.071.687.525.252.605.856 2.091.932 2.244.076.153.126.332.025.535-.1.205-.151.332-.302.508-.151.176-.317.393-.453.528-.151.151-.31.316-.134.619.176.303.78 1.288 1.674 2.085 1.15 1.025 2.119 1.343 2.422 1.494.303.151.48.126.657-.076.176-.202.756-.883.958-1.186.202-.303.404-.252.681-.151.277.101 1.764.832 2.067.983.303.151.504.227.58.353.076.126.076.73-.176 1.44z"/></svg>'
SVG_MAPS = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
SVG_MAIL = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
SVG_RECEITA = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
SVG_PIN = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
SVG_CHECK = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px"><polyline points="20 6 9 17 4 12"/></svg>'
SVG_ALERT = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
SVG_INSTAGRAM = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>'
SVG_SEARCH = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'

# ══════════════════════════════════════════════════════════════
# 4. CARREGAMENTO E NORMALIZAÇÃO DE DADOS
# ══════════════════════════════════════════════════════════════
def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    str_cols = ["RAZÃO SOCIAL", "NOME FANTASIA", "MUNICIPIO", "ESTADO", "BAIRRO", "CEP", "ORIGEM_CNAE", "SEGMENTO"]
    for c in str_cols:
        if c in df.columns:
            df[c] = df[c].fillna("").astype(str).str.strip()

    if "CNPJ" in df.columns:
        df["CNPJ"] = df["CNPJ"].apply(
            lambda v: f"{int(str(v).replace('.', '').replace('-', '').replace('/', '')):014d}"
            if pd.notna(v) and str(v).replace(".", "").replace("-", "").replace("/", "").isdigit()
            else str(v).strip()
        )

    bool_cols = ["TEM_EMAIL", "TEM_TELEFONE", "EMAIL_CONTABILIDADE", "MEI", "SIMPLES"]
    for c in bool_cols:
        if c in df.columns:
            df[c] = df[c].apply(lambda v: True if v is True or str(v).strip().upper() in ("SIM", "TRUE", "1") else False)

    porte_map = {
        "MICRO EMPRESA": "ME", "EMPRESA DE PEQUENO PORTE": "EPP", "DEMAIS": "Grande",
        "MEI": "MEI", "ME": "ME", "EPP": "EPP", "GRANDE": "Grande",
    }
    if "PORTE" in df.columns:
        df["PORTE"] = df["PORTE"].apply(lambda v: porte_map.get(str(v).strip().upper(), str(v).strip()))

    if "SEGMENTO" not in df.columns or df["SEGMENTO"].eq("").all():
        cnae_seg_map = {
            "9602501": "Salões e Barbearias", "9602-5/01": "Salões e Barbearias",
            "9602502": "Clínicas de Estética", "9602-5/02": "Clínicas de Estética",
            "4646001": "Distribuidores Atacadistas", "4772500": "Lojas e Pontos de Venda",
            "4635401": "Representantes e Agentes", "2063100": "Fábricas e Marcas",
        }
        base = df["CNAE_PRINCIPAL_CODIGO"] if "CNAE_PRINCIPAL_CODIGO" in df.columns else None
        if base is not None:
            df["SEGMENTO"] = base.astype(str).map(lambda c: cnae_seg_map.get(c, "Salões e Barbearias"))
        else:
            df["SEGMENTO"] = "Salões e Barbearias"

    if "INICIO ATIVIDADE" in df.columns:
        df["INICIO ATIVIDADE"] = pd.to_datetime(df["INICIO ATIVIDADE"], errors="coerce")
        today = datetime.now()
        df["ANOS_ATIVIDADE"] = ((today - df["INICIO ATIVIDADE"]).dt.days / 365.25).fillna(0).round(1)

    if "CAPITAL SOCIAL" in df.columns:
        df["CAPITAL SOCIAL"] = pd.to_numeric(df["CAPITAL SOCIAL"], errors="coerce").fillna(0)

    for i in range(1, 4):
        for col in (f"WHATSAPP_{i}", f"TELEFONE_{i}"):
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str).str.strip().replace("nan", "")

    return df


@st.cache_data
def get_data() -> pd.DataFrame:
    csv_path = "plano/bd_teste/9602501_AP.csv"
    if os.path.exists(csv_path):
        try:
            return normalize_df(pd.read_csv(csv_path, sep=";", encoding="utf-8"))
        except Exception:
            pass

    today = date.today()
    this_month = date(today.year, today.month, 1)

    rows = [
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="12.345.678/0001-90",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos",
             **{"RAZÃO SOCIAL": "Studio Bella Arte Cabeleireiros Ltda", "NOME FANTASIA": "Studio Bella Arte Concept"},
             TELEFONE_1="(11) 3456-7890", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 98765-4321", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL": "contato@studiobella.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Pinheiros", CEP="05422-001", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA": "Rua dos Pinheiros, 100 - Pinheiros, São Paulo - SP",
                "MAPS": "https://maps.google.com/?q=Studio+Bella+Arte+Pinheiros"},
             **{"MATRIZ FILIAL": "Matriz", "PORTE": "ME", "CAPITAL SOCIAL": "50000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE": "2018-03-15",
                "RECEITA FEDERAL": "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=12345678000190",
                "NATUREZA_JURIDICA": "Sociedade Empresária Limitada", "SITE": "www.studiobella.com.br"},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="98.765.432/0001-10",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL": "Barbearia Vintage Club Eireli", "NOME FANTASIA": "Barbearia Vintage Moema"},
             TELEFONE_1="(11) 3333-4444", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 97777-8888", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL": "barba@vintageclub.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Moema", CEP="04510-000", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA": "Av. Moema, 450 - Moema, São Paulo - SP",
                "MAPS": "https://maps.google.com/?q=Barbearia+Vintage+Moema"},
             **{"MATRIZ FILIAL": "Matriz", "PORTE": "ME", "CAPITAL SOCIAL": "30000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE": "2020-07-01",
                "RECEITA FEDERAL": "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=98765432000110",
                "NATUREZA_JURIDICA": "Empresário Individual", "SITE": ""},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="78.901.234/0001-56",
             CNAE_PRINCIPAL_CODIGO="9602502", CNAE_PRINCIPAL_NOME="Atividades de estética e outros cuidados com a beleza",
             CNAE_SECUNDARIO_CODIGO="9602501", CNAE_SECUNDARIO_NOME="Cabeleireiros, manicure e pedicure",
             **{"RAZÃO SOCIAL": "Clínica Estética Evolução Ltda", "NOME FANTASIA": "Evolução Estética Avançada"},
             TELEFONE_1="(31) 3111-2222", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(31) 99111-2222", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL": "contato@evolucaoestetica.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Savassi", CEP="30140-071", MUNICIPIO="Belo Horizonte", ESTADO="MG",
             **{"ENDERECO MAPA": "Rua Pernambuco, 1000 - Savassi, Belo Horizonte - MG",
                "MAPS": "https://maps.google.com/?q=Evolucao+Estetica+Savassi"},
             **{"MATRIZ FILIAL": "Matriz", "PORTE": "ME", "CAPITAL SOCIAL": "80000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE": this_month.strftime("%Y-%m-%d"),
                "RECEITA FEDERAL": "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=78901234000156",
                "NATUREZA_JURIDICA": "Sociedade Empresária Limitada", "SITE": "www.evolucaoestetica.com.br"},
             SEGMENTO="Clínicas de Estética"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="44.333.222/0001-99",
             CNAE_PRINCIPAL_CODIGO="4646001", CNAE_PRINCIPAL_NOME="Comércio atacadista de cosméticos e produtos de perfumaria",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos",
             **{"RAZÃO SOCIAL": "Distribuidora Belezamix MG Ltda", "NOME FANTASIA": "Belezamix Distribuidora"},
             TELEFONE_1="(31) 3444-5555", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(31) 98444-5555", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL": "vendas@belezamixmg.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Centro", CEP="30110-000", MUNICIPIO="Belo Horizonte", ESTADO="MG",
             **{"ENDERECO MAPA": "Av. Afonso Pena, 1500 - Centro, Belo Horizonte - MG",
                "MAPS": "https://maps.google.com/?q=Belezamix+BH"},
             **{"MATRIZ FILIAL": "Matriz", "PORTE": "EPP", "CAPITAL SOCIAL": "500000"},
             MEI=False, SIMPLES=False,
             **{"INICIO ATIVIDADE": "2012-05-10",
                "RECEITA FEDERAL": "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=44333222000199",
                "NATUREZA_JURIDICA": "Sociedade Empresária Limitada", "SITE": "www.belezamixmg.com.br"},
             SEGMENTO="Distribuidores Atacadistas"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="secundario",
             CNPJ="55.666.777/0001-88",
             CNAE_PRINCIPAL_CODIGO="4729699", CNAE_PRINCIPAL_NOME="Comércio varejista de produtos alimentícios",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos e perfumaria",
             **{"RAZÃO SOCIAL": "Mercado Rosa Cosméticos ME", "NOME FANTASIA": "Rosa Cosméticos Tatuapé"},
             TELEFONE_1="(11) 2222-3333", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL": "rosa@cosm.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Tatuapé", CEP="03308-000", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA": "Rua Tuiuti, 1200 - Tatuapé, São Paulo - SP",
                "MAPS": "https://maps.google.com/?q=Rosa+Cosmeticos+Tatuape"},
             **{"MATRIZ FILIAL": "Matriz", "PORTE": "EPP", "CAPITAL SOCIAL": "120000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE": "2015-11-20",
                "RECEITA FEDERAL": "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=55666777000188",
                "NATUREZA_JURIDICA": "Sociedade Empresária Limitada", "SITE": ""},
             SEGMENTO="Lojas e Pontos de Venda"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="88.111.333/0001-55",
             CNAE_PRINCIPAL_CODIGO="2063100", CNAE_PRINCIPAL_NOME="Fabricação de cosméticos, produtos de perfumaria e de higiene pessoal",
             CNAE_SECUNDARIO_CODIGO="4646001", CNAE_SECUNDARIO_NOME="Comércio atacadista de cosméticos",
             **{"RAZÃO SOCIAL": "Indústria Mineira de Cosméticos S/A", "NOME FANTASIA": "MineCosm Indústria"},
             TELEFONE_1="(31) 3666-7777", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL": "contato@contabil-mg.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=True,
             BAIRRO="Distrito Industrial", CEP="32670-000", MUNICIPIO="Betim", ESTADO="MG",
             **{"ENDERECO MAPA": "Av. das Indústrias, 500 - Betim - MG",
                "MAPS": "https://maps.google.com/?q=MineCosm+Betim+MG"},
             **{"MATRIZ FILIAL": "Matriz", "PORTE": "Grande", "CAPITAL SOCIAL": "10000000"},
             MEI=False, SIMPLES=False,
             **{"INICIO ATIVIDADE": "2001-03-20",
                "RECEITA FEDERAL": "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=88111333000155",
                "NATUREZA_JURIDICA": "Sociedade Anônima", "SITE": "www.minecosm.ind.br"},
             SEGMENTO="Fábricas e Marcas"),
    ]

    return normalize_df(pd.DataFrame(rows))

# ══════════════════════════════════════════════════════════════
# 5. HELPERS
# ══════════════════════════════════════════════════════════════
def minify(html: str) -> str:
    return re.sub(r"\n[ \t]*", " ", html).strip()

def clean_cnae_code(code):
    if not code or pd.isna(code):
        return ""
    return re.sub(r"\D", "", str(code)).strip()

def is_beauty_cnae(code):
    cp = clean_cnae_code(code)
    return cp in BEAUTY_CNAES or str(code).strip() in BEAUTY_CNAES

def get_cnae_label(code):
    cp = clean_cnae_code(code)
    return BEAUTY_CNAES.get(cp, BEAUTY_CNAES.get(str(code).strip(), ""))

def get_secondary_cnaes(row):
    raw_cods = str(row.get("CNAE_SECUNDARIO_CODIGO", ""))
    raw_noms = str(row.get("CNAE_SECUNDARIO_NOME", ""))
    if not raw_cods or raw_cods.strip() in ("nan", "None", ""):
        return []
    cods = [c.strip() for c in raw_cods.split(",") if c.strip()]
    noms = [n.strip() for n in raw_noms.split("|") if n.strip()]
    items = []
    for i, cod in enumerate(cods):
        cp = clean_cnae_code(cod)
        name = KNOWN_CNAES.get(cp) or KNOWN_CNAES.get(cod) or (noms[i] if i < len(noms) else "Outra atividade secundária")
        is_b = is_beauty_cnae(cod)
        label = get_cnae_label(cod)
        items.append({"code": cod, "clean_code": cp, "name": name, "is_beauty": is_b, "beauty_label": label})
    return items

def format_phone_display(phone_str):
    if not phone_str or pd.isna(phone_str):
        return ""
    s = str(phone_str).strip()
    digits = "".join(c for c in s if c.isdigit())
    if not digits or digits.count("0") == len(digits):
        return ""
    if digits.startswith("55") and len(digits) in (12, 13):
        digits = digits[2:]
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    if len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return s

def get_display_name(row):
    nf = escape(str(row.get("NOME FANTASIA", "")).strip())
    rs = escape(str(row.get("RAZÃO SOCIAL", "")).strip())
    return (nf, rs) if nf else (rs, "")

def get_initials(name):
    if not name or not str(name).strip():
        return "CN"
    parts = str(name).strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return str(name)[:2].upper()

def clean_phone(phone):
    return "".join(c for c in str(phone) if c.isdigit())

def wa_link(phone, nome=""):
    if not phone or str(phone).strip() in ("", "#", "nan", "None"):
        return "#"
    raw = str(phone).strip()
    cp = clean_phone(raw)
    num = f"55{cp}" if not cp.startswith("55") else cp
    msg = f"Olá! Tudo bem? Entro em contato da plataforma comercial sobre os serviços do estabelecimento {nome}."
    return f"https://wa.me/{num}?text={msg.replace(' ', '%20')}"

def is_new(dt, months=1):
    if pd.isna(dt):
        return False
    return dt >= datetime.now() - timedelta(days=30 * months)

def format_capital(val):
    try:
        return f"R$ {float(val):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "—"

# ══════════════════════════════════════════════════════════════
# 6. ESTADO & FILTROS (SINGLE SOURCE OF TRUTH)
# ══════════════════════════════════════════════════════════════
FILTER_DEFAULTS = {
    "tem_email": False,
    "sem_contador": False,
    "tem_whatsapp": False,
    "segmentos": [],
    "origem_cnae": "Principal ou Secundário",
    "estados": [],
    "municipios": [],
    "bairros": [],
    "busca_texto": "",
    "portes": [],
    "mei": "Todos",
    "simples": "Todos",
    "anos_range": (0, 25),
}

def k(name):
    return f"f_{name}"

def init_state():
    defaults = {
        "user_email": "pro@achei.com",
        "user": MOCK_USERS["pro@achei.com"].copy(),
        "saved_views": [
            {"name": "SP · Salões com WhatsApp", "filters": {"estados": ["SP"], "segmentos": ["Salões e Barbearias"], "tem_whatsapp": True}},
            {"name": "MG · Distribuidores", "filters": {"estados": ["MG"], "segmentos": ["Distribuidores Atacadistas"]}},
            {"name": "Beleza no CNAE principal", "filters": {"origem_cnae": "Apenas CNAE principal"}},
        ],
    }
    for key, val in defaults.items():
        st.session_state.setdefault(key, val)
    for name, val in FILTER_DEFAULTS.items():
        st.session_state.setdefault(k(name), val)

def read_filters():
    return {name: st.session_state.get(k(name), val) for name, val in FILTER_DEFAULTS.items()}

def reset_filters(new_values=None):
    for name, val in FILTER_DEFAULTS.items():
        st.session_state[k(name)] = val
    for name, val in (new_values or {}).items():
        if name in FILTER_DEFAULTS:
            st.session_state[k(name)] = val

def active_filter_chips(filters):
    chips = []
    if filters.get("tem_whatsapp"):
        chips.append(("Com WhatsApp", "tem_whatsapp", None))
    if filters.get("tem_email"):
        chips.append(("Com e-mail", "tem_email", None))
    if filters.get("sem_contador"):
        chips.append(("Sem contador", "sem_contador", None))
    for seg in filters.get("segmentos", []):
        chips.append((seg, "segmentos", seg))
    for uf in filters.get("estados", []):
        chips.append((f"UF {uf}", "estados", uf))
    for mun in filters.get("municipios", []):
        chips.append((mun, "municipios", mun))
    for bai in filters.get("bairros", []):
        chips.append((bai, "bairros", bai))
    for porte in filters.get("portes", []):
        chips.append((f"Porte {porte}", "portes", porte))
    if filters.get("busca_texto"):
        chips.append((f"“{filters['busca_texto']}”", "busca_texto", None))
    if filters.get("origem_cnae") != FILTER_DEFAULTS["origem_cnae"]:
        chips.append((filters["origem_cnae"], "origem_cnae", None))
    if filters.get("mei") != "Todos":
        chips.append((f"MEI: {filters['mei']}", "mei", None))
    return chips

def remove_filter(name, value=None):
    if value is None:
        st.session_state[k(name)] = FILTER_DEFAULTS[name]
    else:
        current = list(st.session_state.get(k(name), []))
        st.session_state[k(name)] = [v for v in current if v != value]

# ══════════════════════════════════════════════════════════════
# 7. SIDEBAR (FILTROS + PRESETS + UPLOAD + CONTROLE DE PLANOS)
# ══════════════════════════════════════════════════════════════
def count_active(names, filters):
    n = 0
    for name in names:
        val = filters.get(name)
        default = FILTER_DEFAULTS[name]
        if isinstance(default, list):
            n += len(val or [])
        elif isinstance(default, tuple):
            n += 1 if tuple(val) != default else 0
        elif isinstance(default, bool):
            n += 1 if val else 0
        else:
            n += 1 if val != default else 0
    return n

def group_title(title, names, filters):
    n = count_active(names, filters)
    return f"{title}  ·  {n}" if n else title

def show_sidebar(df):
    prev = read_filters()

    with st.sidebar:
        # Brand Header matching React Light Theme
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #e2e8f0;">
              <div style="width:36px;height:36px;border-radius:10px;background:#4f46e5;color:#fff;font-weight:800;font-size:18px;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(79,70,229,.3);">
                ✂️
              </div>
              <div>
                <div style="font-size:15px;font-weight:800;color:#0f172a;line-height:1.2;letter-spacing:-0.02em;">AcheiMeuCliente</div>
                <div style="font-size:11px;color:#64748b;font-weight:600;">Inteligência B2B Beleza</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sel = st.selectbox(
            "Perfil de Usuário (Simulação de Plano):",
            options=list(PROFILE_LABELS.keys()),
            format_func=lambda x: PROFILE_LABELS[x],
            index=list(PROFILE_LABELS.keys()).index(st.session_state.get("user_email", "pro@achei.com")),
            key="profile_switcher",
        )
        if sel != st.session_state.get("user_email"):
            st.session_state.user_email = sel
            st.session_state.user = MOCK_USERS[sel].copy()
            st.toast(f"Perfil: {PROFILE_LABELS[sel]}")
            st.rerun()

        # Header de Filtros com contador e botão de limpar
        total_active = len(active_filter_chips(prev))
        st.markdown(
            f"""
            <div class="sidebar-header-bar">
              <div class="sidebar-title">
                <span>⚙️ Filtros Avançados</span>
                {"<span class='sidebar-counter'>" + str(total_active) + "</span>" if total_active else ""}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if total_active > 0:
            if st.button("↺ Limpar filtros", key="reset_all_btn", use_container_width=True):
                reset_filters()
                st.rerun()

        # Visualizações Rápidas (Pílulas com texto e botão Aplicar à direita)
        st.markdown('<div class="sec-label">🔖 VISUALIZAÇÕES RÁPIDAS</div>', unsafe_allow_html=True)
        preset_list = [
            {"name": "Macapá · Salões com WhatsApp", "filters": {"estados": ["AP"], "municipios": ["Macapá"], "segmentos": ["Salões e Barbearias"], "tem_whatsapp": True}},
            {"name": "Clínicas de Estética & Spas", "filters": {"segmentos": ["Clínicas de Estética"], "tem_whatsapp": True}},
            {"name": "Distribuidores e Fábricas B2B", "filters": {"segmentos": ["Distribuidores Atacadistas", "Fábricas e Marcas"]}},
            {"name": "Apenas CNAE Principal em Beleza", "filters": {"origem_cnae": "Apenas CNAE principal"}},
        ]
        for i, ps in enumerate(preset_list):
            c_p1, c_p2 = st.columns([3, 1])
            with c_p1:
                st.markdown(f'<div style="font-size:12px;font-weight:600;color:#334155;padding-top:5px;">{ps["name"]}</div>', unsafe_allow_html=True)
            with c_p2:
                if st.button("Aplicar", key=f"ps_btn_{i}"):
                    reset_filters(ps["filters"])
                    st.toast(f"Filtro “{ps['name']}” aplicado")
                    st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        # Grupos de Filtros Avançados
        with st.expander(group_title("📞 Canais de Contato", ["tem_email", "sem_contador", "tem_whatsapp"], prev), expanded=True):
            st.checkbox("Com WhatsApp Confirmado", key=k("tem_whatsapp"))
            st.checkbox("Com E-mail Cadastrado", key=k("tem_email"))
            st.checkbox("Excluir e-mails de contabilidade", key=k("sem_contador"))

        with st.expander(group_title("🛍️ Segmentos de Beleza", ["segmentos", "origem_cnae"], prev), expanded=False):
            st.multiselect("Segmentos Selecionados", list(SEG_CFG.keys()), key=k("segmentos"), placeholder="Todos os segmentos")
            st.selectbox(
                "Origem do CNAE:",
                ["Principal ou Secundário", "Apenas CNAE principal", "Apenas CNAE secundário"],
                key=k("origem_cnae"),
            )

        with st.expander(group_title("📍 Localização", ["estados", "municipios", "bairros"], prev), expanded=False):
            estados = sorted(df["ESTADO"].dropna().unique().tolist())
            st.multiselect("Estado (UF)", estados, key=k("estados"), placeholder="Todos")

            sel_uf = st.session_state.get(k("estados"), [])
            base = df[df["ESTADO"].isin(sel_uf)] if sel_uf else df
            mun_opts = sorted(base["MUNICIPIO"].dropna().unique().tolist())
            st.session_state[k("municipios")] = [m for m in st.session_state.get(k("municipios"), []) if m in mun_opts]
            st.multiselect("Município", mun_opts, key=k("municipios"), placeholder="Todos")

            sel_mun = st.session_state.get(k("municipios"), [])
            bai_opts = sorted(df[df["MUNICIPIO"].isin(sel_mun)]["BAIRRO"].dropna().unique().tolist()) if sel_mun else []
            st.session_state[k("bairros")] = [b for b in st.session_state.get(k("bairros"), []) if b in bai_opts]
            st.multiselect("Bairro", bai_opts, key=k("bairros"), placeholder="Todos os bairros")

        with st.expander(group_title("🏢 Porte & Tributação", ["portes", "mei", "simples", "anos_range"], prev), expanded=False):
            st.markdown('<div style="font-size:12px;font-weight:600;color:#475569;margin-bottom:6px;">Porte da Empresa</div>', unsafe_allow_html=True)
            col_p1, col_p2 = st.columns(2)
            sel_portes = set(st.session_state.get(k("portes"), []))
            for i, p_item in enumerate(["MEI", "ME", "EPP", "Grande"]):
                col_target = col_p1 if i % 2 == 0 else col_p2
                is_sel = p_item in sel_portes
                btn_label = f"✓ {p_item}" if is_sel else p_item
                if col_target.button(btn_label, key=f"porte_btn_{p_item}", use_container_width=True):
                    if is_sel:
                        st.session_state[k("portes")] = [x for x in sel_portes if x != p_item]
                    else:
                        st.session_state[k("portes")] = list(sel_portes | {p_item})
                    st.rerun()

            st.selectbox("Filtro MEI:", ["Todos", "Apenas MEI", "Excluir MEI"], key=k("mei"))
            st.selectbox("Simples Nacional:", ["Todos", "Sim", "Não"], key=k("simples"))
            st.slider("Anos de atividade", 0, 25, key=k("anos_range"))

        st.markdown('<div class="sec-label">💾 SALVAR FILTRO ATUAL</div>', unsafe_allow_html=True)
        name_v = st.text_input("Nome da visualização:", key="save_view_name", placeholder="Ex: Macapá · Salões WhatsApp", label_visibility="collapsed")
        if st.button("Salvar Filtro Atual", key="save_view_btn", use_container_width=True):
            if name_v.strip():
                st.session_state.saved_views.append({"name": name_v.strip(), "filters": read_filters().copy()})
                st.toast(f"“{name_v.strip()}” salvo com sucesso!")
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

    return read_filters()

# ══════════════════════════════════════════════════════════════
# 8. APLICAÇÃO DOS FILTROS
# ══════════════════════════════════════════════════════════════
def apply_filters(df, filters):
    mask = pd.Series([True] * len(df), index=df.index)

    if filters.get("tem_email"):
        mask &= df["TEM_EMAIL"] == True
    if filters.get("sem_contador"):
        mask &= df["EMAIL_CONTABILIDADE"] == False
    if filters.get("tem_whatsapp"):
        mask &= df["WHATSAPP_1"].astype(str).str.strip().str.len() > 0
    if filters.get("segmentos"):
        mask &= df["SEGMENTO"].isin(filters["segmentos"])
    if filters.get("estados"):
        mask &= df["ESTADO"].isin(filters["estados"])
    if filters.get("municipios"):
        mask &= df["MUNICIPIO"].isin(filters["municipios"])
    if filters.get("bairros"):
        mask &= df["BAIRRO"].isin(filters["bairros"])

    origem = filters.get("origem_cnae", "Principal ou Secundário")
    if origem == "Apenas CNAE principal":
        mask &= df["ORIGEM_CNAE"].astype(str).str.lower() == "principal"
    elif origem == "Apenas CNAE secundário":
        mask &= df["ORIGEM_CNAE"].astype(str).str.lower() == "secundario"

    if filters.get("busca_texto"):
        q = filters["busca_texto"].lower()
        mask &= (
            df["NOME FANTASIA"].astype(str).str.lower().str.contains(q, na=False)
            | df["RAZÃO SOCIAL"].astype(str).str.lower().str.contains(q, na=False)
            | df["CNPJ"].astype(str).str.lower().str.contains(q, na=False)
            | df["BAIRRO"].astype(str).str.lower().str.contains(q, na=False)
        )
    if filters.get("portes"):
        mask &= df["PORTE"].isin(filters["portes"])

    mei_f = filters.get("mei", "Todos")
    if mei_f == "Apenas MEI":
        mask &= df["MEI"] == True
    elif mei_f == "Excluir MEI":
        mask &= df["MEI"] == False

    simples_f = filters.get("simples", "Todos")
    if simples_f == "Sim":
        mask &= df["SIMPLES"] == True
    elif simples_f == "Não":
        mask &= df["SIMPLES"] == False

    anos_r = filters.get("anos_range", (0, 25))
    if "ANOS_ATIVIDADE" in df.columns:
        mask &= (df["ANOS_ATIVIDADE"] >= anos_r[0]) & (df["ANOS_ATIVIDADE"] <= anos_r[1])

    return df[mask].copy()

# ══════════════════════════════════════════════════════════════
# 9. CONSTRUÇÃO DO CARD DE LEAD (GEOMETRIC + NOTION)
# ══════════════════════════════════════════════════════════════
def build_card_html(row):
    main_name, sub_name = get_display_name(row)
    initials = get_initials(main_name)
    seg = row.get("SEGMENTO", "Salões e Barbearias")
    seg_icon = SEG_CFG.get(seg, {"e": "✂"})["e"]

    cod_p = escape(str(row.get("CNAE_PRINCIPAL_CODIGO", "")))
    nom_p = escape(str(row.get("CNAE_PRINCIPAL_NOME", "")))
    sec_cnaes = get_secondary_cnaes(row)
    beauty_sec = sum(1 for c in sec_cnaes if c["is_beauty"])

    is_b_p = is_beauty_cnae(cod_p)
    b_label_p = get_cnae_label(cod_p)

    if is_b_p:
        strip_html = (
            f'<div class="cnae-strip-highlight">'
            f'<div class="cnae-strip-title">{SVG_CHECK} BELEZA NO CNAE PRINCIPAL ({b_label_p.upper()})</div>'
            f'<div class="cnae-code"><b>{cod_p}</b> · {nom_p} {"· (+" + str(len(sec_cnaes)) + " secundários)" if sec_cnaes else ""}</div>'
            f'</div>'
        )
    else:
        sec_line = (
            f'<div class="cnae-badge cnae-badge-ok" style="margin-top:4px">{SVG_CHECK} Beleza em {beauty_sec} CNAE secundário(s)</div>'
            if beauty_sec else
            f'<div class="cnae-badge" style="margin-top:4px">{len(sec_cnaes)} CNAE(s) secundário(s)</div>'
        )
        strip_html = (
            f'<div class="cnae-strip-highlight" style="background:#fef3c7;border-color:#fde047;color:#92400e;">'
            f'<div class="cnae-strip-title" style="color:#b45309;">{SVG_ALERT} CNAE PRINCIPAL FORA DA BELEZA</div>'
            f'<div class="cnae-code"><b>{cod_p}</b> · {nom_p}</div>{sec_line}'
            f'</div>'
        )

    tags = f'<span class="tag">{seg_icon} {escape(seg)}</span>'
    if is_new(row.get("INICIO ATIVIDADE")):
        tags += '<span class="tag tag-new">Nova</span>'
    if row.get("EMAIL_CONTABILIDADE"):
        tags += '<span class="tag tag-warn">E-mail de contador</span>'

    bairro_str = escape(str(row.get("BAIRRO", "")))
    mun_str = escape(str(row.get("MUNICIPIO", "")))
    uf_str = escape(str(row.get("ESTADO", "")))
    cep = escape(str(row.get("CEP", "")))
    loc_text = f"{bairro_str} · {mun_str} — {uf_str}" if bairro_str else f"{mun_str} — {uf_str}"

    cnpj = escape(str(row.get("CNPJ", "—")))
    porte = escape(str(row.get("PORTE", "ME")))
    capital = format_capital(row.get("CAPITAL SOCIAL", 0))
    nat_jur = escape(str(row.get("NATUREZA_JURIDICA", "—")))
    dt = row.get("INICIO ATIVIDADE")
    inicio_full = pd.to_datetime(dt).strftime("%d/%m/%Y") if pd.notna(dt) else "—"
    anos_str = f"{row.get('ANOS_ATIVIDADE', 0):.1f} a" if pd.notna(dt) else "—"

    pills_html = f'<span class="meta-pill meta-pill-porte">{porte}</span>'
    if row.get("SIMPLES"):
        pills_html += '<span class="meta-pill meta-pill-simples">SIMPLES</span>'
    if row.get("MEI"):
        pills_html += '<span class="meta-pill meta-pill-mei">MEI</span>'

    meta_panel_html = f"""
    <div class="card-meta-panel">
      <div class="meta-cnpj">{cnpj}</div>
      <div class="meta-capital">Capital {capital}</div>
      <div class="meta-pills">{pills_html}</div>
      <div class="meta-sub">Abertura: <b>{inicio_full}</b> ({anos_str})</div>
    </div>
    """

    # Contatos
    added, c_rows = set(), ""
    for i in range(1, 4):
        num = row.get(f"WHATSAPP_{i}", "")
        fmt = format_phone_display(num)
        if fmt and fmt not in added:
            added.add(fmt)
            c_rows += (
                f'<div class="contact-pill-wa">'
                f'<div style="display:flex;align-items:center;gap:8px;">'
                f'<span style="color:#059669">{SVG_WHATSAPP}</span><b style="font-family:var(--mono)">{fmt}</b>'
                f'</div>'
                f'<a class="btn-abordar" href="{wa_link(str(num), main_name)}" target="_blank">🚀 Abordar WhatsApp ↗</a>'
                f'</div>'
            )

    email = escape(str(row.get("E-MAIL", "")).strip())
    is_contador = bool(row.get("EMAIL_CONTABILIDADE", False))
    if email and email != "nan" and not is_contador:
        c_rows += (
            f'<div class="contact-pill-mail">'
            f'<div style="display:flex;align-items:center;gap:8px;color:#c2410c;">'
            f'<span>{SVG_MAIL}</span><span>{email}</span>'
            f'</div>'
            f'<a class="btn-email" href="mailto:{email}">E-mail</a>'
            f'</div>'
        )
    elif email and email != "nan" and is_contador:
        c_rows += f'<div style="font-size:11px;color:#b45309;padding:4px 0;">{SVG_ALERT} E-mail contábil identificado</div>'

    if not c_rows:
        c_rows = '<div style="font-size:11.5px;color:#94a3b8;padding:4px 0;">Nenhum contato direto identificado neste cadastro</div>'

    maps_url = escape(str(row.get("MAPS", "#")), quote=True)
    rf_url = escape(str(row.get("RECEITA FEDERAL", "#")).strip(), quote=True)
    query_base = escape(f"{main_name} {mun_str} {uf_str}".strip(), quote=True)
    ig_url = f"https://www.google.com/search?q={query_base}+instagram"
    web_url = f"https://www.google.com/search?q={query_base}"

    rf_btn = f'<a class="act-btn act-btn-rf" href="{rf_url}" target="_blank">{SVG_RECEITA} Receita</a>' if rf_url and rf_url != "#" else ""
    maps_btn = f'<a class="act-btn act-btn-maps" href="{maps_url}" target="_blank">{SVG_MAPS} Maps</a>' if maps_url and maps_url != "#" else ""
    ig_btn = f'<a class="act-btn act-btn-ig" href="{ig_url}" target="_blank">{SVG_INSTAGRAM} Instagram</a>'
    web_btn = f'<a class="act-btn act-btn-web" href="{web_url}" target="_blank">{SVG_SEARCH} Google</a>'

    endereco = escape(str(row.get("ENDERECO MAPA", "—")))

    cnae_items = []
    cnae_items.append(
        f'<div class="cnae-item-row {"cnae-item-row-beauty" if is_b_p else ""}">'
        f'<span class="cnae-type-badge cnae-type-principal">PRINCIPAL</span>'
        f'<div><b>{cod_p}</b> — {nom_p}</div></div>'
    )
    if sec_cnaes:
        for sc in sec_cnaes:
            cnae_items.append(
                f'<div class="cnae-item-row {"cnae-item-row-beauty" if sc["is_beauty"] else ""}">'
                f'<span class="cnae-type-badge cnae-type-secundario">SECUNDÁRIO</span>'
                f'<div><b>{escape(sc["code"])}</b> — {escape(sc["name"])}</div></div>'
            )

    return f"""
<div class="lead-card">
  <div class="card-top">
    <div class="card-header-flex">
      <div class="card-identity">
        <div class="card-avatar-purple">{initials}</div>
        <div class="name-block">
          <div class="company-main">{main_name}</div>
          {"<div class='company-sub'>" + sub_name + "</div>" if sub_name else ""}
          <div>{tags}</div>
        </div>
      </div>
      {meta_panel_html}
    </div>
    <div class="card-info">
      <div class="info-row">{SVG_PIN} {loc_text} · CEP {cep}</div>
    </div>
    {strip_html}
  </div>
  <div class="contact-pill-box">{c_rows}</div>
  <div class="action-buttons">{rf_btn}{maps_btn}{ig_btn}{web_btn}</div>
  <details class="card-expand">
    <summary>Endereço completo e CNAEs secundários ({len(sec_cnaes)})</summary>
    <div class="expand-body">
      <div class="exp-card">
        <div class="exp-card-title">ENDEREÇO CADASTRADO</div>
        <div style="font-weight:700;color:var(--text);">{endereco}</div>
        <div style="font-size:11px;color:var(--text-2);margin-top:2px;">Natureza: {nat_jur}</div>
      </div>
      <div class="exp-card">
        <div class="exp-card-title">TODAS AS ATIVIDADES ECONÔMICAS ({1 + len(sec_cnaes)})</div>
        <div class="cnae-list-box">{"".join(cnae_items)}</div>
      </div>
    </div>
  </details>
</div>"""

# ══════════════════════════════════════════════════════════════
# 10. APLICAÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════
def main():
    init_state()

    df_full = st.session_state.get("custom_df", get_data())
    filters = show_sidebar(df_full)
    df = apply_filters(df_full, filters)

    user = st.session_state.user
    tier_label = TIER_CFG[user.get("tier", "operacional")]["label"]

    # Topbar
    c_top_l, c_top_r = st.columns([2.5, 1])
    with c_top_l:
        st.markdown(
            f"""<div class="brand">
              <div class="brand-mark">✂️</div>
              <div>
                <div class="brand-name">AcheiMeuCliente
                  <span class="plan-chip"><span class="plan-dot"></span>Plano {tier_label}</span>
                </div>
                <div class="brand-sub">{user.get('nome','Usuário')} · Inteligência de Mercado para Salões e Clínicas</div>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c_top_r:
        st.text_input(
            "Buscar",
            key=k("busca_texto"),
            placeholder="Buscar por nome, bairro ou CNPJ...",
            label_visibility="collapsed",
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # KPIs
    total_leads = len(df)
    c_whats = int(df["WHATSAPP_1"].astype(str).str.strip().str.len().gt(0).sum()) if total_leads else 0
    c_email = int(df["TEM_EMAIL"].sum()) if total_leads else 0
    c_cnae_p = int((df["ORIGEM_CNAE"] == "principal").sum()) if total_leads else 0

    pct_w = f"{(c_whats/total_leads*100):.0f}% do filtro" if total_leads else "—"
    pct_e = f"{(c_email/total_leads*100):.0f}% do filtro" if total_leads else "—"

    cols = st.columns(4)
    with cols[0]:
        st.markdown(f'<div class="kpi"><div class="kpi-label">Leads Filtrados</div><div class="kpi-value">{total_leads}</div><div class="kpi-sub">de {len(df_full)} no banco</div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="kpi" style="--kpi-c:var(--green)"><div class="kpi-label">Com WhatsApp</div><div class="kpi-value kpi-accent">{c_whats}</div><div class="kpi-sub">{pct_w}</div></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="kpi" style="--kpi-c:var(--coral-dark)"><div class="kpi-label">Com E-mail</div><div class="kpi-value">{c_email}</div><div class="kpi-sub">{pct_e}</div></div>', unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f'<div class="kpi" style="--kpi-c:var(--purple)"><div class="kpi-label">CNAE Principal</div><div class="kpi-value">{c_cnae_p}</div><div class="kpi-sub">Serviço beleza core</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Chips de Filtros Ativos
    chips = active_filter_chips(filters)
    if chips:
        st.markdown('<div class="sec-label">FILTROS ATIVOS · CLIQUE PARA REMOVER</div>', unsafe_allow_html=True)
        chip_cols = st.columns(min(6, len(chips)))
        for i, (label, name, value) in enumerate(chips):
            with chip_cols[i % len(chip_cols)]:
                if st.button(f"✕ {label}", key=f"chip_{i}_{name}", use_container_width=True):
                    remove_filter(name, value)
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # Abas Principais (Matching React Tabs)
    tab_cards, tab_table, tab_geo, tab_pitch, tab_export = st.tabs([
        "🗂️ Cards de Leads",
        "📊 Tabela Dinâmica",
        "🗺️ Bairros & Rotas",
        "💬 Smart Pitch WhatsApp",
        "📥 Exportar Base"
    ])

    # ABA 1: CARDS
    with tab_cards:
        if total_leads == 0:
            st.info("Nenhum lead encontrado com os filtros atuais.")
        else:
            page_size = 6
            total_pages = max(1, math.ceil(total_leads / page_size))
            c_info, c_pag = st.columns([3, 1])
            with c_info:
                st.caption(f"Exibindo {total_leads} estabelecimentos qualificados")
            with c_pag:
                page = st.selectbox("Página:", range(1, total_pages + 1), index=0, key="pag_cards")

            start_idx = (page - 1) * page_size
            df_page = df.iloc[start_idx: start_idx + page_size]

            cols_cards = st.columns(2)
            for i, (_, row) in enumerate(df_page.iterrows()):
                with cols_cards[i % 2]:
                    st.markdown(minify(build_card_html(row)), unsafe_allow_html=True)

    # ABA 2: TABELA
    with tab_table:
        if total_leads > 0:
            disp_data = []
            for _, row in df.iterrows():
                m_name, _ = get_display_name(row)
                disp_data.append({
                    "Estabelecimento": m_name,
                    "CNPJ": str(row.get("CNPJ", "—")),
                    "Segmento": str(row.get("SEGMENTO", "—")),
                    "Bairro": str(row.get("BAIRRO", "—")),
                    "Cidade/UF": f"{row.get('MUNICIPIO','')}/{row.get('ESTADO','')}",
                    "WhatsApp": format_phone_display(row.get("WHATSAPP_1", "")),
                    "Porte": str(row.get("PORTE", "—")),
                    "Simples": "Sim" if row.get("SIMPLES") else "Não",
                    "MEI": "Sim" if row.get("MEI") else "Não",
                })
            st.dataframe(pd.DataFrame(disp_data), use_container_width=True, height=500)
        else:
            st.info("Sem dados para tabela.")

    # ABA 3: GEO
    with tab_geo:
        st.subheader("Densidade Geográfica para Roteirização Comercial")
        if total_leads > 0 and "BAIRRO" in df.columns:
            b_counts = df["BAIRRO"].value_counts().reset_index()
            b_counts.columns = ["Bairro", "Quantidade"]
            
            fig = go.Figure(go.Bar(
                x=b_counts["Quantidade"],
                y=b_counts["Bairro"],
                orientation="h",
                marker_color="#4f46e5",
                text=b_counts["Quantidade"],
                textposition="outside"
            ))
            fig.update_layout(
                yaxis={"autorange": "reversed"},
                margin=dict(l=20, r=20, t=30, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=max(250, len(b_counts) * 35)
            )
            st.plotly_chart(fig, use_container_width=True)

    # ABA 4: SMART PITCH
    with tab_pitch:
        st.subheader("Gerador de Script de Abordagem WhatsApp")
        if total_leads > 0:
            lead_names = df["NOME FANTASIA"].tolist()
            sel_lead = st.selectbox("Selecione o Estabelecimento:", lead_names, key="pitch_sel")
            sel_row = df[df["NOME FANTASIA"] == sel_lead].iloc[0]
            
            bairro = sel_row.get("BAIRRO", "")
            wa_num = "".join(c for c in str(sel_row.get("WHATSAPP_1", "")) if c.isdigit())

            obj = st.radio(
                "Objetivo Comercial:",
                ["Apresentação & Tabela de Preços", "Oferta de Lançamento", "Visita Presencial"],
                horizontal=True
            )

            if obj == "Apresentação & Tabela de Preços":
                script = f"Olá, equipe do {sel_lead}! Tudo bem?\n\nMe chamo consultor da AcheiMeuCliente. Acompanhamos o trabalho de vocês no bairro {bairro} e gostaríamos de apresentar nossa linha com preços direto de fábrica.\n\nPodemos conversar 2 minutinhos?"
            elif obj == "Oferta de Lançamento":
                script = f"Olá {sel_lead}! Tudo bem?\n\nEstamos com uma condição exclusiva de desconto para salões do {bairro} esta semana. Gostaria de receber o catálogo com margem especial?"
            else:
                script = f"Olá {sel_lead}! Tudo bem?\n\nEstarei na região de {bairro} nesta semana. Poderia passar aí 15 minutos para apresentar os lançamentos e deixar amostras grátis com a gerência?"

            st.text_area("Mensagem Gerada:", script, height=130)
            if wa_num:
                url_dispatch = f"https://wa.me/55{wa_num}?text={script.replace(' ', '%20').replace('\n', '%0A')}"
                st.markdown(f'<a href="{url_dispatch}" target="_blank" class="btn-abordar" style="display:inline-flex;margin-top:8px;">🚀 Abrir WhatsApp Web com esta mensagem</a>', unsafe_allow_html=True)
            else:
                st.warning("Este salão não possui número de WhatsApp cadastrado.")

    # ABA 5: EXPORTAÇÃO
    with tab_export:
        st.subheader("Exportação de Dados")
        tier = user.get("tier", "operacional")
        exp_limit = TIER_CFG[tier]["limit"]
        
        if tier == "explorador":
            st.error("O download de dados é bloqueado no plano Explorador. Alterne para o perfil Operacional ou Regional na barra lateral para testar.")
        else:
            st.write(f"Exportando **{total_leads} leads**. Limite do seu plano: **{exp_limit}**.")
            c_csv, c_xlsx = st.columns(2)
            with c_csv:
                csv_data = df.to_csv(sep=";", index=False).encode("utf-8-sig")
                st.download_button(
                    label="📥 Baixar em CSV (Ponto e Vírgula)",
                    data=csv_data,
                    file_name=f"achei_leads_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            with c_xlsx:
                buf = BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                st.download_button(
                    label="📊 Baixar em Planilha Excel (.xlsx)",
                    data=buf.getvalue(),
                    file_name=f"achei_leads_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

if __name__ == "__main__":
    main()
