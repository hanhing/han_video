import os
from django.conf import settings
import time
import shutil
from app.libs.base_qiniu import video_qiniu
from app.models import VideoSub, Video
from app.tasks.task import video_task


def check_and_get_video_type(type_obj, type_value, message):
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}
    return {'code': 0, 'msg': 'success'}


def remove(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


def handle_video(video_file, video_id, number):
    path = os.path.join(settings.BASE_DIR, 'app\\dashboard\\temp')
    name = '{}_{}'.format(int(time.time()), video_file.name)
    # path_name = path + '\\' +name
    path_name = 'F:\\Tmooc\\PROJECT\\han_video\\video\\app\\dashbboard\\temp\\' + name

    # FILE对象有个临时地址属性
    temp_path = video_file.temporary_file_path()
    # 将临时地址存入文件夹
    shutil.copyfile(temp_path, path_name)
    out_name = name.split('.')[0]
    out_path = 'F:\\Tmooc\\PROJECT\\han_video\\video\\app\\dashbboard\\temp_out\\{}'.format(out_name)
    command = 'ffmpeg -i {} -c copy {}.mp4'.format(path_name, out_path)
    video = Video.objects.get(pk=video_id)
    videosub = VideoSub.objects.create(
                video=video,
                url='',
                number=number
            )
    video_task(command, out_path, path_name, video_file.name, videosub.id)
    return False