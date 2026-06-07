import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("HandshakeTest")

def run_handshake():
    # Przykładowy adres n8n (możesz go podmienić na faktyczny, testowy lub produkcyjny)
    webhook_url = "http://localhost:5678/webhook-test/549770bd-c2ee-422d-82b3-13e901ac0e3c"
    
    mock_payload = [
        {
            "data_wydania_decyzji": "2024-05-01",
            "miejscowosc": "Warszawa",
            "inwestor": "Handshake Sp. z o.o.",
            "nr_dzialki_ewid": "999/1",
            "obreb_ewid": "0001 Śródmieście",
            "jednostka_ew": "146501_1 Warszawa",
            "trace_id": "test-handshake-12345"
        }
    ]
    
    logger.info(f"Rozpoczynam próbny uścisk dłoni z webhookiem: {webhook_url}")
    
    try:
        response = requests.post(webhook_url, json=mock_payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"SUKCES! Webhook odpowiedział statusem 200 OK.")
            logger.info(f"Odpowiedź: {response.text}")
        else:
            logger.warning(f"Otrzymano odpowiedź, ale status to: {response.status_code}")
            logger.warning(f"Treść: {response.text}")
    except requests.exceptions.ConnectionError:
        logger.error(f"NIEPOWODZENIE. Brak połączenia. Upewnij się, że n8n jest uruchomione na localhost:5678, a workflow jest nasłuchujący.")
    except Exception as e:
        logger.error(f"Wystąpił inny błąd podczas testu: {str(e)}")

if __name__ == "__main__":
    run_handshake()
