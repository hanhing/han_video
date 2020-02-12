$('#comment-submit').click(function () {
    var content = $('#comment-content').val();
    // var csrftoken = $('#django-csrf-token').val();
    var videoId = $(this).attr('data-video-id');
    var userId = $(this).attr('data-user-id');
    var url = $(this).attr('data-url');
    var ajax_comment_show = $('#ajax-comment-show');

    if (!content){
        alert('评论不能为空')
        return
    }
    $.ajax({
        url: url,
        data:{
            // csrfmiddlewaretoken: csrftoken
            content: content,
            videoId: videoId,
            userId: userId,
        },
        type: 'post',
        success: function (data) {
            console.log('ok')
        },
        fail: function (e) {
            console.log(e)
            
        }
    })

});