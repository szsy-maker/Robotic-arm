import voice_cmd_recongnize
import json

def load_config(config_file="config.json"):
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    return config_data

config_data =load_config("config.json")

CONFIG = config_data['CONFIG']
AUDIO_PARAMS = config_data['AUDIO_PARAMS']
COMMAND_MAP = config_data['COMMAND_MAP']

recognizer = voice_cmd_recongnize.VoiceCommandRecognizer(CONFIG, AUDIO_PARAMS, COMMAND_MAP)
# 单次调用示例
result = recognizer.indentify()
print(f"结果: {result}")