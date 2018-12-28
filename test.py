import pandas as pd
file=open("header.txt")
line=file.readline()
headers=line.split('|')
headers=[i.replace("\n","") for i in headers]

df=pd.read_csv("file",sep="|",low_memory=False)
df=df.drop(df.columns[len(df.columns)-1],axis=1)
df.columns = headers
#print(df.head())

lista=[]

for i in range(1,len(df.columns)):
    row={}
    row["Field"]=df.columns[i]
    row["Type"]=str(df[df.columns[i]].dtypes)
    df_aux = df[df.columns[i]].value_counts()
    if len(df_aux) == 0:
        row["information"]="Static Null"
        row["Value"] = str(df[df.columns[i]].iloc[0])
    else:
        if len(df_aux) == 1:
            row["information"]="Static"
            row["Value"] = str(df[df.columns[i]].iloc[0])
        else:
            row["information"]="Dinamic"
            row["Value"] = "See more values"
    lista.append(row)

aux= pd.json.dumps(lista)
df1=pd.read_json(aux)
diccionario={"float64":"Float","object":"String","int64":"Integer"}
df1["Type"] = df1["Type"].apply(lambda  x : diccionario[str(x).lower()])
df1.to_csv("output.csv",index=False)

print (df1.head())







