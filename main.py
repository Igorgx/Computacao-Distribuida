import random
import math
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def disponibilidade_analitica(n, k, p):

    soma = 0

    for i in range(k, n + 1):
        soma += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))

    return soma

def simulacao(n, k, p, rodadas=10000):

    sucesso = 0

    for _ in range(rodadas):

        ativos = 0

        for _ in range(n):

            if random.random() < p:
                ativos += 1

        if ativos >= k:
            sucesso += 1

    return sucesso / rodadas


st.title("Simulador de Disponibilidade de Serviços Replicados")

st.sidebar.header("Parâmetros")

valores_n = st.sidebar.multiselect("Escolha valores de n", [3,5,10], default=[5])
p_values = [i/10 for i in range(11)]

resultados = []

for n in valores_n:

    valores_k = [1, math.ceil(n/2), n]

    for k in valores_k:

        for p in p_values:

            analitico = disponibilidade_analitica(n,k,p)
            sim = simulacao(n,k,p)

            resultados.append([n,k,p,analitico,sim])


df = pd.DataFrame(resultados, columns=["n","k","p","Analitico","Simulacao"])


st.subheader("Tabela de Resultados")

st.dataframe(df)


#Gráficos

st.subheader("Gráfico de Disponibilidade")

sns.set(style="whitegrid")

fig, ax = plt.subplots()

for n in valores_n:

    subset_n = df[df["n"] == n]

    for k in subset_n["k"].unique():

        subset = subset_n[subset_n["k"] == k]

        ax.plot(
            subset["p"],
            subset["Analitico"],
            marker="o",
            label=f"n={n}, k={k}"
        )

ax.set_xlabel("Probabilidade de servidor disponível (p)")
ax.set_ylabel("Disponibilidade do serviço")
ax.legend()

st.pyplot(fig)