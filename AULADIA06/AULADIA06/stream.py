import streamlit as st

st.write("Meu primeiro dashboard")
st.header("Turma 3C2")
st.subheader("Turma bagunceira que amo!")
st.write("Olá, mundo!")

alunos = "Pedro Var"

notas = pd.DataFrame({"Disciplina": ["Portugues", "Matematica","Python"], "notas":[1,5,19]})


notificacoes = st.multiselect("Escolha os alunos:", ["Matheus", "Marçal"])

num1, num2 = st.columns([1,1])

num1.title("Soma")

with st.form('addition'):
    a = st.number_input('a')
    b = st.number_input('b')

if submit:
    num2.title(f'{a+b:.2f}')