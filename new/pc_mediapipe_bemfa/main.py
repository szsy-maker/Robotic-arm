from pc_mediapipe_bemfa import Mediapipe
uid = "0742b4ae2f2c4e1a8ef41a715647bec8"
topic = "raspi"
state_num = 6 # 01234 一共六个
joint_list = [[7, 6, 5], [11, 10, 9], [15, 14, 13], [19, 18, 17], [4, 3, 2]]  # 手指关节序列

if __name__ == '__main__':
    hand1 = Mediapipe(joint_list,state_num,uid, topic)
    hand1.Setup()
    hand1.Start()