# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 10:55
# @Author  : Lincvic
# @Email   : lincvic@yahoo.com
# @File    : run.py
# @SoftwareName: PyCharm

from custom_voice_Util import ssmlBuilder, creatRequest
from speech_util import record, speech_2_text
import wave
import pyaudio


def play():
    '''

    播放音频
    :return: nil

    '''
    filepath = "output.wav"
    f = wave.open(filepath, 'rb')
    player = pyaudio.PyAudio()
    pms = f.getparams()
    nchannels, sampwidth, framerate, nframes = pms[:4]
    s = player.open(format=player.get_format_from_width(sampwidth),
                    channels=nchannels,
                    rate=framerate,
                    output=True)
    data = f.readframes(1024)
    while True:
        data = f.readframes(1024)
        s.write(data)


if __name__ == '__main__':
    # 录音
    record()

    # To Text
    data = speech_2_text()
    print(data)

    # 变声
    # TODO ssmlBuilder 三个参数分别对应， 语言、 Endpoint声音名称、 要转换为语音的语句
    ssml = ssmlBuilder("zh-CN", " ", data)
    creatRequest(ssml)

    # 播放
    print("音频播放中....")
    play()
