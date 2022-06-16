import json
from requests import Response
from streamlink import Streamlink, NoPluginError, StreamError
from flask import Flask, request, Response

app = Flask(__name__)

def isSupported(url:str):
    try:
        return Streamlink().streams(url)
    except NoPluginError as err:
        return err

def isStreaming(url):
    return True

def get_stream_list(url:str):
    temp = isSupported(url)
    if isStreaming(temp):
        return {key:temp[key] for key in temp}
    else:
        return temp

def read_stream(opened_stream, chunk_size:int):
    while True:
        yield opened_stream.read(chunk_size)


@app.route('/info/', methods=['POST'])
def get_streams():
    url = request.json['url']
    stream_list = get_stream_list(url)
    if type(stream_list) == NoPluginError:
        return str(stream_list), 404
    else:
        return {key:stream_list[key].json for key in stream_list}, 200

@app.route('/open/', methods=['POST'])
def open_stream():
    url = request.json['url']
    quality = request.json['quality']
    stream_list = get_stream_list(url)
    stream = stream_list[quality].open()
    response = Response(read_stream(stream, 1024), mimetype='multipart/x-mixed-replace; boundary=frame')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)