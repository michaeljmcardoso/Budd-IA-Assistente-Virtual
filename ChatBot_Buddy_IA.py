import google.generativeai as genai
import PySimpleGUI as sg
import Constantes
import Config_modelo

def main():
    genai.configure(api_key=Constantes.CHAVE_API)

    modelo = genai.GenerativeModel('gemini-pro', generation_config=Config_modelo.CONFIG_GERACAO, safety_settings=Config_modelo.CONFIG_SEGURANCA)

    chat = modelo.start_chat(history=[])

    def chat_loop():
        treinamento = Constantes.TREINAMENTO

        sg.theme(Constantes.TEMA_JANELA)

        layout = Constantes.LAYOUT_JANELA

        janela = sg.Window('Buddy AI - Assistante Virtual', layout)

        while True:
            event, values = janela.read()

            if event == sg.WIN_CLOSED or event == '-SAIR-':
                break

            if event == '-ENVIAR-':
                prompt = values['-ENTRADA-']
                response = chat.send_message(f'{treinamento} {prompt}')
                janela['-SAIDA-'](f'Buddy IA: {response.text}\n')
                janela['-ENTRADA-'].update('')

        janela.close()

    chat_loop()

if __name__ == "__main__":
    main()