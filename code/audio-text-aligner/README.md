# Forced alignment

## Usage

To try the REST server, run the following then visit <http://localhost:5000/>

```shell
docker build --no-cache=true -t alignservice .
docker run -d -p 5000:5000 alignservice
```

To download generated split audio and script, try `curl -X POST "http://localhost:5000/align/download/" -H "Content-Type: application/x-www-form-urlencoded" -d "zip_file=static%2Fupload%2Fattempts%2Fmyuploaded.mp3.audio_script.zip" > split.zip`.
