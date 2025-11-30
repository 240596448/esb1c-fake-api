import os
from esb1c import Application

application = Application(
    url=os.getenv("APPLICATION_URL"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
)
