import requests
import os
import cloudinary.uploader
import matplotlib.pyplot as plt
import cloudinary
from variables import TOKEN, CDNCONFIG
from database import LEVELDATABASE


def RankBar(serverid, limit):

    if not str(serverid) in LEVELDATABASE.list_collection_names():
        return "This server does not have any rankings"

    GuildData = LEVELDATABASE[str(serverid)]
    Users = GuildData.find().sort("xp", -1).limit(limit)
    Username = []

    Experience = []
    Avatars = []

    for i in Users:
        user = requests.get(f"https://discord.com/api/v8/users/{i['_id']}", headers={"Authorization": f"Bot {TOKEN}"}).json()
        try:
            Username.append(user["username"])
            Avatars.append(f"https://cdn.discordapp.com/avatars/{i['_id']}/{user['avatar']}.png")
            Experience.append(i.get("xp"))
        except:
            print(f"\nError: {i}")

    TEXTCOLOUR = '#CBCBCB'
    plt.rcParams['text.color'] = TEXTCOLOUR
    plt.rcParams['axes.labelcolor'] = TEXTCOLOUR
    plt.rcParams['xtick.color'] = TEXTCOLOUR
    plt.rcParams['ytick.color'] = TEXTCOLOUR


    if limit <= 10:
        fig_width=  15
        xfont_size = 14
        yfont_size = 18
    elif limit <= 20:
        fig_width = 25
        xfont_size = 12
        yfont_size = 15
    else:
        fig_width = 28
        xfont_size = 8
        yfont_size = 12

    fig, ax = plt.subplots(figsize=(fig_width, 10))
    plt.xticks(rotation=15, size=xfont_size)

    plt.yticks(size=yfont_size)

    ax.set_title(f"Top {limit} users", size=yfont_size+10, color="white")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color("white")
    ax.spines['left'].set_color("white")

    bars = plt.bar(Username, Experience, width=.8, color="#0075FF", align="center")
    bars[0].set_color("#00D1FF")
    plt.savefig(os.getcwd()+f"/{serverid}.png", facecolor="#1C1B37", transparent=True)

    savedimage = os.getcwd()+f"/{serverid}.png"
    hostedimage = cloudinary.uploader.upload(savedimage, folder="Axiol/")

    return hostedimage["url"]

