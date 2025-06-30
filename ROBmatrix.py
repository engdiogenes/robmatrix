import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="ROBmatrix - Comprar ou Reparar", layout="centered")

# Sidebar com descrição institucional
with st.sidebar:
    st.title("🤖 ROBmatrix")
    st.markdown("""
    **Sistema de Apoio à Decisão para Engenharia de Manutenção**

    **Objetivo:**  
    Auxiliar na tomada de decisão entre comprar ou reparar um componente com base em critérios técnicos e financeiros.

    **Usabilidade:**  
    - Preencha os dados de custo, tempo e criticidade.  
    - Obtenha diagnóstico automático com gráficos explicativos.

    **Fundamentação Teórica:**  
    Baseado em princípios de Engenharia de Manutenção, RCM (Reliability-Centered Maintenance) e análise multicritério.

    **Créditos:**  
    Desenvolvido por **Diógenes Oliveira**  
    Engenheiro de Manutenção
    """)

# Inicializar variáveis na session_state se não existirem
if "resultado" not in st.session_state:
    st.session_state.resultado = None
    st.session_state.graficos = None

# Criação das abas superiores
aba1, aba2 = st.tabs(["🧮 Formulário de Decisão", "📚 Referencial Teórico"])

with aba1:
    st.header("🔧 Diagnóstico Técnico: Comprar ou Reparar")

    col1, col2 = st.columns(2)
    with col1:
        custo_reparo = st.number_input("Custo do Reparo (R$)", min_value=0.0, format="%.2f")
        tempo_reparo = st.number_input("Tempo de Reparo (em dias)", min_value=0.01)
        criticidade = st.selectbox("Criticidade Operacional", ["Baixa", "Média", "Alta"])
    with col2:
        custo_novo = st.number_input("Custo da Peça Nova (R$)", min_value=0.01, format="%.2f")
        tempo_permitido = st.number_input("Tempo de Parada Permitido (em dias)", min_value=0.0)

    if st.button("📊 Analisar Decisão"):
        # Cálculos principais
        indice_custo = (custo_reparo / custo_novo) * 100 if custo_novo > 0 else 999
        if indice_custo <= 30: pont_custo = 5
        elif indice_custo <= 50: pont_custo = 4
        elif indice_custo <= 70: pont_custo = 3
        elif indice_custo <= 90: pont_custo = 2
        else: pont_custo = 1

        if tempo_permitido == 0:
            percentual_tempo = float("inf")
            pont_tempo = 1
        else:
            percentual_tempo = (tempo_reparo / tempo_permitido) * 100
            if percentual_tempo <= 50: pont_tempo = 5
            elif percentual_tempo <= 80: pont_tempo = 4
            elif percentual_tempo <= 100: pont_tempo = 3
            elif percentual_tempo <= 150: pont_tempo = 2
            else: pont_tempo = 1

        pont_crit = {"Baixa": 5, "Média": 3, "Alta": 1}[criticidade]
        score = pont_custo * 0.4 + pont_tempo * 0.3 + pont_crit * 0.3

        # Diagnóstico
        if score >= 4.5:
            decisao = "✅ Excelente cenário para REPARO."
        elif score >= 4.0:
            decisao = "ℹ️ Reparo recomendado com atenção."
        elif score >= 3.0:
            decisao = "⚠️ Tendência à COMPRA. Avaliar riscos."
        else:
            decisao = "❌ Recomendado: COMPRAR NOVO."

        # Salva resultados para uso em outras abas
        st.session_state.resultado = {
            "indice_custo": indice_custo,
            "percentual_tempo": percentual_tempo,
            "pont_custo": pont_custo,
            "pont_tempo": pont_tempo,
            "pont_crit": pont_crit,
            "criticidade": criticidade,
            "score": score,
            "decisao": decisao
        }

        # Gráficos
        fig = go.Figure(data=[
            go.Bar(x=["Custo", "Tempo", "Criticidade"], y=[pont_custo, pont_tempo, pont_crit], marker_color="darkcyan")
        ])
        fig.update_layout(title="Pontuação por Critério", yaxis=dict(range=[0, 5]), height=400)

        comparativo = pd.DataFrame({"Pontuação": [score, 5 - score]}, index=["Reparar", "Comprar"])

        st.session_state.graficos = (fig, comparativo)

    # Exibição de resultados salvos
    if st.session_state.resultado:
        r = st.session_state.resultado
        st.subheader("🧾 Explicação do Diagnóstico")
        st.markdown(f"- 💰 **Índice de Custo** = {r['indice_custo']:.1f}% → Pontuação: {r['pont_custo']}")
        if tempo_permitido == 0:
            st.markdown("- ⏱️ **Tempo permitido = 0 dias** → Tolerância zero → Pontuação: 1")
        else:
            st.markdown(f"- ⏱️ **Índice de Tempo** = {r['percentual_tempo']:.1f}% → Pontuação: {r['pont_tempo']}")
        st.markdown(f"- ⚙️ **Criticidade** = {r['criticidade']} → Pontuação: {r['pont_crit']}")
        st.markdown(f"### 📊 Score Final = `{r['score']:.2f}`")

        st.info(r['decisao'])

        st.subheader("📈 Gráfico por Critério")
        st.plotly_chart(st.session_state.graficos[0])

        st.subheader("🔍 Comparativo Visual")
        st.bar_chart(st.session_state.graficos[1])

with aba2:
    st.title("📚 Referencial Teórico")
    st.markdown("""
### 🎯 Objetivo da Metodologia

Ajudar na decisão entre **comprar ou reparar** um item de manutenção com base em critérios técnicos e financeiros aplicados pela Engenharia de Manutenção.

---

### 📐 Critérios Utilizados

1. **Índice de Custo (%)**  
$$ \\frac{\\text{Custo do Reparo}}{\\text{Custo da Peça Nova}} \\times 100 $$

2. **Índice de Tempo (%)**  
$$ \\frac{\\text{Tempo de Reparo}}{\\text{Tempo Permitido}} \\times 100 $$

3. **Criticidade Operacional**  
Pontuação definida pela importância da peça no processo produtivo

---

### 🧮 Score Final

$$ \\text{Score Final} = (Custo \\times 0{,}4) + (Tempo \\times 0{,}3) + (Criticidade \\times 0{,}3) $$

---

### 📌 Interpretação dos Resultados

| Score        | Diagnóstico                     |
|--------------|----------------------------------|
| ≥ 4.5        | ✅ Reparo altamente recomendado   |
| 4.0 – 4.4    | ℹ️ Reparo possível com cautela    |
| 3.0 – 3.9    | ⚠️ Tendência à Compra             |
| < 3.0        | ❌ Recomenda-se Compra da peça nova|

---

### 🔍 Fundamentação

A metodologia segue os princípios de:
- **Manutenção Centrada em Confiabilidade (RCM)**
- **Análise Multicritério**
- **Gestão de Ativos Industriais**

É uma abordagem prática e adaptável para ajudar engenheiros, analistas e supervisores a tomar decisões rápidas, justificáveis e padronizadas em campo.
    """)
