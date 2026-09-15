import time
import sys

def clear_screen():
    print('\033[2J\033[H', end='')

def print_status(distance, vibration_level):
    clear_screen()
    print("="*55)
    print(" 🛠️  SIMULADOR DO BRACELETE INTELIGENTE ESP32")
    print(" Autores: Matheus Schionato e Vairtles Liel")
    print("="*55)
    print("\n[ SENSOR ULTRASSÔNICO HC-SR04 ]")
    print(f"📡 Distância detectada no espaço aéreo: {distance:03} cm")
    
    print("\n[ MOTOR DE VIBRAÇÃO (PWM) ]")
    
    # Barra de progresso visual simulando a intensidade da vibração
    bars = int((vibration_level / 255) * 20)
    empty_bars = 20 - bars
    bar_str = "█" * bars + "░" * empty_bars
    
    if vibration_level == 0:
        print(f"Status: Caminho Livre    [{bar_str}] (Desligado)")
    elif vibration_level < 100:
        print(f"Status: Alerta Leve      [{bar_str}] (Vibração Fraca)")
    elif vibration_level < 200:
        print(f"Status: Alerta Médio     [{bar_str}] (Vibração Média)")
    else:
        print(f"Status: PERIGO IMINENTE! [{bar_str}] (VIBRAÇÃO MÁXIMA!)")
    
    print("\n" + "="*55)
    print("Pressione Ctrl+C para encerrar a simulação.")

def main():
    try:
        # Simulando uma caminhada onde o usuário vai se aproximando
        # de um obstáculo suspenso (ex: orelhão ou placa na rua)
        distancias_simuladas = [300, 250, 190, 140, 110, 85, 60, 45, 30, 20, 15]
        
        for d in distancias_simuladas:
            if d > 150:
                vib = 0
            elif d > 100:
                vib = 80
            elif d > 50:
                vib = 150
            else:
                vib = 255
                
            print_status(d, vib)
            time.sleep(1.5) # Pausa de 1.5s para a audiência conseguir ler na tela
            
        print("\n\n✅ Simulação concluída! O usuário desviou do obstáculo aéreo com sucesso.")
        
    except KeyboardInterrupt:
        print("\nSimulação encerrada pelo usuário.")
        sys.exit(0)

if __name__ == "__main__":
    main()
