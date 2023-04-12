# CO2 Emissions REST API

## Serve the REST API

`uvicorn co2_emissions_api.api.main:app --reload --port 8888 --host 0.0.0.0`

and open it in your web browser [http://localhost:8888](http://localhost:8888)



## Deployment on fly.io (free cloud service)

### Update requirements.txt

`poetry export --format=requirements.txt --output=requirements.txt --without-hashes`

- blabla
- blabla
