from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from app.libs.base_render import render_to_response
from app.utils.utils import dashboard_auth
from app.model.video import VideoType, FromType, Nationality, Video, VideoSub, IdentityType, VideoStar
from app.utils.common import check_and_get_video_type


class ExternaVideo(View):  # 外链视频
    TEMPLATE = 'dashboard/video/externa_video.html'

    def get(self, request):
        error = request.GET.get('error')
        videos = Video.objects.exclude(from_to=FromType.custom.value, )
        data = {'error': error, 'videos': videos}
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
    def get(self, request):
        name = request.GET['name']
        video_type = request.GET['video_type']
        img = request.GET['img']
        video_nationality = request.GET['video_nationality']
        from_to = request.GET['from_to']
        info = request.GET['info']

        if not all([name, video_nationality, video_type, img, from_to]):
            return redirect('{}?error{}'.format(reverse('externa_video'), '缺少必要的信息'))

        result = check_and_get_video_type(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error{}'.format(reverse('externa_video'), result['msg']))
        print('1' * 50)

        result = check_and_get_video_type(FromType, from_to, '非法的视频来源')
        if result.get('code') != 0:
            return redirect('{}?error{}'.format(reverse('externa_video'), result['msg']))
        print('2' * 50)

        result = check_and_get_video_type(Nationality, video_nationality, '非法的国籍')
        if result.get('code') != 0:
            return redirect('{}?error{}'.format(reverse('externa_video'), result['msg']))
        print('3' * 50)
        Video.objects.create(
            name=name,
            image=img,
            video_type=video_type,
            from_to=from_to,
            nationality=video_nationality,
            info=info,
        )
        print('4' * 50)
        return redirect(reverse('externa_video'))


class VideoSubView(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        error = request.GET.get('error', '')
        data['video'] = video
        data['error'] = error
        print(data)
        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request, video_id):
        pass
    # 由于mako csrf验证问题,所以改用get提交表单


class VideoSubGet(View):

    def get(self, request, video_id):
        url = request.GET.get('url')
        video = Video.objects.get(pk=video_id)
        length = video.video_sub.count()
        number = length + 1
        path = '{}'.format(redirect(reverse('video_sub', kwargs={'video_id': video_id})))
        try:
            VideoSub.objects.create(video=video, url=url, number=number)
        except:
            return redirect('{}?error={}'.format(path, '创建失败'))
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
            print('11' * 50)
        except:
            return redirect('{}?error={}'.format(path, '创建失败'))

        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


# 删除演员信息
class StarDelete(View):
    def get(self, request, star_id, video_id):
        print('*' * 50)
        print(star_id, video_id)
        VideoStar.objects.filter(id=star_id).delete()
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))
