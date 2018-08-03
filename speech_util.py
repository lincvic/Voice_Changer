# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 17:23
# @Author  : Lincvic
# @Email   : lincvic@yahoo.com
# @File    : speech_util.py
# @SoftwareName: PyCharm
import pyaudio, requests
import wave
from speech_config import URL, PARAM, SUB_KEY, AUTH_HOST

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "speech.wav"


def record():
    '''

    录音
    :return: nil

    '''
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音, 录音有 " + str(RECORD_SECONDS) + " 秒")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


def auth():
    '''

    auth Token
    :return: Token

    '''

    headers = {
        "Ocp-Apim-Subscription-Key": SUB_KEY,
        "Content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(AUTH_HOST, headers=headers)

    response.raise_for_status()

    return response.text


def speech_2_text():
    '''

    转化为文本
    :return: text

    '''
    url = URL + PARAM
    headers = {
        "Content-type": "audio/wav; codec=\"audio/pcm\"; samplerate=16000",
        "Accept": "application/json;text/xml",
        "Authorization": "Bearer " + auth()
    }
    with open("speech.wav", "rb") as f:
        data = f.read()

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    data = response.json()

    return data['DisplayText']


if __name__ == '__main__':
    # record()
    print(speech_2_text())
