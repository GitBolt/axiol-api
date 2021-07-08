import requests
import os
import cloudinary.uploader
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import cloudinary
from variables import TOKEN
from database import LEVELDATABASE


def BarGraph(serverid, limit):

    if not str(serverid) in LEVELDATABASE.list_collection_names():
        return "This server does not have any rankings"

    GuildData = LEVELDATABASE[str(serverid)]
    Users = GuildData.find().sort("xp", -1).limit(limit)
    Username = []

    Experience = []

    for i in Users:
        user = requests.get(f"https://discord.com/api/v8/users/{i['_id']}", headers={"Authorization": f"Bot {TOKEN}"}).json()
        try:
            Username.append(user["username"])
            Experience.append(i.get("xp"))
        except Exception as e:
            print(f"{e}: {i}")

    TEXTCOLOUR = '#CBCBCB'
    plt.rcParams['text.color'] = TEXTCOLOUR
    plt.rcParams['axes.labelcolor'] = TEXTCOLOUR
    plt.rcParams['xtick.color'] = TEXTCOLOUR
    plt.rcParams['ytick.color'] = TEXTCOLOUR

    if limit <= 10:
        bottom_gap = 0.21
        fig_width=  16
        fig_height = 9

    elif limit <= 20:
        bottom_gap = 0.25
        fig_width=  18
        fig_height = 9

    else:
        bottom_gap = 0.25
        fig_width = 18
        fig_height = 9

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    plt.xticks(rotation=90, size=15)

    plt.yticks(size=10)
    plt.ylabel("XP", size=25, color="white")
    ax.yaxis.set_major_locator(ticker.MultipleLocator(round(Experience[0], -1) / 15))
    ax.set_title(f"Top {limit} users", size=20, color="white")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color("white")
    ax.spines['left'].set_color("white")

    plt.gcf().subplots_adjust(bottom=bottom_gap)

    bars = plt.bar(Username, Experience, width=0.8, color="#0075FF", align="center")
    bars[0].set_color("#00D1FF")

    plt.savefig(os.getcwd()+f"/{serverid}.png", facecolor="#1C1B37", transparent=True)

    savedimage = os.getcwd()+f"/{serverid}.png"
    hostedimage = cloudinary.uploader.upload(savedimage, folder="RankGraphs/")
    os.remove(savedimage)
    return hostedimage["url"]

