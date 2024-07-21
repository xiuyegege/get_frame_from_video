import concurrent.futures
import cv2
import os
from decord import VideoReader, cpu


# 定义一个函数用于从单个视频中提取帧
def extract_frames(video_path, frames_dir, every, overwrite=False):
    vr = VideoReader(video_path, ctx=cpu(0))
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)

    saved_count = 0
    for index in range(0, len(vr), every):
        frame = vr[index]
        save_path = os.path.join(frames_dir, f"{video_name}_{index:04d}.jpg")

        if not os.path.exists(save_path) or overwrite:
            cv2.imwrite(save_path, cv2.cvtColor(frame.asnumpy(), cv2.COLOR_RGB2BGR))
            saved_count += 1

    return (video_path, saved_count)


# 使用线程池处理文件夹中的所有视频
def process_videos_in_folder(video_src_dir, frames_dir, every):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 收集所有要处理的任务
        futures = [executor.submit(extract_frames,
                                   os.path.join(video_src_dir, filename),
                                   frames_dir,
                                   every)
                   for filename in os.listdir(video_src_dir)
                   if filename.endswith('.mp4') or filename.endswith('.avi')]

        # 处理每个任务的结果
        for future in concurrent.futures.as_completed(futures):
            video_path, saved_count = future.result()
            print(f"Processed video: {video_path}")
            print(f"Extracted {saved_count} frames from {video_path}")


# 主程序入口
if __name__ == "__main__":
    video_src_dir = './video_src'
    frames_dir = './imgs'
    # every = int(input("请输入提取图片的间隔帧数："))
    every = 30

    process_videos_in_folder(video_src_dir, frames_dir, every)