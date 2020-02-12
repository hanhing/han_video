var inputNumber = $('#number');
var inputUrl = $('#url');
var videosubIputId = $('#videosub-input-id');

$('.updata-btn').click(function () {
    var videosubId = $(this).attr('data-id');
    var videosubNumber = $(this).attr('data-number');
    var videosubUrl = $(this).attr('data-url');
    inputNumber.val(videosubNumber);
    inputUrl.val(videosubUrl);
    videosubIputId.val(videosubId);

});


// $('#play').click(function () {
//     var src = $('#play').getAttribute('href')
//     var page = window.open();
//    var html="<video controls src='"+src+ "'></video>";
//     page.document.write(html);
//
// })

function playideo(src){
    var page = window.open();
   var html="<video controls src='"+src+ "'></video>";
    page.document.write(html);
}
