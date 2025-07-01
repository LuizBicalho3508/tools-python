import streamlit as st
from moviepy.editor import VideoFileClip
import os

# --- Configuração da Página ---
st.set_page_config(
    page_title="Conversor MP4 para MP3",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- Funções Auxiliares ---

def converter_mp4_para_mp3(arquivo_video_temporario, arquivo_audio_saida):
    """
    Converte um arquivo de vídeo (MP4) para um arquivo de áudio (MP3).

    Args:
        arquivo_video_temporario (str): O caminho para o arquivo de vídeo MP4 salvo temporariamente.
        arquivo_audio_saida (str): O caminho onde o arquivo MP3 será salvo.
    
    Returns:
        bool: True se a conversão for bem-sucedida, False caso contrário.
    """
    try:
        # Carrega o clipe de vídeo
        video_clip = VideoFileClip(arquivo_video_temporario)
        
        # Extrai o áudio do clipe
        audio_clip = video_clip.audio
        
        # Escreve o arquivo de áudio
        audio_clip.write_audiofile(arquivo_audio_saida, codec='mp3')
        
        # Libera os recursos
        audio_clip.close()
        video_clip.close()
        
        return True
    except Exception as e:
        st.error(f"Ocorreu um erro durante a conversão: {e}")
        return False

# --- Interface do Streamlit ---

st.title(" conversor de midias🎵")
st.markdown("Faça o upload do seu arquivo de vídeo MP4 para extrair o áudio em formato MP3.")

# Widget para upload de arquivo
uploaded_file = st.file_uploader(
    "Escolha um arquivo MP4",
    type=["mp4"],
    help="O limite de tamanho do arquivo é de 200MB no Streamlit Cloud."
)

if uploaded_file is not None:
    # Define os nomes dos arquivos temporários
    nome_base = os.path.splitext(uploaded_file.name)[0]
    arquivo_mp4_temp = f"temp_{nome_base}.mp4"
    arquivo_mp3_saida = f"{nome_base}.mp3"

    # Salva o arquivo carregado em disco temporariamente para que o moviepy possa processá-lo
    with open(arquivo_mp4_temp, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Arquivo MP4 carregado. Iniciando a conversão...")

    # Bloco de processamento com spinner
    with st.spinner(f"Convertendo '{uploaded_file.name}' para MP3... Por favor, aguarde."):
        sucesso = converter_mp4_para_mp3(arquivo_mp4_temp, arquivo_mp3_saida)

    # Limpa o arquivo de vídeo temporário após a conversão
    os.remove(arquivo_mp4_temp)

    if sucesso:
        st.success("Conversão concluída com sucesso!")
        
        # Exibe o player de áudio
        st.markdown("### Ouça o resultado:")
        st.audio(arquivo_mp3_saida, format='audio/mp3')

        # Oferece o botão de download
        st.markdown("### Baixe seu arquivo MP3:")
        with open(arquivo_mp3_saida, "rb") as file:
            st.download_button(
                label="Baixar MP3",
                data=file,
                file_name=arquivo_mp3_saida,
                mime="audio/mp3"
            )
        
        # Limpa o arquivo de áudio gerado após o download (opcional, mas bom para gerenciamento de espaço)
        # st.info("O arquivo será removido do servidor após o download.")
        # No Streamlit Cloud, o sistema de arquivos é efêmero, então a limpeza manual nem sempre é crítica.

else:
    st.warning("Aguardando o upload de um arquivo MP4.")
