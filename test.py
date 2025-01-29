import logging
import threading
import time

def log_background():
        while True:
            logging.info("Background log message.")
            time.sleep(2)  # Log every 2 seconds



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')

   

    # Start logging in the background
    threading.Thread(target=log_background, daemon=True).start()

    user_input = input("Enter something: ")
    print(f"You entered: {user_input}")
