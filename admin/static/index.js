
$(document).ready(function(){
  wireCreateClickHandler();
  wireRowClickHandlers(document);

});

function wireCreateClickHandler() {
  $("#create-button").click(function () {
    window.location.href = url_advertisee_base;
  });
}

function wireRowClickHandlers(el) {
  $(el).find(".advertisee").click(visitAdvertiseeOnClick);
}

function visitAdvertiseeOnClick() {
  var row = $(this).closest("tr")
  var url_visit = url_advertisee_base + row.attr('advertisee-id')
  window.location.href = url_visit
}
