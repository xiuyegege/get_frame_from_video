# get_frame_from_video
往video_src文件夹中放入视频，读取这些视频，并抽帧获取图片。

这个脚本是为了方便我从视频当中抽帧提取图片写的。

“get_img_video_by_thread.py”是多线程并发，提取速度更快。直接执行这个脚本就行。
脚本中，抽帧的间隔帧数变量值 every 设置的默认是30帧，可以自行更改。

创建一个文件夹，名字为：video_src，在这个文件夹中放入视频文件。
创建一个文件夹：名字为：imgs ,取出的图片会存入这个文件夹中
