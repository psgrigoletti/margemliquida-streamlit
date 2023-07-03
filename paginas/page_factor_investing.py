import streamlit as st
import pandas as pd
from libs.market_data.fundamentus.lista import get_df_acoes, get_df_fiis

@st.cache_data(show_spinner="Buscando dados fundamentalistas para ações.", ttl=3600)
def get_resultado_acoes():
    df = get_df_acoes()
    df = df[df["Div.Yield"]>0]
    df = df[df["Cotação"]>0]
    df = df[df["Liq. Corr."]>0]
    df = df[df["Liq.2meses"]>0]
    return df

@st.cache_data(show_spinner="Buscando dados fundamentalistas para FIIs.", ttl=3600)
def get_resultado_fiis():
    df = get_df_fiis()
    df = df[df["Dividend Yield"] > 0]
    df = df[df["Cotação"] > 0]
    df = df[df["Liquidez"] > 0]
    return df 

def main():
    st.title(":star: Factor Investing")
    mensagens = st.container()

    if st.button("Carregar dados...") or ('lista_fiis' in st.session_state and 'lista_acoes' in st.session_state):
        st.write("## Ações")
        st.markdown("**Filtros iniciais:** Dividend Yield > 0; Cotação > 0; Liq. Corr. > 0; Liq.2meses > 0") 

        if 'lista_acoes' not in st.session_state:
            df_acoes = get_resultado_acoes()
            st.session_state['lista_acoes'] = df_acoes
        else:
            df_acoes = st.session_state['lista_acoes']

        st.write(df_acoes)
        
        st.write("## FIIs")
        st.markdown("**Filtros iniciais:** Dividend Yield > 0; Cotação > 0; Liquidez > 0")      

        if 'lista_fiis' not in st.session_state:
            df_fiis = get_resultado_fiis()
            st.session_state['lista_fiis'] = df_fiis
        else:
            df_fiis = st.session_state['lista_fiis']


        with st.form("form_fiis"):
            col1, _, col2, _, col3, _ = st.columns([4,1,4,1,4,1])

            with col1:
                segmentos_possiveis = ["Todos"] + list(df_fiis["Segmento"].dropna().unique())
                filtro_segmento = st.selectbox("Segmento:", segmentos_possiveis)

            with col2:       
                menor_cotacao = float(df_fiis["Cotação"].min(numeric_only=True))
                maior_cotacao = float(df_fiis["Cotação"].max(numeric_only=True))
                
                filtro_cotacao = st.slider("Cotação", menor_cotacao, maior_cotacao,
                                        (menor_cotacao, maior_cotacao), step=0.1)

                menor_pvp = float(df_fiis["P/VP"].min(numeric_only=True))
                maior_pvp = float(df_fiis["P/VP"].max(numeric_only=True))
                
                filtro_pvp = st.slider("P/VP", menor_pvp, maior_pvp,
                                        (menor_pvp, maior_pvp), step=0.1)

            with col3:        
                filtro_dy = st.slider("Dividend Yield", 0, 100,
                                        (0, 100), step=1)
                
                menor_valor_mercado = float(df_fiis["Valor de Mercado"].min(numeric_only=True))/1000000
                maior_valor_mercado = float(df_fiis["Valor de Mercado"].max(numeric_only=True))/1000000
                
                filtro_valor_mercado = st.slider("Valor de Mercado mínimo (em milhões de R$)", menor_valor_mercado,
                                                maior_valor_mercado)            
                    
            if st.form_submit_button("Filtrar"):
                df_fiis_tela = df_fiis.copy()
                if filtro_segmento != "Todos":
                    df_fiis_tela = df_fiis_tela[df_fiis_tela["Segmento"] == filtro_segmento]
                df_fiis_tela = df_fiis_tela[df_fiis_tela["Cotação"] >= filtro_cotacao[0]]            
                df_fiis_tela = df_fiis_tela[df_fiis_tela["Cotação"] <= filtro_cotacao[1]] 
                df_fiis_tela = df_fiis_tela[df_fiis_tela["Dividend Yield"] >= filtro_dy[0]/100]            
                df_fiis_tela = df_fiis_tela[df_fiis_tela["Dividend Yield"] <= filtro_dy[1]/100] 
                df_fiis_tela = df_fiis_tela[df_fiis_tela["P/VP"] >= filtro_pvp[0]]            
                df_fiis_tela = df_fiis_tela[df_fiis_tela["P/VP"] <= filtro_pvp[1]] 
                df_fiis_tela = df_fiis_tela[df_fiis_tela["Valor de Mercado"] >= filtro_valor_mercado*1000000]            
                        
                st.write(df_fiis_tela)
            
        # ranking = pd.DataFrame()
        # ranking['pos'] = range(1,151)
        # #st.write(ranking)        
        # ranking['EV/EBIT'] = df[ df['evebit'] > 0 ].sort_values(by=['evebit']).index[:150].values
        # ranking['ROIC'] = df.sort_values(by=['roic'], ascending=False).index[:150].values
        # #st.write(ranking)    
        # ranking = pd.concat([
        #     ranking.pivot_table(columns='EV/EBIT', values='pos'),
        #     ranking.pivot_table(columns='ROIC', values='pos')
        # ])
        # ranking = ranking.dropna(axis=1).sum()
        # n_shares = 20
        # magic_formula = ranking.sort_values()[:n_shares]
        # st.write(magic_formula)
        
        
