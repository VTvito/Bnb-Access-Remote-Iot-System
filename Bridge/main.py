import logging
import time
from bridge import Bridge
from bridge_config import init_firebase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# parametri di configurazione passati al bridge relativi alla serratura
PORTNAME = 'COM3'
DEVICE_ID = 'Home_77F2A2' 
FIREBASE_CREDENTIALS = "Bridge/baris-iot-vito-firebase-adminsdk-baww0-19695e55a0.json"
NAME = "Home"
LATITUDE = "44.48130278433922"
LONGITUDE = "11.367877878271969"

if __name__ == '__main__':
    db = init_firebase(FIREBASE_CREDENTIALS)
    bridge = Bridge(port=PORTNAME, device_id=DEVICE_ID, db=db, name=NAME, latitude=LATITUDE, longitude=LONGITUDE)
    
    bridge.setup_serial()

# Avvia i thread per ascoltare i pacchetti da Arduino e monitorarne la connettività
    bridge.start_remote_thread()
    bridge.start_offline_check_thread()

# Esegue un ciclo per leggere lo stato da Firebase limitando le richiesto ogni 2s
    try:
        while bridge.running:
            bridge.read_from_firebase()
            time.sleep(2)
    except KeyboardInterrupt:
        logging.info("Interrotto dall'utente.")
    except Exception as e:
        logging.error(f"Errore nel loop principale: {e}")
    finally:
        bridge.stop()