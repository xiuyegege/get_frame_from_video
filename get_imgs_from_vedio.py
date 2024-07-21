# 引入所需库
import cv2
import os
from decord import VideoReader, cpu


# 定义一个函数用于从单个视频中提取帧
def extract_frames(video_path, frames_dir, every, overwrite=False):
    # 创建 VideoReader 对象来读取视频，ctx=cpu(0) 表示使用 CPU 处理
    vr = VideoReader(video_path, ctx=cpu(0))

    # 获取视频文件名（去掉扩展名）
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)

    # 初始化保存的帧数计数器
    saved_count = 0

    # 遍历视频的每一帧，步长为 'every'，即每 'every' 帧提取一次
    for index in range(0, len(vr), every):
        # 读取当前帧
        frame = vr[index]

        # 构建保存图片的路径，使用视频名称和帧序号作为图片名称
        save_path = os.path.join(frames_dir, f"{video_name}_{index:04d}.jpg")

        # 如果图片不存在或允许覆盖已存在的图片，则保存当前帧
        if not os.path.exists(save_path) or overwrite:
            # 转换颜色空间为 BGR（OpenCV 使用的颜色空间）并保存图片
            cv2.imwrite(save_path, cv2.cvtColor(frame.asnumpy(), cv2.COLOR_RGB2BGR))

            # 增加保存的帧数计数器
            saved_count += 1

    # 返回保存的帧数
    return saved_count


# 定义一个函数用于处理文件夹中的所有视频
def process_videos_in_folder(video_src_dir, frames_dir, every):
    # 遍历视频源目录中的所有文件
    for filename in os.listdir(video_src_dir):
        # 检查文件是否为 mp4 或 avi 视频文件
        if filename.endswith('.mp4') or filename.endswith('.avi'):
            # 构建视频文件的完整路径
            video_path = os.path.join(video_src_dir, filename)

            # 输出正在处理的视频文件名
            print(f"Processing video: {filename}")

            # 调用 extract_frames 函数提取并保存视频帧
            saved_count = extract_frames(video_path, frames_dir, every)

            # 输出提取了多少帧
            print(f"Extracted {saved_count} frames from {filename}")


# 主程序入口
if __name__ == "__main__":
    # 设置视频源目录和目标帧目录
    video_src_dir = './video_src'
    frames_dir = './imgs'

    # 用户输入提取帧的间隔
    every = int(input("请输入提取图片的间隔帧数："))

    # 调用函数处理目录中的所有视频
    process_videos_in_folder(video_src_dir, frames_dir, every)