import requests
import json
from bokeh.io import output_file, show, save
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, HoverTool
)
import utm

app = Flask(__name__)

app.ticker = ''
app.state = 'input'
app.option = 'Accidentes_Total'

@app.route('/')
def main():
    if app.state == 'input':
        return redirect('/index')
    else:
        return redirect('/result')


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index2():
    app.option = request.form['option']
    app.state = 'output'
    return redirect('/')

@app.route('/result', methods=['GET'])
def plot_result():
    app.state = 'input'

    if app.option == 'Accidentes_Total':
        app.df=pd.read_csv('Expedientes.csv', delimiter = ';')
        
        latitudes = app.df['GPS_x'].tolist()
        longitudes = app.df['GPS_y'].tolist()
        ###Cambio de unidades de las coordenadas que tenemos (UTM) a geográficas
        for i in xrange(len(latitudes)):
            if latitudes[i] > 999999 :
                latitudes[i] = latitudes[i]/1000

        for i in xrange(len(longitudes)):
            if longitudes[i] > 9999999 :
                longitudes[i] = longitudes[i]/1000
        

        latitudes = [float(lat) for lat in latitudes]
        longitudes = [float(lon) for lon in longitudes]
        lats = []
        lons = []
        for i in xrange(len(latitudes)):
    
                k=utm.to_latlon(latitudes[i], longitudes[i], 30, 'N')
                lats.append(k[0])
                lons.append(k[1])
                
    elif app.option =="Accidentes_Mortales":
        
        app.df=pd.read_csv('Expedientes.csv', delimiter = ';')
        Expedientes_muertos = app.df[app.df["N_Muertos"] >0]
        latitudes_muertos = Expedientes_muertos['GPS_x'].astype(float).tolist()
        longitudes_muertos = Expedientes_muertos['GPS_y'].astype(float).tolist()

        for i in xrange(len(latitudes_muertos)):
            if latitudes_muertos[i] > 999999 :
                latitudes_muertos[i] = latitudes_muertos[i]/1000

        for i in xrange(len(longitudes_muertos)):
            if longitudes_muertos[i] > 9999999 :
                longitudes_muertos[i] = longitudes_muertos[i]/1000
      

        latitudes_muertos = [float(lat) for lat in latitudes_muertos]
        longitudes_muertos = [float(lon) for lon in longitudes_muertos]
        lats = []
        lons = []
        for i in xrange(len(latitudes_muertos)):
    
                k=utm.to_latlon(latitudes_muertos[i], longitudes_muertos[i], 30, 'N')
                lats.append(k[0])
                lons.append(k[1])
                
    elif app.option =="Accidentes_Graves":
        
        app.df=pd.read_csv('Expedientes.csv', delimiter = ';')
        Expedientes_graves = app.df[(app.df["N_Muertos"] ==0) & (app.df["N_Graves"] >0)]
        latitudes_graves = Expedientes_graves['GPS_x'].astype(float).tolist()
        longitudes_graves = Expedientes_graves['GPS_y'].astype(float).tolist()

        for i in xrange(len(latitudes_graves)):
            if latitudes_graves[i] > 999999 :
                latitudes_graves[i] = latitudes_graves[i]/1000

        for i in xrange(len(longitudes_graves)):
            if longitudes_graves[i] > 9999999 :
                longitudes_graves[i] = longitudes_graves[i]/1000
      

        latitudes_graves = [float(lat) for lat in latitudes_graves]
        longitudes_graves = [float(lon) for lon in longitudes_graves]
        lats = []
        lons = []
        for i in xrange(len(latitudes_graves)):
    
                k=utm.to_latlon(latitudes_graves[i], longitudes_graves[i], 30, 'N')
                lats.append(k[0])
                lons.append(k[1])
                
    elif app.option =="Accidentes_Leves": 
        
        app.df=pd.read_csv('Expedientes.csv', delimiter = ';')
        Expedientes_leves = app.df[(app.df["N_Muertos"] ==0) & (app.df["N_Graves"] ==0) & (app.df["N_Leves"] >0)]
        latitudes_leves = Expedientes_leves['GPS_x'].astype(float).tolist()
        longitudes_leves = Expedientes_leves['GPS_y'].astype(float).tolist()

        for i in xrange(len(latitudes_leves)):
            if latitudes_leves[i] > 999999 :
                latitudes_leves[i] = latitudes_leves[i]/1000

        for i in xrange(len(longitudes_leves)):
            if longitudes_leves[i] > 9999999 :
                longitudes_leves[i] = longitudes_leves[i]/1000
      

        latitudes_leves = [float(lat) for lat in latitudes_leves]
        longitudes_leves = [float(lon) for lon in longitudes_leves]
        lats = []
        lons = []
        for i in xrange(len(latitudes_leves)):
    
                k=utm.to_latlon(latitudes_leves[i], longitudes_leves[i], 30, 'N')
                lats.append(k[0])
                lons.append(k[1])

    ###
            
        #Mapa de accidentes
        zoom = 14
        rad = 30
        gmap = gmplot.GoogleMapPlotter(39.481936, -0.376628, zoom)
        gmap.heatmap(lats, lons, radius = rad)
#        gmap.scatter(lats, lons, '#3B0B39', size=50, marker=False)
        gmap.draw("Templates/Accidentes_total.html")
    return render_template('Accidentes_total.html')
        
    #return render_template('choropleth.html')
if __name__ == '__main__':
    app.run(port=33507)
