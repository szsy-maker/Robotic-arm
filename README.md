#无接触智能识别机械臂
---
##主要使用python库
- 计算机视觉和机器学习 --> opencv TensorFlow mediapipe yolo
- 通信协议 --> sokect
- 互联网+框架 --> [参考巴法云](https://bemfa.com/)
- 输出硬件接口 --> ~~前舵机控制RPi.GPIO​​~~ 现舵机控制Arm_Lib Oled显示 Adafruit_SSD1306 PIL
- 语音识别 --> 百度aip pyaudio 
- 数据处理 --> re numpy ast
---
## 变动
- 2024.6.9立项
- python --version 应该是3.9
- 执行程序在new,分不同的文件夹表示不同发方案与运行设备
- 增加了语音识别,更智能的bemfa云互联网方案/voice
- 增加了oled调用
- 2025.8.9改程序结构，树莓派4b改为使用jetson nano
- 环境应该不能乱装其他机器学习方面的库
---
## 结构
- 项目根目录
  - ├─demo #演示用程序
  - ├─improvement #用于性能改进的测试
  - │  └─bemfa_hand
  - ├─new #最新的程序结构，可以直接使用
  - │  ├─important
  - │  ├─nano_bemfa #开发板bemfa云下运行程序
  - │  ├─nano_mediapipe #开发板本地运行mediapipe
  - │  ├─pc_medaipipe_sokect #笔电发送端+局域网下直接sokect通信
  - │  ├─pc_mediapipe_bemfa #笔电发送端+手部识别+bemfa
  - │  └─pc_voice_bemfa #笔电发送端+语音识别+bemfa
  - ├─step_motor_test 步进舵机测试程序
  - ├─test_old 部分老程序，部分模块的测试程序
  - └─voice 语音识别的测试程序
---
## 快速部署
- `git clone https://github.com/szsy-maker/Robotic-arm`
- `cd Robotic-arm`
- `pip install -r requirements.txt`
- ~~混乱的requirements~~
<p>还在改进:(<p>


