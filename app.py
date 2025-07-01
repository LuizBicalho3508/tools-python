import streamlit as st

# --- Configuração da Página ---
st.set_page_config(
    page_title="Login - Ferramentas Defecon",
    page_icon="🔐",
    layout="centered"
)

# --- Função de Autenticação ---
def check_password():
    """Retorna `True` se o usuário inseriu a senha correta."""

    def password_entered():
        """Verifica se a senha inserida pelo usuário corresponde à senha correta."""
        if st.session_state["password"] == st.secrets["credentials"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Não guardar a senha na session state
        else:
            st.session_state["password_correct"] = False

    # --- Lógica de Exibição do Login ---
    # Se a senha ainda não foi validada, mostra os campos de login
    if not st.session_state.get("password_correct", False):
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjY3h-b5z9-mI4gV2Qc-Z-Q2A1b-g8XJd&s", width=150) # Exemplo de logo
        st.title("Área Restrita - Ferramentas Defecon")
        st.markdown("---")
        
        # Inputs para usuário e senha
        st.text_input("Usuário", key="username")
        st.text_input(
            "Senha", type="password", on_change=password_entered, key="password"
        )
        
        # Mensagem de erro se a senha estiver errada
        if "password_correct" in st.session_state and not st.session_state.password_correct:
            st.error("😕 Usuário ou senha incorretos.")
        
        return False
        
    # Se a senha foi validada, retorna True
    else:
        # Validação extra para o nome de usuário
        if st.session_state.get("username") == st.secrets["credentials"]["username"]:
            return True
        else:
            # Se o usuário estiver errado, reseta a autenticação
            st.session_state["password_correct"] = False
            st.error("😕 Usuário ou senha incorretos.")
            st.rerun() # Força a recarga para mostrar o formulário de login novamente
            return False


# --- Execução Principal ---
if check_password():
    st.sidebar.success("Login realizado com sucesso!")
    st.sidebar.markdown("---")
    
    # Botão de Logout na barra lateral
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.session_state["username"] = "" # Limpa o nome de usuário
        st.rerun()

    # Conteúdo da página principal após o login
    st.title("Bem-vindo ao Painel de Ferramentas! 👋")
    st.markdown("---")
    st.write("Use a barra lateral à esquerda para navegar entre as ferramentas disponíveis.")
    st.info("Você está logado. Todas as ferramentas estão agora acessíveis.")

