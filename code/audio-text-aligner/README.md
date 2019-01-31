# Forced alignment

## Usage

To try the REST server, run the following then visit <http://localhost:5000/>

```shell
virtualenv -p python3 venv
source venv/bin/activate
pip install numpy
pip install -r requirements.txt
python app.py
```

To download generated split audio and script, try `curl -X POST "http://localhost:5000/align/download/" -H "Content-Type: application/x-www-form-urlencoded" -d "zip_file=static%2Fupload%2Fattempts%2Fmyuploaded.mp3.audio_script.zip" > split.zip`.
