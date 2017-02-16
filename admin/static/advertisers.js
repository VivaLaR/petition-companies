
$(document).ready(function(){
  wireCreateClickHandler();
  wireRowClickHandlers();
});

function wireCreateClickHandler() {
  $("#create-button").click(function () {
    window.location.href = url_advertiser_base;
  });
}

function wireRowClickHandlers() {
  $(".advertiser").click(function () {
    var row = $(this).closest("tr")
    var url_visit = url_advertiser_base + row.attr('advertiser-id')
    window.location.href = url_visit
  });
}
