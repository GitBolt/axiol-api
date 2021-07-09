import os
import cloudinary


CDNCONFIG = cloudinary.config( 
  cloud_name = "axiolbot",
  api_key = os.environ.get("api_key"),
  api_secret = os.environ.get("api_secret"),
)

TOKEN = os.environ.get("TOKEN")

