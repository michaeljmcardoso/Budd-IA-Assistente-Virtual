import os
import time
import pandas as pd
import sqlite3
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da chave API
CHAVE_API = os.getenv("CHAVE_API")
genai.configure(api_key=CHAVE_API)

# Configuração do modelo e da sessão de chat
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_output_tokens": 200,
}

system_instruction = (
    "Você é um assistente virtual especialista em análise de dados. "
    "Responda de forma concisa com base nos dados fornecidos."
)

# Função para iniciar a sessão de chat com a API Gemini
def iniciar_chat():
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction,
    )
    chat_session = model.start_chat()
    return chat_session

# Função para conectar ao banco de dados e retornar os dados
def conectar_banco_de_dados(db_path="database.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM atendimentos", conn)
    conn.close()
    return df

# Função para converter DataFrame em CSV
def exportar_para_csv(df):
    csv_path = "dados.csv"
    df.to_csv(csv_path, index=False)
    return csv_path

# Função para fazer upload do CSV para a API Gemini
def upload_para_gemini(csv_path):
    file = genai.upload_file(csv_path, mime_type="text/csv")
    return file.uri

# Função para configurar o tema da aplicação
def configurar_tema():
    st.markdown(
        """
        <style>
        .main { background-color: #f0f2f6; }
        h1 { color: #4CAF50; }
        </style>
        """, unsafe_allow_html=True
    )

# Interface do Streamlit
def main():
    st.set_page_config(page_title="Assistente de Dados", layout="wide")
    configurar_tema()

    # Inicializar st.session_state
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = None
        st.session_state.history = []

    # Menu de navegação
    menu = ["Home", "Dashboard", "Chat", "Sobre"]
    escolha = st.sidebar.selectbox("Selecione a Página", menu)

    # Página Home
    if escolha == "Home":
        st.title("📊 Assistente de Dados com Gemini")
        
        # Conectar ao banco e exibir dados
        st.subheader("Dados do Banco de Dados")
        df = conectar_banco_de_dados()
        st.dataframe(df)

        # Exportar dados para CSV
        st.subheader("Exportar Dados para CSV e Enviar para Gemini")
        if st.button("Exportar e Enviar"):
            csv_path = exportar_para_csv(df)
            file_uri = upload_para_gemini(csv_path)
            st.success("Dados enviados para a API Gemini com sucesso!")

            # Iniciar sessão de chat
            st.session_state.chat_session = iniciar_chat()
            st.session_state.history.append({"role": "user", "parts": [file_uri]})

    # Página Dashboard
    elif escolha == "Dashboard":
        st.title("📈 Dashboard de Visualização")
        df = conectar_banco_de_dados()
        
        # Visualizações simples
        st.subheader("Atendimentos por Município")
        municipio_count = df['municipio'].value_counts()
        st.bar_chart(municipio_count)

        st.subheader("Atendimentos por Data")
        df['data'] = pd.to_datetime(df['data'])
        atendimentos_por_data = df.groupby(df['data'].dt.date).size()
        st.line_chart(atendimentos_por_data)

# Página Chat
    elif escolha == "Chat":
        st.title("💬 Chat com Assistente de Dados")

    # Inicializar sessão de chat, se necessário
    if not st.session_state.chat_session:
        st.session_state.chat_session = iniciar_chat()

    # Interface do chat
    user_input = st.text_input("Digite sua pergunta:")

    if st.button("Enviar"):
        if user_input:
            # Enviar pergunta para o assistente
            response = st.session_state.chat_session.send_message(user_input)

            # Armazenar histórico
            st.session_state.history.append({"role": "user", "content": user_input})
            
            # Extrair texto dos objetos Part, se necessário
            if hasattr(response, 'parts'):
                resposta_texto = ' '.join(part.text for part in response.parts)
            else:
                resposta_texto = response.text

            st.session_state.history.append({"role": "assistant", "content": resposta_texto})

            # Mostrar histórico de chat
            st.subheader("Histórico de Chat")
            for message in st.session_state.history:
                if message['role'] == "user":
                    st.write(f"**Você**: {message.get('content', '')}")
                elif message['role'] == "assistant":
                    st.write(f"**Assistente**: {message.get('content', '')}")


                
    # Página Sobre
    elif escolha == "Sobre":
        st.title("ℹ️ Sobre a Aplicação")
        st.write("""
        Esta aplicação foi desenvolvida para demonstrar o uso da API Gemini da Google 
        para interagir com dados do usuário. A aplicação conecta-se a um banco de dados SQLite, 
        permite a exportação de dados em CSV e envia para a API para fornecer respostas inteligentes.
        """)

if __name__ == "__main__":
    main()


