import requests
import os
import cloudinary.uploader
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import cloudinary
from variables import TOKEN
from database import LEVELDATABASE


def PieChart(serverid):

    if not str(serverid) in LEVELDATABASE.list_collection_names():
        return "This server does not have any rankings"

    GuildData = LEVELDATABASE[str(serverid)]
    Users = GuildData.find().sort("xp", -1).limit(10)
    Username = []

    Experience = []

    for i in Users:
        user = requests.get(f"https://discord.com/api/v8/users/{i['_id']}", headers={"Authorization": f"Bot {TOKEN}"}).json()
        try:
            Username.append(user["username"])
            Experience.append(i.get("xp"))
        except:
            print(f"\nError: {i}")
    TEXTCOLOUR = '#CBCBCB'
    plt.rcParams['text.color'] = TEXTCOLOUR
    plt.rcParams['axes.labelcolor'] = TEXTCOLOUR
    plt.rcParams['xtick.color'] = TEXTCOLOUR
    plt.rcParams['ytick.color'] = TEXTCOLOUR

    explode = [0.0 for _ in range(len(Experience))]
    explode[0] = 0.05

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.pie(Experience, explode=tuple(explode), labels=Username, autopct='%1.1f%%',
            startangle=90)
    ax.axis('equal')

    plt.savefig(os.getcwd()+f"/{serverid}.png", facecolor="#1C1B37", transparent=True)

    savedimage = os.getcwd()+f"/{serverid}.png"
    hostedimage = cloudinary.uploader.upload(savedimage, folder="PieCharts/")
    os.remove(savedimage)
    return hostedimage["url"]