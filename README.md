# CO2 Emissions REST API

## Serve the REST API

`uvicorn co2_emissions_api.api.main:app --reload --port 8888 --host 0.0.0.0`

and open it in your web browser [http://localhost:8888](http://localhost:8888)



## Deployment on fly.io (free cloud service)

### Update requirements.txt

`poetry export --format=requirements.txt --output=requirements.txt --without-hashes`

### Remote development from [GitHub Codespaces](https://github.com/features/codespaces)

1. Open your Codespace from the GitHub repo by clicking on the green button "Code" > "Codepsaces".
1. Build you Docker image: `docker build -t local:latest .`
1. Try to run the app from a Docker container: `docker run -it local:latest`

### Deployment with Fly.io (from Linux/Ubuntu)

1. Install the fly.io CLI (flyctl): `curl -L https://fly.io/install.sh | sh`
1. Sign in with flyctl: `flyctl auth login` and click on the generated URL
1. Deploy the app with Fly.io which will detect the Dockerfile available in the repo and assumes that the app runs on port 8080: `fly launch --now`
