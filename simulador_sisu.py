# simulador_sisu.py

try:
    import streamlit as st
except ModuleNotFoundError:
    raise ModuleNotFoundError("O módulo 'streamlit' não está instalado. Execute 'pip install streamlit' no terminal antes de rodar este app.")

import pandas as pd
from unidecode import unidecode
import gspread
from google.oauth2.service_account import Credentials

# === Função para normalizar texto ===
def normalizar(texto):
    return unidecode(str(texto).strip().lower())

# === Conectar ao Google Sheets ===
@st.cache_data
def carregar_dados():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("service_account.json", scopes=scopes)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1DsmrCrp0Z0gZT6OGKR1jPo2WhHYU7bqvgUoxi1-0HdU/edit")
    worksheet = spreadsheet.worksheet("SISU_2024")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # Tratar notas de corte
    df['NU_NOTACORTE'] = (
        df['NU_NOTACORTE'].astype(str).str.replace(',', '.', regex=False).str.strip()
    )
    df['NU_NOTACORTE'] = pd.to_numeric(df['NU_NOTACORTE'], errors='coerce')
    df['NU_NOTACORTE'] = df['NU_NOTACORTE'].apply(lambda x: x / 100 if x > 1000 else x)
    return df

# === Layout do Streamlit ===
st.set_page_config(page_title="Simulador SISU", layout="centered")
st.title("🎓 Simulador de Cursos SISU")
st.markdown("Entre com suas notas e veja cursos que você pode alcançar!")

# === Entradas ===
col1, col2 = st.columns(2)
with col1:
    nota_cn = st.number_input("Ciências da Natureza (CN)", min_value=0.0, max_value=1000.0, step=1.0)
    nota_ch = st.number_input("Ciências Humanas (CH)", min_value=0.0, max_value=1000.0, step=1.0)
    nota_lc = st.number_input("Linguagens e Códigos (LC)", min_value=0.0, max_value=1000.0, step=1.0)

with col2:
    nota_mt = st.number_input("Matemática (MT)", min_value=0.0, max_value=1000.0, step=1.0)
    nota_red = st.number_input("Redação", min_value=0.0, max_value=1000.0, step=1.0)

filtro_curso = st.text_input("Curso desejado (ex: medicina, arquitetura, engenharia civil)")
filtro_estado = st.text_input("Estado (sigla, ex: SP)").upper().strip()

# === Simular ===
if st.button("Simular"):
    with st.spinner("Buscando cursos compatíveis..."):
        df_sisu = carregar_dados()
        media = (nota_cn + nota_ch + nota_lc + nota_mt + nota_red) / 5

        df_filtrado = df_sisu[df_sisu['NU_NOTACORTE'] <= media]

        if filtro_curso:
            curso_normalizado = normalizar(filtro_curso)
            df_filtrado = df_filtrado[df_filtrado['NO_CURSO'].apply(lambda x: curso_normalizado in normalizar(x))]

        if filtro_estado:
            df_filtrado = df_filtrado[df_filtrado['SG_UF_CAMPUS'].str.upper() == filtro_estado]

        df_filtrado = df_filtrado[
            df_filtrado['DS_MOD_CONCORRENCIA'].str.strip().str.lower().isin(["ampla concorrência", "ac"])
        ]

        df_filtrado = df_filtrado.sort_values(by='NU_NOTACORTE', ascending=False)

        if not df_filtrado.empty:
            st.success(f"{len(df_filtrado)} cursos encontrados com sua média: {media:.2f}")
            st.dataframe(df_filtrado[[
                'NO_IES', 'NO_CURSO', 'DS_TURNO', 'SG_UF_CAMPUS',
                'DS_MOD_CONCORRENCIA', 'NU_NOTACORTE']].head(30))

            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📁 Baixar resultados em CSV",
                data=csv,
                file_name=f"relatorio_sisu_{int(media)}.csv",
                mime='text/csv'
            )
        else:
            st.warning("Nenhum curso encontrado com sua média e filtros aplicados.")
