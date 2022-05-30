from esp_ble_uart import *
from sgp30 import SGP30
from time import *
import sys

# Définition du raccourci de fonction de capteur :
sgp30 = SGP30()

# Définition du réseau Bluetooth Low Energy :
nom = 'SKair'
UUID_UART = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_TX = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_RX = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'

uart = Bleuart(nom, UUID_UART, UUID_TX, UUID_RX)
uart.close()

# Fonction pour envoyer des données :
def envoi(val_tx):
    uart.write(str(val_tx))  
    print("Donnée mesurée = ", val_tx)

print("Le capteur se calibre, s'il vous plaît attendez...")
def crude_progress_bar():
    sys.stdout.write('.')
    sys.stdout.flush()

sgp30.start_measurement(crude_progress_bar)
sys.stdout.write('\n')

while True:
    envoi(sgp30.get_air_quality())       
    time.sleep_ms(500)