from bemfa import Connect
import pyaudio
import json
from voice_cmd_recongnize import VoiceCommandRecognizer

def load_config(config_file="config.json"):
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    return config_data

config_data =load_config("config.json")
CONFIG = config_data['CONFIG']
AUDIO_PARAMS = config_data['AUDIO_PARAMS']
COMMAND_MAP = config_data['COMMAND_MAP']

#创建bemfa
uid = "0742b4ae2f2c4e1a8ef41a715647bec8"
topic = "raspi"
i = 5
send1 = Connect(uid, topic)
send1.ConnTCP()

#创建在线录音对象
recognizer = VoiceCommandRecognizer(CONFIG, AUDIO_PARAMS, COMMAND_MAP)

def Send_bemfa():
    result = recognizer.indentify()
    print(result)
    send1.Send_Message(str(result))

if __name__ =="__main__":
    while True:
        Send_bemfa()


