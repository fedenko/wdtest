$(function() {
  $(".context-menu-btn").popover({
    container: "body",
    html: true,
    content: function(){
      var imageId = $(this).closest(".thumbnail").data("image-id");
      var $content = $($("#context-menu-content").html());
      $(":input[name=image_id]", $content).attr("value", imageId);
      return  $content;
    }
  }).data("popover").tip().on( "submit", "#add-list", function() {
    $.ajax({
      url     : $(this).attr('action'),
      type    : $(this).attr('method'),
      dataType: 'json',
      data    : $(this).serialize(),
      success : function( data ) {
        if (!data.success){
          alert(data.error);
        } else {

        }
      },
      error   : function( xhr, err ) {
         alert('Error');
      }
    });
    return false;
  });
});
