import os 

if os.path.isfile('.env'):
    from decouple import Config, RepositoryEnv
    config = Config(RepositoryEnv('.env'))
else:
    from decouple import config
    
STREAMING_SLEEP_TIME = config('STREAMING_SLEEP_TIME', cast=float, default=0.002)

BOT_AVATAR = config('BOT_AVATAR', cast=str,
                    default='./assets/chatbot.png')

USER_AVATAR = config('USER_AVATAR', cast=str,
                    default='./assets/user.png')

FAVICON = config('FAVICON', cast=str,
                    default='./assets/robot.png')