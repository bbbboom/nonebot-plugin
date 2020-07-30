import nonebot
import config

if __name__ == "__main__":
    nonebot.init(config)
    nonebot.load_plugins("mybot/plugins", 'mybot.plugins')
    nonebot.run(host="0.0.0.0", port=8080)
