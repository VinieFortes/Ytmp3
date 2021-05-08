import requests
import urllib.request
from PySimpleGUI import PySimpleGUI as sg

sg.theme('Reddit')

fstatus = 'no'


def inicio():
    layout = [
        [sg.Text('Digite o nome da Musica'), sg.Input(key='nome')],
        [sg.Text('Url da musica do YouTube'), sg.Input(key='url')],
        [sg.Text('Escolha um diretorio para salvar'), sg.Input(), sg.FolderBrowse('Escolher')],
        [sg.Button('BAIXAR')],
        [sg.Text('Status:                                                                                             '
                 '                       ', key='status')],
        [sg.Text('\nby Vinie')]
    ]

    janela(layout)


def resultadoNome(nome, direct):
    r = requests.get('https://videfikri.com/api/ytplayv2/?query=' + nome)
    resultado = r.json()
    folder = direct
    url = resultado['result']['source']
    print(url)
    baixar(url, folder)


def baixar(url, diretorio):
    r = requests.get('https://api.zeks.xyz/api/ytmp3/2?url=' + url + '&apikey=apivinz')
    resultado = r.json()

    url = resultado['result']['link']
    nome = resultado['result']['title']
    urllib.request.urlretrieve(url, diretorio + '/' + nome + '.mp3')
    print(url)
    global fstatus
    fstatus = 'ok'


def janela(layout):
    window = sg.Window('YTMP3', layout)
    while True:
        eventos, valores = window.read()
        if eventos == sg.WIN_CLOSED:
            break
        if eventos == 'BAIXAR':
            diretorio = valores['Escolher']
            nomeyt = valores['nome']
            urlyt = valores['url']

            if nomeyt == '' and urlyt == '':
                window.Element('status').Update('Status: Erro ! ambos os campos estão vazios !')
            elif diretorio == '':
                window.Element('status').Update('Status: Defina um diretorio valido')
            elif nomeyt == '':
                window.Element('status').Update('Status: Fazendo Download, aguarde !')
                baixar(urlyt, diretorio)
            elif urlyt == '':
                window.Element('status').Update('Status: Fazendo Download, aguarde !')
                resultadoNome(nomeyt, diretorio)
            else:
                window.Element('status').Update('Status: Erro ! ambos os campos estão preenchidos!')

            global fstatus

            if fstatus == 'ok':
                window.Element('status').Update('Status: Salvo em ' + diretorio)


inicio()
