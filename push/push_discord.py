# Discord发送依赖
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
# 日志服务
from common.basicLog import logger

class push_discord():
    def __init__(self, webhook):
        self.discord_webhook = DiscordWebhook(url=webhook)

    def set_proxies(self, proxy):
        self.discord_webhook.set_proxies(proxy)

    def pushMessage(self, message, title='test title'):
        embed = DiscordEmbed(title=title, description=message, color=0x00ff00)
        embed.set_author(name='Auto_Attendance',
                         url='https://github.com/DoraTiger/Auto_Attendance')
        embed.set_footer(
            text=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.discord_webhook.add_embed(embed)
        try:
            response = self.discord_webhook.execute()
            if response.status_code == 200:
                logger.info("Discord-Bot 消息发送成功")
            else:
                logger.error("Discord-Bot 消息发送失败" + response.json())
        except Exception as e:
            logger.error(e)
            logger.error("Discord-Bot 消息发送失败" + "，网络超时，请尝试代理")
        finally:
            pass
            
