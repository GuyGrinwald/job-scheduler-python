# This is the gunicron config file. For more information on the configs here see - https://docs.gunicorn.org/en/stable/settings.html

loglevel = "debug"

worker_class = "gthread"

workers = 1  # set this to 1 for easy debug purposes

threads = 2

bind = "127.0.0.1:5000"
