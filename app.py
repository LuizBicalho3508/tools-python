# app.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- CONFIGURAÇÃO DE AUTENTICAÇÃO ---

# Carregando a configuração do st.secrets
# st.secrets lê o arquivo secrets.toml localmente ou os segredos na nuvem
with open('.streamlit/secrets.toml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# --- PÁGINA DE LOGIN ---
st.title("Kit de Ferramentas Online 🛠️")

# O método login() renderiza os campos de email/senha
name, authentication_status, username = authenticator.login('main')

# --- LÓGICA PÓS-LOGIN ---

if authentication_status:
    # Mostra o botão de logout na barra lateral
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.title(f"Bem-vindo(a) ✨, {name}!")

    # --- AQUI COMEÇA O ACESSO ÀS FERRAMENTAS ---
    st.header("Ferramentas Disponíveis")
    # Adicionaremos a ferramenta de conversão aqui

elif authentication_status is False:
    st.error('E-mail/senha incorreto(a)')
elif authentication_status is None:
    st.warning('Por favor, digite seu e-mail e senha')
