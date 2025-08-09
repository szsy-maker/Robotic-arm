import time
from new.pc_voice_bemfa import voice_cmd_recongnize, bemfa
import pyaudio

# bafa

uid = "0742b4ae2f2c4e1a8ef41a715647bec8"
topic = "raspi"
send1 = bemfa.Connect(uid, topic)
send1.ConnTCP()

# 测试输出模式
#     send1.Get_Message()
# while True:
#     print(send1.Out_put())

# 测试输入模式

CONFIG = {
    "APP_ID": "33572742",
    "API_KEY": "G4evlhpvvcvtrOACGElE0hp1",
    "SECRET_KEY": "giYGTGDF8BQ5W5rtEnC8gcKSzBH1jgnf"
}
# 音频参数配置（可选）
AUDIO_PARAMS = {
    'FORMAT': pyaudio.paInt16,
    'CHANNELS': 1,
    'RATE': 16000,
    'CHUNK': 1024,
    'RECORD_SECONDS': 3,
    'WAVE_OUTPUT_FILENAME': "output.wav"
}

# 指令模糊表
COMMAND_MAP = {
    "你好": ["你好"],
    "打开": ["开", "打开", "开启", "启动"],
    "关闭": ["关", "关闭", "关掉", "停止"],
    "上转": ["上", "尚"],
    "下转": ["下", '夏'],
    "左转": ["左", "做", "坐", "作"],
    "右转": ["右", "有", "又", ]
}
while True:
    recognizer = (voice_cmd_recongnize.VoiceCommandRecognizer(CONFIG, AUDIO_PARAMS, COMMAND_MAP))
    # 单次调用示例
    result = recognizer.indentify()
    send1.Send_Message(result)
    time.sleep(1)
    print(f"结果: {result}")
