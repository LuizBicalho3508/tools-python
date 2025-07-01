import streamlit as st
from moviepy.editor import VideoFileClip
import os

# --- Verificação de Autenticação ---
# A primeira coisa a fazer em qualquer página protegida.
if not st.session_state.get("password_correct", False):
    st.error("Você não está autorizado a acessar esta página.")
    st.info("Por favor, faça o login na página principal para continuar.")
    st.stop() # Interrompe a execução se não estiver logado

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
    # Usa o ID da sessão para criar nomes de arquivo únicos
    nome_base = os.path.splitext(uploaded_file.name)[0]
    session_id = st.session_state.session_id
    temp_dir = "temp_files"
    
    # Cria um diretório temporário se não existir
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    arquivo_mp4_temp = os.path.join(temp_dir, f"temp_{nome_base}_{session_id}.mp4")
    arquivo_mp3_saida = os.path.join(temp_dir, f"{nome_base}_{session_id}.mp3")

    with open(arquivo_mp4_temp, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info(f"Arquivo '{uploaded_file.name}' carregado. Iniciando a conversão...")

    with st.spinner("Convertendo... Por favor, aguarde."):
        sucesso = converter_mp4_para_mp3(arquivo_mp4_temp, arquivo_mp3_saida)

    # Limpa o arquivo de vídeo temporário
    if os.path.exists(arquivo_mp4_temp):
        os.remove(arquivo_mp4_temp)

    if sucesso and os.path.exists(arquivo_mp3_saida):
        st.success("Conversão concluída com sucesso!")
        
        st.markdown("### Ouça o resultado:")
        st.audio(arquivo_mp3_saida, format='audio/mp3')

        st.markdown("### Baixe seu arquivo MP3:")
        with open(arquivo_mp3_saida, "rb") as file:
            st.download_button(
                label="Baixar MP3",
                data=file,
                # Oferece um nome de arquivo limpo para o usuário
                file_name=f"{nome_base}.mp3",
                mime="audio/mp3"
            )
else:
    st.warning("Aguardando o upload de um arquivo MP4.")
