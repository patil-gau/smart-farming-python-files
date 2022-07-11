from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import requests as req
# import RPi.GPIO as GPIO
from time import sleep



mode = "auto"


app = Flask('__name__')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='smartuser', password='smartuser', server='localhost', database='smartfarming')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)  


# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(motarpin,GPIO.OUT)

# GPIO.setup(fanpin,GPIO.OUT)

# GPIO.setup(lightpin,GPIO.OUT)

motarpin = 15
fanpin = 11
lightpin = 13


class sensor_value(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    moisture_value = db.Column(db.Integer)
    ld_value = db.Column(db.Integer)
    temp_value = db.Column(db.Float)
    motar_state = db.Column(db.String(10))
    light_state = db.Column(db.String(10))
    fan_state = db.Column(db.String(10))




@app.route('/getValues',methods=['GET'])
def getValues():
    global mode
    indata = request.query_string
    print(indata)
    try:
       dataToSend = {}      
       result = db.session.query(sensor_value).order_by(sensor_value.id.desc()).first()
       print(result)
       
       moisture_value = result.moisture_value

       ldr_value = result.ld_value

       temp_value = result.temp_value

       motar_state = result.motar_state

       light_state = result.light_state

       fan_state = result.fan_state

       dataToSend['moisture_value'] = moisture_value

       dataToSend['ldr_value'] = ldr_value

       dataToSend['temp_value'] = temp_value

       dataToSend['motar_state'] = motar_state

       dataToSend['light_state'] = light_state

       dataToSend['fan_state'] = fan_state
       return jsonify({"result":dataToSend,"status":1,"message":"success"})

    except Exception as e:
       print("Error :", str(e))

       return jsonify({"result":{},"status":0,"message":str(e)})


@app.route('/selectmode',methods=['POST'])
def selectMode():
   global mode
   mode = request.get_json()['mode']
   return jsonify({"result":"success"})
 
@app.route('/motar',methods=['POST'])
def manualMotar():
   global mode
   state = request.get_json()['state']
   print(type(state))
   inmode = request.get_json()['mode']
   if mode == inmode:
    #    GPIO.output(motarpin,state) 
       return jsonify({"result":"success"})
   else:
       return jsonify({"result":"wrong mode set"})
       
@app.route('/light',methods=['POST'])
def manualLight():
   global mode
   state = request.get_json()['state']
   inmode = request.get_json()['mode']
   print(state)
   if mode == inmode:
    #    GPIO.output(lightpin,state) 
       return jsonify({"result":"success"})
   else:
       return jsonify({"result":"wrong mode set"})
   
@app.route('/fan',methods=['POST'])
def manualfan():
   global mode
   state = request.get_json()['state']
   inmode = request.get_json()['mode']
   if mode == inmode:
    #    GPIO.output(fanpin,state) 
       return jsonify({"result":"success"})
   else:
       return jsonify({"result":"wrong mode set"})
   
       



if __name__ == '__main__':

    app.run(host="0.0.0.0",debug=True,port=8000)

    

    
 
