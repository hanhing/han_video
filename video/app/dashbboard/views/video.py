from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from app.libs.base_render import render_to_response
from app.utils.utils import dashboard_auth
from app.model.video import (VideoType, FromType, Nationality,
                             Video, VideoSub, IdentityType,
                             VideoStar)
from app.utils.common import check_and_get_video_type, handle_video


class ExternaVideo(View):  # 外链视频
    TEMPLATE = 'dashboard/video/externa_video.html'

    @dashboard_auth
    def get(self, request):
        error = request.GET.get('error', '')
        data = {'error': error}

        cus_videos = Video.objects.filter(from_to=FromType.custom.value)
        ex_videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['cus_videos'] = cus_videos
        data['ex_videos'] = ex_videos

        return render_to_response(request, self.TEMPLATE, data)

    # def post(self, request):
    #     name = request.POST.get('name')
    #     video_type = request.POST.get('video_type')
    #     img = request.POST.get('img')
    #     video_nationality = request.POST.get('video_nationality')
    #     from_to = request.POST.get('from_to')
    #     print(name, video_nationality, video_type, img, from_to)
    #     return redirect(reverse('externa_video'))


class ExternaVideoPost(View):  # 由上面的post存在跨域问题,所以改成get提交
    TEMPLATE = 'dashboard/video/externa_video.html'
    def get(self, request):
        name = request.GET['name']
        video_type = request.GET['video_type']
        img = request.GET['img']
        video_nationality = request.GET['video_nationality']
        from_to = request.GET['from_to']
        info = request.GET['info']
        # 视频编辑
        video_id = request.GET.get('video_id', '')
        if video_id:
            reverse_path = reverse('video_update', kwargs={'video_id': video_id})
        else:
            reverse_path = reverse('externa_video')
        if not all([name, video_nationality, video_type, img, from_to]):
            return redirect('{}?error{}'.format(reverse_path, '缺少必要的信息'))

        result = check_and_get_video_type(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error{}'.format(reverse_path, result['msg']))

        result = check_and_get_video_type(FromType, from_to, '非法的视频来源')
        if result.get('code') != 0:
            return redirect('{}?error{}'.format(reverse_path, result['msg']))

        result = check_and_get_video_type(Nationality, video_nationality, '非法的国籍')
        if result.get('code') != 0:
            return redirect('{}?error{}'.format(reverse_path, result['msg']))
        if not video_id:
            try:
                Video.objects.create(
                    name=name,
                    image=img,
                    video_type=video_type,
                    from_to=from_to,
                    nationality=video_nationality,
                    info=info,
                )
            except:
                return redirect('{}?error{}'.format(reverse_path, '创建失败'))
        else:
            try:
                video = Video.objects.get(pk=video_id)
                video.name = name
                video.image = img
                video.video_type = video_type
                video.from_to = from_to
                video.nationality = video_nationality
                video.info = info
                video.save()
            except:
                return redirect('{}?error{}'.format(reverse_path, '修改失败'))
        return redirect(reverse('externa_video'))
        # return render_to_response(request, self.TEMPLATE)

class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        error = request.GET.get('error', '')
        data['video'] = video
        data['error'] = error
        return render_to_response(request, self.TEMPLATE, data)
        # return render(request, self.TEMPLATE, data)
    # def post(self, request, video_id):
    #     pass
    # 由于mako csrf验证问题,所以改用get提交表单


class VideoSubGet(View):

    def post(self, request, video_id):
        number = request.POST.get('number')
        videosub_id = request.POST.get('videosub_id')
        video = Video.objects.get(pk=video_id)

        if FromType(video.from_to) == FromType.custom:
            url = request.FILES.get('url')
        else:
            url = request.POST.get('url')

        url_format = reverse('video_sub', kwargs={'video_id': video_id})
        if not all([url, number]):
            return redirect('{}?error={}'.format(url_format, '缺少必要字段'))

        if FromType(video.from_to) == FromType.custom:
            handle_video(url, video_id, number)
            return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

        video = Video.objects.get(pk=video_id)
        # 如果存在则为更新,不存在则创建
        if not videosub_id:
            try:
                VideoSub.objects.create(video=video, url=url, number=number)
            except:
                return redirect('{}?error={}'.format(url_format, '创建失败'))
        else:
            video_sub = VideoSub.objects.get(pk=videosub_id)
            video_sub.url = url
            video_sub.number = number
            video_sub.save()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


# 此处应为post
class VideoStarView(View):
    def get(self, request):
        name = request.GET.get('name')
        identity = request.GET.get('identity')
        video_id = request.GET.get('video_id')
        path = '{}'.format(redirect(reverse('video_sub', kwargs={'video_id': video_id})))
        if not all([name, identity, video_id]):
            return redirect('{}?error={}'.format(path, '缺少必要字段'))

        result = check_and_get_video_type(IdentityType, identity, '非法的身份')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(path, result['msg']))

        video = Video.objects.get(pk=video_id)
        try:
            VideoStar.objects.create(video=video, name=name, identity=identity)
        except:
            return redirect('{}?error={}'.format(path, '创建失败'))

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


# 删除演员信息
class StarDelete(View):
    def get(self, request, star_id, video_id):
        VideoStar.objects.filter(id=star_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


# 删除电影的信息
class SubDelete(View):
    def get(self, request, videosub_id, video_id):
        VideoSub.objects.filter(id=videosub_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


# 编辑按钮视图
class VideoUpdate(View):
    TEMPLATE = 'dashboard/video/video_update.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        data['video'] = video
        return render_to_response(request, self.TEMPLATE, data=data)


# 视频状态修改
class VideoUpdateStatus(View):

    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        video.status = not video.status
        video.save()
        return redirect(reverse('externa_video'))
