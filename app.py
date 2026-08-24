"""
╔══════════════════════════════════════════════════════════════════╗
║   FILTRADOR DE LEADS — PHD BELEZA / QUALQUER SEGMENTO           ║
║   Streamlit App — Deploy gratuito no Streamlit Community Cloud  ║
╚══════════════════════════════════════════════════════════════════╝

Para rodar localmente:
    pip install streamlit pandas openpyxl chardet
    streamlit run app.py

Para deploy gratuito:
    1. Sobe esse arquivo para um repositório GitHub
    2. Acessa https://share.streamlit.io
    3. Conecta o repositório → deploy automático
"""

import io
import unicodedata
from datetime import datetime

import chardet
import pandas as pd
import streamlit as st

# ──────────────────────────────────────────────────────────────────
#  CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Filtrador de Leads | PHD Beleza",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────
#  KEYWORDS PADRÃO (pré-carregadas, editáveis pelo usuário na UI)
# ──────────────────────────────────────────────────────────────────

DEFAULT_INCLUIR = """CABELEIREIRO
CABELEIREIRA
SALAO
SALAO DE BELEZA
BELEZA
BELA
BELLA
ESTETICA
CABELO
CABELOS
CAPILAR
PENTEADO
PENTEADOS
PENTEADISTA
NOIVA
NOIVAS
CASAMENTO
FESTA
FESTAS
EVENTO
EVENTOS
DEBUTANTE
FORMATURA
MAQUIAGEM
MAKE
HAIR
BEAUTY
HAIR STYLIST
HAIRSTYLE
STUDIO
ESTUDIO
ESPACO
COLORIMETRIA
COLORACAO
COIFFURE
COIFFEUR
VISAGISMO
TRANCAS
CACHOS
AFRO
MEGA HAIR
GLAMOUR
GLAM
ATELIER
MAISON
STYLING
BELLE
BELISSIMA
INSTITUTO
ESCOLA DE BELEZA"""

DEFAULT_EXCLUIR = """CONTABILIDADE
CONTABIL
CONTADOR
ADVOCACIA
ADVOGADO
FARMACIA
DROGARIA
ODONTOLOGIA
DENTISTA
IMOBILIARIA
ACADEMIA DE GINASTICA
SUPERMERCADO
MEDICINA
CLINICA MEDICA"""

# ──────────────────────────────────────────────────────────────────
#  UTILITÁRIOS
# ──────────────────────────────────────────────────────────────────

def normalizar(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.upper().strip()


def detectar_encoding(raw_bytes: bytes) -> str:
    resultado = chardet.detect(raw_bytes[:50_000])
    enc = resultado.get("encoding") or "utf-8"
    if enc.lower() in ("ascii", "windows-1252", "iso-8859-1"):
        return "latin-1"
    return enc


def ler_csv(arquivo_bytes: bytes, sep: str) -> pd.DataFrame | None:
    enc = detectar_encoding(arquivo_bytes)
    for encoding in [enc, "utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(
                io.BytesIO(arquivo_bytes),
                sep=sep,
                dtype=str,
                encoding=encoding,
                low_memory=False,
                on_bad_lines="skip",
            )
            return df
        except Exception:
            continue
    return None


def checar_positivo(razao: str, fantasia: str, kw_list: list[str]) -> dict | None:
    r_norm = normalizar(razao)
    f_norm = normalizar(fantasia)
    matches = []
    for kw in kw_list:
        kw_n = normalizar(kw)
        cols = []
        if kw_n in r_norm:
            cols.append("RAZÃO SOCIAL")
        if kw_n in f_norm:
            cols.append("NOME FANTASIA")
        if cols:
            matches.append({"termo": kw, "colunas": " + ".join(cols)})
    if not matches:
        return None
    return {
        "KEYWORD_MATCH": matches[0]["termo"],
        "TODOS_MATCHES": " | ".join(m["termo"] for m in matches),
        "QTD_MATCHES": len(matches),
        "COLUNA_MATCH": matches[0]["colunas"],
    }


def checar_negativo(razao: str, fantasia: str, excluir_list: list[str]) -> bool:
    r_norm = normalizar(razao)
    f_norm = normalizar(fantasia)
    return any(normalizar(t) in r_norm or normalizar(t) in f_norm for t in excluir_list)


def filtrar_df(
    df: pd.DataFrame,
    col_razao: str,
    col_fantasia: str,
    kw_incluir: list[str],
    kw_excluir: list[str],
) -> pd.DataFrame:
    resultados = []
    for _, row in df.iterrows():
        razao    = str(row.get(col_razao, ""))
        fantasia = str(row.get(col_fantasia, ""))
        if checar_negativo(razao, fantasia, kw_excluir):
            continue
        match = checar_positivo(razao, fantasia, kw_incluir)
        if match is None:
            continue
        r = row.to_dict()
        r.update(match)
        resultados.append(r)
    return pd.DataFrame(resultados)


def deduplicar(df: pd.DataFrame, col_cnpj: str) -> pd.DataFrame:
    if df.empty or col_cnpj not in df.columns:
        return df
    df["QTD_MATCHES"] = pd.to_numeric(df.get("QTD_MATCHES", 0), errors="coerce").fillna(0)
    df = df.sort_values("QTD_MATCHES", ascending=False)
    return df.drop_duplicates(subset=[col_cnpj], keep="first").reset_index(drop=True)


def gerar_excel(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="TODOS", index=False)
        for kw in sorted(df["KEYWORD_MATCH"].dropna().unique())[:10]:
            sub = df[df["KEYWORD_MATCH"] == kw]
            nome_aba = str(kw)[:31]
            sub.to_excel(writer, sheet_name=nome_aba, index=False)
    return buf.getvalue()


# ──────────────────────────────────────────────────────────────────
#  SIDEBAR — CONFIGURAÇÕES
# ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ✂️ Filtrador de Leads")
    st.markdown("---")

    st.markdown("### ⚙️ Configurações do arquivo")
    separador = st.selectbox(
        "Separador do CSV",
        options=[";", ",", "\t"],
        format_func=lambda x: {";" : "Ponto e vírgula  ;",
                                "," : "Vírgula  ,",
                                "\t": "Tab  \\t"}[x],
        index=0,
    )

    col_razao    = st.text_input("Coluna — Razão Social",   value="RAZÃO SOCIAL")
    col_fantasia = st.text_input("Coluna — Nome Fantasia",  value="NOME FANTASIA")
    col_cnpj     = st.text_input("Coluna — CNPJ",          value="CNPJ")

    st.markdown("---")
    st.markdown("### 🟢 Palavras para INCLUIR")
    st.caption("Uma por linha. Sem acentos ou com — o sistema normaliza.")
    kw_incluir_raw = st.text_area(
        "Palavras-chave de inclusão",
        value=DEFAULT_INCLUIR,
        height=300,
        label_visibility="collapsed",
    )

    st.markdown("### 🔴 Palavras para EXCLUIR")
    st.caption("Remove leads com essas palavras no nome.")
    kw_excluir_raw = st.text_area(
        "Palavras-chave de exclusão",
        value=DEFAULT_EXCLUIR,
        height=150,
        label_visibility="collapsed",
    )

    # Processa as listas
    kw_incluir = [l.strip() for l in kw_incluir_raw.splitlines() if l.strip()]
    kw_excluir = [l.strip() for l in kw_excluir_raw.splitlines() if l.strip()]

    st.markdown("---")
    st.markdown(f"**{len(kw_incluir)}** termos de inclusão  \n**{len(kw_excluir)}** termos de exclusão")


# ──────────────────────────────────────────────────────────────────
#  ÁREA PRINCIPAL
# ──────────────────────────────────────────────────────────────────

st.title("🗂️ Filtrador de Leads por Palavras-Chave")
st.markdown(
    "Faça upload do seu CSV de leads, configure as palavras-chave na barra lateral "
    "e baixe o arquivo filtrado pronto para prospecção."
)

# ── Upload de arquivo ──
st.markdown("### 📁 Carregue seu arquivo de leads")
arquivo = st.file_uploader(
    "Arraste ou selecione o arquivo CSV",
    type=["csv", "txt"],
    help="Arquivo CSV exportado do Achei Meu Cliente ou de qualquer fonte de CNPJ.",
)

if arquivo is not None:
    raw_bytes = arquivo.read()
    df_raw = ler_csv(raw_bytes, separador)

    if df_raw is None or df_raw.empty:
        st.error("❌ Não foi possível ler o arquivo. Tente mudar o separador na barra lateral.")
        st.stop()

    # ── Preview do arquivo bruto ──
    st.success(f"✅ Arquivo carregado: **{arquivo.name}** — {len(df_raw):,} registros | {len(df_raw.columns)} colunas")

    with st.expander("👁️ Prévia do arquivo original (primeiras 5 linhas)", expanded=False):
        st.dataframe(df_raw.head(5), use_container_width=True)

    with st.expander("📋 Colunas detectadas no arquivo", expanded=False):
        st.write(list(df_raw.columns))

    st.markdown("---")

    # ── Botão de processar ──
    if st.button("🚀 Filtrar Leads", type="primary", use_container_width=True):

        if col_razao not in df_raw.columns and col_fantasia not in df_raw.columns:
            st.error(
                f"❌ Nenhuma das colunas de busca encontrada no arquivo.  \n"
                f"Você configurou: **{col_razao}** e **{col_fantasia}**  \n"
                f"Colunas disponíveis: {list(df_raw.columns)}"
            )
            st.stop()

        # Preenche colunas ausentes com string vazia
        for c in [col_razao, col_fantasia]:
            if c not in df_raw.columns:
                df_raw[c] = ""

        with st.spinner("Filtrando leads..."):
            df_filtrado = filtrar_df(
                df_raw,
                col_razao=col_razao,
                col_fantasia=col_fantasia,
                kw_incluir=kw_incluir,
                kw_excluir=kw_excluir,
            )

        if df_filtrado.empty:
            st.warning("⚠️ Nenhum lead passou pelo filtro. Revise as palavras-chave.")
            st.stop()

        # Deduplica
        df_final = deduplicar(df_filtrado, col_cnpj)

        # ── Métricas de resultado ──
        st.markdown("### 📊 Resultado do Filtro")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📥 Total lido",        f"{len(df_raw):,}")
        c2.metric("✅ Após filtro",        f"{len(df_filtrado):,}")
        c3.metric("🔑 CNPJs únicos",       f"{len(df_final):,}")
        reducao = round((1 - len(df_final) / max(len(df_raw), 1)) * 100, 1)
        c4.metric("📉 Redução",            f"{reducao}%")

        # ── Top keywords ──
        st.markdown("#### 🏷️ Keywords mais encontradas")
        if "TODOS_MATCHES" in df_final.columns:
            from collections import Counter
            todos = []
            for val in df_final["TODOS_MATCHES"].dropna():
                todos.extend([t.strip() for t in str(val).split("|")])
            contagem = Counter(todos).most_common(15)
            df_kw = pd.DataFrame(contagem, columns=["Keyword", "Ocorrências"])
            st.dataframe(df_kw, use_container_width=True, height=200)

        # ── Prévia do resultado ──
        st.markdown("#### 👁️ Prévia dos leads filtrados")
        colunas_preview = [col_cnpj, col_razao, col_fantasia,
                           "KEYWORD_MATCH", "TODOS_MATCHES", "QTD_MATCHES", "COLUNA_MATCH"]
        colunas_preview = [c for c in colunas_preview if c in df_final.columns]
        st.dataframe(df_final[colunas_preview].head(20), use_container_width=True)

        # ── Download ──
        st.markdown("---")
        st.markdown("### 💾 Baixar resultado")

        nome_base = f"leads_filtrados_{datetime.now().strftime('%Y%m%d_%H%M')}"

        col_dl1, col_dl2 = st.columns(2)

        # CSV
        csv_bytes = df_final.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig")
        col_dl1.download_button(
            label="⬇️ Baixar CSV",
            data=csv_bytes,
            file_name=nome_base + ".csv",
            mime="text/csv",
            use_container_width=True,
        )

        # Excel
        excel_bytes = gerar_excel(df_final)
        col_dl2.download_button(
            label="⬇️ Baixar Excel (.xlsx)",
            data=excel_bytes,
            file_name=nome_base + ".xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        st.success(
            f"✅ Processamento concluído!  \n"
            f"**{len(df_final):,}** leads prontos para prospecção — {reducao}% do volume original."
        )

else:
    # Estado vazio — instruções
    st.info(
        "👈 **Configure as palavras-chave** na barra lateral e **carregue seu CSV** acima para começar."
    )

    with st.expander("ℹ️ Como usar", expanded=True):
        st.markdown("""
**Passo a passo:**

1. **Barra lateral** → ajuste as palavras de inclusão e exclusão conforme seu segmento
2. **Carregue o CSV** exportado do Achei Meu Cliente ou de qualquer base de CNPJs
3. Clique em **Filtrar Leads**
4. Veja o resultado e **baixe o arquivo filtrado** (CSV ou Excel)

**Colunas geradas no output:**
| Coluna | O que é |
|---|---|
| `KEYWORD_MATCH` | Melhor palavra-chave que bateu |
| `TODOS_MATCHES` | Todos os termos encontrados |
| `QTD_MATCHES` | Quantidade de termos — quanto maior, mais qualificado |
| `COLUNA_MATCH` | Se bateu na Razão Social, Nome Fantasia ou ambos |

**Dica:** O sistema ignora acentos e maiúsculas/minúsculas automaticamente.  
"Estética", "ESTETICA" e "estetica" são tratados como a mesma palavra.
        """)

# ──────────────────────────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Filtrador de Leads · PHD Beleza · Desenvolvido com Streamlit")
