import streamlit as st
import uuid

# --- Configuração da Página (deve ser o primeiro comando Streamlit) ---
# Esta configuração é válida para todas as páginas.
st.set_page_config(
    page_title="Login - Ferramentas",
    page_icon="🔐",
    layout="centered"
)

# --- Inicialização do Estado da Sessão ---
# Garante que as chaves necessárias existam desde o início para evitar erros.
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# --- Função de Autenticação com Formulário ---
def check_password():
    """Retorna `True` se o usuário estiver logado, `False` caso contrário."""

    # Se o usuário já está logado, retorna True.
    if st.session_state.get("password_correct", False):
        return True

    # Se não, mostra o formulário de login.
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjY3h-b5z9-mI4gV2Qc-Z-Q2A1b-g8XJd&s", width=150)
    st.title("Área Restrita")
    st.markdown("---")

    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            # Busca as credenciais do arquivo secrets (local ou no Streamlit Cloud)
            correct_username = st.secrets["credentials"]["username"]
            correct_password = st.secrets["credentials"]["password"]

            # Verifica se as credenciais estão corretas
            if username == correct_username and password == correct_password:
                st.session_state["password_correct"] = True
                st.session_state["username"] = username
                st.rerun() # Recarrega a página para refletir o estado de login
            else:
                st.error("😕 Usuário ou senha incorretos.")
    
    return False

# --- Execução Principal ---
if check_password():
    # --- Interface Pós-Login ---
    # Mostra status e botão de logout na barra lateral
    st.sidebar.success(f"Logado como: {st.session_state['username']}")
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.session_state["username"] = ""
        st.rerun()

    # Conteúdo da página principal após login
    st.title("Bem-vindo ao Painel de Ferramentas! 👋")
    st.markdown("---")
    st.write("Use a barra lateral à esquerda para navegar entre as ferramentas disponíveis.")
    st.info("Você está logado. Todas as ferramentas estão agora acessíveis.")
else:
    # --- Interface Pré-Login ---
    # Esconde a barra lateral de navegação de páginas se não estiver logado
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )
