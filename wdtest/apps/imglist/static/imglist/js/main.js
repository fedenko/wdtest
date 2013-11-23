$(function() {
  $(".context-menu-btn").popover({
    container: "body",
    html: true,
    content: function(){
      return $("#context-menu-content").html();
    }
  });
});
