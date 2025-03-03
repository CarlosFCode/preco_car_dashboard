import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.read_csv('car_price_dataset.csv')

# Renomear colunas para português
df = df.rename(columns={
    'Brand': 'Marca',
    'Model': 'Modelo',
    'Year': 'Ano',
    'Engine_Size': 'Tamanho_Motor',
    'Fuel_Type': 'Tipo_combustivel',
    'Transmission': 'Transmissao',
    'Mileage': 'Quilometragem',
    'Doors': 'Portas',
    'Owner_Count': 'Cont_dono',
    'Price': 'Preco'
})

# Título do dashboard
st.title('Dashboard de Preços de Carros')

# Sidebar para filtros
st.sidebar.header('Filtros')

# Filtro de marca
marcas_selecionadas = st.sidebar.multiselect('Selecione as marcas:', df['Marca'].unique())

# Filtro de modelo
if marcas_selecionadas:
    modelos_disponiveis = df[df['Marca'].isin(marcas_selecionadas)]['Modelo'].unique()
else:
    modelos_disponiveis = []

modelos_selecionados = st.sidebar.multiselect('Selecione o modelo:', modelos_disponiveis)

# Filtro de tipo de combustível
tipo_combustivel = st.sidebar.selectbox('Escolha um tipo de combustível:', df['Tipo_combustivel'].unique())

# Filtro de tipo de transmissão
tipo_transmissao = st.sidebar.selectbox('Escolha um tipo de transmissão:', df['Transmissao'].unique())

# Filtro de preço
preco_maximo = st.sidebar.slider(
    'Escolha o limite para o preço:',
    int(df['Preco'].min()),
    int(df['Preco'].max()),
    int(df['Preco'].mean())
)

# Aplicar filtros
df_filtrado = df[
    (df['Marca'].isin(marcas_selecionadas)) &
    (df['Modelo'].isin(modelos_selecionados)) &
    (df['Tipo_combustivel'] == tipo_combustivel) &
    (df['Transmissao'] == tipo_transmissao) &
    (df['Preco'] <= preco_maximo)
]

st.write("### Dados Filtrados")
st.dataframe(df_filtrado)

# Gráfico 1: Preço vs Tamanho do Motor
st.write("### Preço vs Tamanho do Motor")
fig1 = px.scatter(
    df_filtrado,
    x='Tamanho_Motor',
    y='Preco',
    color='Modelo',
    title="Preço vs Tamanho do Motor"
)
st.plotly_chart(fig1)

# Gráfico 4: Quilometragem vs Preço
st.write("### Quilometragem vs Preço")
fig4 = px.scatter(
    df_filtrado,
    x='Quilometragem',
    y='Preco',
    color='Marca',
    title="Quilometragem vs Preço"
)
st.plotly_chart(fig4)


fig_treemap = px.treemap(
    df_filtrado,
    path=['Marca', 'Modelo'],
    values='Preco',
    color='Preco',
    title='Distribuição de Preços por Marca e Modelo'
)

st.plotly_chart(fig_treemap)
