import streamlit as st
from pydub import AudioSegment
import os

# --- Verificação de Autenticação ---
if not st.session_state.get("password_correct", False):
    st.error("Você não está autorizado a acessar esta página.")
    st.info("Por favor, faça o login na página principal para continuar.")
    st.stop()

# --- Funções Auxiliares com a nova biblioteca (pydub) ---
def converter_com_pydub(arquivo_video_temporario, arquivo_audio_saida):
    """Converte um arquivo de vídeo para áudio MP3 usando pydub."""
    try:
        # Carrega o arquivo de vídeo e extrai o áudio
        audio = AudioSegment.from_file(arquivo_video_temporario, format="mp4")
        
        # Exporta o áudio para o formato MP3
        audio.export(arquivo_audio_saida, format="mp3")
        
        return True
    except Exception as e:
        # Pydub pode dar um erro mais genérico se o ffmpeg não for encontrado
        st.error(f"Ocorreu um erro durante a conversão: {e}")
        st.warning("Certifique-se de que o arquivo 'packages.txt' com 'ffmpeg' existe no seu repositório.")
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
    session_id = st.session_state.session_id
    temp_dir = "temp_files"
    
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    arquivo_mp4_temp = os.path.join(temp_dir, f"temp_{nome_base}_{session_id}.mp4")
    arquivo_mp3_saida = os.path.join(temp_dir, f"{nome_base}_{session_id}.mp3")

    with open(arquivo_mp4_temp, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info(f"Arquivo '{uploaded_file.name}' carregado. Iniciando a conversão...")

    with st.spinner("Convertendo com a nova abordagem... Por favor, aguarde."):
        sucesso = converter_com_pydub(arquivo_mp4_temp, arquivo_mp3_saida)

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
                file_name=f"{nome_base}.mp3",
                mime="audio/mp3"
            )
else:
    st.warning("Aguardando o upload de um arquivo MP4.")
