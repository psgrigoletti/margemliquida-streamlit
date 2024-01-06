import streamlit as st
from libs.importador.importador_fii import arquivos_pdf_2_df


@st.cache_data(ttl=3600, show_spinner="Carregando Notas de Corretagem...")
def retornar_df_das_notas(uploaded_files):
    df = arquivos_pdf_2_df(uploaded_files)
    df["Nota"] = "XXXX"  # soh para não expor o número das notas...
    return df


def main():
    st.title(
        ":book: Importador de notas",
    )
    mensagens = st.container()

    uploaded_files = st.file_uploader(
        "Escolha suas notas em formato PDF (*.pdf)", accept_multiple_files=True
    )

    nomes_arquivos = [uploaded_file.name for uploaded_file in uploaded_files]
    if len(set(nomes_arquivos)) != len(nomes_arquivos):
        st.error(
            "Foram selecionados arquivos com mesmo nome. Deixe apenas um arquivo de cada nota."
        )
        st.stop()

    from libs.importador.importador_fii import df_2_excel

    df = retornar_df_das_notas(uploaded_files)

    st.write(df)

    if uploaded_files:
        import uuid

        myuuid = str(uuid.uuid4())
        nome_arquivo = f"download_notas_{myuuid}.xls"
        buffer = df_2_excel(df, nome_arquivo)

        st.download_button(
            label="Download formato XLS",
            data=buffer,
            file_name=nome_arquivo,
            mime="application/vnd.ms-excel",
        )
