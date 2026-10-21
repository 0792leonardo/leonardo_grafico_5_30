#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gráfico 5.30 – CO – Evolução das médias anuais das concentrações máximas diárias (médias de 8 horas) RMSP – Demais escalas
================================================================================

Este script gera um gráfico interativo em HTML mostrando a evolução temporal
das concentrações médias anuais de CO (monóxido de carbono) para diferentes
estações de monitoramento, com filtro para o período 2016-2025.

DIFERENCIAL: Usa pd.read_csv() com parâmetros específicos para arquivos CSV
no padrão brasileiro (separador ; e decimal ,) de forma nativa e eficiente.

CO = Monóxido de carbono - gás incolor e inodoro produzido pela combustão
incompleta de combustíveis fósseis. É tóxico porque se liga à hemoglobina,
reduzindo a capacidade do sangue de transportar oxigênio.

Autor: Leonardo Rocha
Data: 2026-09-18
Versão: 1.0.0
"""

# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path  # Para manipulação de caminhos de arquivos de forma segura
import pandas as pd       # Para leitura e manipulação de dados em tabelas (DataFrames)
import plotly.graph_objects as go  # Para criação de gráficos interativos


# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

# Define o caminho do arquivo CSV com os dados
CSV = Path("Dd_grafico_5_30_v2.csv")

# Lê o arquivo CSV com parâmetros específicos para o padrão brasileiro:
# - sep=";": separador ponto-e-vírgula (comum em arquivos brasileiros)
# - decimal=",": vírgula como separador decimal (padrão brasileiro)
# - encoding="utf-8-sig": remove o BOM automaticamente
# 
# VANTAGEM: O pandas já faz a conversão de "1,5" para 1.5 automaticamente
df = pd.read_csv(CSV, sep=";", decimal=",", encoding="utf-8-sig")


# =============================================================================
# PREPARAÇÃO DOS DADOS
# =============================================================================

# Nome da coluna que contém os nomes das estações
station_col = "estacao"

# Identifica TODAS as colunas de anos e as ORDENA numericamente
# key=int garante ordem cronológica correta (2000 < 2001 < ... < 2025)
year_cols = sorted(
    [c for c in df.columns if str(c).isdigit()],
    key=int
)

# FILTRA apenas os anos de interesse para exibição (2016-2025)
# Esta lista será usada para plotar o gráfico
years = [c for c in year_cols if 2016 <= int(c) <= 2025]

# --- Conversão de segurança das colunas de anos ---
# Embora pd.read_csv com decimal="," já converta, este passo garante
# compatibilidade com valores que possam ter sido lidos como strings
# (ex: células mistas com texto e número)
for c in year_cols:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"  # Valores inválidos se tornam NaN
    )


# =============================================================================
# DEFINIÇÃO DOS ESTILOS VISUAIS
# =============================================================================

# Lista de estilos (cor + símbolo) para as estações
# 10 combinações diferentes para garantir variedade visual
# Os estilos são aplicados ciclicamente se houver mais estações que estilos
styles = [
    ("#009BC2", "square"),           # Azul ciano - Quadrado
    ("#E600C7", "square-open"),      # Rosa choque - Quadrado vazado
    ("#F2A900", "circle-open"),      # Amarelo dourado - Círculo vazado
    ("#00A651", "circle"),           # Verde - Círculo
    ("#003BDE", "circle"),           # Azul - Círculo
    ("#FF0000", "x"),                # Vermelho - X
    ("#F2B000", "diamond-open"),     # Laranja claro - Losango vazado
    ("#8B2E2E", "x"),                # Marrom avermelhado - X
    ("#0B2B66", "square-open"),      # Azul marinho - Quadrado vazado
    ("#7A5A9A", "diamond")           # Roxo - Losango
]


# =============================================================================
# CRIAÇÃO DO GRÁFICO
# =============================================================================

# Inicializa uma figura vazia
fig = go.Figure()

# Itera sobre cada linha do DataFrame (cada linha = uma estação)
for i, row in df.iterrows():
    # Seleciona estilo (cor + símbolo) com base no índice
    # O operador % (módulo) garante repetição cíclica se necessário
    color, symbol = styles[i % len(styles)]
    
    # Extrai os valores de CO para os anos exibidos (2016-2025)
    y = [row[c] for c in years]
    
    # Prepara os valores para o tooltip com formatação brasileira:
    # - Valores NaN (pd.isna) → string vazia
    # - Valores numéricos → formatados com 1 decimal e vírgula como separador
    # Exemplo: 1.5 → "1,5"
    # Nota: float(v) garante que o valor seja tratado como número
    customdata = [
        "" if pd.isna(v) else f"{float(v):.1f}".replace(".", ",")
        for v in y
    ]
    
    # Adiciona uma série (traço) ao gráfico
    fig.add_trace(go.Scatter(
        # Dados do eixo X (anos) e eixo Y (valores de CO)
        x=years,
        y=y,
        
        # Modo: linha conectando pontos + marcadores nos pontos
        mode="lines+markers",
        
        # Nome da estação (convertido para string por segurança)
        name=str(row[station_col]),
        
        # Não conecta gaps (NaN) - a linha terá interrupções onde faltam dados
        connectgaps=False,
        
        # Configuração da linha
        line=dict(
            color=color,          # Cor definida pela lista styles
            width=1.7             # Espessura da linha
        ),
        
        # Configuração dos marcadores
        marker=dict(
            color=color,          # Cor do marcador (mesma da linha)
            symbol=symbol,        # Símbolo definido pela lista styles
            size=8                # Tamanho do marcador
        ),
        
        # Dados customizados para o tooltip (valores formatados em BR)
        # Acessados via %{customdata} no hovertemplate
        customdata=customdata,
        
        # Template do tooltip usando customdata
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"  # Nome da estação em negrito
            "CO: %{customdata} ppm<extra></extra>"  # Valor formatado em BR
        )
    ))


# =============================================================================
# CONFIGURAÇÃO DO LAYOUT (APARÊNCIA DO GRÁFICO)
# =============================================================================

fig.update_layout(
    # Tema claro com fundo branco
    template="plotly_white",
    
    # Altura da figura em pixels
    height=760,
    
    # Margens ao redor do gráfico
    # Margem esquerda maior (105px) para título do eixo Y
    # Margem inferior (180px) para a legenda horizontal
    margin=dict(l=105, r=35, t=25, b=180),
    
    # Cor de fundo do papel (área externa ao gráfico)
    paper_bgcolor="#ffffff",                  # Azul muito claro
    
    # Cor de fundo da área do gráfico
    plot_bgcolor="#ffffff",                   # Mesma cor para consistência
    
    # Modo de hover: exibe informações de todas as séries simultaneamente
    hovermode="x unified",
    
    # Configuração da fonte global
    font=dict(
        family="Arial, sans-serif",           # Fonte sans-serif
        size=14,                              # Tamanho padrão
        color="#222222"                       # Cinza muito escuro
    ),
    
    # Configuração do eixo X (horizontal)
    xaxis=dict(
        type="category",                      # Tipo categórico (anos como rótulos)
        tickmode="array",                     # Ticks definidos manualmente
        tickvals=years,                       # Posições dos ticks = anos
        ticktext=[str(y) for y in years],     # Rótulos dos ticks = anos (strings)
        showgrid=False,                       # Sem linhas de grade verticais
        zeroline=False,                       # Sem linha no zero
        showline=True,                        # Mostra a linha do eixo
        linecolor="#B8B8B8",                   # Cor da linha do eixo
        ticks="inside",                            # Marcadores dentro do eixo
        range=[-0.0, len(year_cols) - 0.0],           # Cola o 1º ponto no eixo Y
        categoryorder="array",                        # Mantém ordem original
        categoryarray=[str(c) for c in year_cols],    # Ordem das categorias
    ),
    
    # Configuração do eixo Y (vertical)
    yaxis=dict(
        title="CO (ppm)",                     # Título do eixo (ppm!)
        range=[0, 3],                         # Limites: 0 a 3 ppm
        
        # Ticks personalizados com formato brasileiro (vírgula decimal)
        tickmode="array",
        tickvals=[0, 1, 2, 3],                # Posições numéricas
        ticktext=["0,0", "1,0", "2,0", "3,0"],  # Rótulos com vírgula
        
        showgrid=True,                        # Mostra linhas de grade horizontais
        gridcolor="rgba(110,110,110,0.35)",   # Cinza com 35% de opacidade
        griddash="dot",                       # Linhas pontilhadas
        zeroline=False,                       # Sem linha no zero
        showline=True,                        # Mostra a linha do eixo
        linecolor="#B8B8B8",                   # Cor da linha do eixo
        ticks="outside"                           # Marcadores fora do eixo
    ),
    
    # Configuração da legenda
    legend=dict(
        orientation="h",                      # Horizontal
        yanchor="top",                        # Âncora no topo
        y=-0.15,                              # Posicionada abaixo do gráfico
        xanchor="center",                     # Centralizada horizontalmente
        x=0.5,                                # Centro do eixo X
        font=dict(size=11.5)                  # Fonte menor para muitas séries
    )
)


# =============================================================================
# EXPORTAÇÃO DO GRÁFICO
# =============================================================================

# Salva o gráfico em um arquivo HTML (autônomo, com Plotly embutido)
fig.write_html(
    "index.html",                             # Nome do arquivo de saída
    include_plotlyjs=True,                    # Inclui a biblioteca Plotly (offline)
    full_html=True,                           # Gera um documento HTML completo
    config={                                  # Configurações do gráfico
        "responsive": True,                   # Gráfico se adapta à tela
        "displaylogo": False,                 # Remove o logo da Plotly
        "scrollZoom": True                    # Permite zoom com scroll
    }
)


# =============================================================================
# MENSAGEM DE CONFIRMAÇÃO
# =============================================================================

print("=" * 70)
print("✅ GRÁFICO DE CO GERADO COM SUCESSO!")
print("=" * 70)
print(f"📊 Arquivo: index.html")
print(f"📍 Local: {Path.cwd()}")
print(f"📈 Estações: {len(df)}")
print(f"📅 Anos no CSV: {year_cols[0]} a {year_cols[-1]} ({len(year_cols)} anos)")
print(f"👁️  Anos exibidos: {years[0]} a {years[-1]} ({len(years)} anos)")
print(f"🎨 Estilos disponíveis: {len(styles)}")
print("=" * 70)
print("🌐 Abra o arquivo no navegador para visualizar o gráfico interativo.")