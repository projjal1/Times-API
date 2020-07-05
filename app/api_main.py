import flask
from flask import request,jsonify,render_template
import requests as r
import json

app=flask.Flask(__name__)
app.config["DEBUG"]=True

invalid_req="<h1>Invalid Request</h1> <p>Check documentation for usage</p>"

@app.route('/',methods=['GET'])
def home():
    return render_template('base.html')
    
@app.route('/api-docs',methods=['GET'])
def docs():
    return render_template('docs.html')
    
@app.route('/refs',methods=['GET'])
def refs():
    return render_template('attr.html')
    
@app.route('/api/lat-long',methods=['GET'])
def api_lat_long():
    if 'city' in request.args:
        city=request.args['city']
        
        #Output dict to store data
        output=dict()
        
        #Now query url for city data
        url='http://open.mapquestapi.com/geocoding/v1/address?key=peVM41X5wGi9vpUZfV1iOzzGcJGj1uFk&location='+city
        response=r.get(url)
        
        #Now load into json contents of latitude and longitude 
        data=json.loads(response.content)
        output['country-code']=data['results'][0]['locations'][0]['adminArea1']
        output['county']=data['results'][0]['locations'][0]['adminArea3']
        output['co-ord']=data['results'][0]['locations'][0]['latLng']
        output['map-url']=data['results'][0]['locations'][0]['mapUrl']
        
        return jsonify(output)        
        
    else:
        return invalid_req
        
@app.route('/api/sunrise-sunset',methods=['GET'])
def api_sun_set():
    if 'city' in request.args:
        city=request.args['city']
        
        #Output dict to store data
        output=dict()
        
        #First load co-ordinate of city
        url='http://open.mapquestapi.com/geocoding/v1/address?key=peVM41X5wGi9vpUZfV1iOzzGcJGj1uFk&location='+city
        response=r.get(url)
        data=json.loads(response.content)
        co_ord=data['results'][0]['locations'][0]['latLng']
        lat,long=str(co_ord['lat']),str(co_ord['lng'])
        
        #Now query url for data
        url="https://api.sunrise-sunset.org/json?lat="+lat+"&lng="+long+"&date=today"
        response=r.get(url)
        data=json.loads(response.content)
        data=data['results']
        return jsonify(data)        
        
    else:
        return invalid_req    
        
app.run()