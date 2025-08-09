'''
调用百度api的语音指令，具体使用参考代码
'''
from aip import AipSpeech
import pyaudio
import wave

from typing import Optional, Dict, List, Union


class VoiceCommandRecognizer:

    def __init__(self, config: Dict[str, str], audio_params: Dict[str, Union[int, str]] = None,
                 command_map: Dict[str, List[str]] = None):
        self.client = AipSpeech(config['APP_ID'], config['API_KEY'], config['SECRET_KEY'])
        self.audio_params = audio_params or self._get_default_audio_params()
        self.command_map = command_map or self._get_default_command_map()
        self.output_file = self.audio_params['WAVE_OUTPUT_FILENAME']

    def record_audio(self, output_file: Optional[str] = None) -> None:
        output_file = output_file or self.output_file
        p = pyaudio.PyAudio()

        stream = p.open(
            format=pyaudio.paInt16,
            channels=self.audio_params['CHANNELS'],
            rate=self.audio_params['RATE'],
            input=True,
            frames_per_buffer=self.audio_params['CHUNK']
        )
        print("start......")
        frames = [stream.read(self.audio_params['CHUNK'])
                  for _ in range(int(self.audio_params['RATE'] / self.audio_params['CHUNK'] *
                                     self.audio_params['RECORD_SECONDS']))]

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(self.audio_params['CHANNELS'])
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.audio_params['RATE'])
            wf.writeframes(b''.join(frames))

        print("end")

    def recognize_speech(self, audio_file: Optional[str] = None) -> Optional[str]:
        audio_file = audio_file or self.output_file

        with open(audio_file, 'rb') as f:
            audio_data = f.read()

        result = self.client.asr(audio_data, 'wav', self.audio_params['RATE'], {'dev_pid': 1537})

        if result.get('err_no') == 0:
            return result['result'][0]
        else:
            print(f"识别失败: {result.get('err_msg', '未知错误')}")
            return None

    def process_command(self, command_text: Optional[str]) -> Optional[str]:
        if not command_text:
            return None

        print(f"识别结果: {command_text}")

        for action, keywords in self.command_map.items():
            if any(keyword in command_text for keyword in keywords):
                print(f"指令——{action}")
                return action

        print("未识别到有效指令")
        return None

    def indentify(self) -> Optional[str]:

        self.record_audio()
        recognized_text = self.recognize_speech()
        return self.process_command(recognized_text)

    def run_continuously(self) -> None:
        while True:
            input("\n按Enter键开始录音，按Ctrl+C退出...")
            self.indentify()


if __name__ == "__main__":
    # 百度语音识别API配置
    # 牢刚的api
    CONFIG = {
        "APP_ID": "33572742",
        "API_KEY": "G4evlhpvvcvtrOACGElE0hp1",
        "SECRET_KEY": "giYGTGDF8BQ5W5rtEnC8gcKSzBH1jgnf"
    }
    # 音频参数配置
    AUDIO_PARAMS = {
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

    recognizer = VoiceCommandRecognizer(CONFIG, AUDIO_PARAMS, COMMAND_MAP)
    # 单次调用示例
    result = recognizer.indentify()
    print(f"结果: {result}")

    # 连续调用示例
    # recognizer.run_continuously()
