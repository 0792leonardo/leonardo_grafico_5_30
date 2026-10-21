# Gráfico 5.30 — CO

Gráfico interativo em Python + Plotly baseado no CSV fornecido.

## Formato do CSV

- Separador de campos: `;`
- Separador decimal: `,`
- Campo das estações: `estacao`
- Anos disponíveis no CSV: 2007–2025
- Período exibido no gráfico: **2016–2025**, conforme a imagem de referência.

O CSV original é mantido no pacote.

## Visual

- Eixo Y: 0–3 ppm
- Intervalos: 1 ppm
- Rótulos do eixo Y: `0,0`, `1,0`, `2,0`, `3,0`
- Tooltip com valores em vírgula decimal
- Uma série por estação
- Marcadores diferenciados
- Fundo `#DDE9F4`
- Grade horizontal pontilhada
- Legenda horizontal
- Valores ausentes permanecem como lacunas
- HTML autocontido para GitHub Pages

## Gerar

```bash
pip install pandas plotly
python gerar_grafico.py
```

## Publicar

```bash
git init
git add .
git commit -m "Adicionar grafico 5.30 CO"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:
**Settings → Pages → Build and deployment → Source → GitHub Actions**
