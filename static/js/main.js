console.log("readyee")

$(document).ready(function(){
  $('.row .like_u').click(function(){
    var clicked = $(this)
    var img = $(this).find($('.post_id'))
    console.log(img.val())
    $.get('/likes/'+img.val()+'',
    function(data){
      if (data.status){
        clicked.css({
          "color":"red",
        })
       var likes= $(".post"+data.img+" .image_likes").text()
       $(".post"+data.img+" .image_likes").text(parseInt(likes)+1)
       
      }
      else{
        clicked.css({
          "color":"black",
        })
        var likes= $(".post"+data.img+" .image_likes").text()
        $(".post"+data.img+" .image_likes").text(parseInt(likes)-1)
        
      }
    })
    })
  })


