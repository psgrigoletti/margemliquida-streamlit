import pandas as pd
import plotly.express as px
import streamlit as st
from margemliquida_market_data.fundsexplorer import fundsexplorer


@st.cache_data(show_spinner="Carregando dados do IFIX", ttl=60 * 5)
def buscar_dados_ifix():
    from libs.market_data.b3.b3 import CarteiraTeoricaB3

    return CarteiraTeoricaB3.buscar_dados_ifix()


@st.cache_data(show_spinner="Carregando dados do site fundsexplorer", ttl=60 * 5)
def buscar_dados_fundsexplorer():
    return fundsexplorer.buscar_dados_fundsexplorer()


@st.cache_data(show_spinner="Carregando dados do IBOV", ttl=60 * 5)
def buscar_dados_ibov():
    from libs.market_data.b3.b3 import CarteiraTeoricaB3

    return CarteiraTeoricaB3.buscar_dados_ibov()


def main():
    st.title(
        ":flashlight: Composição dos índices (IBOV e IFIX)",
    )
    st.write(
        "**Fonte**: https://b3.com.br e https://www.fundsexplorer.com.br/ via [selenium](https://pypi.org/project/selenium/)"
    )
    alertas = st.empty()

    if st.button("Carregar dados..."):
        with alertas:
            st.info(
                "O carregamento dos dados pode demorar um pouco... aguarde...",
                icon="⌛",
            )
        tab_ibov, tab_ifix = st.tabs(["IBOV", "IFIX"])
        with tab_ifix:
            st.title("IFIX")
            tab_ifix1, tab_ifix2, tab_ifix3, tab_ifix4, tab_ifix5 = st.tabs(
                [
                    ":memo: Dados B3",
                    ":memo: Dados fundsexplorer",
                    ":memo: Dados consolidados",
                    ":bar_chart: Gráfico sunburst",
                    ":bar_chart: Gráfico treemap",
                ]
            )

            ibov = buscar_dados_ibov()
            ifix = buscar_dados_ifix()
            funds = buscar_dados_fundsexplorer()
            ifix_final = pd.merge(ifix, funds, how="left", on="Código")
            ifix_final["Setor"] = ifix_final["Setor"].fillna("?")

            with tab_ifix1:
                st.write(ifix)

            with tab_ifix2:
                st.write(funds)

            with tab_ifix3:
                st.write(ifix_final)

            with tab_ifix4:
                fig1_ifix = px.sunburst(
                    data_frame=ifix_final,
                    path=["Setor", "Código"],
                    values="Part. (%)",
                    height=800,
                )
                fig1_ifix.update_traces(
                    textfont_color="black",
                    textfont_size=15,
                    # hovertemplate="<b>%{label}:</b> %{value:.2f}%",
                )
                st.write(fig1_ifix)

            with tab_ifix5:
                fig2_ifix = px.treemap(
                    data_frame=ifix_final,
                    path=["Setor", "Código"],
                    values="Part. (%)",
                    height=800,
                )
                fig2_ifix.update_traces(
                    textfont_color="black",
                    textfont_size=15,
                    # hovertemplate="<b>%{label}:</b> %{value:.2f}%",
                )
                st.write(fig2_ifix)

        with tab_ibov:
            st.title("IBOV")
            tab_ibov1, tab_ibov2, tab_ibov3 = st.tabs(
                [
                    ":memo: Dados B3",
                    ":bar_chart: Gráfico sunburst",
                    ":bar_chart: Gráfico treemap",
                ]
            )

            with tab_ibov1:
                st.write(ibov)

            with tab_ibov2:
                fig1_ibov = px.sunburst(
                    data_frame=ibov,
                    path=["Setor", "Subsetor", "Código"],
                    values="Part. (%)",
                    height=800,
                )
                fig1_ibov.update_traces(
                    textfont_color="black",
                    textfont_size=15,
                    # hovertemplate="<b>%{label}:</b> %{value:.2f}%",
                )
                st.write(fig1_ibov)

            with tab_ibov3:
                fig2_ibov = px.treemap(
                    data_frame=ibov,
                    path=["Setor", "Subsetor", "Código"],
                    values="Part. (%)",
                    height=800,
                )
                fig2_ibov.update_traces(
                    textfont_color="black",
                    textfont_size=15,
                    # hovertemplate="<b>%{label}:</b> %{value:.2f}%",
                )
                st.write(fig2_ibov)
        with alertas:
            st.empty()
            st.success("Dados carregados com sucesso...", icon="✅")
