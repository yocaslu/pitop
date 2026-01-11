from sys import exit
from loguru import logger
from pprint import pprint
from modules.system import System
from modules.server import app
import json

def main():
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
        pi = System()
        pi.update()
        pprint(json.dumps(pi.__dict__, indent=4))
    except Exception as e:
        logger.error(f'failed to initiate server: {e}')
        exit(1)


       

if __name__ == "__main__":
    main()
