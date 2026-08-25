"""
AcheiMeuCliente — Plataforma de Inteligência de Mercado para Beleza
app.py — dashboard Streamlit de arquivo único (Streamlit Community Cloud)

Fase 1: dados mock / CSV local.
Para produção: trocar apenas o corpo de get_data() por uma consulta DuckDB.
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
    page_title="AcheiMeuCliente",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# 2. DESIGN SYSTEM (Notion / Linear)
# ══════════════════════════════════════════════════════════════
CSS = """
<style>
:root{
  --bg:#ffffff;
  --surface:#ffffff;
  --surface-2:#fbfbfa;
  --border:#e9e9e7;
  --border-strong:#dcdcd9;
  --text:#37352f;
  --text-2:#6b6b66;
  --muted:#9b9a97;
  --accent:#2f6fed;
  --accent-soft:#eef3fe;
  --green:#0f7b47;
  --green-soft:#eaf6ef;
  --amber:#9a6400;
  --amber-soft:#fdf6e7;
  --red:#b3261e;
  --radius:8px;
  --font:-apple-system,BlinkMacSystemFont,"Inter","Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"]{
  font-family:var(--font) !important;
  color:var(--text);
}
[data-testid="stAppViewContainer"]{ background:var(--bg); }
[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:2.2rem; padding-bottom:4rem; max-width:1380px; }

h1,h2,h3,h4,h5{ font-family:var(--font) !important; color:var(--text) !important; letter-spacing:-0.02em; }
hr{ border-color:var(--border) !important; margin:1rem 0 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"]{ background:var(--surface-2); border-right:1px solid var(--border); }
[data-testid="stSidebar"] .block-container{ padding-top:1.5rem; }
[data-testid="stSidebar"] [data-testid="stExpander"]{
  border:1px solid var(--border); border-radius:var(--radius); background:var(--surface);
}
[data-testid="stSidebar"] summary p{ font-size:12.5px !important; font-weight:600 !important; color:var(--text) !important; }
[data-testid="stSidebar"] label p{ font-size:12px !important; color:var(--text-2) !important; }

/* ── Botões ── */
.stButton>button, .stDownloadButton>button{
  border-radius:6px; border:1px solid var(--border-strong); background:var(--surface);
  color:var(--text); font-size:12.5px; font-weight:500; box-shadow:none;
  transition:background .12s ease, border-color .12s ease;
}
.stButton>button:hover, .stDownloadButton>button:hover{
  background:var(--surface-2); border-color:var(--muted); color:var(--text);
}
.stButton>button[kind="primary"]{ background:var(--text); border-color:var(--text); color:#fff; }
.stButton>button[kind="primary"]:hover{ background:#000; border-color:#000; color:#fff; }

/* ── Inputs ── */
[data-baseweb="input"], [data-baseweb="select"]>div, [data-baseweb="base-input"]{
  border-radius:6px !important; font-size:13px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{ gap:2px; border-bottom:1px solid var(--border); }
.stTabs [data-baseweb="tab"]{
  height:36px; padding:0 12px; background:transparent; font-size:13px;
  font-weight:500; color:var(--text-2); border-radius:6px 6px 0 0;
}
.stTabs [aria-selected="true"]{ color:var(--text) !important; box-shadow:inset 0 -2px 0 var(--text); }

/* ── Topbar ── */
.topbar{ display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:2px; }
.brand{ display:flex; align-items:center; gap:10px; }
.brand-mark{
  width:30px; height:30px; border-radius:7px; background:var(--text); color:#fff;
  display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700;
}
.brand-name{ font-size:19px; font-weight:600; letter-spacing:-0.02em; color:var(--text); }
.brand-sub{ font-size:12px; color:var(--muted); margin-top:1px; }
.plan-chip{
  display:inline-flex; align-items:center; gap:5px; font-size:11px; font-weight:600;
  padding:3px 9px; border-radius:20px; border:1px solid var(--border);
  background:var(--surface-2); color:var(--text-2); margin-left:8px; vertical-align:middle;
}
.plan-dot{ width:6px; height:6px; border-radius:50%; background:var(--green); }

/* ── Section label ── */
.sec-label{
  font-size:10.5px; font-weight:600; letter-spacing:.08em; text-transform:uppercase;
  color:var(--muted); margin:6px 0 8px;
}

/* ── KPI ── */
.kpi{
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  padding:14px 16px; height:100%;
}
.kpi-label{ font-size:11px; font-weight:600; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); }
.kpi-value{ font-size:26px; font-weight:600; letter-spacing:-0.03em; color:var(--text); margin-top:6px; line-height:1.1; }
.kpi-sub{ font-size:11.5px; color:var(--text-2); margin-top:4px; }
.kpi-accent{ color:var(--green); }
.kpi-warn{ color:var(--red); }

.mini-strip{
  display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;
}
.mini{
  flex:1 1 180px; border:1px solid var(--border); border-radius:var(--radius);
  background:var(--surface-2); padding:9px 12px; display:flex;
  align-items:baseline; justify-content:space-between; gap:10px;
}
.mini-k{ font-size:11.5px; color:var(--text-2); }
.mini-v{ font-size:13.5px; font-weight:600; color:var(--text); }

/* ── Chips de filtro ── */
.chip{
  display:inline-flex; align-items:center; gap:6px; font-size:11.5px; font-weight:500;
  padding:3px 9px; border-radius:20px; border:1px solid var(--border);
  background:var(--surface-2); color:var(--text-2); margin:0 5px 5px 0;
}

/* ── Card de lead ── */
.lead-card{
  background:var(--surface); border:1px solid var(--border); border-radius:10px;
  overflow:hidden; margin-bottom:12px; transition:border-color .12s ease, box-shadow .12s ease;
}
.lead-card:hover{ border-color:var(--border-strong); box-shadow:0 2px 8px rgba(15,15,15,.06); }
.card-top{ padding:14px 16px 12px; }
.card-identity{ display:flex; gap:11px; align-items:flex-start; margin-bottom:10px; }
.card-avatar{
  width:34px; height:34px; border-radius:7px; flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
  font-size:12.5px; font-weight:600; background:var(--surface-2);
  color:var(--text-2); border:1px solid var(--border);
}
.name-block{ flex:1; min-width:0; }
.company-main{ font-size:14.5px; font-weight:600; color:var(--text); line-height:1.3; letter-spacing:-0.01em; }
.company-sub{ font-size:11.5px; color:var(--muted); margin-top:2px; }
.tag{
  display:inline-flex; align-items:center; gap:5px; font-size:10.5px; font-weight:500;
  padding:2px 8px; border-radius:5px; border:1px solid var(--border);
  background:var(--surface-2); color:var(--text-2); margin-top:6px; margin-right:4px;
}
.tag-new{ background:var(--green-soft); border-color:#cfe8da; color:var(--green); }
.tag-warn{ background:var(--amber-soft); border-color:#f0e2bf; color:var(--amber); }

.card-info{ display:flex; flex-direction:column; gap:4px; font-size:11.5px; color:var(--text-2); margin-bottom:10px; }
.info-row{ display:flex; align-items:center; gap:6px; }

.cnae-strip{ padding:8px 10px; border-radius:6px; border:1px solid var(--border); background:var(--surface-2); font-size:11px; }
.cnae-strip-outside{ background:var(--amber-soft); border-color:#f0e2bf; }
.cnae-badge{ display:inline-flex; align-items:center; gap:4px; font-size:10px; font-weight:600;
  letter-spacing:.03em; text-transform:uppercase; color:var(--text-2); margin-bottom:5px; }
.cnae-badge-ok{ color:var(--green); }
.cnae-badge-out{ color:var(--amber); }
.cnae-code{ font-family:var(--mono); font-size:11px; color:var(--text); line-height:1.45; }

/* ── Contatos ── */
.contact-section{ border-top:1px solid var(--border); background:var(--surface-2); padding:6px 16px; }
.c-row{ display:flex; align-items:center; justify-content:space-between; gap:10px;
  padding:7px 0; border-bottom:1px solid var(--border); font-size:12px; }
.c-row:last-child{ border-bottom:none; }
.c-left{ display:flex; align-items:center; gap:9px; min-width:0; }
.c-ico{ width:22px; height:22px; border-radius:5px; display:inline-flex; align-items:center;
  justify-content:center; flex-shrink:0; background:#fff; border:1px solid var(--border); color:var(--text-2); }
.c-ico-wa{ color:var(--green); }
.c-val{ font-family:var(--mono); font-size:11.5px; color:var(--text); overflow:hidden; text-overflow:ellipsis; }
.c-link{ font-size:11px; font-weight:500; text-decoration:none; padding:3px 9px;
  border-radius:5px; border:1px solid var(--border); background:#fff; color:var(--text-2); white-space:nowrap; }
.c-link:hover{ border-color:var(--muted); color:var(--text); }
.c-link-wa{ color:var(--green); border-color:#cfe8da; background:var(--green-soft); }
.c-note{ font-size:11px; color:var(--amber); padding:7px 0; display:flex; align-items:center; gap:6px; }
.c-empty{ font-size:11px; color:var(--muted); padding:7px 0; }

/* ── Ações ── */
.action-buttons{ display:flex; gap:6px; padding:10px 16px; background:var(--surface); border-top:1px solid var(--border); }
.act-btn{
  flex:1; padding:6px 8px; border-radius:6px; border:1px solid var(--border);
  font-size:11.5px; font-weight:500; text-align:center; text-decoration:none;
  display:inline-flex; align-items:center; justify-content:center; gap:6px;
  background:var(--surface); color:var(--text-2); transition:all .12s ease;
}
.act-btn:hover{ background:var(--surface-2); border-color:var(--muted); color:var(--text); }
.act-btn-off{ opacity:.4; }

details.card-expand{ border-top:1px solid var(--border); }
details.card-expand summary{
  padding:9px 16px; font-size:11.5px; color:var(--text-2); cursor:pointer;
  list-style:none; display:flex; align-items:center; gap:6px; font-weight:500;
}
details.card-expand summary::-webkit-details-marker{ display:none; }
details.card-expand summary::before{ content:"›"; font-weight:700; transition:transform .15s; }
details.card-expand[open] summary::before{ transform:rotate(90deg); }
.expand-body{ padding:12px 16px; border-top:1px solid var(--border); background:var(--surface-2); }
.exp-section{ margin-bottom:14px; }
.exp-section:last-child{ margin-bottom:0; }
.exp-title{ font-size:10px; font-weight:600; letter-spacing:.07em; color:var(--muted);
  margin-bottom:6px; text-transform:uppercase; }
.box{ background:#fff; border:1px solid var(--border); border-radius:6px; padding:9px 11px;
  font-size:12px; color:var(--text); line-height:1.6; }
.cnae-item{ display:flex; gap:8px; align-items:center; font-size:11.5px; color:var(--text); padding:3px 0; }
.cnae-dot{ width:6px; height:6px; border-radius:50%; flex-shrink:0; }
.data-grid{ display:grid; grid-template-columns:1fr 1fr; gap:8px 16px; }
.data-item{ font-size:11.5px; }
.data-label{ color:var(--muted); display:block; margin-bottom:1px; }
.data-value{ color:var(--text); font-weight:500; }

/* ── Tabela ── */
.list-table-wrap{ overflow-x:auto; border:1px solid var(--border); border-radius:var(--radius); background:#fff; }
.list-table{ border-collapse:collapse; width:100%; font-size:12px; white-space:nowrap; }
.list-table th, .list-table td{ padding:8px 12px; border-bottom:1px solid var(--border); text-align:left; }
.list-table thead th{ background:var(--surface-2); color:var(--text-2); font-weight:600;
  font-size:11px; letter-spacing:.02em; position:sticky; top:0; }
.list-table tr.list-group th{ background:#f3f3f1; color:var(--muted); font-size:10px;
  text-transform:uppercase; letter-spacing:.08em; border-right:1px solid var(--border); }
.list-table tbody tr:hover{ background:var(--surface-2); }
.list-link{ color:var(--accent); text-decoration:none; font-weight:500; }

/* ── Barras horizontais ── */
.bar-row{ display:flex; align-items:center; gap:10px; margin-bottom:9px; font-size:12px; }
.bar-name{ width:132px; color:var(--text); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.bar-track{ flex:1; background:#efefed; border-radius:3px; height:6px; }
.bar-fill{ height:6px; border-radius:3px; background:var(--text); }
.bar-val{ width:34px; text-align:right; font-weight:600; color:var(--text); }

/* ── Estado vazio / avisos ── */
.empty{
  border:1px dashed var(--border-strong); border-radius:var(--radius); background:var(--surface-2);
  padding:34px 20px; text-align:center;
}
.empty-t{ font-size:14px; font-weight:600; color:var(--text); }
.empty-s{ font-size:12.5px; color:var(--text-2); margin-top:6px; }
.notice{
  border:1px solid var(--border); border-left:3px solid var(--accent); border-radius:6px;
  background:var(--surface-2); padding:11px 14px; font-size:12.5px; color:var(--text-2);
}
.notice-lock{ border-left-color:var(--amber); }

@media (max-width:768px){
  .block-container{ padding-top:1.2rem; }
  .data-grid{ grid-template-columns:1fr !important; }
  .action-buttons{ flex-wrap:wrap; }
  .act-btn{ flex:1 1 calc(50% - 3px); }
  .kpi-value{ font-size:21px; }
  .bar-name{ width:100px; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 3. CONSTANTES
# ══════════════════════════════════════════════════════════════
BEAUTY_CNAES = {
    "9602501": "Salões e Barbearias",
    "9602502": "Clínicas de Estética",
    "4646001": "Distribuidores Atacadistas",
    "4772500": "Lojas e Pontos de Venda",
    "4635401": "Representantes e Agentes",
    "2063100": "Fábricas e Marcas",
}

SEG_CFG = {
    "Salões e Barbearias": {"e": "✂"},
    "Clínicas de Estética": {"e": "✦"},
    "Distribuidores Atacadistas": {"e": "▤"},
    "Lojas e Pontos de Venda": {"e": "▣"},
    "Fábricas e Marcas": {"e": "▲"},
    "Representantes e Agentes": {"e": "◇"},
}

TIER_CFG = {
    "explorador":  {"label": "Explorador",  "limit": 0,      "states": 1},
    "operacional": {"label": "Operacional", "limit": 300,    "states": 1},
    "regional":    {"label": "Regional",    "limit": 1000,   "states": 5},
    "nacional":    {"label": "Nacional",    "limit": 999999, "states": 27},
}

MOCK_USERS = {
    "pro@achei.com":        {"nome": "Amanda",     "senha": "pro123",  "tier": "regional",    "exports_used": 45},
    "demo@achei.com":       {"nome": "Rafael",     "senha": "demo123", "tier": "operacional", "exports_used": 253},
    "admin@achei.com":      {"nome": "Admin",      "senha": "admin123","tier": "nacional",    "exports_used": 0},
    "explorador@achei.com": {"nome": "Explorador", "senha": "demo",    "tier": "explorador",  "exports_used": 0},
}

PROFILE_LABELS = {
    "pro@achei.com": "Amanda · Regional",
    "demo@achei.com": "Rafael · Operacional",
    "admin@achei.com": "Admin · Nacional",
    "explorador@achei.com": "Explorador · Gratuito",
}

KNOWN_CNAES = {
    "9602501": "Cabeleireiros, manicure e pedicure",
    "9602502": "Atividades de estética e outros serviços de cuidados com a beleza",
    "4772500": "Comércio varejista de cosméticos, produtos de perfumaria e de higiene pessoal",
    "4646001": "Comércio atacadista de cosméticos e produtos de perfumaria",
    "4618401": "Representantes comerciais de cosméticos e perfumaria",
    "2063100": "Fabricação de cosméticos, produtos de perfumaria e higiene pessoal",
    "4781400": "Comércio varejista de artigos do vestuário e acessórios",
    "4789002": "Comércio varejista de plantas e flores naturais",
    "4789001": "Comércio varejista de suvenires, bijuterias e artesanatos",
    "4789005": "Comércio varejista de produtos saneantes domissanitários",
    "4782201": "Comércio varejista de calçados",
    "4639701": "Comércio atacadista de produtos alimentícios em geral",
    "4642701": "Comércio atacadista de artigos do vestuário e acessórios",
    "4649408": "Comércio atacadista de produtos de higiene, limpeza e conservação",
    "8593700": "Ensino de idiomas",
    "9511800": "Reparação e manutenção de computadores",
    "1412601": "Confecção de peças de vestuário",
    "4729699": "Comércio varejista de produtos alimentícios em geral",
}

# ── Ícones SVG ──
SVG_WHATSAPP = '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:-2px"><path d="M12.012 2c-5.506 0-9.989 4.478-9.99 9.984 0 1.764.459 3.487 1.334 5.006l-1.417 5.176 5.297-1.389c1.464.798 3.116 1.218 4.774 1.219h.004c5.507 0 9.991-4.479 9.991-9.986 0-2.668-1.038-5.177-2.924-7.062a9.924 9.924 0 0 0-7.063-2.948zm5.952 14.183c-.252.71-1.464 1.348-2.016 1.408-.504.055-1.156.079-3.704-.972-3.08-1.272-5.074-4.423-5.228-4.63-.151-.205-1.246-1.657-1.246-3.161 0-1.503.785-2.241 1.063-2.548.277-.307.605-.383.807-.383.202 0 .404.001.58.01.187.008.439-.071.687.525.252.605.856 2.091.932 2.244.076.153.126.332.025.535-.1.205-.151.332-.302.508-.151.176-.317.393-.453.528-.151.151-.31.316-.134.619.176.303.78 1.288 1.674 2.085 1.15 1.025 2.119 1.343 2.422 1.494.303.151.48.126.657-.076.176-.202.756-.883.958-1.186.202-.303.404-.252.681-.151.277.101 1.764.832 2.067.983.303.151.504.227.58.353.076.126.076.73-.176 1.44z"/></svg>'
SVG_MAPS = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
SVG_MAIL = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'
SVG_PHONE = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
SVG_RECEITA = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
SVG_PIN = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
SVG_BUILDING = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="9" y1="6" x2="9" y2="6.01"/><line x1="15" y1="6" x2="15" y2="6.01"/><line x1="9" y1="10" x2="9" y2="10.01"/><line x1="15" y1="10" x2="15" y2="10.01"/><line x1="9" y1="14" x2="9" y2="14.01"/><line x1="15" y1="14" x2="15" y2="14.01"/></svg>'
SVG_CHECK = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px"><polyline points="20 6 9 17 4 12"/></svg>'
SVG_ALERT = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-1px"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'


# ══════════════════════════════════════════════════════════════
# 4. DADOS  (troque o corpo de get_data() por DuckDB em produção)
# ══════════════════════════════════════════════════════════════
def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    str_cols = ["RAZÃO SOCIAL", "NOME FANTASIA", "MUNICIPIO", "ESTADO", "BAIRRO", "CEP", "ORIGEM_CNAE", "SEGMENTO"]
    for c in str_cols:
        if c in df.columns:
            df[c] = df[c].fillna("").astype(str).str.strip()

    if "CNPJ" in df.columns:
        df["CNPJ"] = df["CNPJ"].apply(
            lambda v: f"{int(v):014d}"
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
             **{"RAZÃO SOCIAL": "Studio Bella Arte Cabeleireiros Ltda", "NOME FANTASIA": "Studio Bella Arte"},
             TELEFONE_1="(11) 3456-7890", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 98765-4321", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL": "contato@studiobella.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Pinheiros", CEP="05422-001", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA": "Rua dos Pinheiros, 100 - Pinheiros, São Paulo - SP",
                "MAPS": "https://maps.google.com/?q=Studio+Bella+Arte+Pinheiros"},
             **{"MATRIZ FILIAL": "Matriz", "PORTE": "ME", "CAPITAL SOCIAL": "50000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE": "2018-03-15",
                "RECEITA FEDERAL": "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=12345678000190",
                "NATUREZA_JURIDICA": "Empresário Individual", "SITE": "www.studiobella.com.br"},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="98.765.432/0001-10",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL": "Barbearia Vintage Club Eireli", "NOME FANTASIA": "Barbearia Vintage"},
             TELEFONE_1="(11) 3333-4444", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 97777-8888", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL": "barba@vintageclub.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Moema", CEP="04510-000", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA": "Av. Moema, 450 - Moema, São Paulo - SP",
                "MAPS": "https://maps.google.com/?q=Barbearia+Vintage+Moema"},
             **{"MATRIZ FILIAL": "Matriz", "PORTE": "ME", "CAPITAL SOCIAL": "30000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE": "2020-07-01",
                "RECEITA FEDERAL": "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=98765432000110",
                "NATUREZA_JURIDICA": "EIRELI", "SITE": ""},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="secundario",
             CNPJ="55.666.777/0001-88",
             CNAE_PRINCIPAL_CODIGO="4729699", CNAE_PRINCIPAL_NOME="Comércio varejista de produtos alimentícios",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos e perfumaria",
             **{"RAZÃO SOCIAL": "Mercado Rosa Cosméticos ME", "NOME FANTASIA": "Rosa Cosméticos"},
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
             CNPJ="78.901.234/0001-56",
             CNAE_PRINCIPAL_CODIGO="9602502", CNAE_PRINCIPAL_NOME="Atividades de estética e cuidados com a beleza",
             CNAE_SECUNDARIO_CODIGO="9602501", CNAE_SECUNDARIO_NOME="Cabeleireiros, manicure e pedicure",
             **{"RAZÃO SOCIAL": "Clínica Estética Evolução Ltda", "NOME FANTASIA": "Evolução Estética"},
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
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
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
    """Colapsa HTML multi-linha em linha única para o parser de Markdown."""
    return re.sub(r"\n[ \t]*", " ", html).strip()


def get_secondary_cnaes(row):
    raw_cods = str(row.get("CNAE_SECUNDARIO_CODIGO", ""))
    raw_noms = str(row.get("CNAE_SECUNDARIO_NOME", ""))
    if not raw_cods or raw_cods.strip() in ("nan", "None", ""):
        return []
    cods = [c.strip() for c in raw_cods.split(",") if c.strip()]
    noms = [n.strip() for n in raw_noms.split("|") if n.strip()]
    items = []
    for i, cod in enumerate(cods):
        name = KNOWN_CNAES.get(cod) or (noms[i] if i < len(noms) else "Outra atividade cadastrada")
        items.append({"code": cod, "name": name, "is_beauty": cod in BEAUTY_CNAES})
    return items


def format_phone_display(phone_str):
    if not phone_str or pd.isna(phone_str) or str(phone_str).strip() in ("", "nan", "None"):
        return ""
    s = str(phone_str).strip()
    digits = "".join(c for c in s if c.isdigit())
    if digits.startswith("55") and len(digits) >= 12:
        digits = digits[2:]
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    if len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return s.split(".")[0]


def get_display_name(row):
    nf = escape(str(row.get("NOME FANTASIA", "")).strip())
    rs = escape(str(row.get("RAZÃO SOCIAL", "")).strip())
    return (nf, rs) if nf else (rs, "")


def get_cnae_status(row):
    origem = str(row.get("ORIGEM_CNAE", "")).lower()
    cod_p = str(row.get("CNAE_PRINCIPAL_CODIGO", "")).replace("-", "").replace("/", "").replace(".", "")
    nom_p = str(row.get("CNAE_PRINCIPAL_NOME", ""))
    cod_s = str(row.get("CNAE_SECUNDARIO_CODIGO", "")).replace("-", "").replace("/", "").replace(".", "")
    nom_s = str(row.get("CNAE_SECUNDARIO_NOME", ""))
    is_beauty_principal = cod_p in BEAUTY_CNAES
    if origem == "principal" and is_beauty_principal:
        return "primary", cod_p, nom_p
    if origem == "secundario" or not is_beauty_principal:
        return "secondary", cod_s, nom_s
    return "primary", cod_p, nom_p


def get_initials(name):
    if not name or not str(name).strip():
        return "CN"
    parts = str(name).strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return str(name)[:2].upper()


def clean_phone(phone):
    return "".join(c for c in str(phone) if c.isdigit())


def wa_link(phone):
    if not phone or str(phone).strip() in ("", "#", "nan", "None"):
        return "#"
    raw = str(phone).strip()
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    cp = clean_phone(raw)
    if cp.startswith("55") and len(cp) >= 12:
        return f"https://wa.me/{cp}"
    if len(cp) >= 10:
        return f"https://wa.me/55{cp}"
    return "#"


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
# 6. ESTADO — fonte única de verdade dos filtros
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

CHIP_LABELS = {
    "tem_email": "Com e-mail",
    "sem_contador": "Sem e-mail de contador",
    "tem_whatsapp": "Com WhatsApp",
    "origem_cnae": "CNAE",
    "busca_texto": "Busca",
    "mei": "MEI",
    "simples": "Simples",
    "anos_range": "Anos de atividade",
}


def k(name):
    """Chave do widget correspondente ao filtro."""
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
    if not st.session_state.get("user"):
        st.session_state.user = MOCK_USERS["pro@achei.com"].copy()
        st.session_state.user_email = "pro@achei.com"


def read_filters():
    return {name: st.session_state.get(k(name), val) for name, val in FILTER_DEFAULTS.items()}


def reset_filters(new_values=None):
    for name, val in FILTER_DEFAULTS.items():
        st.session_state[k(name)] = val
    for name, val in (new_values or {}).items():
        if name in FILTER_DEFAULTS:
            st.session_state[k(name)] = val


def active_filter_chips(filters):
    """Lista de (label, nome_do_filtro, valor_a_remover)."""
    chips = []
    for name in ("tem_email", "sem_contador", "tem_whatsapp"):
        if filters.get(name):
            chips.append((CHIP_LABELS[name], name, None))
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
    if filters.get("simples") != "Todos":
        chips.append((f"Simples: {filters['simples']}", "simples", None))
    if tuple(filters.get("anos_range", (0, 25))) != (0, 25):
        a, b = filters["anos_range"]
        chips.append((f"{a}–{b} anos", "anos_range", None))
    return chips


def remove_filter(name, value=None):
    if value is None:
        st.session_state[k(name)] = FILTER_DEFAULTS[name]
    else:
        current = list(st.session_state.get(k(name), []))
        st.session_state[k(name)] = [v for v in current if v != value]


# ══════════════════════════════════════════════════════════════
# 7. SIDEBAR — navegação e filtros
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
        st.markdown(
            '<div class="brand"><div class="brand-mark">A</div>'
            '<div><div class="brand-name" style="font-size:15px">AcheiMeuCliente</div>'
            '<div class="brand-sub">Inteligência de mercado</div></div></div>',
            unsafe_allow_html=True,
        )
        st.markdown("")

        sel = st.selectbox(
            "Perfil de acesso",
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

        st.markdown('<div class="sec-label">Visualizações salvas</div>', unsafe_allow_html=True)
        for i, sv in enumerate(st.session_state.saved_views):
            if st.button(sv["name"], key=f"sv_{i}", width="stretch"):
                reset_filters(sv["filters"])
                st.toast(f"Visualização “{sv['name']}” aplicada")
                st.rerun()

        st.markdown('<div class="sec-label">Filtros</div>', unsafe_allow_html=True)

        with st.expander(group_title("Contato", ["tem_email", "sem_contador", "tem_whatsapp"], prev), expanded=True):
            st.checkbox("Com e-mail", key=k("tem_email"))
            st.checkbox("Excluir e-mail de contador", key=k("sem_contador"))
            st.checkbox("Com WhatsApp confirmado", key=k("tem_whatsapp"))

        with st.expander(group_title("Segmento e CNAE", ["segmentos", "origem_cnae"], prev), expanded=False):
            st.multiselect("Segmento", list(SEG_CFG.keys()), key=k("segmentos"), placeholder="Todos")
            st.selectbox(
                "Origem do match CNAE",
                ["Principal ou Secundário", "Apenas CNAE principal", "Apenas CNAE secundário"],
                key=k("origem_cnae"),
            )

        with st.expander(group_title("Localização", ["estados", "municipios", "bairros"], prev), expanded=False):
            estados = sorted(df["ESTADO"].dropna().unique().tolist())
            st.multiselect("Estado", estados, key=k("estados"), placeholder="Todos")

            sel_uf = st.session_state.get(k("estados"), [])
            base = df[df["ESTADO"].isin(sel_uf)] if sel_uf else df
            mun_opts = sorted(base["MUNICIPIO"].dropna().unique().tolist())
            st.session_state[k("municipios")] = [m for m in st.session_state.get(k("municipios"), []) if m in mun_opts]
            st.multiselect("Município", mun_opts, key=k("municipios"), placeholder="Todos")

            sel_mun = st.session_state.get(k("municipios"), [])
            bai_opts = sorted(df[df["MUNICIPIO"].isin(sel_mun)]["BAIRRO"].dropna().unique().tolist()) if sel_mun else []
            st.session_state[k("bairros")] = [b for b in st.session_state.get(k("bairros"), []) if b in bai_opts]
            st.multiselect("Bairro", bai_opts, key=k("bairros"), placeholder="Selecione um município primeiro")

        with st.expander(group_title("Perfil da empresa", ["portes", "mei", "simples", "anos_range"], prev), expanded=False):
            st.multiselect("Porte", ["MEI", "ME", "EPP", "Grande"], key=k("portes"), placeholder="Todos")
            st.selectbox("MEI", ["Todos", "Apenas MEI", "Excluir MEI"], key=k("mei"))
            st.selectbox("Simples Nacional", ["Todos", "Sim", "Não"], key=k("simples"))
            st.slider("Anos de atividade", 0, 25, key=k("anos_range"))

        filters = read_filters()

        if active_filter_chips(filters):
            if st.button("Limpar filtros", key="clear_all", width="stretch"):
                reset_filters()
                st.toast("Filtros limpos")
                st.rerun()

        st.markdown('<div class="sec-label">Salvar visualização</div>', unsafe_allow_html=True)
        name = st.text_input("Nome", key="save_view_name", placeholder="Ex: SP · Salões 2026", label_visibility="collapsed")
        if st.button("Salvar filtro atual", key="save_view", width="stretch"):
            if name.strip():
                st.session_state.saved_views.append({"name": name.strip(), "filters": filters.copy()})
                st.toast(f"“{name.strip()}” salvo")
                st.rerun()
            else:
                st.toast("Dê um nome para a visualização")

    return filters


# ══════════════════════════════════════════════════════════════
# 8. FILTROS
# ══════════════════════════════════════════════════════════════
def apply_filters(df, filters):
    mask = pd.Series([True] * len(df), index=df.index)

    if filters.get("tem_email"):
        mask &= df["TEM_EMAIL"] == True  # noqa: E712
    if filters.get("sem_contador"):
        mask &= df["EMAIL_CONTABILIDADE"] == False  # noqa: E712
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
        )
    if filters.get("portes"):
        mask &= df["PORTE"].isin(filters["portes"])

    mei_f = filters.get("mei", "Todos")
    if mei_f == "Apenas MEI":
        mask &= df["MEI"] == True  # noqa: E712
    elif mei_f == "Excluir MEI":
        mask &= df["MEI"] == False  # noqa: E712

    simples_f = filters.get("simples", "Todos")
    if simples_f == "Sim":
        mask &= df["SIMPLES"] == True  # noqa: E712
    elif simples_f == "Não":
        mask &= df["SIMPLES"] == False  # noqa: E712

    anos_r = filters.get("anos_range", (0, 25))
    if "ANOS_ATIVIDADE" in df.columns:
        mask &= (df["ANOS_ATIVIDADE"] >= anos_r[0]) & (df["ANOS_ATIVIDADE"] <= anos_r[1])

    return df[mask].copy()


# ══════════════════════════════════════════════════════════════
# 9. TOPBAR
# ══════════════════════════════════════════════════════════════
def show_topbar(df_full):
    user = st.session_state.user
    tier = user.get("tier", "operacional")
    tier_label = TIER_CFG[tier]["label"]

    left, right = st.columns([2.4, 1])
    with left:
        st.markdown(
            f"""<div class="brand">
              <div class="brand-mark">A</div>
              <div>
                <div class="brand-name">AcheiMeuCliente
                  <span class="plan-chip"><span class="plan-dot"></span>{tier_label}</span>
                </div>
                <div class="brand-sub">{user.get('nome','Usuário')} · base com {len(df_full):,} empresas de beleza</div>
              </div>
            </div>""".replace(",", "."),
            unsafe_allow_html=True,
        )
    with right:
        st.text_input(
            "Buscar",
            key=k("busca_texto"),
            placeholder="Buscar por nome, razão social ou CNPJ",
            label_visibility="collapsed",
        )

    st.markdown("<hr>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 10. KPIs
# ══════════════════════════════════════════════════════════════
def kpi(label, value, sub, cls=""):
    return f"""<div class="kpi">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value {cls}">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>"""


def show_kpis(df, user):
    total = len(df)
    c_whats = int(df["WHATSAPP_1"].astype(str).str.strip().str.len().gt(0).sum()) if total else 0
    c_email = int(df["TEM_EMAIL"].sum()) if total else 0
    c_nova = int(df["INICIO ATIVIDADE"].apply(lambda d: is_new(d, 1)).sum()) if total else 0
    c_sem_c = int((df["EMAIL_CONTABILIDADE"] == False).sum()) if total else 0  # noqa: E712
    avg_anos = df["ANOS_ATIVIDADE"].mean() if total else float("nan")
    avg_str = f"{avg_anos:.0f} anos" if not pd.isna(avg_anos) else "—"

    tier = user.get("tier", "operacional")
    exp_used = user.get("exports_used", 0)
    exp_limit = TIER_CFG[tier]["limit"]
    if tier == "explorador":
        exp_str = "Bloqueado"
    elif exp_limit >= 999999:
        exp_str = "Ilimitado"
    else:
        exp_str = f"{exp_used} / {exp_limit}"

    pct_w = f"{c_whats/total*100:.0f}% do filtro" if total else "—"
    pct_e = f"{c_email/total*100:.0f}% do filtro" if total else "—"

    cols = st.columns(4)
    cards = [
        kpi("Leads", f"{total:,}".replace(",", "."), "no filtro atual"),
        kpi("Com WhatsApp", f"{c_whats:,}".replace(",", "."), pct_w, "kpi-accent"),
        kpi("Com e-mail", f"{c_email:,}".replace(",", "."), pct_e),
        kpi("Novas no mês", f"{c_nova:,}".replace(",", "."), "abertas nos últimos 30 dias"),
    ]
    for col, card in zip(cols, cards):
        col.markdown(minify(card), unsafe_allow_html=True)

    st.markdown(
        minify(f"""<div class="mini-strip">
          <div class="mini"><span class="mini-k">Idade média da empresa</span><span class="mini-v">{avg_str}</span></div>
          <div class="mini"><span class="mini-k">Contato direto (sem contador)</span><span class="mini-v">{c_sem_c}</span></div>
          <div class="mini"><span class="mini-k">Exports do plano</span><span class="mini-v">{exp_str}</span></div>
        </div>"""),
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════
# 11. GRÁFICOS
# ══════════════════════════════════════════════════════════════
def bar_fig(labels, values):
    fig = go.Figure(
        go.Bar(
            x=values, y=labels, orientation="h",
            marker_color="#37352f", marker_line_width=0,
            text=values, textposition="outside",
            textfont=dict(size=11, color="#6b6b66"),
            hovertemplate="%{y}: %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        margin=dict(l=0, r=34, t=4, b=0),
        height=max(120, 34 * len(labels)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#37352f")),
        showlegend=False, bargap=0.35,
        font=dict(family="-apple-system, BlinkMacSystemFont, Inter, sans-serif"),
    )
    return fig


def bars_html(pairs, accent="var(--text)"):
    max_c = max([v for _, v in pairs], default=0)
    out = []
    for name, val in pairs:
        pct = (val / max_c * 100) if max_c else 0
        out.append(
            f'<div class="bar-row"><span class="bar-name">{escape(str(name))}</span>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct:.0f}%;background:{accent}"></div></div>'
            f'<span class="bar-val">{val}</span></div>'
        )
    return "".join(out)


def show_charts(df):
    if len(df) == 0:
        return
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="sec-label">CNAE principal — top 5</div>', unsafe_allow_html=True)
        top_p = df.groupby("CNAE_PRINCIPAL_NOME").size().sort_values(ascending=False).head(5).reset_index()
        top_p.columns = ["CNAE", "Count"]
        labels = [c[:30] + ("…" if len(c) > 30 else "") for c in top_p["CNAE"]]
        st.plotly_chart(bar_fig(labels, top_p["Count"].tolist()), width="stretch", config={"displayModeBar": False})

    with c2:
        st.markdown('<div class="sec-label">CNAE secundário — top 5</div>', unsafe_allow_html=True)
        sec_df = df[df["CNAE_SECUNDARIO_NOME"].astype(str).str.strip() != ""]
        if len(sec_df) == 0:
            st.markdown('<div class="notice">Nenhum CNAE secundário no filtro atual.</div>', unsafe_allow_html=True)
        else:
            top_s = sec_df.groupby("CNAE_SECUNDARIO_NOME").size().sort_values(ascending=False).head(5).reset_index()
            top_s.columns = ["CNAE", "Count"]
            labels = [c[:30] + ("…" if len(c) > 30 else "") for c in top_s["CNAE"]]
            st.plotly_chart(bar_fig(labels, top_s["Count"].tolist()), width="stretch", config={"displayModeBar": False})

    st.markdown('<div class="sec-label">Empresas por município — top 6</div>', unsafe_allow_html=True)
    top_m = df.groupby("MUNICIPIO").size().sort_values(ascending=False).head(6).reset_index()
    top_m.columns = ["Município", "Count"]
    pairs = list(zip(top_m["Município"], top_m["Count"]))
    cols_m = st.columns(3)
    for i in range(3):
        chunk = pairs[i::3]
        if chunk:
            cols_m[i].markdown(minify(bars_html(chunk)), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# 12. CARD DE LEAD
# ══════════════════════════════════════════════════════════════
def build_card_html(row):
    main_name, sub_name = get_display_name(row)
    initials = get_initials(main_name)
    seg = row.get("SEGMENTO", "Salões e Barbearias")
    seg_icon = SEG_CFG.get(seg, {"e": "◇"})["e"]

    cnae_status, _, _ = get_cnae_status(row)
    cod_p = escape(str(row.get("CNAE_PRINCIPAL_CODIGO", "")))
    nom_p = escape(str(row.get("CNAE_PRINCIPAL_NOME", "")))
    sec_cnaes = get_secondary_cnaes(row)
    beauty_sec = sum(1 for c in sec_cnaes if c["is_beauty"])

    if cnae_status == "primary":
        strip_cls = "cnae-strip"
        extra = f" · +{len(sec_cnaes)} secundário(s)" if sec_cnaes else ""
        strip_html = (
            f'<div class="cnae-badge cnae-badge-ok">{SVG_CHECK} Beleza no CNAE principal</div>'
            f'<div class="cnae-code">{cod_p} · {nom_p}{extra}</div>'
        )
    else:
        strip_cls = "cnae-strip cnae-strip-outside"
        sec_line = (
            f'<div class="cnae-badge cnae-badge-ok" style="margin-top:5px">{SVG_CHECK} Beleza em {beauty_sec} CNAE secundário(s)</div>'
            if beauty_sec else
            f'<div class="cnae-badge" style="margin-top:5px">{len(sec_cnaes)} CNAE(s) secundário(s)</div>'
        )
        strip_html = (
            f'<div class="cnae-badge cnae-badge-out">{SVG_ALERT} CNAE principal fora da beleza</div>'
            f'<div class="cnae-code">{cod_p} · {nom_p}</div>{sec_line}'
        )

    tags = f'<span class="tag">{seg_icon} {escape(seg)}</span>'
    if is_new(row.get("INICIO ATIVIDADE")):
        tags += '<span class="tag tag-new">Nova</span>'
    if row.get("EMAIL_CONTABILIDADE"):
        tags += '<span class="tag tag-warn">E-mail de contador</span>'

    bairro_str = escape(str(row.get("BAIRRO", "")))
    mun_str = escape(str(row.get("MUNICIPIO", "")))
    uf_str = escape(str(row.get("ESTADO", "")))
    loc_text = f"{bairro_str} · {mun_str} — {uf_str}" if bairro_str else f"{mun_str} — {uf_str}"

    # ── Contatos ──
    added, c_rows = set(), ""
    for i in range(1, 4):
        num = row.get(f"WHATSAPP_{i}", "")
        fmt = format_phone_display(num)
        if fmt and fmt not in added:
            added.add(fmt)
            c_rows += (
                f'<div class="c-row"><div class="c-left">'
                f'<span class="c-ico c-ico-wa">{SVG_WHATSAPP}</span><span class="c-val">{fmt}</span></div>'
                f'<a class="c-link c-link-wa" href="{wa_link(str(num))}" target="_blank">WhatsApp</a></div>'
            )
    for i in range(1, 4):
        num = row.get(f"TELEFONE_{i}", "")
        fmt = format_phone_display(num)
        if fmt and fmt not in added:
            added.add(fmt)
            c_rows += (
                f'<div class="c-row"><div class="c-left">'
                f'<span class="c-ico">{SVG_PHONE}</span><span class="c-val">{fmt}</span></div>'
                f'<a class="c-link" href="tel:{clean_phone(str(num))}">Ligar</a></div>'
            )

    email = escape(str(row.get("E-MAIL", "")).strip())
    is_contador = bool(row.get("EMAIL_CONTABILIDADE", False))
    if email and email != "nan" and not is_contador:
        c_rows += (
            f'<div class="c-row"><div class="c-left">'
            f'<span class="c-ico">{SVG_MAIL}</span><span class="c-val">{email}</span></div>'
            f'<a class="c-link" href="mailto:{email}">E-mail</a></div>'
        )
    elif email and email != "nan" and is_contador:
        c_rows += f'<div class="c-note">{SVG_ALERT} E-mail de contador — evite usar em prospecção</div>'

    if not c_rows:
        c_rows = '<div class="c-empty">Nenhum contato direto neste cadastro</div>'

    maps_url = escape(str(row.get("MAPS", "#")), quote=True)
    rf_url = escape(str(row.get("RECEITA FEDERAL", "#")).strip(), quote=True)
    rf_btn = (
        f'<a class="act-btn" href="{rf_url}" target="_blank">{SVG_RECEITA} Receita Federal</a>'
        if rf_url and rf_url != "#" else
        f'<span class="act-btn act-btn-off">{SVG_RECEITA} Sem Receita</span>'
    )
    maps_btn = (
        f'<a class="act-btn" href="{maps_url}" target="_blank">{SVG_MAPS} Google Maps</a>'
        if maps_url and maps_url != "#" else
        f'<span class="act-btn act-btn-off">{SVG_MAPS} Sem Maps</span>'
    )

    endereco = escape(str(row.get("ENDERECO MAPA", "—")))
    cep = escape(str(row.get("CEP", "")))
    porte = escape(str(row.get("PORTE", "—")))
    anos_str = f"{row.get('ANOS_ATIVIDADE', 0):.1f} anos"
    dt = row.get("INICIO ATIVIDADE")
    abertura = pd.to_datetime(dt).strftime("%m/%Y") if pd.notna(dt) else "—"
    inicio = pd.to_datetime(dt).strftime("%d/%m/%Y") if pd.notna(dt) else "—"

    cnae_items = []
    is_b_p = cod_p.replace("-", "").replace("/", "").replace(".", "") in BEAUTY_CNAES
    cnae_items.append(
        f'<div class="cnae-item"><div class="cnae-dot" style="background:{"#0f7b47" if is_b_p else "#c9c9c5"}"></div>'
        f'<b>Principal</b> · {cod_p} — {nom_p}</div>'
    )
    if sec_cnaes:
        for sc in sec_cnaes:
            cnae_items.append(
                f'<div class="cnae-item"><div class="cnae-dot" style="background:{"#0f7b47" if sc["is_beauty"] else "#c9c9c5"}"></div>'
                f'<b>Secundário</b> · {escape(sc["code"])} — {escape(sc["name"])}</div>'
            )
    else:
        cnae_items.append('<div class="cnae-item"><div class="cnae-dot" style="background:#e0e0dd"></div>Sem CNAEs secundários</div>')

    return f"""
<div class="lead-card">
  <div class="card-top">
    <div class="card-identity">
      <div class="card-avatar">{initials}</div>
      <div class="name-block">
        <div class="company-main">{main_name}</div>
        {"<div class='company-sub'>" + sub_name + "</div>" if sub_name else ""}
        <div>{tags}</div>
      </div>
    </div>
    <div class="card-info">
      <div class="info-row">{SVG_PIN} {loc_text}</div>
      <div class="info-row">{SVG_BUILDING} {porte} · abertura {abertura} · {anos_str}</div>
    </div>
    <div class="{strip_cls}">{strip_html}</div>
  </div>
  <div class="contact-section">{c_rows}</div>
  <div class="action-buttons">{rf_btn}{maps_btn}</div>
  <details class="card-expand">
    <summary>Dados cadastrais completos</summary>
    <div class="expand-body">
      <div class="exp-section">
        <div class="exp-title">Endereço</div>
        <div class="box">{endereco}<br>{bairro_str} · {mun_str}/{uf_str} · CEP {cep}</div>
      </div>
      <div class="exp-section">
        <div class="exp-title">CNAEs ({1 + len(sec_cnaes)})</div>
        <div class="box">{"".join(cnae_items)}</div>
      </div>
      <div class="exp-section">
        <div class="exp-title">Cadastro</div>
        <div class="data-grid">
          <div class="data-item"><span class="data-label">CNPJ</span><span class="data-value">{escape(str(row.get('CNPJ','—')))}</span></div>
          <div class="data-item"><span class="data-label">Porte</span><span class="data-value">{porte}</span></div>
          <div class="data-item"><span class="data-label">Capital social</span><span class="data-value">{format_capital(row.get('CAPITAL SOCIAL', 0))}</span></div>
          <div class="data-item"><span class="data-label">Natureza jurídica</span><span class="data-value">{escape(str(row.get('NATUREZA_JURIDICA','—')))}</span></div>
          <div class="data-item"><span class="data-label">MEI</span><span class="data-value">{"Sim" if row.get("MEI") else "Não"}</span></div>
          <div class="data-item"><span class="data-label">Simples Nacional</span><span class="data-value">{"Sim" if row.get("SIMPLES") else "Não"}</span></div>
          <div class="data-item"><span class="data-label">Início de atividade</span><span class="data-value">{inicio}</span></div>
          <div class="data-item"><span class="data-label">Matriz / filial</span><span class="data-value">{escape(str(row.get('MATRIZ FILIAL','—')))}</span></div>
        </div>
      </div>
    </div>
  </details>
</div>"""


# ══════════════════════════════════════════════════════════════
# 13. VIEWS
# ══════════════════════════════════════════════════════════════
def empty_state(msg="Nenhum lead com os filtros atuais."):
    st.markdown(
        minify(f"""<div class="empty">
          <div class="empty-t">{msg}</div>
          <div class="empty-s">Remova um filtro na barra lateral ou nos chips acima para ampliar o resultado.</div>
        </div>"""),
        unsafe_allow_html=True,
    )
    if st.button("Limpar todos os filtros", key="empty_clear", type="primary"):
        reset_filters()
        st.rerun()


def paginate(df, page_size, key):
    total_pages = max(1, math.ceil(len(df) / page_size))
    page = 1
    if total_pages > 1:
        c1, c2 = st.columns([1, 4])
        with c1:
            page = st.number_input("Página", 1, total_pages, 1, 1, key=key, label_visibility="collapsed")
        with c2:
            ini = (page - 1) * page_size + 1
            fim = min(page * page_size, len(df))
            st.caption(f"Página {page} de {total_pages} · exibindo {ini}–{fim} de {len(df)} leads")
    return df.iloc[(page - 1) * page_size: page * page_size]


def show_cards(df):
    if len(df) == 0:
        empty_state()
        return
    df_page = paginate(df, 20, "page_cards")
    cols = st.columns(2)
    for i in range(len(df_page)):
        with cols[i % 2]:
            st.markdown(minify(build_card_html(df_page.iloc[i])), unsafe_allow_html=True)


def show_list(df):
    if len(df) == 0:
        empty_state()
        return
    df_page = paginate(df, 50, "page_list")

    column_groups = [
        ("Empresa", ["RAZÃO SOCIAL", "NOME FANTASIA", "MUNICIPIO", "ESTADO"]),
        ("Classificação", ["SEGMENTO", "CNAE_MATCHED", "ORIGEM_CNAE"]),
        ("Contatos", ["WHATSAPP_1", "TELEFONE_1", "E-MAIL", "TEM_EMAIL", "TEM_TELEFONE", "EMAIL_CONTABILIDADE"]),
        ("Localização", ["BAIRRO", "CEP", "ENDERECO MAPA", "MAPS"]),
        ("Cadastro", ["CNPJ", "PORTE", "CAPITAL SOCIAL", "MEI", "SIMPLES", "MATRIZ FILIAL", "INICIO ATIVIDADE", "NATUREZA_JURIDICA"]),
        ("Atividade", ["CNAE_PRINCIPAL_CODIGO", "CNAE_PRINCIPAL_NOME", "CNAE_SECUNDARIO_CODIGO", "CNAE_SECUNDARIO_NOME"]),
        ("Origem", ["RECEITA FEDERAL", "SITE"]),
    ]
    columns = [c for _, group in column_groups for c in group]
    labels = {
        "RAZÃO SOCIAL": "Razão Social", "NOME FANTASIA": "Nome Fantasia", "CNAE_MATCHED": "CNAE Matched",
        "ORIGEM_CNAE": "Origem CNAE", "TEM_EMAIL": "Tem E-mail", "TEM_TELEFONE": "Tem Telefone",
        "EMAIL_CONTABILIDADE": "E-mail Contabilidade", "ENDERECO MAPA": "Endereço", "MAPS": "Maps",
        "CAPITAL SOCIAL": "Capital Social", "MATRIZ FILIAL": "Matriz/Filial", "INICIO ATIVIDADE": "Início Atividade",
        "NATUREZA_JURIDICA": "Natureza Jurídica", "RECEITA FEDERAL": "Receita Federal",
        "CNAE_PRINCIPAL_CODIGO": "CNAE Principal", "CNAE_PRINCIPAL_NOME": "Nome CNAE Principal",
        "CNAE_SECUNDARIO_CODIGO": "CNAE Secundário", "CNAE_SECUNDARIO_NOME": "Nome CNAE Secundário",
    }

    def cell_value(row, column):
        value = row.get(column, "")
        if not isinstance(value, (list, tuple, dict)) and pd.isna(value):
            return "—"
        if column in {"MEI", "SIMPLES", "TEM_EMAIL", "TEM_TELEFONE", "EMAIL_CONTABILIDADE", "CNAE_MATCHED"}:
            return "Sim" if bool(value) else "Não"
        if column == "CAPITAL SOCIAL":
            return format_capital(value)
        if column == "INICIO ATIVIDADE":
            return pd.to_datetime(value).strftime("%d/%m/%Y") if value else "—"
        return str(value).strip() or "—"

    def render_cell(row, column):
        value = cell_value(row, column)
        if column in {"MAPS", "RECEITA FEDERAL", "SITE"} and value != "—":
            href = escape(value if column != "SITE" else f"http://{value}", quote=True)
            label = "Mapa" if column == "MAPS" else ("Abrir" if column == "RECEITA FEDERAL" else "Visitar")
            return f'<a class="list-link" href="{href}" target="_blank">{label}</a>'
        return escape(value)

    body = "".join(
        "<tr>" + "".join(f"<td>{render_cell(row, c)}</td>" for c in columns) + "</tr>"
        for _, row in df_page.iterrows()
    )
    group_headers = "".join(f'<th colspan="{len(g)}">{name}</th>' for name, g in column_groups)
    column_headers = "".join(f"<th>{labels.get(c, c.title())}</th>" for c in columns)

    st.markdown(
        minify(f"""<div class="list-table-wrap">
          <table class="list-table">
            <thead><tr class="list-group">{group_headers}</tr><tr>{column_headers}</tr></thead>
            <tbody>{body}</tbody>
          </table>
        </div>"""),
        unsafe_allow_html=True,
    )
    st.caption("Deslize a tabela horizontalmente para ver todos os campos.")


def show_bairro(df):
    if len(df) == 0:
        empty_state()
        return

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-label">Concentração por município</div>', unsafe_allow_html=True)
        top_m = df.groupby("MUNICIPIO").size().sort_values(ascending=False).head(10).reset_index()
        top_m.columns = ["Município", "Empresas"]
        st.markdown(minify(bars_html(list(zip(top_m["Município"], top_m["Empresas"])))), unsafe_allow_html=True)

    with c2:
        municipios = sorted(df["MUNICIPIO"].dropna().unique().tolist())
        sel_mun = st.selectbox("Detalhar bairros de", municipios, key="select_bairro_mun")
        if sel_mun:
            top_b = (
                df[df["MUNICIPIO"] == sel_mun].groupby("BAIRRO").size()
                .sort_values(ascending=False).head(12).reset_index()
            )
            top_b.columns = ["Bairro", "Empresas"]
            st.markdown(
                minify(bars_html(list(zip(top_b["Bairro"], top_b["Empresas"])), accent="var(--green)")),
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="notice">Use a concentração por bairro para montar rotas de visita: '
        'filtre um município na barra lateral e ataque primeiro o bairro com mais leads qualificados.</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════
# 14. EXPORT
# ══════════════════════════════════════════════════════════════
def register_export(count):
    if st.session_state.get("user"):
        st.session_state.user["exports_used"] = st.session_state.user.get("exports_used", 0) + count
        st.toast(f"Export registrado · {count} leads")


def show_export(df, user):
    tier = user.get("tier", "explorador")
    exp_used = user.get("exports_used", 0)
    exp_limit = TIER_CFG[tier]["limit"]
    total = len(df)

    st.markdown("<hr>", unsafe_allow_html=True)

    if tier == "explorador":
        st.markdown(
            '<div class="notice notice-lock"><b>Export bloqueado no plano Explorador.</b><br>'
            'Faça upgrade para o plano Operacional para baixar sua lista em CSV ou Excel.</div>',
            unsafe_allow_html=True,
        )
        return

    if exp_limit < 999999 and exp_used >= exp_limit:
        st.markdown(
            f'<div class="notice notice-lock"><b>Limite mensal atingido.</b><br>'
            f'Você usou {exp_used} de {exp_limit} exports do plano {TIER_CFG[tier]["label"]}.</div>',
            unsafe_allow_html=True,
        )
        return

    restante = "ilimitado" if exp_limit >= 999999 else f"{exp_limit - exp_used} restantes"
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        st.markdown(
            f'<div class="kpi-sub" style="padding-top:8px">Plano {TIER_CFG[tier]["label"]} · '
            f'{exp_used} exports usados · {restante} · exportando {total} leads do filtro atual</div>',
            unsafe_allow_html=True,
        )

    export_df = df.drop(columns=["ANOS_ATIVIDADE"], errors="ignore")
    with c2:
        st.download_button(
            "Baixar CSV", export_df.to_csv(index=False, sep=";").encode("utf-8-sig"),
            f"achei_leads_{date.today()}.csv", "text/csv",
            width="stretch", key="btn_dl_csv", on_click=register_export, args=(total,),
            disabled=total == 0,
        )
    with c3:
        buf = BytesIO()
        export_df.to_excel(buf, index=False)
        buf.seek(0)
        st.download_button(
            "Baixar Excel", buf.read(), f"achei_leads_{date.today()}.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch", key="btn_dl_xlsx", on_click=register_export, args=(total,),
            disabled=total == 0,
        )


# ══════════════════════════════════════════════════════════════
# 15. MAIN
# ══════════════════════════════════════════════════════════════
def main():
    init_state()

    df_full = get_data()
    filters = show_sidebar(df_full)
    show_topbar(df_full)

    filters = read_filters()
    df = apply_filters(df_full, filters)

    show_kpis(df, st.session_state.user)

    with st.expander("Visão geral dos dados", expanded=False):
        show_charts(df)

    # Chips de filtros ativos (clicar remove)
    chips = active_filter_chips(filters)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    if chips:
        st.markdown('<div class="sec-label">Filtros ativos · clique para remover</div>', unsafe_allow_html=True)
        chip_cols = st.columns(min(6, len(chips)))
        for i, (label, name, value) in enumerate(chips):
            with chip_cols[i % len(chip_cols)]:
                if st.button(f"✕  {label}", key=f"chip_{i}_{name}", width="stretch"):
                    remove_filter(name, value)
                    st.rerun()

    tab_cards, tab_list, tab_geo = st.tabs(["Cards", "Lista", "Por bairro"])
    with tab_cards:
        show_cards(df)
    with tab_list:
        show_list(df)
    with tab_geo:
        show_bairro(df)

    show_export(df, st.session_state.user)


main()
