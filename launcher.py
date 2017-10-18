import sys
from watashi import Watashi

if __name__ == "__main__":
    try:
        config_path = sys.argv[1]
    except:
        config_path = 'config.json'

    bot = Watashi(config_path)
    bot.run()
