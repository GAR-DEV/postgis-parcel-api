# postgis-parcel-api
RESTful API that can deliver NYS geoJSON tax parcel data given an SBL printkey and SWIS code. 

Currently being used and deployed on Azure at:
https://parcelview.azurewebsites.net/parcel?printkey={printkey here}&swis={swis here}

## .ENV file required format below:
WORK_DIR=
DB_HOST=
DB_NAME=
DB_PORT=5432
DB_USER=
PGPASSWORD=
