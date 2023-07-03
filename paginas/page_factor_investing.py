from matplotlib import pyplot as plt
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
        
        tab1, tab2 = st.tabs(["Ações", "FIIs"])
        with tab1:
            st.write("## Ações")
            st.markdown("**Filtros iniciais:** Dividend Yield > 0; Cotação > 0; Liq. Corr. > 0; Liq.2meses > 0") 

            if 'lista_acoes' not in st.session_state:
                df_acoes = get_resultado_acoes()
                st.session_state['lista_acoes'] = df_acoes
            else:
                df_acoes = st.session_state['lista_acoes']

            st.write(df_acoes)

        with tab2:        
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
                                            (menor_cotacao, maior_cotacao), step=1.0, format="R$ %.2f")

                    menor_pvp = float(df_fiis["P/VP"].min(numeric_only=True))
                    maior_pvp = float(df_fiis["P/VP"].max(numeric_only=True))
                    
                    filtro_pvp = st.slider("P/VP", menor_pvp, maior_pvp,
                                            (menor_pvp, maior_pvp), step=0.1, format="%.2f")

                with col3:        
                    filtro_dy = st.slider("Dividend Yield (%)", 0, 100,
                                            (0, 100), step=1, format="%.2f")
                    
                    menor_valor_mercado = float(df_fiis["Valor de Mercado"].min(numeric_only=True))/1000000
                    maior_valor_mercado = float(df_fiis["Valor de Mercado"].max(numeric_only=True))/1000000
                    
                    filtro_valor_mercado = st.slider("Valor mínimo de Mercado", 
                                                     menor_valor_mercado,
                                                    maior_valor_mercado, 
                                                    value=menor_valor_mercado,
                                                    step=1.0, format="%.2f milhões de R$")
                    
                    #pergunta = st.text_input("Pergunta para o ChatGPT:", "Considerando cotação, dy e p/vp, qual melhor ativo para comprar hoje, se tenho 10 mil reais?")
                        
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
                    df_fiis_tela.set_index('Papel', drop=True, inplace=True)
                                        
                    tab_resultado, tab_stats = st.tabs(["Resultado", "Estatísticas"])
                    
                    with tab_resultado:
                        st.write("#### " + str(df_fiis_tela.count().unique()[0]) + " registros retornados")
                        st.write(df_fiis_tela)
                        
                        import plotly.express as px
                        import plotly.graph_objects as go

                        fiis = df_fiis_tela.index

                        fig = go.Figure(data=[
                            go.Bar(name='Cotação', x=fiis, y=df_fiis_tela["Cotação"]),
                            go.Bar(name='DY', x=fiis, y=df_fiis_tela["Dividend Yield"]),
                            go.Bar(name='P/VP', x=fiis, y=df_fiis_tela["P/VP"]),
                            go.Bar(name='Valor de Mercado', x=fiis, y=df_fiis_tela["Valor de Mercado"]),                            
                            go.Bar(name='Liquidez', x=fiis, y=df_fiis_tela["Liquidez"]),                            
                        ])
                        # Change the bar mode
                        fig.update_layout(barmode='group')


                        #pd.options.plotting.backend = "plotly"
                        #fig = px.bar(df_fiis_tela, x= df_fiis_tela.index, y = ['Cotação', 'Dividend Yield', "P/VP", "Valor de Mercado", "Liquidez"])
                        st.plotly_chart(fig)

                    with tab_stats:
                        st.write("#### Estatísticas")
                        df_fiis_stats = pd.DataFrame()
                        df_fiis_stats["Menor valor"] = df_fiis_tela.min(numeric_only=True)
                        df_fiis_stats["Valor médio"] = df_fiis_tela.mean(numeric_only=True)
                        df_fiis_stats["Desvio padrão"] = df_fiis_tela.std(numeric_only=True)
                        df_fiis_stats["Maior valor"] = df_fiis_tela.max(numeric_only=True)

                        st.write(df_fiis_stats)
                    
                    # from pandasai.llm.openai import OpenAI
                    # from pandasai import PandasAI

                    # OPEN_API_TOKEN = st.secrets["open_api"]["token"]

                    # llm = OpenAI(api_token=OPEN_API_TOKEN)
                    
                    # pandas_ai = PandasAI(llm)
                    
                    # st.write("### Resposta do ChatGPT")
                    
                    # df_ia = pandas_ai(df_fiis_tela, prompt=pergunta)
                    # st.write(df_ia)
                
                
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
        
        
