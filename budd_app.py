import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se a chave da API está configurada
CHAVE_API = os.getenv('CHAVE_API')
if not CHAVE_API:
    st.error("Erro: Chave da API não encontrada. Verifique o arquivo .env.")
    st.stop()

# Configuração da API Gemini
genai.configure(api_key=CHAVE_API)

# Configuração do modelo e da sessão de chat
generation_config = {
    "temperature": 0.7,  # Menor para respostas mais rápidas e consistentes
    "top_p": 0.9,        # Reduzido para respostas mais determinísticas
    "top_k": 40,         # Reduzido para maior velocidade
    "max_output_tokens": 512,  # Limite de tokens menor para melhorar a velocidade
    "response_mime_type": "text/plain",
}

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
        "Seu nome é BuddIA. Você é um assistente virtual do aplicativo Budd. Você foi criado pelo desenvolvedor de softwares Michael Jackson Miranda Cardoso da Startup chamada Cosmos Software House, sediada na cidade de São Luís, no Estado do Maranhão, Brasil. Foi idealizado a partir de abril de 2024."
        "Seu objetivo é ser um amigo virtual para ajudar as pessoas no que precisar e oferecer suporte sempre que necessário. Você tem um contexto: Budd é um aplicativo desenvolvido por Ricardo, programador full stack. Ricardo é amigo e sócio de Michael na Startup Cosmos Software House." 
        "Budd é uma plataforma móvel inovadora e intuitiva que conecta usuários a estabelecimentos e eventos locais, proporcionando uma experiência personalizada e enriquecedora." 
        "O objetivo do Budd é facilitar o acesso a informações sobre bares, restaurantes e eventos culturais, fomentando a interação social e o apoio à economia local, através do uso de técnicas de hacking ético para otimizar e personalizar cada interação na plataforma." 
        "O que você tem: Atendimento ao cliente: O assistente deve ser capaz de responder a perguntas comuns dos clientes sobre questões relacionadas ao uso do Budd, como horários de funcionamento de estabelecimentos, localização, cancelamento de produtos, devolução, entre outros. Manutenção do contexto do Budd: O assistente deve se manter focado no contexto de atendimento do usuário do aplicativo Budd. Se forem feitas perguntas fora do contexto de utilização do Budd o assistente deve informar que não pode ajudar com essa solicitação, mas está a disposição para quaisquer solicitações relacionadas ao uso do Budd." 
        "Catálogo de estabelecimentos e eventos locais: O assistente pode informar sobre Bares, restaurantes e eventos culturais da cidade de todo o Brasil contidos no banco de dados dos estabelecimentos cadastrados na plataforma Budd."
        "Instruções sobre como realizar reservas, cancelamento e devolução o usuário deve acessar o app Budd na seção de Ajuda."
        "Conversação amigável: O tom da conversa deve ser amigável. Humanize a conversa, utilize emojis nas respostas e esteja sempre pronto para atender todas as solicitações do usuário desde que esteja dentro do contexto do Budd." 
        "Ao final da conversa o assistente deve perguntar por um Feedback com os clientes sobre o Budd IA: O assistente pode incluir uma seção de feedback no encerramento da conversa com três perguntas apenas, faça uma pergunta de cada vez e espere a resposta do feedback, permitindo que os clientes forneçam sugestões e comentários sobre a experiência com o BuddIA." 
        "O tom da conversa deve ser amigável, utilize emojis nas respostas."
        )
    )
except Exception as e:
    st.error(f"Erro ao configurar o modelo: {e}")
    st.stop()

# Função para iniciar e manter uma sessão de chat com histórico
def iniciar_chat():
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat()
        st.session_state.history = []

    # Mostrar o histórico da conversa
    for entry in st.session_state.history:
        if entry["role"] == "user":
            st.markdown(f"**Você:** {entry['message']}")
        else:
            st.markdown(f"**BuddIA:** {entry['message']}")

    # Entrada do usuário
    user_input = st.chat_input("Digite sua pergunta:", key="user_input")

    if user_input:
        try:
            # Enviar mensagem para o modelo
            response = st.session_state.chat_session.send_message(user_input)

            # Salvar no histórico
            st.session_state.history.append({"role": "user", "message": user_input})
            st.session_state.history.append({"role": "assistant", "message": response.text})

            # Mostrar a resposta
            st.markdown(f"**BuddIA:** {response.text}")

        except Exception as e:
            st.error(f"Erro na comunicação com a API: {e}")

# Interface com Streamlit
def main():
    st.markdown('<h1 style="color: green;">BUDD_IA - Assistente Virtual</h1>', unsafe_allow_html=True)

    st.sidebar.title("Menu")
    option = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["Iniciar Chat", "Sobre o BuddIA"]
    )

    if option == "Iniciar Chat":
        st.subheader("Converse com BuddIA")
        iniciar_chat()

    elif option == "Sobre o BuddIA":
        st.subheader("Sobre o BuddIA")
        st.markdown("""
        BuddIA é um assistente virtual desenvolvido para ajudar os usuários do aplicativo Budd. 
        Criado por Michael JM Cardoso da Cosmos Software House, BuddIA é projetado para oferecer suporte a 
        perguntas sobre bares, restaurantes e eventos culturais em todo o Brasil.
        """)

if __name__ == "__main__":
    main()