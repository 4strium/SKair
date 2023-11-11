import time
from esp_ble_uart import *
import uSGP30
import sys
import machine

# Définition du cablage (input SGP30) :

# I2C Data (SDA) = GPIO 18 :
I2C_SCL_GPIO = const(18)

# I2C Clock (SCL) = GPIO 19 :
I2C_SDA_GPIO = const(19)

# Fréquence :
I2C_FREQ = const(400000)


i2c = machine.SoftI2C(
    scl=machine.Pin(I2C_SCL_GPIO, machine.Pin.OUT),
    sda=machine.Pin(I2C_SDA_GPIO, machine.Pin.OUT),
    freq=I2C_FREQ
)


# Définition du raccourci de fonction de capteur :
sgp30 = uSGP30.SGP30(i2c)


# Définition du cablage (input LEDs) :
# Rouge :
I2C_RED_GPIO = const(13)
pRED = machine.Pin(I2C_RED_GPIO, machine.Pin.OUT)
pRED.value(0)

# Jaune :
I2C_YELLOW_GPIO = const(12)
pYELLOW = machine.Pin(I2C_YELLOW_GPIO, machine.Pin.OUT)
pYELLOW.value(0)

# Vert :
I2C_GREEN_GPIO = const(14)
pGREEN = machine.Pin(I2C_GREEN_GPIO, machine.Pin.OUT)
pGREEN.value(0)

# Bleu :
I2C_BLUE_GPIO = const(27)
pBLUE = machine.Pin(I2C_BLUE_GPIO, machine.Pin.OUT)
pBLUE.value(0)

# Définition du port valeur du buzzer :
I2C_BUZZ_GPIO = const(25)
pBUZZ = machine.Pin(I2C_BUZZ_GPIO, machine.Pin.OUT)
pBUZZ.value(0)

# Définition du réseau Bluetooth Low Energy :
nom = 'SKAIR Sensor'
UUID_UART = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_TX = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
UUID_RX = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'

uart = Bleuart(nom, UUID_UART, UUID_TX, UUID_RX)
uart.close()

# Fonction pour envoyer des données :
def envoi(val_tx, val_ty):
    uart.write("\n\n")
    uart.write("Valeur mesurée d'équivalent CO₂ : " + str(val_tx) + " ppm.\n")  
    uart.write("Composés organiques volatils totaux : " + str(val_ty) + " ppb.") 

sgp30.set_absolute_humidity(62)
sgp30.measure_iaq()
time.sleep(15)
uart.write("Le capteur se calibre, patientez s'il vous plaît...\n")
for i in range(10,100,10):
    time.sleep(5)
    uart.write(i,"% ...\n")
    sgp30.mesure_iaq()
time.sleep(2)
uart.write("Calibrage complété avec succès !\n")

runtime = 120 # Changer ici le temps d'exécution total des mesures
interval = 2 # Changer ici l'intervalle entre chaque mesure

timecode = "Temps en secondes;"
val_lst_co2 = "Valeurs mesurées d'équivalent CO₂ (en ppm) :;"
val_lst_tvoc = "Composés organiques volatils totaux (en ppb) :;"
checktime = 0

while checktime < runtime:
    co2eq_ppm, tvoc_ppb = sgp30.measure_iaq()
    envoi(co2eq_ppm, tvoc_ppb)
    val_lst_co2 += str(co2eq_ppm)+";"
    val_lst_tvoc += str(tvoc_ppb)+";"
    timecode += str(checktime)+";"
    if co2eq_ppm >= 1000 :
        pYELLOW.value(0)
        pGREEN.value(0)
        pBLUE.value(0)
        pRED.value(1)
        pBUZZ.value(1)
    if 999 >= co2eq_ppm >= 800 :
        pGREEN.value(0)
        pBLUE.value(0)
        pRED.value(0)
        pBUZZ.value(0)
        pYELLOW.value(1)
    if 799 >= co2eq_ppm >= 600 :
        pBLUE.value(0)
        pRED.value(0)
        pYELLOW.value(0)
        pBUZZ.value(0)
        pGREEN.value(1)
    if 599 >= co2eq_ppm :
        pRED.value(0)
        pYELLOW.value(0)
        pGREEN.value(0)
        pBUZZ.value(0)
        pBLUE.value(1)
    checktime += interval
    time.sleep(interval)
    
file = open("rapport.txt", "w")
file.write(timecode+"\n")
file.write(val_lst_co2+"\n")
file.write(val_lst_tvoc+"\n")
file.close()
raise KeyboardInterrupt
