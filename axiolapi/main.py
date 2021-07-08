from fastapi import FastAPI
from visuals.bargraph import BarGraph
from visuals.piechart import PieChart

app = FastAPI()


@app.get('/')
def index():
    return {
        "Rank BarGraph": "/bargraph/{serverid}",
        "Rank PieChart": "/piechart/{serverid}"
        }

    
#Returns top 10 users by default, using limit more users can be fetched
@app.get('/bargraph/{serverid}')
def index(serverid: int, limit:int=10):
    if limit > 30:
        return {"message": "You cannot get a bar graph of more than 30 users"}
    else:
        Data = BarGraph(serverid, limit)
        
        return {"message": Data}


@app.get('/piechart/{serverid}')
def index(serverid: int):
    Data = PieChart(serverid)
        
    return {"message": Data}
