from new.pc_voice_bemfa import voice_cmd_recongnize
import pyaudio
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
    "打开": ["开", "打开", "开启", "启动"],
    "关闭": ["关", "关闭", "关掉", "停止"],
    "向上转": ["上"],
    "向下转": ["下"],
    "左转": ["左"],
    "右转": ["右"]
}

recognizer = (voice_cmd_recongnize.VoiceCommandRecognizer(CONFIG, AUDIO_PARAMS, COMMAND_MAP))
# 单次调用示例
result = recognizer.indentify()
print(f"结果: {result}")