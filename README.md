# Budd IA - Assistente Virtual

O programa implementa um assistente virtual chamado Budd IA usando a biblioteca `Streamlit` e `PySimpleGUI` para a interface gráfica do usuário (GUI) e a API `google.generativeai` para geração de texto.

**Funcionalidade Principal:**

- **Interação do Usuário:** 
  - O usuário digita uma mensagem na interface.
  - O assistente virtual responde à mensagem, fornecendo informações ou suporte, conforme programado.

**Detalhes Técnicos:**

- **Interface Gráfica:**
  - Criada com `PySimpleGUI == 4.60.5`, a interface foi a primeira versão de testes. Inclui uma área de entrada de texto, botões para enviar a mensagem e sair, e uma área de saída de texto para exibir as respostas do assistente. Roda apenas em ambiente desktop.
  - Criada com `Streamlit`, a segunda versão da interface possui as mesmas funcionalidades da primeira versão `PySimpleGUI`, com o diferencial que pode ser carregada tanto em ambiente desktop quanto mobile. Com Streamlit Cloud fizemos o deploy da aplicação.
  
- **API de Geração de Texto:**
  - Configurada com uma chave API, a API `google.generativeai` gera respostas baseadas no texto de treinamento fornecido e na mensagem do usuário.

- **Modelo de Geração:**
  - Configurado para produzir uma única resposta (`candidate_count: 1`) com uma temperatura de 0.9, que controla a criatividade da resposta.
  - Configurações de segurança desativadas (`BLOCK_NONE`) para várias categorias de conteúdo.
  - Utiliza modelo `gemini-1.5-flash`, modelo multimodal mais rápido.

**Exemplo de Uso:**

1. **Usuário:** Digita uma pergunta sobre o horário de funcionamento de um restaurante.
2. **Assistente Buddy IA:** Responde com o horário de funcionamento baseado no texto de treinamento.

**Objetivo:**

- **Assistência Virtual:** Budd IA foi projetado para ajudar os usuários com informações sobre estabelecimentos locais, eventos, reservas, e processos de atendimento ao cliente, mantendo um tom amigável e humanizado.

O programa combina geração de texto avançada com uma interface simples e intuitiva para criar uma experiência de chat interativa e útil.
