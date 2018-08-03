# -*- coding: utf-8 -*-
# @Time    : 2018/7/29 14:44
# @Author  : Lincvic
# @Email   : lincvic@yahoo.com
# @File    : custom_voice_Util.py
# @SoftwareName: PyCharm

import requests
from custom_voice_Config import ENDPOINT, HOST_NAME, SUB_KEY, ENCODE_TYPE, GUID


def authentication():
    '''

    认证
    :return: Token

    '''
    headers = {
        'Ocp-Apim-Subscription-Key': SUB_KEY
    }

    response = requests.post(HOST_NAME, headers=headers)

    return response.content


def creatRequest(ssml):
    '''

    请求CustomVoice
    :param ssml: SSML XML Format
    :return:

    '''

    url = ENDPOINT
    authToken = authentication()
    encodeType = ENCODE_TYPE

    headers = {
        'Content-Type': 'application/ssml+xml',
        'X-MICROSOFT-OutputFormat': encodeType,
        'X-FD-ClientID': 'RadioStationService',
        'X-FD-ImpressionGUID': GUID,
        'User-Agent': 'TTSClient',
        'Authorization': authToken
    }



    response = requests.post(url, headers=headers, data=ssml.encode('utf-8'))
    response.raise_for_status()

    with open("output.wav", "wb") as f:
        f.write(response.content)

    return response


def ssmlBuilder(lang, voicename, text):
    '''

    构造ssml
    :param lang: 语言
    :param voicename: Custom Voice 语音名称
    :param text: 要转化为语音的文本
    :return: ssml text

    '''
    ssml = u"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='{0}'><voice name = '{1}'>{2}</voice></speak>"

    return ssml.format(lang, voicename, text)

if __name__ == '__main__':
    print(creatRequest(ssmlBuilder("zh-CN", "wangyijiang1", "你好")))

