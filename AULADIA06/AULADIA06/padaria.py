import streamlit as st
import pandas as pd

st.write("Sistema da Padaria")
st.header("Padaria Pão Quentinho")
st.subheader("Escolha seus itens favoritos!")
st.write("Olá, seja bem-vindo!")

cardapio = pd.DataFrame({
    "Item": ["Pão Francês", "Pão de Queijo", "Bolo de Cenoura", "Café", "Sonho", "Coxinha"],
    "Preço (R$)": [0.80, 3.50, 6.00, 4.00, 5.50, 7.00]
})

st.write(cardapio)


precos = dict(zip(cardapio["Item"], cardapio["Preço (R$)"]))


itens = st.multiselect("Escolha os itens:", list(precos.keys()))


num1, num2 = st.columns([1, 1])
num1.title("Total")


with st.form("pedido"):
    quantidades = {}
    for item in itens:
        quantidades[item] = st.number_input(f"Quantidade de {item}", min_value=0, value=1, step=1)
    submit = st.form_submit_button("Calcular total")

if submit:
    total = sum(precos[item] * qtd for item, qtd in quantidades.items())
    num2.title(f"R$ {total:.2f}")

    resumo = pd.DataFrame({
        "Item": list(quantidades.keys()),
        "Quantidade": list(quantidades.values()),
        "Subtotal (R$)": [precos[i] * q for i, q in quantidades.items()]
    })
    st.subheader("Resumo do pedido")
    st.write(resumo)