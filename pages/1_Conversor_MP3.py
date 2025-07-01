import streamlit as st
from moviepy.editor import VideoFileClip
import os

# --- Verificação de Autenticação ---
# Esta é a parte mais importante para proteger a página.
# Ele verifica o `session_state` que foi definido em `app.py`.
if not st.session_state.get("password_correct", False):
    st.error("Você não está autorizado a acessar esta página.")
    st.info("Por favor, faça o login na página principal para continuar.")
    st.stop() # Interrompe a execução da página se não estiver logado

# --- O restante do código do conversor permanece o mesmo ---

# --- Configuração da Página ---
st.set_page_config(
    page_title="Conversor MP4 para MP3",
    page_icon="🎵",
    layout="centered"
)

# --- Funções Auxiliares ---
def converter_mp4_para_mp3(arquivo_video_temporario, arquivo_audio_saida):
    """Converte um arquivo de vídeo (MP4) para um arquivo de áudio (MP3)."""
    try:
        video_clip = VideoFileClip(arquivo_video_temporario)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(arquivo_audio_saida, codec='mp3')
        audio_clip.close()
        video_clip.close()
        return True
    except Exception as e:
        st.error(f"Ocorreu um erro durante a conversão: {e}")
        return False

# --- Interface do Streamlit ---
st.title("Conversor de Mídias 🎵")
st.markdown("Faça o upload do seu arquivo de vídeo MP4 para extrair o áudio em formato MP3.")

uploaded_file = st.file_uploader(
    "Escolha um arquivo MP4",
    type=["mp4"],
    help="O limite de tamanho do arquivo é de 200MB no Streamlit Cloud."
)

if uploaded_file is not None:
    nome_base = os.path.splitext(uploaded_file.name)[0]
    arquivo_mp4_temp = f"temp_{nome_base}.mp4"
    arquivo_mp3_saida = f"{nome_base}.mp3"

    with open(arquivo_mp4_temp, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Arquivo MP4 carregado. Iniciando a conversão...")

    with st.spinner(f"Convertendo '{uploaded_file.name}' para MP3... Por favor, aguarde."):
        sucesso = converter_mp4_para_mp3(arquivo_mp4_temp, arquivo_mp3_saida)

    os.remove(arquivo_mp4_temp)

    if sucesso:
        st.success("Conversão concluída com sucesso!")
        
        st.markdown("### Ouça o resultado:")
        st.audio(arquivo_mp3_saida, format='audio/mp3')

        st.markdown("### Baixe seu arquivo MP3:")
        with open(arquivo_mp3_saida, "rb") as file:
            st.download_button(
                label="Baixar MP3",
                data=file,
                file_name=arquivo_mp3_saida,
                mime="audio/mp3"
            )
else:
    st.warning("Aguardando o upload de um arquivo MP4.")

