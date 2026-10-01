# %%
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

np.random.seed(42)


def gerar_dataset_ficticio(caminho="vendas.csv", n=2000):
    lojas = {
        "Loja Centro": "Sudeste",
        "Loja Savassi": "Sudeste",
        "Loja Norte Shopping": "Norte",
        "Loja Sul Plaza": "Sul",
        "Loja Nordeste Mall": "Nordeste",
    }
    produtos = {
        "Notebook": ("Eletrônicos", 3500),
        "Smartphone": ("Eletrônicos", 2200),
        "Fone Bluetooth": ("Eletrônicos", 250),
        "Camiseta": ("Vestuário", 60),
        "Calça Jeans": ("Vestuário", 140),
        "Tênis": ("Vestuário", 320),
        "Cafeteira": ("Casa", 210),
        "Liquidificador": ("Casa", 130),
        "Panela de Pressão": ("Casa", 95),
        "Mochila": ("Acessórios", 150),
        "Relógio": ("Acessórios", 480),
    }
    datas = pd.to_datetime(
        np.random.choice(pd.date_range("2025-01-01", "2025-12-31"), n)
    )
    loja = np.random.choice(list(lojas), n, p=[0.30, 0.25, 0.15, 0.18, 0.12])
    produto = np.random.choice(list(produtos), n)
    df = pd.DataFrame(
        {
            "data": datas,
            "loja": loja,
            "regiao": [lojas[l] for l in loja],
            "produto": produto,
            "categoria": [produtos[p][0] for p in produto],
            "quantidade": np.random.randint(1, 8, n).astype(float),
            "preco_unitario": [
                round(produtos[p][1] * np.random.uniform(0.85, 1.15), 2)
                for p in produto
            ],
        }
    ).sort_values("data")
    idx_q = np.random.choice(df.index, 40, replace=False)
    idx_p = np.random.choice(df.index, 40, replace=False)
    df.loc[idx_q, "quantidade"] = np.nan
    df.loc[idx_p, "preco_unitario"] = np.nan
    df.to_csv(caminho, index=False)


if not os.path.exists("vendas.csv"):
    gerar_dataset_ficticio()

df = pd.read_csv("vendas.csv")
df["data"] = pd.to_datetime(df["data"])
df.head()

df["faturamento"] = df["quantidade"] * df["preco_unitario"]
df.head()

print("=== .info() ===")
df.info()

print("\n=== Valores ausentes (.isnull().sum()) ===")
print(df.isnull().sum())

print("\n=== Resumo estatístico (.describe()) ===")
print(df.describe())

df["preco_unitario"] = df["preco_unitario"].fillna(df["preco_unitario"].mean())
df["quantidade"] = df["quantidade"].fillna(df["quantidade"].mean())

df["faturamento"] = df["quantidade"] * df["preco_unitario"]

print("Nulos restantes:\n", df.isnull().sum())

fat_loja = (
    df.groupby("loja")["faturamento"].sum().sort_values(ascending=False)
)
print(fat_loja.round(2))

ticket_medio = (
    df.groupby("loja")["faturamento"].sum() / df.groupby("loja").size()
).sort_values(ascending=False)
print(ticket_medio.round(2))

top5_produtos = (
    df.groupby("produto")["quantidade"].sum().sort_values(ascending=False).head(5)
)
print(top5_produtos)

fat_mensal = df.groupby(df["data"].dt.to_period("M"))["faturamento"].sum()

mes_max = fat_mensal.idxmax().strftime("%m/%Y")
mes_min = fat_mensal.idxmin().strftime("%m/%Y")
print(f"Maior faturamento: {mes_max} (R$ {fat_mensal.max():,.2f})")
print(f"Menor faturamento: {mes_min} (R$ {fat_mensal.min():,.2f})")

df["mes"] = df["data"].dt.month
df.head()

sns.set_style("whitegrid")
sns.set_palette(sns.color_palette("deep"))
paleta = sns.color_palette("deep")

os.makedirs("graficos", exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 6))
barras = ax.bar(fat_loja.index, fat_loja.values, color=paleta[: len(fat_loja)],
                label="Faturamento total")
ax.set_title("Faturamento Total por Loja em 2025")
ax.set_xlabel("Loja")
ax.set_ylabel("Faturamento (R$)")
ax.bar_label(barras, labels=[f"R$ {v:,.0f}" for v in fat_loja.values], padding=3)
ax.legend()
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("graficos/faturamento_por_loja.png", dpi=150)
plt.show()

resumo_mensal = df.groupby("mes")["faturamento"].sum()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(resumo_mensal.index, resumo_mensal.values, marker="o",
        color=paleta[0], label="Faturamento mensal")
for x, y in zip(resumo_mensal.index, resumo_mensal.values):
    ax.annotate(f"{y/1000:,.0f}k", (x, y), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=9)
ax.set_xticks(range(1, 13))
ax.set_title("Evolução Mensal do Faturamento em 2025")
ax.set_xlabel("Mês")
ax.set_ylabel("Faturamento (R$)")
ax.legend()
plt.tight_layout()
plt.savefig("graficos/evolucao_mensal.png", dpi=150)
plt.show()

fat_regiao = df.groupby("regiao")["faturamento"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(fat_regiao.values, labels=fat_regiao.index, autopct="%1.1f%%",
       startangle=90, colors=paleta[: len(fat_regiao)],
       wedgeprops={"edgecolor": "white"})
ax.set_title("Distribuição do Faturamento por Região")
plt.tight_layout()
plt.savefig("graficos/faturamento_por_regiao.png", dpi=150)
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x="quantidade", y="faturamento", hue="categoria", ax=ax)
ax.set_title("Relação entre Quantidade Vendida e Faturamento por Categoria")
ax.set_xlabel("Quantidade de itens vendidos")
ax.set_ylabel("Faturamento (R$)")
ax.legend(title="Categoria")
plt.tight_layout()
plt.savefig("graficos/dispersao_quantidade_faturamento.png", dpi=150)
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x="categoria", y="preco_unitario", hue="categoria",
            palette="deep", legend=False, ax=ax)
ax.set_title("Variação do Preço Unitário por Categoria de Produto")
ax.set_xlabel("Categoria")
ax.set_ylabel("Preço unitário (R$)")
handles = [plt.Rectangle((0, 0), 1, 1, color=paleta[i])
           for i in range(df["categoria"].nunique())]
ax.legend(handles, sorted(df["categoria"].unique()), title="Categoria")
plt.tight_layout()
plt.savefig("graficos/boxplot_preco_por_categoria.png", dpi=150)
plt.show()

corr = df[["quantidade", "preco_unitario", "faturamento", "mes"]].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
ax.set_title("Matriz de Correlação das Variáveis Numéricas")
plt.tight_layout()
plt.savefig("graficos/heatmap_correlacao.png", dpi=150)
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].bar(fat_loja.index, fat_loja.values, color=paleta[: len(fat_loja)])
axes[0].set_title("Faturamento Total por Loja")
axes[0].set_xlabel("Loja")
axes[0].set_ylabel("Faturamento (R$)")
axes[0].tick_params(axis="x", rotation=25)

axes[1].bar(fat_regiao.index, fat_regiao.values, color=paleta[: len(fat_regiao)])
axes[1].set_title("Faturamento Total por Região")
axes[1].set_xlabel("Região")
axes[1].set_ylabel("Faturamento (R$)")

fig.suptitle("Comparativo de Faturamento: Loja x Região", fontsize=15)
plt.tight_layout()
plt.savefig("graficos/painel_loja_regiao.png", dpi=150)
plt.show()

resumo_analitico = pd.DataFrame(
    {
        "faturamento_total": fat_loja,
        "ticket_medio": ticket_medio,
        "quantidade_total": df.groupby("loja")["quantidade"].sum(),
    }
).sort_values("faturamento_total", ascending=False).round(2)
resumo_analitico.index.name = "loja"
resumo_analitico.to_csv("resumo_analitico.csv")
print(resumo_analitico)

print("Arquivos gerados:", sorted(os.listdir("graficos")))

# COMENTÁRIO FINAL — O QUE FOI OBSERVADO NAS VISUALIZAÇÕES
# - O gráfico de barras mostra a Loja Centro liderando o faturamento
#   (cerca de R$ 1,59 milhão), enquanto a Loja Nordeste Mall tem o menor
#   (cerca de R$ 596 mil).
# - No gráfico de pizza, a região Sudeste concentra cerca de 56,5% de todo o
#   faturamento, bem à frente das demais regiões.
# - A Loja Savassi tem o maior ticket médio (R$ 2.871,57), mesmo não sendo a
#   que mais fatura: cada venda dela tem valor mais alto.
# - No gráfico de linhas, janeiro/2025 foi o mês de maior faturamento e
#   março/2025 o de menor.
# - No gráfico de dispersão, a quantidade vendida explica pouco o faturamento;
#   os pontos mais altos (outliers) vêm de produtos caros, como eletrônicos.
# - O heatmap confirma isso: correlação de 0,87 entre preço unitário e
#   faturamento, contra apenas 0,28 entre quantidade e faturamento.
# - No boxplot, Eletrônicos tem o maior preço mediano e a maior variação de
#   preços entre as categorias.
# - O produto mais vendido em quantidade foi a Cafeteira (cerca de 842
#   unidades), seguida por Tênis e Camiseta.
