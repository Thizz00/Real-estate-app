# Real-estate-app 🏠

<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white"/>  <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white"/>  <img src = "https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>

## A brief description:

Application that allows you to scrap information about announcements of current real estate data for apartments for *sale* for two websites ie:

* https://www.olx.pl
* https://www.otodom.pl

## Cloud streamlit

Test applications via cloud streamlit: https://real-estate-app-poland.streamlit.app

## Run Locally

#### Clone the project

```bash
  git clone https://github.com/Thizz00/Real-estate-app.git
```

## Logs

#### If you want the logs to be saved on any path, add to docker-compose.yaml:
```yaml
  volumes:
      - "your-path:/app/logs"
  ```
## Build a Docker image

```bash
  docker-compose build
```

### Start container

```bash
  docker-compose up
```

### Stop container

```bash
  docker-compose down
```

## Author

- [@Thizz00](https://github.com/Thizz00)
