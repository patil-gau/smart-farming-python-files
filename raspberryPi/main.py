import serial 

import RPi.GPIO as GPIO

import mysql.connector as mysql

from time import sleep
import requests as req





api_url = "http://localhost:8000/"
plantName = input("Enter the plant name in want to grow ")



try: 

   conn=mysql.connect(

    host="localhost",

    user="myuser",

    password="Password",

    database="SmartAgriculture"    

    )

except Exception as error:   

    print(error)

    exit(0)

    

    

curs = conn.cursor()



curs.execute("select * from crops where cropName=%s",(plantName,))



result = curs.fetchone()



if result is None:

    print("we are sorry to inform you that the plant is not added in our database, please add it first")

    exit(0)



requiredMoistureValue =  int(result[2])

requiredTemperatureValue = float(result[4])

requiredLdrValue = int(result[3])



currentMoistureValue = 0

currentTemperatureValue = 0.0

currentLdrValue = 0



moistureFlag = 0

temperatureFlag = 0

ldrFlag = 0



motar_state = "OFF"

fan_state = "OFF"

light_state = "OFF"



PORT = '/dev/ttyUSB0'

BAURDRATE = 9600











ser = serial.Serial(

port=PORT,

baudrate=BAURDRATE,

)



while True:

  try:   

    values=ser.readline().decode('utf-8')     

    listOfAllValues = values.split(';')

    currentMoistureValue = int(listOfAllValues[0])

    currentTemperatureValue = float(listOfAllValues[1])

    currentLdrValue = int(listOfAllValues[2])

    print(f"Sensor Moisture value : {currentMoistureValue} Required Moisture Value {requiredMoistureValue}")

    print(f"Sensor Temperature value : {currentTemperatureValue} Required Temperature Value {requiredTemperatureValue}")

    print(f"Sensor LDR value : {currentLdrValue} Required LDR Value {requiredLdrValue}")

    

    if (currentMoistureValue > requiredMoistureValue):

       print("motar on ")

       if moistureFlag == 0:

         motar_state="ON"

         res = req.post(api_url+"motar",{"state":True,"mode":"auto"})

         moistureFlag = 1

    else:

        print("motar off ")

        if moistureFlag == 1:

            motar_state="OFF"

            moistureFlag = 0

            res = req.post(api_url+"motar",{"state":False,"mode":"auto"})

        

        

    if (currentTemperatureValue > requiredTemperatureValue ):

       print("fan on ")

       if temperatureFlag == 0:

         fan_state="ON"

         res = req.post(api_url+"fan",{"state":True,"mode":"auto"})

         temperatureFlag = 1

    else:

        print("fan off")

        if temperatureFlag == 1:

            fan_state="OFF"

            temperatureFlag = 0

            res = req.post(api_url+"fan",{"state":True,"mode":"auto"})

                  

    if (currentLdrValue < requiredLdrValue ):

       print("light On")

       if ldrFlag == 0:

         ldrFlag="ON"

         res = req.post(api_url+"light",{"state":True,"mode":"auto"})

         ldrFlag = 1

    else:

        print("light off")

        if ldrFlag == 1:

          ldrFlag="OFF"

          ldrFlag = 0

          res = req.post(api_url+"light",{"state":True,"mode":"auto"})

            

    curs.execute("INSERT INTO `sensor_value` VALUES(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE moisture_value=%s,ld_value=%s,temp_value=%s,motar_state=%s,light_state=%s,fan_state=%s",(1,currentMoistureValue,currentLdrValue,currentTemperatureValue,motar_state,light_state,fan_state,currentMoistureValue,currentLdrValue,currentTemperatureValue,motar_state,light_state,fan_state))  

    conn.commit()  

    sleep(10) 

       

  except Exception as error:

      print(error)

      

GPIO.cleanup()      
