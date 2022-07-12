import json
import requests
import pandas as pd

# tokeGen = "https://<ArcServerDomain>/server/admin/generateToken"
# dir = "https://<ArcServerDomain>/server/admin/services/"




# Generate Token
username = input("username")
password = input("password")
client = "requestip"
tokeDict = { 'username': username, 'password': password, 'client': client, 'f':'json' }

tokePost = requests.post(url=tokeGen, data=tokeDict)
tokeResp = json.loads(tokePost.text)
token = tokeResp['token']

# Data Fields
fldr = []
serviceName = []
serviceURL = []
serviceType = []
serviceDB = []
serviceServer = []
serviceDBUser = []
serviceDataset = []
onPremPath = []
pubClient = []

parameters = {"token":token, "f":"json"}
dirGet = requests.get(dir, params=parameters)
dirResp = json.loads(dirGet.text)
folders = dirResp["folders"]
rootServices = dirResp["services"]
if rootServices != []:
    for srv in rootServices:
        rootServName = rootServices[0]["serviceName"]
        rootServType = rootServices[0]["type"]
        rootServURL= (dir + "/"+ rootServName + "." + rootServType)
        root = "/"

        mani = rootServURL + "/iteminfo/manifest/manifest.json"
        maniParameters = {"token":token}
        maniGet = requests.get(mani, params=maniParameters)
        maniHeaders = maniGet.headers
        if maniHeaders['Content-Type'] != 'application/json;charset=UTF-8':
            fldr.append(root)
            serviceName.append(rootServName)
            serviceURL.append(rootServURL)
            serviceType.append(rootServType)
            serviceDB.append("No Manifest")
            serviceServer.append("No Manifest")
            serviceDBUser.append("No Manifest")
            serviceDataset.append("No Manifest")
            onPremPath.append("No Manifest")
            pubClient.append("No Manifest")
        else:
            maniResp = json.loads(maniGet.text)
            if maniResp["databases"] != []:
                for db in maniResp["databases"]:
                    parsedb =db["onPremiseConnectionString"].replace(":", "-").replace(";",'","').replace("\\","\\\\")
                    parsedb2 = '{"' + str(parsedb).replace("=","' : '").replace("'", '"') + '"}'
                    dbjson = json.loads(parsedb2)
                    for ds in db["datasets"]:
                        fldr.append(root)
                        serviceName.append(rootServName)
                        serviceURL.append(rootServURL)
                        serviceType.append(rootServType)
                        serviceDB.append(dbjson['DATABASE'])
                        serviceDataset.append(ds["onServerName"])
                        if 'DB_CONNECTION_PROPERTIES' in dbjson:
                            serviceServer.append(dbjson['DB_CONNECTION_PROPERTIES'])
                            serviceDBUser.append(dbjson["USER"])
                        else:
                            serviceServer.append("")
                            serviceDBUser.append("")
                        for res in maniResp['resources']:
                            onPremPath.append(res["onPremisePath"])
                            pubClient.append(res["clientName"])
            else:
                for res in maniResp['resources']:
                    fldr.append(root)
                    serviceName.append(rootServName)
                    serviceURL.append(rootServURL)
                    serviceType.append(rootServType)
                    serviceDB.append("")
                    serviceServer.append("")
                    serviceDBUser.append("")
                    serviceDataset.append("")
                    onPremPath.append(res["onPremisePath"])
                    pubClient.append(res["clientName"])

for fld in folders:
    fldURL = dir + fld
    fldGet = requests.get(fldURL, params=parameters)
    if fld != [] and fld not in ['System', 'Utilities']:
        fldResp = json.loads(fldGet.text)
        services = fldResp["services"]
        if services != []:
            for srvs in services:
                servName = srvs["serviceName"]
                servType = srvs["type"]
                servURL = (dir + fld + "/"+ servName + "." + servType)
                servFld = fld      
                mani = servURL + "/iteminfo/manifest/manifest.json"
                maniParameters = {"token":token}
                maniGet = requests.get(mani, params=maniParameters)
                # print(maniGet.url)
                maniHeaders = maniGet.headers
                if maniHeaders['Content-Type'] != 'application/json;charset=UTF-8':
                        fldr.append(servFld)
                        serviceName.append(servName)
                        serviceURL.append(servURL)
                        serviceType.append(servType)
                        serviceDB.append("No Manifest")
                        serviceServer.append("No Manifest")
                        serviceDBUser.append("No Manifest")
                        serviceDataset.append("No Manifest")
                        onPremPath.append("No Manifest")
                        pubClient.append("No Manifest")
                else:
                    maniResp = json.loads(maniGet.text)
                    if maniResp["databases"] != []:
                        for db in maniResp["databases"]:
                            parsedb =db["onPremiseConnectionString"].replace(":", "-").replace(";",'","').replace("\\","\\\\")
                            parsedb2 = '{"' + str(parsedb).replace("=","' : '").replace("'", '"') + '"}'
                            dbjson = json.loads(parsedb2)
                            # print(dbjson)
                            for ds in db["datasets"]:
                                fldr.append(servFld)
                                serviceName.append(servName)
                                serviceURL.append(servURL)
                                serviceType.append(servType)
                                serviceDB.append(dbjson['DATABASE'])
                                serviceDataset.append(ds["onServerName"])
                                if 'DB_CONNECTION_PROPERTIES' in dbjson:
                                    serviceServer.append(dbjson['DB_CONNECTION_PROPERTIES'])
                                    if dbjson['AUTHENTICATION_MODE'] == "OSA":
                                        serviceDBUser.append("OSA")
                                    else:
                                        serviceDBUser.append(dbjson["USER"])
                                    
                                else:
                                    serviceServer.append("")
                                    serviceDBUser.append("")
                                for res in maniResp['resources']:
                                    onPremPath.append(res["onPremisePath"])
                                    pubClient.append(res["clientName"])
                    else:
                        for res in maniResp['resources']:
                            fldr.append(servFld)
                            serviceName.append(servName)
                            serviceURL.append(servURL)
                            serviceType.append(servType)
                            serviceDB.append("")
                            serviceServer.append("")
                            serviceDBUser.append("")
                            serviceDataset.append("")
                            onPremPath.append(res["onPremisePath"])
                            pubClient.append(res["clientName"])

colNames = ["fldr",
"serviceName",
"serviceURL",
"serviceType",
"serviceDB",
"serviceServer",
"serviceDBUser",
"serviceDataset",
"onPremPath",
"pubClient"]

df = pd.DataFrame(list(zip(fldr,
serviceName,
serviceURL,
serviceType,
serviceDB,
serviceServer,
serviceDBUser,
serviceDataset,
onPremPath,
pubClient)), columns=colNames)
# print(df)
df.to_csv(r"<Directory>\\Manifest.csv")


