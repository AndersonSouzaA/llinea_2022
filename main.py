import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import datetime as dt
from PIL import Image
import matplotlib.pyplot as plt


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title='DASHBOARD GRUPO LLINEA - 2022',
    page_icon='💲',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'http://www.meusite.com.br',
        'Report a bug': "http://www.meuoutrosite.com.br",
        'About': "Esse app foi desenvolvido por Anderson."
    }
)

# --- Criar o dataframe
df = pd.read_excel(r'Gerencial Grupo Llinea 2022.xlsx')
df['mm'] = df['Mês/Ano'].dt.strftime('%m/%Y')


# -- Criar o sidebar
with st.sidebar:
    logo_teste = Image.open('.\logo Empresa.jpg')
    st.image(logo_teste, width=250)
    st.header('MENU - DASHBOARD DE 2022')
   
    fEmpresa = st.selectbox("Selecione a Empresa:",options= df['Empresa'] .unique())
    st.write('Você selecionou:',fEmpresa)
        
    fUnidade = st.selectbox("Selecione a Unidade:",options = df.loc[df['Empresa']==fEmpresa]['Unidade'] .unique())
    st.write('Você selecionou:',fUnidade)
   
    fMesAno = st.selectbox("Selecione o Mês/Ano:",options = df.loc[(df['Empresa']==fEmpresa)&(df['Unidade']==fUnidade)]['mm'].unique())
    st.write('Você selecionou:',fMesAno)
  
 
# Vendas Mensais
tab1_proventos = df.loc[(
    df['Empresa'] == fEmpresa) &
    (df['Unidade'] == fUnidade) &
    (df['mm'] == fMesAno)]
#tab1_proventos   
  
   ### PÁGINA PRINCIPAL ###
st.header(":bar_chart: DASHBOARD DE GRUPO LLÍNEA 2022",)
st.subheader('Visualização Mês:')
total_horas_extras = round(tab1_proventos['Horas Extras e DSR'].sum(),2)
total_noturno = round(tab1_proventos['Adicional Noturno'].sum(),2)
total_gratificacoes = round(tab1_proventos['Gratificações'].sum(),2)
total_difpaga = round(tab1_proventos['Diferenças Pagas'].sum(),2)
total_decimoterceiro = round(tab1_proventos['Líquido 13º'].sum(),2)
total_ferias = round(tab1_proventos['Líquido de Férias'].sum(),2)
total_rescisao = round(tab1_proventos['Líquido de Rescisão'].sum(),2)


dst1, dst2, dst3, dst4, dst5, dst6,dst7= st.columns([5,5,5,5,5,5,1])
with dst1:
    st.write('***Horas Extras:***')
    st.subheader(f"R$ {total_horas_extras:.2f}")
    
with dst2:
    st.write('***Adicional Noturno:***')
    st.subheader(f"R$ {total_noturno:.2f}")

with dst3:
    st.write('***Gratificações:***')
    st.subheader(f"R$ {total_gratificacoes:.2f}")

with dst4:
    st.write('***Férias:***')
    st.subheader(f"R$ {total_ferias:.2f}")

with dst5:
    st.write('***Rescisões:***')
    st.subheader(f"R$ {total_rescisao:.2f}") 

with dst6:
    st.write('***13º Salário:***')
    st.subheader(f"R$ {total_decimoterceiro:.2f}")       
    
st.markdown("---")



dst1, dst2 = st.columns([5,5])

with dst1:
    st.subheader(fEmpresa)
with dst2:
    st.subheader(fUnidade)

st.subheader('Visualização por Ano:')
 
##### PADRÕES #########
cor_grafico = '#4C49A8'
altura_grafico=300


##### GRÁFICOS #########
tab2_geral = df.loc[(
    df['Empresa'] == fEmpresa) &
    (df['Unidade'] == fUnidade)]

tab2_geral = tab2_geral.drop(columns = ['Gestor'])

beneficios_media = tab2_geral.groupby(["Empresa","Unidade",'mm'])[["Cesta Básica","Seguro de Vida","Vale Transporte","Plano de Saúde"]].mean().reset_index()
beneficios_media['Total Média Benefícios'] = beneficios_media["Cesta Básica"]+beneficios_media["Seguro de Vida"]+beneficios_media["Vale Transporte"]+beneficios_media["Plano de Saúde"]
beneficios_media2= beneficios_media[["Empresa","Unidade","mm",'Total Média Benefícios']]
#beneficios_media2
Encargos_safe_EPI = tab2_geral
Encargos_safe_EPI['Total Empresa'] = tab2_geral["ENCARGOS EMPRESA"]+tab2_geral["SAFE"]+tab2_geral["UNIFORMES E EPI"]+tab2_geral["Cooperados"]
Encargos_safe_EPI= Encargos_safe_EPI[["Empresa","Unidade","mm",'Total Empresa']]


#GRÁFICO 1.0 Valor Geral Empresa
graf1_valor_geral = alt.Chart(tab2_geral).mark_bar(
    color= cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusTopRight=9,
).encode(
    x = 'mm',
    y = 'Total Geral Empresa:Q',
    tooltip=['mm', 'Total Geral Empresa']
).properties(height=altura_grafico).configure_axis(grid=False
).configure_view(strokeWidth=0)

#GRÁFICO 2.0 Beneficio
graf_total_benf = alt.Chart(beneficios_media2).mark_bar(
    color= cor_grafico,
    cornerRadiusTopLeft=9,
    cornerRadiusTopRight=9
).encode(
    x = alt.X('mm'),
    y = alt.Y('Total Média Benefícios'),
    tooltip=['mm','Total Média Benefícios']
).properties(height=altura_grafico).configure_axis(grid=False).configure_view(strokeWidth=0)

dst1, dst2= st.columns([5,5,])
with dst1:
    st.subheader('Geral')
    st.altair_chart(graf1_valor_geral, use_container_width=True)
    st.subheader('Benefícios')
    st.altair_chart(graf_total_benf, use_container_width=True)

with dst2:
    tipo=st.radio(
    "Selecione tipo de relatório:",
    ('Gráfico','Relatório')
)
    st.subheader('Encargos + Safe + EPI + Cooperados')
    if tipo =="Gráfico":
        graf_Encargos = alt.Chart(Encargos_safe_EPI).mark_bar(
        color= cor_grafico,
        cornerRadiusTopLeft=9,
        cornerRadiusTopRight=9
    ).encode(
        x = alt.X('mm'),
        y = alt.Y('Total Empresa',
    ))
        st.altair_chart(graf_Encargos, use_container_width=True)
    elif tipo=="Relatório":
        st.dataframe(Encargos_safe_EPI)

st.markdown("---")   
