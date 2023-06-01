import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px

df = pd.read_sql_table('Funds', 'sqlite:///database.db')

sectors = df['Sector'].unique()

st.title('**PROVA FINAL**')
st.subheader('Fundos Imobiliarios')
st.markdown('Fundos imobiliários (também conhecidos como FIIs) são investimentos coletivos que aplicam recursos em empreendimentos imobiliários. Eles funcionam como condomínios fechados, em que diversos investidores compram cotas e se tornam donos de uma fração do patrimônio do fundo.')
st.markdown('Os recursos captados pelos FIIs são utilizados na aquisição, construção, desenvolvimento, reforma e/ou gestão de imóveis comerciais, como escritórios, lojas, galpões, shoppings, entre outros. Esses imóveis geram renda por meio de aluguéis, que são distribuídos aos cotistas na forma de dividendos.')
st.markdown('Os FIIs são negociados na bolsa de valores e permitem ao investidor aplicar em imóveis com valores menores do que seria necessário para comprar um imóvel físico diretamente. Além disso, o investimento em FIIs é uma forma de diversificar a carteira de investimentos, uma vez que o desempenho dos fundos não está necessariamente correlacionado com outros ativos financeiros, como ações e títulos públicos.')
st.markdown('Fonte de Dados: https://www.fundsexplorer.com.br/ranking')

st.sidebar.header('**FUNDOS IMOBILIARIOS**')

if st.sidebar.checkbox('Rentabilidade Diária'):

    sector = st.sidebar.selectbox('Selecione o Setor do Fundo', sectors, key=0)
    funds = df[df['Sector'] == sector]

    profitability = (funds['Current Price'] - funds['Current Price'].shift(1) / 1 + funds['Price Variation'].shift(1)) * 100
    profitability.name = sector

    st.subheader(f'Rentabilidade Diária do Setor - {sector}')
    st.markdown('Base de Cálculo: [Preço Atual] - ([Preço Atual] / 1 + [Variação de Preço]) * 100')
    st.area_chart(profitability)

if st.sidebar.checkbox('Variação Diária'):

    sector = st.sidebar.multiselect('Selecione os Setores do Fundo', sectors, key=1)
    funds = df[df['Sector'].isin(sector)]

    chart = alt.Chart(funds).mark_line().encode(x='Current Price', y='Price Variation', color='Sector').properties(width=800, height=500)

    st.subheader('Variação Diária dos Setores')
    st.markdown(f'{sector}')
    st.altair_chart((chart).interactive(), use_container_width=False)

if st.sidebar.checkbox('Relação (Preço - Liquidação)'):

    sector = st.sidebar.multiselect('Selecione os Setores do Fundo', sectors, key=2)
    funds = df[df['Sector'].isin(sector)]

    fig = px.scatter(funds, x='Daily Liquidity', y='Price Variation', color='Sector', size='Daily Liquidity')

    st.subheader('Relação de Variação Diaria do Preço e da Liquidação')
    st.markdown(f'{sector}')
    st.plotly_chart(fig)

if st.sidebar.checkbox('Desempenho por Setor'):
    
    dfProfitability = df.copy()

    dfProfitability['profitability'] = (df['Current Price'] - df['Current Price'].shift(1) / 1 + df['Price Variation'].shift(1)) * 100

    funds = dfProfitability.groupby('Sector')['profitability'].mean()

    fig = px.bar(funds)
    fig.update_layout(yaxis_title='Rentabilidade Diária Média', xaxis_title='Setores')

    st.subheader('Desempenho por Setor')
    st.markdown('Base de Cálculo: [Preço Atual] - ([Preço Atual] / 1 + [Variação de Preço]) * 100')
    st.plotly_chart(fig)

if st.sidebar.checkbox('Volatilidade do Preço'):

    dfVolatility = df.copy()

    dfVolatility['volatility'] = df.groupby('Sector')['Current Price'].diff()

    fig = fig = px.histogram(dfVolatility, x="volatility", nbins=30, color='Sector', barmode="overlay")
    fig.update_layout(xaxis_title="Volatilidade Diária do Preço", yaxis_title="Frequência")

    st.subheader('Volatilidade do Preço')
    st.markdown('Base de Cálculo: Primeira Diferença Discreta de Cada Elemento.')
    st.plotly_chart(fig)

if st.sidebar.checkbox('Comparação Entre Rendimentos de Dividendos'):

    st.subheader('Comparação entre Rendimento de Dividendos e Rendimento Anual de Dividendos')
    
    dfYield = df.copy()

    dfYield['yield'] = dfYield['Dividend Yield'] / 100
    dfYield['annualizedYield'] = dfYield['yield'] * 12

    yieldMin = st.slider('Selecione o Yield Mínimo', min_value=dfYield['yield'].min(), max_value=dfYield['yield'].max(), step=0.001, value=0.0)

    fig = px.scatter(dfYield[dfYield['yield'] >= yieldMin], x='yield', y='annualizedYield', color='Sector')

    fig.update_layout(xaxis_title='Yield', yaxis_title='Yield Anual')

    st.plotly_chart(fig)