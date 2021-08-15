import bs4 as bs
import requests
import yfinance as yf
import json
import plotly.graph_objects as go
import plotly
from flask import Flask, render_template
import pandas as pd

html = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(html.text, 'lxml')
table = soup.find('table', {'class': 'wikitable sortable'})



tickers = []
nombres = []
sectores = []
for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        tickers.append(ticker)
        nombre = row.findAll("td")[1].text
        nombre = nombre[:]
        nombres.append(nombre)
        sector = row.findAll("td")[4].text
        sector = sector[:]
        sectores.append(sector)
        



tabla = pd.DataFrame()
tabla["Ticker"] = tickers
tabla["Nombre"] = nombres
tabla["Sector"] = sectores
lista = list(tabla["Ticker"] + " " + tabla["Nombre"])



app = Flask(__name__)



    
@app.route('/datos/<ticker>')
def datos(ticker):
    data = yf.download(ticker).round(2)
    #data.drop(["Adj Close", "Volume"], inplace=True, axis=1)
    data.reset_index(inplace=True)
    data = data.sort_values(["Date"], ascending=False)
    cols = data.columns
    info = yf.Ticker(ticker)
    descripcion=info.info["longBusinessSummary"]
    financials = info.financials.round(2)
    financials.reset_index(inplace=True)
    financials.dropna(inplace=True)
    cols2=financials.columns

    
    fig = go.Figure(data=[go.Candlestick(
    x=data['Date'],
    open=data['Open'], high=data['High'],
    low=data['Low'], close=data['Close'],
    increasing_line_color= 'green', decreasing_line_color= 'red'
)])
    fig.update_layout(showlegend=False)
    fig['layout'].update(margin=dict(l=0,r=0,b=0,t=30))
    fig.update_layout(xaxis_rangeslider_visible=False)
    
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)







    
    return render_template('datos.html',
                           ticker=ticker,
                           data=data,
                           plot_json=plot_json, 
                           financials=financials,
                           cols = cols,
                           cols2=cols2,
                           descripcion = descripcion,
                           lista = lista, passstatic_url_path='/static')




@app.route('/')
def index1():

    cols = tabla.columns
    return render_template('blank1.html',
                           data=tabla, 
                           cols = cols, 
                           lista = lista, passstatic_url_path='/static')
