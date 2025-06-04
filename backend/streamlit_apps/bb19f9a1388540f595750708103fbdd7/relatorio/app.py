import streamlit as st

# Define o título da aplicação
st.title("Olá, Marley! 👋")

# Adiciona um campo de entrada de texto
user_name = st.text_input("Qual é o seu nome?", "Marley")

# Adiciona um botão
if st.button("Diga Olá"):
    st.write(f"Olá, {user_name}! Bem-vindo ao seu primeiro aplicativo Streamlit.")
    st.balloons() # Efeito de balões para celebrar!

# Adiciona um slider para um número
number = st.slider("Escolha um número", 0, 100, 50)
st.write(f"Você escolheu: {number}")

# Adiciona uma caixa de seleção
if st.checkbox("Mostrar mensagem secreta"):
    st.write("Esta é uma mensagem secreta! 🤫")

# Adiciona um seletor de rádio
option = st.radio(
    "Qual a sua fruta favorita?",
    ("Maçã", "Banana", "Laranja")
)
st.write(f"Sua fruta favorita é: {option}")

# Adiciona um campo para upload de arquivo
uploaded_file = st.file_uploader("Faça upload de um arquivo de texto")
if uploaded_file is not None:
    # Para ler o arquivo como string:
    string_data = uploaded_file.getvalue().decode("utf-8")
    st.write("Conteúdo do arquivo:")
    st.text(string_data)

# Informações sobre como executar o aplicativo
st.markdown(
    """
    ### Como executar este aplicativo:
    1. Salve o código acima em um arquivo chamado `app.py`.
    2. Abra seu terminal ou prompt de comando.
    3. Navegue até o diretório onde você salvou o arquivo.
    4. Execute o comando: `streamlit run app.py`
    5. O aplicativo será aberto automaticamente no seu navegador.
    """
)
