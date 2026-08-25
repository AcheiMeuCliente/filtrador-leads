"""
AcheiMeuCliente — Plataforma de Inteligência de Mercado para Beleza
app.py — Frontend de validação com dados mock (Fase 1)
Para produção: substituir get_data() por consulta DuckDB
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from io import BytesIO
from html import escape
import re

# ══════════════════════════════════════════════════════
# 1. CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="AcheiMeuCliente",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════
# 2. CSS GLOBAL
# ══════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Reset e base ── */
.lead-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 12px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.card-top { padding: 12px 12px 0 12px; }

/* ── CNAE badges ── */
.cnae-badge {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 11px; font-weight: 600;
    padding: 4px 10px; border-radius: 20px; margin-bottom: 8px;
}
.cnae-primary    { background: #1D9E75; color: #ffffff; }
.cnae-outside    { background: #FCEBEB; border: 1px solid #F09595; color: #791F1F; }
.cnae-secondary  { background: #FAEEDA; border: 1px solid #EF9F27; color: #633806; }

/* ── Identidade ── */
.card-identity { display: flex; gap: 10px; align-items: flex-start; margin-bottom: 8px; }
.card-avatar {
    width: 38px; height: 38px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 600; flex-shrink: 0;
}
.av-salao   { background: #E1F5EE; color: #085041; }
.av-clinica { background: #FBEAF0; color: #4B1528; }
.av-dist    { background: #E6F1FB; color: #042C53; }
.av-loja    { background: #FAEEDA; color: #412402; }
.av-fabrica { background: #EEEDFE; color: #26215C; }
.av-rep     { background: #FAECE7; color: #4A1B0C; }

.name-block { flex: 1; min-width: 0; }
.company-main { font-size: 14px; font-weight: 600; color: #111827; line-height: 1.3; }
.company-sub  { font-size: 11px; color: #6b7280; margin-top: 1px; }

/* ── Segment pills ── */
.seg-pill {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 11px; font-weight: 500; padding: 3px 9px;
    border-radius: 20px; border: 1px solid; margin-top: 4px;
}
.seg-salao   { background:#E1F5EE; color:#085041; border-color:#5DCAA5; }
.seg-clinica { background:#FBEAF0; color:#4B1528; border-color:#ED93B1; }
.seg-dist    { background:#E6F1FB; color:#042C53; border-color:#85B7EB; }
.seg-loja    { background:#FAEEDA; color:#412402; border-color:#EF9F27; }
.seg-fabrica { background:#EEEDFE; color:#26215C; border-color:#AFA9EC; }
.seg-rep     { background:#FAECE7; color:#4A1B0C; border-color:#F0997B; }

/* ── Localização ── */
.card-location {
    font-size: 12px; color: #6b7280;
    display: flex; align-items: center; gap: 5px;
    padding: 0 12px; margin-bottom: 6px;
}

/* ── CNAE strip ── */
.cnae-strip {
    margin: 0 12px 8px 12px;
    padding: 9px 12px; border-radius: 8px; border: 1px solid;
}
.cnae-strip-primary  { background:#E1F5EE; border-color:#5DCAA5; }
.cnae-strip-outside  { background:#FFF7ED; border-color:#EF9F27; }
.cnae-strip-unknown  { background:#F9FAFB; border-color:#e5e7eb; }
.cnae-strip-title    { font-size: 11px; font-weight: 600; margin-bottom: 3px; }
.cnae-strip-code     { font-size: 11px; color: #374151; line-height: 1.5; }
.cnae-strip-warn     { font-size: 11px; color: #92400e; margin-top: 3px; }
.cnae-strip-link     { font-size: 11px; color: #1D9E75; cursor: pointer; margin-top: 4px; display: block; }

/* ── Seção de contatos ── */
.contact-section {
    border-top: 1px solid #f3f4f6;
    border-bottom: 1px solid #f3f4f6;
    background: #f9fafb; padding: 8px 12px;
}
.contact-label { font-size: 10px; font-weight: 600; letter-spacing: .05em; color: #9ca3af; margin-bottom: 4px; }
.contact-row {
    display: flex; align-items: center; gap: 8px;
    padding: 4px 0; border-bottom: 1px solid #f3f4f6; font-size: 12px;
}
.contact-row:last-child { border-bottom: none; }
.contact-type  { font-size: 10px; font-weight: 600; color: #9ca3af; width: 30px; flex-shrink: 0; }
.contact-num   { font-family: 'SF Mono', Consolas, monospace; font-size: 12px; color: #111827; flex: 1; }
.contact-icons { display: flex; gap: 5px; }
.c-icon {
    width: 28px; height: 28px; border-radius: 6px; border: 1px solid #e5e7eb;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 14px; text-decoration: none; color: #6b7280;
    background: white;
}
.c-icon-wa  { border-color: #22c55e; color: #16a34a; background: #f0fdf4; }
.c-icon-tel { border-color: #93c5fd; color: #1d4ed8; background: #eff6ff; }

/* ── Botões de ação ── */
.action-buttons { display: flex; gap: 6px; padding: 10px 12px; }
.act-btn {
    flex: 1; padding: 7px 0; border-radius: 7px; border: 1px solid #d1d5db;
    font-size: 11px; font-weight: 500; text-align: center;
    text-decoration: none; display: flex; align-items: center;
    justify-content: center; gap: 5px; background: white;
    color: #374151; cursor: pointer;
}
.btn-rf    { border-color: #93c5fd; color: #1d4ed8; background: #eff6ff; }
.btn-maps  { border-color: #fca5a5; color: #dc2626; background: #fef2f2; }
.btn-site  { border-color: #d1d5db; color: #6b7280; }
.btn-wa-main { border-color: #22c55e; color: #16a34a; background: #f0fdf4; font-weight: 600; }

/* ── Expand (details/summary) ── */
details.card-expand { border-top: 1px solid #f3f4f6; }
details.card-expand summary {
    padding: 8px 12px; font-size: 12px; color: #1D9E75;
    cursor: pointer; list-style: none; display: flex;
    align-items: center; gap: 5px;
}
details.card-expand summary::-webkit-details-marker { display: none; }
details.card-expand summary::before { content: "▶"; font-size: 9px; transition: transform .15s; }
details.card-expand[open] summary::before { content: "▼"; }
.expand-body { padding: 10px 12px 12px; border-top: 1px solid #f3f4f6; background: #f9fafb; }

/* ── Seções dentro do expand ── */
.exp-section { margin-bottom: 10px; }
.exp-section-title {
    font-size: 10px; font-weight: 600; letter-spacing: .05em;
    color: #9ca3af; margin-bottom: 5px; text-transform: uppercase;
}
.address-box {
    background: white; border: 1px solid #e5e7eb; border-radius: 7px;
    padding: 8px 10px; font-size: 12px; color: #374151; line-height: 1.7;
}
.address-actions { display: flex; gap: 6px; margin-top: 6px; }
.addr-btn {
    padding: 4px 10px; border-radius: 6px; border: 1px solid #d1d5db;
    font-size: 11px; text-decoration: none; color: #374151;
    display: inline-flex; align-items: center; gap: 4px; background: white;
}
.addr-btn-maps { border-color: #fca5a5; color: #dc2626; }
.cnae-list { background: white; border: 1px solid #e5e7eb; border-radius: 7px; padding: 7px 10px; }
.cnae-item { display: flex; gap: 7px; align-items: center; font-size: 11px; color: #374151; padding: 3px 0; }
.cnae-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.data-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px 14px; }
.data-item { font-size: 11px; }
.data-label { color: #9ca3af; display: block; margin-bottom: 1px; }
.data-value { color: #374151; font-weight: 500; }

/* ── Badges de status ── */
.badge-nova { background: #dcfce7; color: #166534; font-size: 10px;
    font-weight: 600; padding: 2px 7px; border-radius: 10px; margin-left: 5px; }
.badge-mei  { background: #EEEDFE; color: #26215C; font-size: 10px;
    font-weight: 600; padding: 2px 7px; border-radius: 10px; }

/* ── Tabela lista ── */
.list-tbl { width: 100%; border-collapse: collapse; }
.list-tbl th {
    font-size: 11px; font-weight: 600; color: #6b7280; text-align: left;
    padding: 8px 10px; border-bottom: 1px solid #e5e7eb;
    background: #f9fafb; white-space: nowrap;
}
.list-tbl td { font-size: 12px; padding: 8px 10px; border-bottom: 1px solid #f3f4f6; }
.list-tbl tr:hover td { background: #f9fafb; }

/* ── KPI card ── */
.kpi-box {
    background: white; border: 1px solid #e5e7eb; border-radius: 10px;
    padding: 14px; font-family: -apple-system, sans-serif;
}
.kpi-label { font-size: 12px; color: #6b7280; margin-bottom: 4px; }
.kpi-value { font-size: 24px; font-weight: 600; color: #111827; }
.kpi-sub   { font-size: 11px; color: #9ca3af; margin-top: 2px; }
.kpi-green { color: #16a34a !important; }
.kpi-blue  { color: #1d4ed8 !important; }
.kpi-purple{ color: #7c3aed !important; }
.kpi-red   { color: #dc2626 !important; }

/* ── Barra de exportação ── */
.export-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0; border-top: 1px solid #e5e7eb; margin-top: 12px;
    font-size: 12px; color: #6b7280;
}

/* ── Seção de charts ── */
.chart-card {
    background: white; border: 1px solid #e5e7eb; border-radius: 10px;
    padding: 14px; margin-bottom: 12px;
}
.chart-title { font-size: 11px; font-weight: 600; color: #6b7280;
    letter-spacing: .04em; margin-bottom: 10px; }

/* ── Mobile bottom sheet hint ── */
@media (max-width: 768px) {
    .lead-card { margin-bottom: 10px; }
    .cards-grid { grid-template-columns: 1fr !important; }
    .action-buttons { flex-wrap: wrap; }
    .act-btn { min-width: 80px; }
}

/* ── Misc ── */
.section-title-bar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 10px;
}
.result-count { font-size: 14px; font-weight: 600; color: #111827; }
.result-sub   { font-size: 11px; color: #6b7280; }

/* ── Layout principal dos cards conforme mockup ── */
.lead-card { margin-bottom: 10px; }
.card-top { padding: 14px 14px 10px; }
.card-identity { margin-bottom: 10px; }
.company-main { font-size: 13px; font-weight: 500; }
.company-sub { font-size: 11px; }
.seg-pill { font-size: 10px; padding: 2px 8px; border-radius: 10px; }
.card-location { padding: 0; margin-bottom: 8px; font-size: 12px; }
.card-info { display: flex; flex-direction: column; gap: 5px; font-size: 12px; color: #6b7280; }
.info-row { display: flex; align-items: flex-start; gap: 6px; }
.cnae-strip { margin: 0; padding: 8px 10px; }
.cnae-badge { font-size: 10px; padding: 2px 8px; border-radius: 10px; margin-bottom: 4px; }
.cnae-strip-title, .cnae-strip-warn { font-size: 11px; }
.cnae-strip-code { font-size: 11px; }
.contact-section { border-top: 1px solid #e5e7eb; border-bottom: 0; padding: 10px 14px 6px; text-align: center; }
.contact-note { font-size: 10px; color: #9ca3af; line-height: 1.4; }
.action-buttons { padding: 10px 14px; border-top: 1px solid #e5e7eb; }
.act-btn { min-height: 52px; padding: 7px 4px; border-radius: 7px; font-size: 14px; font-weight: 500; }
.btn-wa-main { border-color: #d1d5db; color: #111827; background: #fff; }
.btn-wa-main:hover { background: #f9fafb; }
.btn-mail { border-color: #d1d5db; color: #111827; background: #fff; }
.btn-maps { border-color: #d1d5db; color: #111827; background: #fff; }

/* ── Lista compacta conforme mockup ── */
.list-table-wrap { width: 100%; overflow: auto; max-height: 68vh; border: 1px solid #d1d5db; }
.list-table { width: max-content; min-width: 100%; border-collapse: separate; border-spacing: 0; background: #fff; }
.list-table th {
    background: #f3f4f6; color: #111827; font-size: 10px; font-weight: 600;
    text-align: left; padding: 7px 9px; border-right: 1px solid #d1d5db;
    border-bottom: 1px solid #d1d5db; white-space: nowrap; text-transform: uppercase;
    position: sticky; top: 0; z-index: 2;
}
.list-table td {
    color: #374151; font-size: 10px; padding: 6px 9px;
    border-right: 1px solid #d1d5db; border-bottom: 1px solid #d1d5db;
    white-space: nowrap; vertical-align: middle; max-width: 280px; overflow: hidden; text-overflow: ellipsis;
}
.list-table tbody tr:hover td { background: #f9fafb; }
.list-table .list-group th { background: #e5e7eb; text-align: center; color: #4b5563; }
.list-table th:first-child, .list-table td:first-child { position: sticky; left: 0; z-index: 1; background: #fff; }
.list-table th:first-child { z-index: 3; background: #f3f4f6; }
.list-table tbody tr:hover td:first-child { background: #f9fafb; }
.list-segment { display: inline-flex; align-items: center; gap: 4px; }
.list-contact-empty { color: #6b7280; }
.list-map-link { color: #111827; text-decoration: none; }
.list-map-link:hover { text-decoration: underline; }
.list-link { color: #2563eb; text-decoration: none; }
.list-link:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# 3. CONSTANTES
# ══════════════════════════════════════════════════════
BEAUTY_CNAES = {
    "9602501": "Salões e Barbearias",
    "9602502": "Clínicas de Estética",
    "4646001": "Distribuidores Atacadistas",
    "4772500": "Lojas e Pontos de Venda",
    "4635401": "Representantes e Agentes",
    "2063100": "Fábricas e Marcas",
}

SEG_CFG = {
    "Salões e Barbearias":      {"e":"💇","av":"av-salao",  "pill":"seg-salao"},
    "Clínicas de Estética":     {"e":"✨","av":"av-clinica","pill":"seg-clinica"},
    "Distribuidores Atacadistas":{"e":"🚛","av":"av-dist",  "pill":"seg-dist"},
    "Lojas e Pontos de Venda":  {"e":"🏪","av":"av-loja",  "pill":"seg-loja"},
    "Fábricas e Marcas":        {"e":"🏭","av":"av-fabrica","pill":"seg-fabrica"},
    "Representantes e Agentes": {"e":"🤝","av":"av-rep",   "pill":"seg-rep"},
}

TIER_CFG = {
    "explorador": {"label":"Explorador","limit":0,     "states":1},
    "operacional":{"label":"Operacional","limit":300,   "states":1},
    "regional":   {"label":"Regional",  "limit":1000,  "states":5},
    "nacional":   {"label":"Nacional",  "limit":999999,"states":27},
}

MOCK_USERS = {
    "demo@achei.com": {"nome":"Rafael","senha":"demo123","tier":"operacional","exports_used":253},
    "pro@achei.com":  {"nome":"Amanda","senha":"pro123", "tier":"regional",  "exports_used":45},
    "admin@achei.com":{"nome":"Admin", "senha":"admin123","tier":"nacional", "exports_used":0},
}


# ══════════════════════════════════════════════════════
# 4. DADOS MOCK  (substitui por get_data() com DuckDB)
# ══════════════════════════════════════════════════════
@st.cache_data
def get_data() -> pd.DataFrame:
    today = date.today()
    this_month = date(today.year, today.month, 1)

    rows = [
        # ── SP · Beleza principal ──────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="12.345.678/0001-90",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos",
             **{"RAZÃO SOCIAL":"Studio Bella Arte Cabeleireiros Ltda","NOME FANTASIA":"Studio Bella Arte"},
             TELEFONE_1="(11) 3456-7890", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 98765-4321", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"contato@studiobella.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Pinheiros", CEP="05422-001", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA":"Rua dos Pinheiros, 812, Sala 05 - Pinheiros, São Paulo/SP, 05422-001",
                "MAPS":"https://maps.google.com/?q=Studio+Bella+Arte+Pinheiros+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"15000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2019-03-15",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=12345678000190",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.studiobella.com.br"},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="22.333.444/0001-55",
             CNAE_PRINCIPAL_CODIGO="4646001", CNAE_PRINCIPAL_NOME="Comércio atacadista de cosméticos, higiene pessoal e perfumaria",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Distribuidora Cosméticos SP Ltda","NOME FANTASIA":"Beauty Supply SP"},
             TELEFONE_1="(11) 4567-8901", TELEFONE_2="(11) 4567-8902", TELEFONE_3="",
             WHATSAPP_1="(11) 99876-5432", WHATSAPP_2="(11) 98765-1234", WHATSAPP_3="",
             **{"E-MAIL":"vendas@beautysupplysp.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Vila Olímpia", CEP="04547-130", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA":"Rua Funchal, 411, 3º Andar - Vila Olímpia, São Paulo/SP, 04547-130",
                "MAPS":"https://maps.google.com/?q=Distribuidora+Cosmeticos+Vila+Olimpia+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"EPP", "CAPITAL SOCIAL":"280000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2015-06-20",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=22333444000155",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.beautysupplysp.com.br"},
             SEGMENTO="Distribuidores Atacadistas"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="33.444.555/0001-66",
             CNAE_PRINCIPAL_CODIGO="9602502", CNAE_PRINCIPAL_NOME="Atividades de estética e outros serviços de cuidados com a beleza",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Clínica Estética Premium Ltda","NOME FANTASIA":"Premium Estética"},
             TELEFONE_1="(11) 3210-9876", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 97654-3210", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"agenda@premiumestetica.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Jardins", CEP="01402-000", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA":"Al. Santos, 700, Cj. 32 - Jardins, São Paulo/SP, 01402-000",
                "MAPS":"https://maps.google.com/?q=Premium+Estetica+Jardins+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"50000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2017-09-10",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=33444555000166",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.premiumestetica.com.br"},
             SEGMENTO="Clínicas de Estética"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="44.555.666/0001-77",
             CNAE_PRINCIPAL_CODIGO="4772500", CNAE_PRINCIPAL_NOME="Comércio varejista de cosméticos, produtos de perfumaria e de higiene pessoal",
             CNAE_SECUNDARIO_CODIGO="4646001", CNAE_SECUNDARIO_NOME="Comércio atacadista de cosméticos",
             **{"RAZÃO SOCIAL":"Loja BellaMais Cosméticos ME","NOME FANTASIA":"BellaMais"},
             TELEFONE_1="(11) 2345-6789", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 96543-2109", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"loja@bellamais.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Santana", CEP="02401-000", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA":"Av. Braz Leme, 1000, Loja 5 - Santana, São Paulo/SP, 02401-000",
                "MAPS":"https://maps.google.com/?q=BellaMais+Santana+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"30000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2020-11-05",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=44555666000177",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Lojas e Pontos de Venda"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="55.666.777/0001-88",
             CNAE_PRINCIPAL_CODIGO="2063100", CNAE_PRINCIPAL_NOME="Fabricação de cosméticos, produtos de perfumaria e de higiene pessoal",
             CNAE_SECUNDARIO_CODIGO="4646001", CNAE_SECUNDARIO_NOME="Comércio atacadista de cosméticos",
             **{"RAZÃO SOCIAL":"Fábrica Cosméticos Natura Max SA","NOME FANTASIA":"Natura Max"},
             TELEFONE_1="(11) 4000-5000", TELEFONE_2="(11) 4000-5001", TELEFONE_3="",
             WHATSAPP_1="(11) 94000-5000", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"comercial@naturamax.ind.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Centro", CEP="09210-300", MUNICIPIO="Santo André", ESTADO="SP",
             **{"ENDERECO MAPA":"Rua Industrial, 2500, Galpão A - Centro, Santo André/SP, 09210-300",
                "MAPS":"https://maps.google.com/?q=Natura+Max+Santo+Andre+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"Grande", "CAPITAL SOCIAL":"5000000"},
             MEI=False, SIMPLES=False,
             **{"INICIO ATIVIDADE":"2005-04-20",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=55666777000188",
                "NATUREZA_JURIDICA":"Sociedade Anônima", "SITE":"www.naturamax.ind.br"},
             SEGMENTO="Fábricas e Marcas"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="66.777.888/0001-99",
             CNAE_PRINCIPAL_CODIGO="4635401", CNAE_PRINCIPAL_NOME="Representantes comerciais e agentes do comércio de cosméticos",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Carlos Augusto Silva ME","NOME FANTASIA":""},
             TELEFONE_1="", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 99999-0001", WHATSAPP_2="(11) 99999-0002", WHATSAPP_3="",
             **{"E-MAIL":"carlossilva.rep@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Centro", CEP="01310-100", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA":"Av. Paulista, 1500, Sala 12 - Bela Vista, São Paulo/SP, 01310-100",
                "MAPS":"https://maps.google.com/?q=Av+Paulista+1500+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2021-08-12",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=66777888000199",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Representantes e Agentes"),

        # ── SP · CNAE fora da beleza (beleza no secundário) ───────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="secundario",
             CNPJ="77.888.999/0001-11",
             CNAE_PRINCIPAL_CODIGO="4729601", CNAE_PRINCIPAL_NOME="Comércio varejista de alimentos em geral",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos, higiene pessoal",
             **{"RAZÃO SOCIAL":"Mercado Rosa ME","NOME FANTASIA":"Mercadinho Rosa"},
             TELEFONE_1="(11) 2233-4455", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 92233-4455", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"mercadorosa@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Mooca", CEP="03103-000", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA":"Rua da Mooca, 450 - Mooca, São Paulo/SP, 03103-000",
                "MAPS":"https://maps.google.com/?q=Mercadinho+Rosa+Mooca+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2018-02-01",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=77888999000111",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Lojas e Pontos de Venda"),

        # ── SP · Aberta este mês (nova) ───────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="88.999.000/0001-22",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Hair Beauty Salon Ltda","NOME FANTASIA":"Hair Beauty"},
             TELEFONE_1="(11) 3344-5566", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 93344-5566", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":""},
             TEM_EMAIL=False, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Brooklin", CEP="04571-010", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA":"Av. Dr. Chucri Zaidan, 333, Loja 2 - Brooklin, São Paulo/SP, 04571-010",
                "MAPS":"https://maps.google.com/?q=Hair+Beauty+Brooklin+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE": str(this_month),
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=88999000000122",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Salões e Barbearias"),

        # ── SP · E-mail de contador ───────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="99.000.111/0001-33",
             CNAE_PRINCIPAL_CODIGO="4646001", CNAE_PRINCIPAL_NOME="Comércio atacadista de cosméticos",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Top Cosméticos Atacado ME","NOME FANTASIA":"Top Cosméticos"},
             TELEFONE_1="(11) 3210-0000", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(11) 98800-0000", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"contador@escritorioabc.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=True,
             BAIRRO="Brás", CEP="03017-000", MUNICIPIO="São Paulo", ESTADO="SP",
             **{"ENDERECO MAPA":"Rua Oriente, 1200 - Brás, São Paulo/SP, 03017-000",
                "MAPS":"https://maps.google.com/?q=Top+Cosmeticos+Bras+SP"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"40000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2016-05-14",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=99000111000133",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Distribuidores Atacadistas"),

        # ── MG ────────────────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="11.222.333/0001-44",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Salão Arte e Estilo Ltda","NOME FANTASIA":"Arte & Estilo"},
             TELEFONE_1="(31) 3456-7890", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(31) 98888-7777", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"arteestilo@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Centro", CEP="30120-000", MUNICIPIO="Belo Horizonte", ESTADO="MG",
             **{"ENDERECO MAPA":"Av. Afonso Pena, 800, Sala 3 - Centro, Belo Horizonte/MG, 30120-000",
                "MAPS":"https://maps.google.com/?q=Arte+Estilo+BH+MG"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"20000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2018-04-10",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=11222333000144",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":""},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="22.333.444/0001-00",
             CNAE_PRINCIPAL_CODIGO="9602502", CNAE_PRINCIPAL_NOME="Atividades de estética e outros serviços de cuidados com a beleza",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Clínica Estética Luz e Beleza ME","NOME FANTASIA":"Luz Estética"},
             TELEFONE_1="(31) 3222-5555", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(31) 97777-5555", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"luz@estetica.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Savassi", CEP="30140-000", MUNICIPIO="Belo Horizonte", ESTADO="MG",
             **{"ENDERECO MAPA":"Rua Pernambuco, 400, Sala 12 - Savassi, BH/MG, 30140-000",
                "MAPS":"https://maps.google.com/?q=Luz+Estetica+Savassi+BH"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"15000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2012-05-20",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=22333444000100",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":"www.luzestetica.com.br"},
             SEGMENTO="Clínicas de Estética"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="33.444.555/0001-11",
             CNAE_PRINCIPAL_CODIGO="4646001", CNAE_PRINCIPAL_NOME="Comércio atacadista de cosméticos",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos",
             **{"RAZÃO SOCIAL":"Costa Distribuidora de Cosméticos Ltda","NOME FANTASIA":"Costa Distribuidora"},
             TELEFONE_1="(31) 4000-8888", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(31) 98000-8888", WHATSAPP_2="(31) 97000-7777", WHATSAPP_3="",
             **{"E-MAIL":"vendas@costadist.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Cidade Industrial", CEP="32040-000", MUNICIPIO="Contagem", ESTADO="MG",
             **{"ENDERECO MAPA":"Av. Industrial, 1500, Galpão B - C. Industrial, Contagem/MG, 32040-000",
                "MAPS":"https://maps.google.com/?q=Costa+Distribuidora+Contagem+MG"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"EPP", "CAPITAL SOCIAL":"150000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2016-07-15",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=33444555000111",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.costadist.com.br"},
             SEGMENTO="Distribuidores Atacadistas"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="44.555.666/0001-22",
             CNAE_PRINCIPAL_CODIGO="4772500", CNAE_PRINCIPAL_NOME="Comércio varejista de cosméticos",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Loja Make Perfeita ME","NOME FANTASIA":"Make Perfeita"},
             TELEFONE_1="(31) 3111-2222", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(31) 91111-2222", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":""},
             TEM_EMAIL=False, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Santa Efigênia", CEP="30240-000", MUNICIPIO="Belo Horizonte", ESTADO="MG",
             **{"ENDERECO MAPA":"Rua dos Tupis, 200, Loja 4 - Santa Efigênia, BH/MG, 30240-000",
                "MAPS":"https://maps.google.com/?q=Make+Perfeita+BH+MG"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2022-11-30",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=44555666000122",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Lojas e Pontos de Venda"),

        # ── MG · CNAE fora da beleza ──────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="secundario",
             CNPJ="55.666.777/0001-33",
             CNAE_PRINCIPAL_CODIGO="4711302", CNAE_PRINCIPAL_NOME="Comércio varejista de mercadorias em geral com predominância alimentar",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos",
             **{"RAZÃO SOCIAL":"Supermercado Bela Ltda","NOME FANTASIA":"Supermercado Bela"},
             TELEFONE_1="(31) 3456-0000", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(31) 96000-0000", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"contato@superbela.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Lourdes", CEP="30180-000", MUNICIPIO="Belo Horizonte", ESTADO="MG",
             **{"ENDERECO MAPA":"Rua Maranhão, 600 - Lourdes, BH/MG, 30180-000",
                "MAPS":"https://maps.google.com/?q=Supermercado+Bela+BH"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"80000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2011-03-25",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=55666777000133",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":""},
             SEGMENTO="Lojas e Pontos de Venda"),

        # ── RJ ────────────────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="66.777.888/0001-00",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="9602502", CNAE_SECUNDARIO_NOME="Atividades de estética",
             **{"RAZÃO SOCIAL":"Salão Rio Hair Design Ltda","NOME FANTASIA":"Rio Hair Design"},
             TELEFONE_1="(21) 3000-4444", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(21) 99000-4444", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"riohaird@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Ipanema", CEP="22420-040", MUNICIPIO="Rio de Janeiro", ESTADO="RJ",
             **{"ENDERECO MAPA":"Rua Garcia D'Ávila, 100 - Ipanema, Rio de Janeiro/RJ, 22420-040",
                "MAPS":"https://maps.google.com/?q=Rio+Hair+Design+Ipanema+RJ"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"25000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2014-01-15",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=66777888000100",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.riohairdesign.com.br"},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="77.888.999/0001-00",
             CNAE_PRINCIPAL_CODIGO="9602502", CNAE_PRINCIPAL_NOME="Atividades de estética e outros serviços de cuidados com a beleza",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Clínica Estética Carioca ME","NOME FANTASIA":"Carioca Estética"},
             TELEFONE_1="(21) 3111-5555", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(21) 97777-5555", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"cariocaestetica@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Barra da Tijuca", CEP="22640-000", MUNICIPIO="Rio de Janeiro", ESTADO="RJ",
             **{"ENDERECO MAPA":"Av. das Américas, 500, Bloco 20 - Barra da Tijuca, RJ, 22640-000",
                "MAPS":"https://maps.google.com/?q=Carioca+Estetica+Barra+RJ"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2020-08-01",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=77888999000100",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Clínicas de Estética"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="88.000.111/0001-55",
             CNAE_PRINCIPAL_CODIGO="4646001", CNAE_PRINCIPAL_NOME="Comércio atacadista de cosméticos",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"RJ Distribuidora de Cosméticos Ltda","NOME FANTASIA":"RJ Beauty Dist."},
             TELEFONE_1="(21) 2500-3000", TELEFONE_2="(21) 2500-3001", TELEFONE_3="",
             WHATSAPP_1="(21) 98500-3000", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"pedidos@rjbeautydist.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Centro", CEP="20040-020", MUNICIPIO="Rio de Janeiro", ESTADO="RJ",
             **{"ENDERECO MAPA":"Av. Rio Branco, 123 - Centro, Rio de Janeiro/RJ, 20040-020",
                "MAPS":"https://maps.google.com/?q=RJ+Beauty+Dist+Centro+RJ"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"EPP", "CAPITAL SOCIAL":"200000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2010-09-01",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=88000111000155",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.rjbeautydist.com.br"},
             SEGMENTO="Distribuidores Atacadistas"),

        # ── PR ────────────────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="99.111.222/0001-66",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Salão Curitibano de Beleza ME","NOME FANTASIA":"Salão Curitibano"},
             TELEFONE_1="(41) 3234-5678", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(41) 99234-5678", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"salaocuritibano@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Batel", CEP="80420-090", MUNICIPIO="Curitiba", ESTADO="PR",
             **{"ENDERECO MAPA":"Rua Sete de Setembro, 540 - Batel, Curitiba/PR, 80420-090",
                "MAPS":"https://maps.google.com/?q=Salao+Curitibano+Batel+PR"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2023-01-10",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=99111222000166",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="11.333.555/0001-77",
             CNAE_PRINCIPAL_CODIGO="4646001", CNAE_PRINCIPAL_NOME="Comércio atacadista de cosméticos",
             CNAE_SECUNDARIO_CODIGO="4635401", CNAE_SECUNDARIO_NOME="Representantes comerciais de cosméticos",
             **{"RAZÃO SOCIAL":"Distribuidora Paraná Beauty Ltda","NOME FANTASIA":"PR Beauty"},
             TELEFONE_1="(44) 3030-1010", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(44) 99030-1010", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"prbeauty@prbeauty.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Zona 01", CEP="87013-000", MUNICIPIO="Maringá", ESTADO="PR",
             **{"ENDERECO MAPA":"Av. Brasil, 5600 - Zona 01, Maringá/PR, 87013-000",
                "MAPS":"https://maps.google.com/?q=PR+Beauty+Maringa"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"60000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2019-06-15",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=11333555000177",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.prbeauty.com.br"},
             SEGMENTO="Distribuidores Atacadistas"),

        # ── RS ────────────────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="22.444.666/0001-88",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Salão Gaúcho de Beleza ME","NOME FANTASIA":"Salão Gaúcho"},
             TELEFONE_1="(51) 3030-4040", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(51) 99030-4040", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"salaogaucho@email.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Moinhos de Vento", CEP="90570-010", MUNICIPIO="Porto Alegre", ESTADO="RS",
             **{"ENDERECO MAPA":"Rua Padre Chagas, 200 - Moinhos de Vento, Porto Alegre/RS, 90570-010",
                "MAPS":"https://maps.google.com/?q=Salao+Gaucho+Moinhos+POA"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2021-03-22",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=22444666000188",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Salões e Barbearias"),

        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="33.555.777/0001-99",
             CNAE_PRINCIPAL_CODIGO="4646001", CNAE_PRINCIPAL_NOME="Comércio atacadista de cosméticos",
             CNAE_SECUNDARIO_CODIGO="4772500", CNAE_SECUNDARIO_NOME="Comércio varejista de cosméticos",
             **{"RAZÃO SOCIAL":"RS Cosméticos Atacado Ltda","NOME FANTASIA":"RS Cosméticos"},
             TELEFONE_1="(54) 3500-6000", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(54) 99500-6000", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"rscosmetics@rscosmetics.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Desvio Rizzo", CEP="95084-000", MUNICIPIO="Caxias do Sul", ESTADO="RS",
             **{"ENDERECO MAPA":"Rua Ernesto Alves, 1100 - Caxias do Sul/RS, 95084-000",
                "MAPS":"https://maps.google.com/?q=RS+Cosmeticos+Caxias+do+Sul"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"EPP", "CAPITAL SOCIAL":"300000"},
             MEI=False, SIMPLES=False,
             **{"INICIO ATIVIDADE":"2008-11-01",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=33555777000199",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.rscosmetics.com.br"},
             SEGMENTO="Distribuidores Atacadistas"),

        # ── BA ────────────────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="44.666.888/0001-11",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="9602502", CNAE_SECUNDARIO_NOME="Atividades de estética",
             **{"RAZÃO SOCIAL":"Studio Bahia Hair Ltda","NOME FANTASIA":"Bahia Hair Studio"},
             TELEFONE_1="(71) 3300-4400", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(71) 99300-4400", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"bahiahair@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Barra", CEP="40140-130", MUNICIPIO="Salvador", ESTADO="BA",
             **{"ENDERECO MAPA":"Av. Oceânica, 2400, Sala 5 - Barra, Salvador/BA, 40140-130",
                "MAPS":"https://maps.google.com/?q=Bahia+Hair+Studio+Salvador"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"ME", "CAPITAL SOCIAL":"18000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2017-07-07",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=44666888000111",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":""},
             SEGMENTO="Salões e Barbearias"),

        # ── CE ────────────────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="55.777.999/0001-22",
             CNAE_PRINCIPAL_CODIGO="9602502", CNAE_PRINCIPAL_NOME="Atividades de estética",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Clínica Estética Fortaleza ME","NOME FANTASIA":"Fortaleza Estética"},
             TELEFONE_1="(85) 3355-6677", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(85) 98355-6677", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"fortalezaestetica@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Meireles", CEP="60160-190", MUNICIPIO="Fortaleza", ESTADO="CE",
             **{"ENDERECO MAPA":"Av. Beira Mar, 3300, Sala 8 - Meireles, Fortaleza/CE, 60160-190",
                "MAPS":"https://maps.google.com/?q=Fortaleza+Estetica+Meireles"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2022-04-01",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=55777999000122",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Clínicas de Estética"),

        # ── SC ────────────────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="66.888.000/0001-33",
             CNAE_PRINCIPAL_CODIGO="4646001", CNAE_PRINCIPAL_NOME="Comércio atacadista de cosméticos",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Santa Catarina Cosméticos Distribuidora Ltda","NOME FANTASIA":"SC Cosméticos"},
             TELEFONE_1="(48) 3200-5000", TELEFONE_2="(48) 3200-5001", TELEFONE_3="",
             WHATSAPP_1="(48) 98200-5000", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"vendas@sccosmeticos.com.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Trindade", CEP="88036-000", MUNICIPIO="Florianópolis", ESTADO="SC",
             **{"ENDERECO MAPA":"Rod. SC-401, 3600 - Trindade, Florianópolis/SC, 88036-000",
                "MAPS":"https://maps.google.com/?q=SC+Cosmeticos+Florianopolis"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"EPP", "CAPITAL SOCIAL":"400000"},
             MEI=False, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2013-09-10",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=66888000000133",
                "NATUREZA_JURIDICA":"Sociedade Empresária Limitada", "SITE":"www.sccosmeticos.com.br"},
             SEGMENTO="Distribuidores Atacadistas"),

        # ── GO ────────────────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="77.999.111/0001-44",
             CNAE_PRINCIPAL_CODIGO="9602501", CNAE_PRINCIPAL_NOME="Cabeleireiros, manicure e pedicure",
             CNAE_SECUNDARIO_CODIGO="", CNAE_SECUNDARIO_NOME="",
             **{"RAZÃO SOCIAL":"Salão Centro-Oeste Beleza ME","NOME FANTASIA":"Centro-Oeste Hair"},
             TELEFONE_1="(62) 3300-1100", TELEFONE_2="", TELEFONE_3="",
             WHATSAPP_1="(62) 99300-1100", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"centroestehair@gmail.com"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Setor Bueno", CEP="74210-010", MUNICIPIO="Goiânia", ESTADO="GO",
             **{"ENDERECO MAPA":"Av. 85, 1300, Sala 2 - Setor Bueno, Goiânia/GO, 74210-010",
                "MAPS":"https://maps.google.com/?q=Centro+Oeste+Hair+Goiania"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"MEI", "CAPITAL SOCIAL":"5000"},
             MEI=True, SIMPLES=True,
             **{"INICIO ATIVIDADE":"2023-06-01",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=77999111000144",
                "NATUREZA_JURIDICA":"Empresário Individual", "SITE":""},
             SEGMENTO="Salões e Barbearias"),

        # ── MG · Fábrica ──────────────────────────────────────────
        dict(CNAE_MATCHED=True, ORIGEM_CNAE="principal",
             CNPJ="88.111.333/0001-55",
             CNAE_PRINCIPAL_CODIGO="2063100", CNAE_PRINCIPAL_NOME="Fabricação de cosméticos, produtos de perfumaria e de higiene pessoal",
             CNAE_SECUNDARIO_CODIGO="4646001", CNAE_SECUNDARIO_NOME="Comércio atacadista de cosméticos",
             **{"RAZÃO SOCIAL":"Indústria Mineira de Cosméticos SA","NOME FANTASIA":"MineCosm"},
             TELEFONE_1="(31) 3600-7000", TELEFONE_2="(31) 3600-7001", TELEFONE_3="(31) 3600-7002",
             WHATSAPP_1="(31) 99600-7000", WHATSAPP_2="", WHATSAPP_3="",
             **{"E-MAIL":"comercial@minecosm.ind.br"},
             TEM_EMAIL=True, TEM_TELEFONE=True, EMAIL_CONTABILIDADE=False,
             BAIRRO="Betim Industrial", CEP="32540-000", MUNICIPIO="Betim", ESTADO="MG",
             **{"ENDERECO MAPA":"Rod. Fernão Dias, Km 467 - Betim/MG, 32540-000",
                "MAPS":"https://maps.google.com/?q=MineCosm+Betim+MG"},
             **{"MATRIZ FILIAL":"Matriz", "PORTE":"Grande", "CAPITAL SOCIAL":"10000000"},
             MEI=False, SIMPLES=False,
             **{"INICIO ATIVIDADE":"2001-03-20",
                "RECEITA FEDERAL":"https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/cnpjrevaesic.asp?cnpj=88111333000155",
                "NATUREZA_JURIDICA":"Sociedade Anônima", "SITE":"www.minecosm.ind.br"},
             SEGMENTO="Fábricas e Marcas"),
    ]

    df = pd.DataFrame(rows)
    df["INICIO ATIVIDADE"] = pd.to_datetime(df["INICIO ATIVIDADE"])
    df["CAPITAL SOCIAL"] = pd.to_numeric(df["CAPITAL SOCIAL"], errors="coerce").fillna(0)
    df["ANOS_ATIVIDADE"] = ((datetime.now() - df["INICIO ATIVIDADE"]).dt.days / 365).round(1)
    return df


# ══════════════════════════════════════════════════════
# 5. SESSION STATE
# ══════════════════════════════════════════════════════
def init_state():
    defaults = {
        "logged_in": True,
        "user_email": "admin@achei.com",
        "user": {},
        "view_mode": "cards",
        "saved_views": [
            {"name": "SP · Salões com WhatsApp",   "count": 4,
             "filters": {"estados": ["SP"], "segmentos": ["Salões e Barbearias"], "tem_whatsapp": True}},
            {"name": "MG · Distribuidores",         "count": 3,
             "filters": {"estados": ["MG"], "segmentos": ["Distribuidores Atacadistas"], "tem_whatsapp": False}},
            {"name": "Beleza principal — todas UF", "count": 22,
             "filters": {"origem_cnae": "Apenas CNAE principal", "tem_whatsapp": False}},
        ],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def minify(html: str) -> str:
    """Colapsa HTML multi-linha em linha única para o parser de Markdown."""
    return re.sub(r"\n[ \t]+", " ", html).strip()


# ══════════════════════════════════════════════════════
# 6. HELPER FUNCTIONS
# ══════════════════════════════════════════════════════
def get_display_name(row):
    nf = str(row.get("NOME FANTASIA", "")).strip()
    rs = str(row.get("RAZÃO SOCIAL", "")).strip()
    return (nf, rs) if nf else (rs, "")


def get_cnae_status(row):
    """Retorna ('primary'|'secondary'|'unknown', cnae_code, cnae_name)"""
    origem = str(row.get("ORIGEM_CNAE", "")).lower()
    cod_p  = str(row.get("CNAE_PRINCIPAL_CODIGO", "")).replace("-","").replace("/","").replace(".","")
    nom_p  = str(row.get("CNAE_PRINCIPAL_NOME", ""))
    cod_s  = str(row.get("CNAE_SECUNDARIO_CODIGO", "")).replace("-","").replace("/","").replace(".","")
    nom_s  = str(row.get("CNAE_SECUNDARIO_NOME", ""))
    is_beauty_principal = cod_p in BEAUTY_CNAES
    if origem == "principal" and is_beauty_principal:
        return "primary", cod_p, nom_p
    elif origem == "secundario" or not is_beauty_principal:
        return "secondary", cod_s, nom_s
    return "primary", cod_p, nom_p


def get_initials(name):
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return name[:2].upper()


def clean_phone(phone):
    return "".join(c for c in phone if c.isdigit())


def wa_link(phone):
    cp = clean_phone(phone)
    if len(cp) >= 10:
        return f"https://wa.me/55{cp}"
    return "#"


def is_new(dt, months=1):
    if pd.isna(dt):
        return False
    cutoff = datetime.now() - timedelta(days=30 * months)
    return dt >= cutoff


def format_capital(val):
    try:
        return f"R$ {float(val):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "—"


# ══════════════════════════════════════════════════════
# 7. LOGIN
# ══════════════════════════════════════════════════════
def show_login():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 🎯 AcheiMeuCliente")
        st.markdown("**Plataforma de Inteligência de Mercado para Beleza**")
        st.markdown("---")
        email = st.text_input("E-mail", placeholder="seu@email.com")
        senha = st.text_input("Senha", type="password", placeholder="••••••••")
        if st.button("Entrar", width="stretch", type="primary"):
            if email in MOCK_USERS and MOCK_USERS[email]["senha"] == senha:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user = MOCK_USERS[email].copy()
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("**Contas de teste:**")
        st.caption("demo@achei.com / demo123 → Plano Operacional")
        st.caption("pro@achei.com / pro123 → Plano Regional")
        st.caption("admin@achei.com / admin123 → Plano Nacional")


# ══════════════════════════════════════════════════════
# 8. SIDEBAR
# ══════════════════════════════════════════════════════
def show_sidebar(df):
    with st.sidebar:
        st.markdown(f"### 🎯 AcheiMeuCliente")
        tier = st.session_state.user.get("tier", "operacional")
        tier_label = TIER_CFG[tier]["label"]
        st.caption(f"👤 {st.session_state.user.get('nome','Usuário')} · Plano {tier_label}")
        if st.button("Sair", width="stretch"):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown("---")

        # ── Visualizações salvas ──
        st.markdown("#### 🔖 Visualizações salvas")
        for i, sv in enumerate(st.session_state.saved_views):
            col_n, col_b = st.columns([4, 1])
            with col_n:
                st.caption(f"**{sv['name']}** · {sv['count']} leads")
            with col_b:
                if st.button("▶", key=f"load_sv_{i}", help="Carregar"):
                    st.info(f"Visualização '{sv['name']}' carregada!")
        st.markdown("---")

        # ── FILTROS ──
        filters = {}

        st.markdown("#### 📋 Filtros")

        # Contato
        st.markdown("**Contato**")
        filters["tem_email"]       = st.checkbox("Com e-mail",          value=False)
        filters["sem_contador"]    = st.checkbox("Excluir e-mail contador", value=False)
        filters["tem_whatsapp"]    = st.checkbox("Com WhatsApp confirmado", value=False)

        # Segmento
        st.markdown("**Segmento**")
        segs = list(SEG_CFG.keys())
        filters["segmentos"] = st.multiselect("Segmento(s)", segs, placeholder="Todos")

        # Origem CNAE
        st.markdown("**Origem CNAE**")
        filters["origem_cnae"] = st.selectbox(
            "Origem do match",
            ["Principal ou Secundário", "Apenas CNAE principal", "Apenas CNAE secundário"],
            label_visibility="collapsed"
        )

        # Localização
        st.markdown("**Localização**")
        estados = sorted(df["ESTADO"].dropna().unique().tolist())
        filters["estados"] = st.multiselect("Estado(s)", estados, placeholder="Todos")

        municipios_opts = []
        if filters["estados"]:
            municipios_opts = sorted(df[df["ESTADO"].isin(filters["estados"])]["MUNICIPIO"].dropna().unique().tolist())
        else:
            municipios_opts = sorted(df["MUNICIPIO"].dropna().unique().tolist())
        filters["municipios"] = st.multiselect("Município(s)", municipios_opts, placeholder="Todos")

        bairros_opts = []
        if filters["municipios"]:
            bairros_opts = sorted(df[df["MUNICIPIO"].isin(filters["municipios"])]["BAIRRO"].dropna().unique().tolist())
        filters["bairros"] = st.multiselect("Bairro(s)", bairros_opts, placeholder="Todos")

        # Identificação
        st.markdown("**Identificação**")
        filters["busca_texto"] = st.text_input("Nome / Razão Social / CNPJ", placeholder="Buscar...")

        # Características
        st.markdown("**Características**")
        filters["portes"] = st.multiselect("Porte", ["MEI","ME","EPP","Grande"], placeholder="Todos")
        filters["mei"]    = st.selectbox("MEI", ["Todos","Apenas MEI","Excluir MEI"], label_visibility="collapsed")
        filters["simples"]= st.selectbox("Simples Nacional", ["Todos","Sim","Não"], label_visibility="collapsed")

        anos_min, anos_max = 0, 25
        filters["anos_range"] = st.slider("Anos de atividade", 0, 25, (0, 25))

        # Botão salvar
        st.markdown("---")
        save_name = st.text_input("Nome da visualização", placeholder="Ex: SP · Salões 2024")
        if st.button("💾 Salvar filtro atual", width="stretch"):
            if save_name:
                st.session_state.saved_views.append({"name": save_name, "count": 0, "filters": filters})
                st.success(f"'{save_name}' salvo!")
            else:
                st.warning("Digite um nome para salvar.")

    return filters


# ══════════════════════════════════════════════════════
# 9. APLICAR FILTROS
# ══════════════════════════════════════════════════════
def apply_filters(df, filters):
    mask = pd.Series([True] * len(df), index=df.index)

    if filters.get("tem_email"):
        mask &= df["TEM_EMAIL"] == True
    if filters.get("sem_contador"):
        mask &= df["EMAIL_CONTABILIDADE"] == False
    if filters.get("tem_whatsapp"):
        mask &= df["WHATSAPP_1"].str.strip().str.len() > 0
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
        mask &= df["ORIGEM_CNAE"].str.lower() == "principal"
    elif origem == "Apenas CNAE secundário":
        mask &= df["ORIGEM_CNAE"].str.lower() == "secundario"

    if filters.get("busca_texto"):
        q = filters["busca_texto"].lower()
        mask &= (
            df["NOME FANTASIA"].str.lower().str.contains(q, na=False) |
            df["RAZÃO SOCIAL"].str.lower().str.contains(q, na=False) |
            df["CNPJ"].str.lower().str.contains(q, na=False)
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
    mask &= (df["ANOS_ATIVIDADE"] >= anos_r[0]) & (df["ANOS_ATIVIDADE"] <= anos_r[1])

    return df[mask].copy()


# ══════════════════════════════════════════════════════
# 10. KPIs
# ══════════════════════════════════════════════════════
def show_kpis(df, user):
    total   = len(df)
    c_whats = df["WHATSAPP_1"].str.strip().str.len().gt(0).sum()
    c_email = df["TEM_EMAIL"].sum()
    c_nova  = df["INICIO ATIVIDADE"].apply(lambda d: is_new(d, 1)).sum()
    c_sem_c = (df["EMAIL_CONTABILIDADE"] == False).sum()
    avg_anos = df["ANOS_ATIVIDADE"].mean()
    avg_anos_str = f"{avg_anos:.0f} anos" if not pd.isna(avg_anos) else "—"

    tier      = user.get("tier", "operacional")
    exp_used  = user.get("exports_used", 0)
    exp_limit = TIER_CFG[tier]["limit"]
    pct_w = f"{c_whats/total*100:.2f}%" if total else "—"
    pct_e = f"{c_email/total*100:.2f}%" if total else "—"

    # Linha 1
    st.markdown("**KPIs PRINCIPAIS**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Total de leads</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">filtro atual</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Com WhatsApp</div>
            <div class="kpi-value kpi-green">{c_whats:,}</div>
            <div class="kpi-sub">{pct_w} do total</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Com e-mail</div>
            <div class="kpi-value kpi-blue">{c_email:,}</div>
            <div class="kpi-sub">{pct_e} do total</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Idade média</div>
            <div class="kpi-value">{avg_anos_str}</div>
            <div class="kpi-sub">abertura de atividade</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Linha 2
    c5, c6, c7 = st.columns(3)
    with c5:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Novas este mês</div>
            <div class="kpi-value kpi-purple">{c_nova:,}</div>
            <div class="kpi-sub">abertas nos últimos 30 dias</div></div>""", unsafe_allow_html=True)
    with c6:
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Sem e-mail contador</div>
            <div class="kpi-value">{c_sem_c:,}</div>
            <div class="kpi-sub">contato direto com o dono</div></div>""", unsafe_allow_html=True)
    with c7:
        if tier == "explorador":
            exp_str = "Sem download"
            exp_color = "kpi-red"
            exp_sub   = "faça upgrade para baixar"
        elif exp_limit >= 999999:
            exp_str = "Ilimitado"
            exp_color = "kpi-green"
            exp_sub   = f"Plano {TIER_CFG[tier]['label']}"
        else:
            exp_str = f"{exp_used} / {exp_limit}"
            exp_color = "kpi-red" if exp_used >= exp_limit * 0.85 else ""
            exp_sub   = f"Plano {TIER_CFG[tier]['label']} — este mês"
        st.markdown(f"""<div class="kpi-box">
            <div class="kpi-label">Exports disponíveis</div>
            <div class="kpi-value {exp_color}">{exp_str}</div>
            <div class="kpi-sub">{exp_sub}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# 11. CHARTS
# ══════════════════════════════════════════════════════
def show_charts(df):
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">CNAE PRINCIPAL — top 5</div>', unsafe_allow_html=True)
        top_p = (df.groupby("CNAE_PRINCIPAL_NOME").size()
                   .sort_values(ascending=False).head(5).reset_index())
        top_p.columns = ["CNAE", "Count"]
        top_p["CNAE_short"] = top_p["CNAE"].str[:28] + "..."
        fig = go.Figure(go.Bar(
            x=top_p["Count"], y=top_p["CNAE_short"],
            orientation="h", marker_color="#1D9E75",
            text=top_p["Count"], textposition="outside",
        ))
        fig.update_layout(
            margin=dict(l=0, r=40, t=0, b=0), height=180,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False), yaxis=dict(autorange="reversed", tickfont_size=11),
            showlegend=False,
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">CNAE SECUNDÁRIO — top 5</div>', unsafe_allow_html=True)
        sec_df = df[df["CNAE_SECUNDARIO_NOME"].str.strip() != ""]
        if len(sec_df) == 0:
            st.caption("Nenhum CNAE secundário no filtro atual.")
        else:
            top_s = (sec_df.groupby("CNAE_SECUNDARIO_NOME").size()
                          .sort_values(ascending=False).head(5).reset_index())
            top_s.columns = ["CNAE", "Count"]
            top_s["CNAE_short"] = top_s["CNAE"].str[:28] + "..."
            fig2 = go.Figure(go.Bar(
                x=top_s["Count"], y=top_s["CNAE_short"],
                orientation="h", marker_color="#7F77DD",
                text=top_s["Count"], textposition="outside",
            ))
            fig2.update_layout(
                margin=dict(l=0, r=40, t=0, b=0), height=180,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False), yaxis=dict(autorange="reversed", tickfont_size=11),
                showlegend=False,
            )
            st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Municípios
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">EMPRESAS POR MUNICÍPIO — top 6</div>', unsafe_allow_html=True)
    top_m = (df.groupby("MUNICIPIO").size().sort_values(ascending=False).head(6).reset_index())
    top_m.columns = ["Município", "Count"]
    max_c = top_m["Count"].max()
    cols_m = st.columns(3)
    for i, row_m in top_m.iterrows():
        col = cols_m[i % 3]
        pct = row_m["Count"] / max_c if max_c else 0
        col.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:12px">
            <span style="width:100px;color:#374151;font-weight:500">{row_m['Município']}</span>
            <div style="flex:1;background:#f3f4f6;border-radius:3px;height:6px">
                <div style="width:{pct*100:.0f}%;background:#378ADD;height:6px;border-radius:3px"></div>
            </div>
            <span style="width:32px;text-align:right;color:#111827;font-weight:600">{row_m['Count']}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# 12. CARD RENDERER
# ══════════════════════════════════════════════════════
def build_card_html(row):
    main_name, sub_name = get_display_name(row)
    initials = get_initials(main_name)
    seg = row.get("SEGMENTO", "Salões e Barbearias")
    seg_info = SEG_CFG.get(seg, SEG_CFG["Salões e Barbearias"])
    av_cls   = seg_info["av"]
    pill_cls = seg_info["pill"]
    emoji    = seg_info["e"]

    # CNAE status
    cnae_status, cnae_cod, cnae_nom = get_cnae_status(row)
    cod_p = str(row.get("CNAE_PRINCIPAL_CODIGO",""))
    nom_p = str(row.get("CNAE_PRINCIPAL_NOME",""))
    cod_s = str(row.get("CNAE_SECUNDARIO_CODIGO",""))
    nom_s = str(row.get("CNAE_SECUNDARIO_NOME",""))

    if cnae_status == "primary":
        badge_html = '<span class="cnae-badge cnae-primary">✔ Beleza — CNAE principal</span>'
        strip_class = "cnae-strip cnae-strip-primary"
        strip_html  = f'{badge_html}<div class="cnae-strip-code">{cod_p} · {nom_p}</div>' \
                      '<div class="cnae-strip-link">⌄ Ver CNAE secundário</div>'
    else:
        badge_html  = '<span class="cnae-badge cnae-outside">⚠ Principal fora da beleza</span>'
        strip_class = "cnae-strip cnae-strip-outside"
        strip_html  = f'{badge_html}<div class="cnae-strip-warn">Principal: {cod_p} · {nom_p}</div>' \
                      f'<span class="cnae-badge cnae-secondary" style="margin-top:5px">✔ Beleza no CNAE secundário</span>' \
                      '<div class="cnae-strip-link">⌄ Analisar todos os CNAEs</div>'

    # Nova badge
    nova_badge = ""
    if is_new(row.get("INICIO ATIVIDADE")):
        nova_badge = '<span class="badge-nova">NOVA</span>'

    # Localização
    loc = f"{row.get('BAIRRO','')} · {row.get('MUNICIPIO','')}"

    # Contatos
    phones_html = ""
    wa_list  = [(row.get(f"WHATSAPP_{i}","")) for i in range(1,4)]
    tel_list = [(row.get(f"TELEFONE_{i}","")) for i in range(1,4)]

    wa_rows = ""
    for num in wa_list:
        if num and str(num).strip():
            link = wa_link(str(num))
            wa_rows += f"""
            <div class="contact-row">
                <span class="contact-type">WA</span>
                <span class="contact-num">{num}</span>
                <span class="contact-icons">
                    <a class="c-icon c-icon-wa" href="{link}" target="_blank" title="Enviar mensagem no WhatsApp">📲</a>
                </span>
            </div>"""

    tel_rows = ""
    for num in tel_list:
        if num and str(num).strip():
            tel_rows += f"""
            <div class="contact-row">
                <span class="contact-type">Tel</span>
                <span class="contact-num">{num}</span>
                <span class="contact-icons">
                    <a class="c-icon c-icon-tel" href="tel:{clean_phone(str(num))}" title="Ligar">📞</a>
                </span>
            </div>"""

    email_row = ""
    email = str(row.get("E-MAIL","")).strip()
    is_contador = row.get("EMAIL_CONTABILIDADE", False)
    if email and not is_contador:
        email_row = f"""
        <div class="contact-row">
            <span class="contact-type">Email</span>
            <span class="contact-num" style="font-size:11px">{email}</span>
            <span class="contact-icons">
                <a class="c-icon" href="mailto:{email}" title="Enviar e-mail">✉️</a>
            </span>
        </div>"""
    elif email and is_contador:
        email_row = f"""
        <div style="font-size:10px;color:#9ca3af;padding:5px 0;font-style:italic">
            ⚠️ E-mail de contador — não usar para prospecção
        </div>"""
    elif not email:
        email_row = '<div style="font-size:10px;color:#9ca3af;padding:5px 0">Sem e-mail cadastrado</div>'

    wa_block  = ""
    tel_block = ""
    if wa_rows:
        wa_block = f'<div class="contact-label">WHATSAPP CONFIRMADO</div>{wa_rows}'
    if tel_rows:
        tel_block = f'<div class="contact-label" style="margin-top:6px">TELEFONE</div>{tel_rows}'

    contact_html = f"""
    <div class="contact-section">
        <div class="contact-note">Número de telefone cadastrado na Receita Federal — confirme se é WhatsApp antes de usar</div>
    </div>"""

    # Botões de ação
    maps_url = str(row.get("MAPS","#"))
    first_wa = next((str(num) for num in wa_list if num and str(num).strip()), "")
    first_email = email if email and not is_contador else ""
    wa_action = f'<a class="act-btn btn-wa-main" href="{wa_link(first_wa)}" target="_blank">◉ Iniciar contato</a>' if first_wa else \
                '<span class="act-btn btn-wa-main" style="opacity:.4;cursor:default">◉ Sem WhatsApp</span>'
    email_action = f'<a class="act-btn btn-mail" href="mailto:{first_email}">✉ E-mail</a>' if first_email else \
                   '<span class="act-btn btn-mail" style="opacity:.4;cursor:default">✉ Sem e-mail</span>'

    # Expand — endereço e dados cadastrais
    endereco = str(row.get("ENDERECO MAPA","—"))
    bairro   = str(row.get("BAIRRO",""))
    cep      = str(row.get("CEP",""))
    municipio= str(row.get("MUNICIPIO",""))
    estado   = str(row.get("ESTADO",""))

    anos_str = f"{row.get('ANOS_ATIVIDADE',0):.1f} anos"
    inicio   = pd.to_datetime(row.get("INICIO ATIVIDADE","")).strftime("%d/%m/%Y") if pd.notna(row.get("INICIO ATIVIDADE")) else "—"
    abertura = pd.to_datetime(row.get("INICIO ATIVIDADE","")).strftime("%m/%Y") if pd.notna(row.get("INICIO ATIVIDADE")) else "—"

    all_cnaes = []
    if cod_p:
        is_b_p = cod_p.replace("-","").replace("/","") in BEAUTY_CNAES
        dot_c  = "#1D9E75" if is_b_p else "#E24B4A"
        all_cnaes.append(f'<div class="cnae-item"><div class="cnae-dot" style="background:{dot_c}"></div>Principal: {cod_p} · {nom_p}</div>')
    if cod_s:
        is_b_s = cod_s.replace("-","").replace("/","") in BEAUTY_CNAES
        dot_c  = "#1D9E75" if is_b_s else "#888780"
        all_cnaes.append(f'<div class="cnae-item"><div class="cnae-dot" style="background:{dot_c}"></div>Secundário: {cod_s} · {nom_s}</div>')
    else:
        all_cnaes.append('<div class="cnae-item"><div class="cnae-dot" style="background:#d1d5db"></div>Sem CNAE secundário</div>')
    cnaes_html = "".join(all_cnaes)

    mei_txt    = "Sim" if row.get("MEI") else "Não"
    simples_txt= "Sim" if row.get("SIMPLES") else "Não"

    html = f"""
<div class="lead-card">
  <div class="card-top">
    <div class="card-identity">
      <div class="card-avatar {av_cls}">{initials}</div>
      <div class="name-block">
        <div class="company-main">{main_name}{nova_badge}</div>
        {"<div class='company-sub'>"+sub_name+"</div>" if sub_name else ""}
        <span class="seg-pill {pill_cls}">{emoji} {seg}</span>
      </div>
    </div>
                <div class="card-info">
                    <div class="info-row">⌖ {loc} — {row.get('ESTADO','')}</div>
                    <div class="info-row">▦ {row.get('PORTE','')} · Abertura: {abertura} · {anos_str}</div>
                </div>
        <div class="{strip_class}">{strip_html}</div>
    </div>
  {contact_html}
  <div class="action-buttons">
        {wa_action}
        {email_action}
        <a class="act-btn btn-maps" href="{maps_url}" target="_blank">⌖ Maps</a>
  </div>
  <details class="card-expand">
    <summary>Ver endereço completo e dados cadastrais</summary>
    <div class="expand-body">
      <div class="exp-section">
        <div class="exp-section-title">ENDEREÇO COMPLETO</div>
        <div class="address-box">
          {endereco}<br>
          {bairro} · {municipio}/{estado} · CEP {cep}
          <div class="address-actions">
            <a class="addr-btn addr-btn-maps" href="{maps_url}" target="_blank">📍 Abrir no Maps</a>
          </div>
        </div>
      </div>
      <div class="exp-section">
        <div class="exp-section-title">TODOS OS CNAEs</div>
        <div class="cnae-list">{cnaes_html}</div>
      </div>
      <div class="exp-section">
        <div class="exp-section-title">DADOS CADASTRAIS</div>
        <div class="data-grid">
          <div class="data-item"><span class="data-label">CNPJ</span><span class="data-value">{row.get('CNPJ','—')}</span></div>
          <div class="data-item"><span class="data-label">Porte</span><span class="data-value">{row.get('PORTE','—')}</span></div>
          <div class="data-item"><span class="data-label">Capital Social</span><span class="data-value">{format_capital(row.get('CAPITAL SOCIAL',0))}</span></div>
          <div class="data-item"><span class="data-label">Natureza Jurídica</span><span class="data-value">{row.get('NATUREZA_JURIDICA','—')}</span></div>
          <div class="data-item"><span class="data-label">MEI</span><span class="data-value">{mei_txt}</span></div>
          <div class="data-item"><span class="data-label">Simples Nacional</span><span class="data-value">{simples_txt}</span></div>
          <div class="data-item"><span class="data-label">Início de atividade</span><span class="data-value">{inicio} ({anos_str})</span></div>
          <div class="data-item"><span class="data-label">Matriz / Filial</span><span class="data-value">{row.get('MATRIZ FILIAL','—')}</span></div>
        </div>
      </div>
    </div>
  </details>
</div>"""
    return html


# ══════════════════════════════════════════════════════
# 13. VIEW CARDS
# ══════════════════════════════════════════════════════
def show_cards(df):
    rows_list = [df.iloc[i] for i in range(len(df))]
    cols = st.columns(2)
    for i, row in enumerate(rows_list):
        with cols[i % 2]:
            st.markdown(minify(build_card_html(row)), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# 14. VIEW LISTA
# ══════════════════════════════════════════════════════
def show_list(df):
    column_groups = [
        ("Empresa", ["RAZÃO SOCIAL", "NOME FANTASIA", "MUNICIPIO", "ESTADO"]),
        ("Classificação", ["SEGMENTO", "CNAE_MATCHED", "ORIGEM_CNAE", "COLUNA_MATCH", "KEYWORD_MATCH", "TODOS_MATCHES", "QTD_MATCHES"]),
        ("Contatos", ["WHATSAPP_1", "WHATSAPP_2", "WHATSAPP_3", "TELEFONE_1", "TELEFONE_2", "TELEFONE_3", "E-MAIL", "TEM_EMAIL", "TEM_TELEFONE", "EMAIL_CONTABILIDADE"]),
        ("Localização", ["BAIRRO", "CEP", "ENDERECO MAPA", "MAPS"]),
        ("Cadastro", ["CNPJ", "PORTE", "CAPITAL SOCIAL", "MEI", "SIMPLES", "MATRIZ FILIAL", "INICIO ATIVIDADE", "NATUREZA_JURIDICA"]),
        ("Atividade", ["CNAE_PRINCIPAL_CODIGO", "CNAE_PRINCIPAL_NOME", "CNAE_SECUNDARIO_CODIGO", "CNAE_SECUNDARIO_NOME"]),
        ("Origem", ["RECEITA FEDERAL", "SITE"]),
    ]
    columns = [column for _, group_columns in column_groups for column in group_columns]
    labels = {
        "RAZÃO SOCIAL": "Razão Social", "NOME FANTASIA": "Nome Fantasia", "CNAE_MATCHED": "CNAE Matched",
        "ORIGEM_CNAE": "Origem CNAE", "COLUNA_MATCH": "Coluna Match", "KEYWORD_MATCH": "Keyword Match",
        "TODOS_MATCHES": "Todos Matches", "QTD_MATCHES": "Qtd. Matches", "TEM_EMAIL": "Tem E-mail",
        "TEM_TELEFONE": "Tem Telefone", "EMAIL_CONTABILIDADE": "E-mail Contabilidade", "ENDERECO MAPA": "Endereço",
        "MAPS": "Maps", "CAPITAL SOCIAL": "Capital Social", "MATRIZ FILIAL": "Matriz/Filial",
        "INICIO ATIVIDADE": "Início Atividade", "NATUREZA_JURIDICA": "Natureza Jurídica", "RECEITA FEDERAL": "Receita Federal",
        "CNAE_PRINCIPAL_CODIGO": "CNAE Principal", "CNAE_PRINCIPAL_NOME": "Nome CNAE Principal",
        "CNAE_SECUNDARIO_CODIGO": "CNAE Secundário", "CNAE_SECUNDARIO_NOME": "Nome CNAE Secundário",
    }

    def cell_value(row, column):
        value = row.get(column, "")
        if pd.isna(value) if not isinstance(value, (list, tuple, dict)) else False:
            return "—"
        if column in {"MEI", "SIMPLES", "TEM_EMAIL", "TEM_TELEFONE", "EMAIL_CONTABILIDADE"}:
            return "Sim" if bool(value) else "Não"
        if column == "CAPITAL SOCIAL":
            return format_capital(value)
        if column == "INICIO ATIVIDADE":
            return pd.to_datetime(value).strftime("%d/%m/%Y") if value else "—"
        return str(value).strip() or "—"

    def render_cell(row, column):
        value = cell_value(row, column)
        safe_value = escape(value)
        if column in {"MAPS", "RECEITA FEDERAL", "SITE"} and value != "—":
            href = escape(value if column != "SITE" else f"http://{value}", quote=True)
            label = "🗺️ Ver" if column == "MAPS" else ("Abrir" if column == "RECEITA FEDERAL" else "Visitar")
            return f'<a class="list-link" href="{href}" target="_blank">{label}</a>'
        return safe_value

    table_rows = []
    for _, row in df.iterrows():
        cells = "".join(f"<td>{render_cell(row, column)}</td>" for column in columns)
        table_rows.append(f"<tr>{cells}</tr>")

    group_headers = "".join(
        f'<th colspan="{len(group_columns)}">{group_name}</th>'
        for group_name, group_columns in column_groups
    )
    column_headers = "".join(f"<th>{labels.get(column, column.title())}</th>" for column in columns)

    table_html = f"""
        <div class="list-table-wrap" title="Deslize horizontalmente para consultar todos os campos">
            <table class="list-table">
                <thead>
                    <tr class="list-group">{group_headers}</tr>
                    <tr>{column_headers}</tr>
                </thead>
                <tbody>{''.join(table_rows)}</tbody>
            </table>
        </div>"""
    st.markdown(minify(table_html), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# 15. VIEW BAIRRO
# ══════════════════════════════════════════════════════
def show_bairro(df):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Por município")
        top_m = df.groupby("MUNICIPIO").size().sort_values(ascending=False).head(10).reset_index()
        top_m.columns = ["Município","Empresas"]
        max_c = top_m["Empresas"].max()
        for _, r in top_m.iterrows():
            pct = r["Empresas"] / max_c if max_c else 0
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:12px">
                <span style="width:130px;font-weight:500">{r['Município']}</span>
                <div style="flex:1;background:#f3f4f6;border-radius:3px;height:6px">
                    <div style="width:{pct*100:.0f}%;background:#378ADD;height:6px;border-radius:3px"></div>
                </div>
                <span style="width:30px;text-align:right;font-weight:600">{r['Empresas']}</span>
            </div>""", unsafe_allow_html=True)

    with c2:
        municipios = sorted(df["MUNICIPIO"].dropna().unique().tolist())
        sel_mun = st.selectbox("Detalhe por bairro:", municipios)
        if sel_mun:
            top_b = (df[df["MUNICIPIO"]==sel_mun]
                       .groupby("BAIRRO").size()
                       .sort_values(ascending=False).head(12).reset_index())
            top_b.columns = ["Bairro","Empresas"]
            max_b = top_b["Empresas"].max()
            st.markdown(f"##### {sel_mun} — por bairro")
            for _, r in top_b.iterrows():
                pct = r["Empresas"] / max_b if max_b else 0
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;font-size:12px">
                    <span style="width:130px">{r['Bairro']}</span>
                    <div style="flex:1;background:#f3f4f6;border-radius:3px;height:5px">
                        <div style="width:{pct*100:.0f}%;background:#1D9E75;height:5px;border-radius:3px"></div>
                    </div>
                    <span style="width:24px;text-align:right;font-weight:600">{r['Empresas']}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:12px;padding:10px 14px;background:#f9fafb;border-radius:8px;
                border:1px solid #e5e7eb;font-size:12px;color:#374151">
        💡 <strong>Como usar:</strong> Identifique os bairros com maior concentração para planejar
        <strong>rotas de visita</strong> otimizadas. Filtre um município na barra lateral e use
        esta view para definir qual bairro atacar primeiro.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# 16. DOWNLOAD
# ══════════════════════════════════════════════════════
def show_download(df, user):
    tier      = user.get("tier","explorador")
    exp_used  = user.get("exports_used", 0)
    exp_limit = TIER_CFG[tier]["limit"]
    total = len(df)

    st.markdown("---")
    c1, c2, c3 = st.columns([3,1,1])
    with c1:
        remaining = exp_limit - exp_used if exp_limit < 999999 else "ilimitado"
        if tier == "explorador":
            st.caption("🔒 **Download bloqueado** — faça upgrade para Operacional para exportar leads.")
        else:
            st.caption(f"Plano {TIER_CFG[tier]['label']} · **{exp_used}** de **{exp_limit if exp_limit < 999999 else '∞'}** exports usados · restam **{remaining}**")

    if tier != "explorador":
        # CSV
        csv_buf = df.drop(columns=["ANOS_ATIVIDADE"], errors="ignore").to_csv(index=False, sep=";").encode("utf-8-sig")
        with c2:
            st.download_button("⬇️ CSV", csv_buf, f"achei_leads_{date.today()}.csv",
                               "text/csv", width="stretch")
        # Excel
        xlsx_buf = BytesIO()
        df.drop(columns=["ANOS_ATIVIDADE"], errors="ignore").to_excel(xlsx_buf, index=False, engine="openpyxl")
        xlsx_buf.seek(0)
        with c3:
            st.download_button("⬇️ Excel", xlsx_buf.read(), f"achei_leads_{date.today()}.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               width="stretch")


# ══════════════════════════════════════════════════════
# 17. MAIN
# ══════════════════════════════════════════════════════
def main():
    init_state()

    if not st.session_state.logged_in:
        show_login()
        return

    df_full = get_data()
    filters = show_sidebar(df_full)
    df = apply_filters(df_full, filters)

    # Header
    col_h1, col_h2 = st.columns([3,1])
    with col_h1:
        st.markdown("## 🎯 AcheiMeuCliente")
        st.caption(f"Plataforma de Inteligência de Mercado para Beleza  ·  Base: **{len(df_full):,}** empresas")
    with col_h2:
        st.markdown("<br>", unsafe_allow_html=True)
        view_labels = {"cards":"🃏 Cards", "lista":"📋 Lista", "bairro":"📍 Por bairro"}
        view_sel = st.radio("Visualização", list(view_labels.keys()),
                            format_func=lambda x: view_labels[x],
                            horizontal=True, label_visibility="collapsed",
                            key="view_mode")

    st.markdown("---")
    show_kpis(df, st.session_state.user)
    show_charts(df)

    # Contagem + view
    st.markdown(f"""
    <div class="section-title-bar">
        <div>
            <div class="result-count">{len(df):,} leads encontrados</div>
            <div class="result-sub">Filtros ativos aplicados</div>
        </div>
    </div>""", unsafe_allow_html=True)

    if view_sel == "cards":
        show_cards(df)
    elif view_sel == "lista":
        show_list(df)
    else:
        show_bairro(df)

    show_download(df, st.session_state.user)


main()
