import streamlit as st

# --- Configuração da Página ---
st.set_page_config(
    page_title="Login - Ferramentas",
    page_icon="🔐",
    layout="centered"
)

# --- Função de Autenticação com Formulário e Botão ---
def check_password():
    """Retorna `True` se o usuário estiver logado, `False` caso contrário."""

    # Se o usuário já está logado, retorna True diretamente.
    if st.session_state.get("password_correct", False):
        return True

    # Se não está logado, mostra o formulário de login.
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjY3h-b5z9-mI4gV2Qc-Z-Q2A1b-g8XJd&s", width=150)
    st.title("Área Restrita - Ferramentas")
    st.markdown("---")

    # Usa um formulário para o login
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        # O botão de login agora é um botão de submissão do formulário
        submitted = st.form_submit_button("Login")

        if submitted:
            # Verifica as credenciais APENAS quando o botão é clicado
            correct_username = st.secrets["credentials"]["username"]
            correct_password = st.secrets["credentials"]["password"]

            if username == correct_username and password == correct_password:
                st.session_state["password_correct"] = True
                st.session_state["username"] = username  # Armazena o nome de usuário
                st.rerun()  # Recarrega a página para refletir o estado de login
            else:
                st.error("😕 Usuário ou senha incorretos.")
    
    return False

# --- Execução Principal ---
if check_password():
    # Mostra o status de login e o botão de logout na barra lateral
    st.sidebar.success(f"Logado como: {st.session_state['username']}")
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        # Limpa o estado da sessão para fazer logout
        st.session_state["password_correct"] = False
        st.session_state["username"] = ""
        st.rerun()

    # Conteúdo da página principal após o login bem-sucedido
    st.title("Bem-vindo ao Painel de Ferramentas! 👋")
    st.markdown("---")
    st.write("Use a barra lateral à esquerda para navegar entre as ferramentas disponíveis.")
    st.info("Você está logado. Todas as ferramentas estão agora acessíveis.")

