# arcManifest

This script was created to create a consolidated list of all REST services located on a ArcGIS ArcServer. The output of this script is a csv file. The csv file will include various infomation related to each service including; server name, service folder, service name, service URL, service type, service database, service database server, service database user, service database datasets, on premise path, and publishing client.

## Getting Started

This script was developed using python version 3.7.11 which was included in ArcGIS Pro.

### Prerequisites

Python 3 is needed to run this script. It is recommended to use the Python 3 that is installed with ESRI's ArcGIS PRO Software, but should be able to run using the standard download.

**Python Modules**

```python
import json
import requests
import pandas as pd
from pathlib import Path
```

**Folder Structure (Script is Relative Path applicable)**

```text
📁arcManifest/
    📝README.md
    📁.git/
    📁Data/
        📝Manifest.csv
    📁Documentation/
    📁Script/
        📝arcManifest.py
        📝connInfo.json
```

## Installing

1. Set up folder structure (If not downloaded from GitHub):

```text
📁arcManifest/
    📝README.md
    📁.git/
    📁Data/
        📝Manifest.csv
    📁Documentation/
    📁Script/
        📝arcManifest.py
        📝connInfo.json
```

2. Link to ArcGIS ArcServer Admin (Multiple servers can be added):

```json
    connInfo.json
        {
            "ServerName": "<Server Name>",
            "TokenGenURL": "https://<ArcServer>/server/admin/generateToken",
            "DirURL": "https://<ArcServer>/server/admin/services/",
            "Username": "",
            "Password": ""
        }
```

## Running the full script

The script is now able to run using the full script using Python 3 via ArcGIS Pro.
This script can be ran in terminal or on a schedule task. 

## Built With

* [ArcGIS Pro 2.4 +](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview) - Software
* [Python 3.7.11](https://www.python.org/downloads/release/python-3711/) - Code Language

## Versioning

* **Update "Installing" section with current version of script after version update.**
* V1.0
  * Initial code.
  * Had manuel entry of username and password.
  * Script used hard coded server urls. 
* V2.0 (Current Version)
  * Modified code read from a json file for url connections and credentials.
  * Using the json file, the script can iterate through multiple ArcServers now. 
  * Created README.md documentation


## Authors

* **Daniel Huneycutt** - Programmer Analyst IV - City of Norfolk, Information Technology, Application Development, GIS Bureau :earth_americas:

## Trouble Shooting & Tips
* none yet!
