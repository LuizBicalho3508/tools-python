# app.py

import streamlit as st
import streamlit_authenticator as stauth
from moviepy.editor import VideoFileClip
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
# Define o título da página e o ícone que aparecem na aba do navegador
st.set_page_config(page_title="Kit de Ferramentas Online", page_icon="🛠️", layout="wide")

# --- AUTENTICAÇÃO ---
# Acessa as configurações de credenciais armazenadas no Streamlit Secrets
# Funciona tanto localmente (lendo .streamlit/secrets.toml) quanto na nuvem.
credentials = st.secrets.get('credentials', {})
cookie_config = st.secrets.get('cookie', {})
preauthorized_config = st.secrets.get('preauthorized', {})

# Inicializa o objeto de autenticação
authenticator = stauth.Authenticate(
    credentials,
    cookie_config.get('name', 'some_cookie_name'),
    cookie_config.get('key', 'some_signature_key'),
    cookie_config.get('expiry_days', 30),
    preauthorized_config
)

# --- PÁGINA DE LOGIN ---
st.title("Kit de Ferramentas Online 🛠️")
st.write("Por favor, faça o login para acessar as ferramentas.")

# Renderiza o widget de login e captura o resultado
name, authentication_status, username = authenticator.login(fields={'Form name': 'Login'})

# --- LÓGICA DE CONTROLE DE ACESSO ---

# Se o login for bem-sucedido
if authentication_status:
    # --- LAYOUT DA APLICAÇÃO PRINCIPAL ---
    # Adiciona um botão de logout na barra lateral
    with st.sidebar:
        st.title(f"Bem-vindo(a) ✨")
        st.write(f"*{name}*")
        authenticator.logout('Logout', 'main')

    st.header("Ferramentas Disponíveis")
    st.markdown("---")

    # --- FERRAMENTA 1: CONVERSOR DE MP4 PARA MP3 ---
    st.subheader("1. Conversor de MP4 para MP3")

    # Widget para upload de arquivo
    uploaded_file = st.file_uploader(
        "Carregue seu arquivo de vídeo (MP4)",
        type=["mp4"],
        help="Apenas arquivos no formato .mp4 são aceitos."
    )

    if uploaded_file is not None:
        # Define caminhos para os arquivos temporários
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir) # Cria a pasta temp se não existir

        temp_video_path = os.path.join(temp_dir, uploaded_file.name)
        mp3_output_path = os.path.join(temp_dir, f"{os.path.splitext(uploaded_file.name)[0]}.mp3")

        # Salva o arquivo carregado no disco temporariamente
        with open(temp_video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")

        # Botão para iniciar a conversão
        if st.button("Converter para MP3", key="convert_button"):
            # Mostra uma mensagem de "carregando" enquanto processa
            with st.spinner("Convertendo... Este processo pode demorar alguns minutos, por favor aguarde."):
                try:
                    # Carrega o clipe de vídeo usando moviepy
                    video_clip = VideoFileClip(temp_video_path)

                    # Extrai o áudio do clipe de vídeo
                    audio_clip = video_clip.audio

                    # Escreve o arquivo de áudio resultante (MP3)
                    audio_clip.write_audiofile(mp3_output_path)

                    # Fecha os clipes para liberar recursos do sistema
                    audio_clip.close()
                    video_clip.close()

                    st.success("Conversão concluída com sucesso!")

                    # Oferece o arquivo MP3 para download
                    with open(mp3_output_path, "rb") as f:
                        st.download_button(
                            label="Clique para baixar o arquivo MP3",
                            data=f,
                            file_name=os.path.basename(mp3_output_path),
                            mime="audio/mpeg"
                        )

                except Exception as e:
                    st.error(f"Ocorreu um erro durante a conversão: {e}")

                finally:
                    # Limpeza: remove os arquivos temporários após a tentativa de conversão
                    if os.path.exists(temp_video_path):
                        os.remove(temp_video_path)
                    if os.path.exists(mp3_output_path):
                        os.remove(mp3_output_path)


# Se a senha/usuário estiverem incorretos
elif authentication_status is False:
    st.error('Usuário ou senha incorreto(a). Por favor, tente novamente.')

# Se nenhum input foi dado ainda (estado inicial)
elif authentication_status is None:
    st.warning('Por favor, digite seu usuário e senha para continuar.')
