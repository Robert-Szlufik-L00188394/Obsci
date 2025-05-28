import logging
import subprocess
import os
from daytime import datetime
import time
import threading

def setup_logger():
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Format the filename as dd-mm-yyyy-obsci.log
    date_str = datetime.datetime.now().strftime('%d-%m-%Y')
    log_filename = f"{date_str}-obsci.log"
    log_path = os.path.join(log_dir, log_filename)

    logger = logging.getLogger('obsci')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # Standard file handler (no rotation here, we're naming the file daily)
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


def log_docker_image_versions(images, logger):
    logger.info("Docker image versions:")
    for image in images:
        try:
            result = subprocess.run(
                ['docker', 'image', 'inspect', image, '--format', '{{.RepoTags}}'],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"{image}: {result.stdout.strip()}")
        except subprocess.CalledProcessError:
            logger.warning(f"Could not retrieve version for image: {image}")

def log_telegraf_output(logger, container_name='telegraf'):
    logger.info("Fetching Telegraf container logs...")
    try:
        result = subprocess.run(
            ['docker', 'logs', '--tail', '20', container_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge both streams
            text=True
        )
        if result.returncode == 0:
            logger.info("Telegraf log tail:\n" + result.stdout)
        else:
            logger.warning("Failed to get Telegraf logs.")
    except Exception as e:
        logger.error(f"Error reading Telegraf logs: {e}")

stop_event = threading.Event()
def periodic_container_info_logger(logger, container_name='telegraf', interval=10):
    print("Starting periodic Telegraf log tailing...")
    logger.info("Starting periodic Telegraf log tailing...")
    def loop():
        print("inside def loop")
        while True:
            print("inside while loop")
            try:
                result = subprocess.run(
                    ['docker', 'logs', '--tail', '20', container_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,  # Merge both streams
                    text=True
                )
                print('result', result)
                if result.returncode == 0:
                    logger.info("Telegraf log tail:\n" + result.stdout)
                else:
                    logger.warning("Failed to get Telegraf logs.")
            except Exception as e:
                logger.error(f"Error reading Telegraf logs: {e}")
            time.sleep(interval)

    print("Starting thread")
    thread = threading.Thread(target=loop)
    thread.start()
