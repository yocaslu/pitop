from sys import exit
from loguru import logger
from modules.server import app

def main():
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f'failed to initiate server: {e}')
        exit(1)

if __name__ == "__main__":
    main()
