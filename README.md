# pocksite-api

## Run

```bash
uvicorn app.main:app --reload --port 8001
```


## Docker

```bash
docker build -t pockite-api .
docker run -p 8001:8001 pockite-api
```