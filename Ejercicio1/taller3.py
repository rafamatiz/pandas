import pandas as pd
df=pd.read_csv("entrada.csv",sep="|",low_memory=False)

lista=['ANI / CPN indicator',
'Call type',
'Carrier connect date',
'Carrier connect time',
'Carrier elapsed time',
'Dialing and presubscription indicator',
'IC / INC Routing Indicator',
'IC / INC indicator',
'IC/INC call event status',
'Operator action',
'Overseas indicator',
'Recording Office_ID',
'Recording Office_Type',
'Sensor_ID',
'Sensor_Type',
'Service feature code',
'Service observed / Traffic sampled',
'Study indicator',
'Time',
'Timing indicator',
'Trunk Group Number'
]

def calsegundos(s):
    if ':' in s:
        min=s.split(':',1)[0]
        seg=s.split(':',1)[1]
        return min*60*1000+seg*1000
    return s

salida=df[lista].copy()
diccionario = {5:"Local message rate call",110:"Interlata call",119:"Incoming CDR",90:None}
salida['Type']=df["Call type"].apply(lambda x: diccionario[(x)])

df['tr1'],df['tr2']=df["Trunk Identification_Routing Indicator"].str.split(",").str
df['tr3'],df['tr4']=df["Trunk Identification_Trunk Group Number"].str.split(",").str
df['tr5'],df['tr6']=df["Trunk Identification_Trunk Member Number"].str.split(",").str

salida['m104.trunkid']=df['tr1']+":"+df['tr3']+":"+df['tr5']
salida['m104.trunkid1']=df['tr2']+":"+df['tr4']+":"+df['tr6']

salida['m119.trunkgroupinfo']=df["Trunk Group_Trunk Group Number - Interoffice"]

salida['originatingnpa']=df["Calling number"].str[:3]
salida['terminatingnpa']=df["Called number"].str[:3]
salida['originatingnumber']=df["Calling number"].str[4:12]
salida['terminatingnumber']=df["Called number"].str[4:12]

salida['elapsedtime']=df["Length of call"].apply(lambda x: calsegundos(str(x)))

salida.to_csv("salidafinal.csv",index=False,sep="|")
