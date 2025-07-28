@st.cache_data
def carregar_dados():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=scopes)
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1DsmrCrp0Z0gZT6OGKR1jPo2WhHYU7bqvgUoxi1-0HdU/edit")
    worksheet = spreadsheet.worksheet("SISU_2024")

    dados = worksheet.get_all_values()
    header = dados[0]  # usa a primeira linha como nome de coluna
    df = pd.DataFrame(dados[1:], columns=header)

    df['NU_NOTACORTE'] = (
        pd.Series(df['NU_NOTACORTE'])
        .astype(str)
        .str.replace(',', '.', regex=False)
        .str.strip()
    )
    df['NU_NOTACORTE'] = pd.to_numeric(df['NU_NOTACORTE'], errors='coerce')
    df['NU_NOTACORTE'] = df['NU_NOTACORTE'].apply(lambda x: x / 100 if x > 1000 else x)
    return df
