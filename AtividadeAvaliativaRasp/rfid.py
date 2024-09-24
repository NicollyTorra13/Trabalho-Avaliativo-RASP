import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep, time
import signal
import sys
import csv
import requests  # Importando a biblioteca requests
from autorizacao import Autorizacoes

# Configurações de hardware
GPIO.setmode(GPIO.BOARD)
LED_VERDE = 8
LED_VERMELHO = 10
BUZZER = 38

GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# Iniciando o leitor RFID
leitorRfid = SimpleMFRC522()

# Controle de acessos
tempo_entrada = {}

# Instâncias de Autorizacoes
autorizacoes = Autorizacoes()

# Lista de itens disponíveis
itens_disponiveis = [
    "Óculos de proteção", "Led", "Registros", "TAG", "Protoboard", 
    "Leitor rfid", "Fonte de alimentação USB tipo C", "Speaker", 
    "Sensor de luminosidade", "Arduino", "Raspberry", "Kit Discovery", 
    "Multímetro", "Cabo colorido macho/macho", "Cabo colorido macho/fêmea", 
    "Pulseira antiestática", "Kit solda", "Sensor de umidade do solo", "Lupa", 
    "Módulo Wi-Fi para Arduino", "Protonoard", "Cabo conversor HD", "Buzzer", 
    "Sensor ultra-sônico", "Kit sensores para Arduino"
]

# Funções para o buzzer
def tocar_buzzer(frequencia, duracao):
    p = GPIO.PWM(BUZZER, frequencia)
    p.start(50)  # Duty cycle de 50%
    sleep(duracao)
    p.stop()

def buzzer_entrada_autorizada():
    tocar_buzzer(1000, 0.2)  # Som curto de entrada autorizada

# Função para enviar os itens retirados para a API
def enviar_itens_para_api(nome, itens):
    url = "https://sua-api-url.com/itens_retirados"  # Substitua pela URL da sua API
    data = {
        "nome": nome,
        "itens": itens
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Itens enviados com sucesso para a API.")
        else:
            print(f"Erro ao enviar itens para a API: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro na conexão com a API: {e}")

# Função para salvar os itens retirados e enviar para a API
def salvar_itens_retirados(nome, itens):
    with open('itens_retirados.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nome, ", ".join(itens), time()])
    
    # Enviar itens para a API
    enviar_itens_para_api(nome, itens)

# Função para o aluno responder sobre os itens retirados
def selecionar_itens(nome):
    itens_retirados = []
    print(f"\n{nome}, você está retirando os seguintes itens? Responda com 'sim' ou 'não':")
    
    for item in itens_disponiveis:
        resposta = input(f"{item}: ").strip().lower()
        if resposta == 'sim':
            itens_retirados.append(item)
    
    # Salva os itens retirados
    salvar_itens_retirados(nome, itens_retirados)
    print(f"Obrigado {nome}, os itens selecionados foram registrados.")

# Função para finalizar o programa
def finalizar_programa(signal, frame):
    print("\nFinalizando o programa.")
    GPIO.cleanup()
    sys.exit(0)

# Captura o sinal de interrupção (CTRL+C)
signal.signal(signal.SIGINT, finalizar_programa)

try:
    while True:
        print("Aguardando leitura da tag...")
        tag, _ = leitorRfid.read()
        print(f"ID do cartão: {tag}")
        
        if tag in autorizacoes:
            nome = autorizacoes[tag]
            
            if tag not in tempo_entrada:
                # Primeira entrada do colaborador
                tempo_entrada[tag] = time()
                print(f"Acesso autorizado, Bem-vindo(a) {nome}!")
                
                GPIO.output(LED_VERDE, GPIO.HIGH)
                buzzer_entrada_autorizada()
                sleep(3)
                GPIO.output(LED_VERDE, GPIO.LOW)
                
                # Seleção dos itens a retirar
                selecionar_itens(nome)
            else:
                print(f"{nome}, você já está com a entrada registrada.")
finally:
    GPIO.cleanup()