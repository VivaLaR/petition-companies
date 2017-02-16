$(document).ready(function(){
  wireSaveButton();
  wireCloseButton();
  wireDeleteButton();

  wirePOCCreateButton();
  wirePOCDeleteButtons();
});

function wireCloseButton() {
  $("#close-advertiser").click(function () {
    window.location.href = url_advertisers;
  });
}

function wireSaveButton() {
  $("#save-advertiser").click(function () {
    var user_data = {};
    user_data['name'] = $("#advertiser-name").html();
    user_data['pocs'] = {};

    $("tr.poc").each(function (i, el) {
      var poc_id = $(el).attr('poc-id');
      user_data['pocs'][poc_id] = {};
      user_data['pocs'][poc_id]['name'] = $(el).find('.poc-name').html();
      user_data['pocs'][poc_id]['email'] = $(el).find('.poc-email').html();
    });

    console.log(user_data);

    $.ajax({
      type: 'POST',
      url: url_advertiser,
      data: JSON.stringify(user_data),
      contentType: "application/json",
      dataType: 'json',
      success: function(data, status, xhr){
        window.location.href = url_advertisers;
      },
      error: function(xhr, status, error){
        console.log("Error", xhr);
      },
    });
  });
}

function wireDeleteButton() {
  $("#delete-advertiser").click(function () {
    $.ajax({
      type: 'DELETE',
      url: url_advertiser,
      contentType: "application/json",
      dataType: 'json',
      success: function (data, status, xhr) {
        window.location.href = url_advertisers;
      },
      error: function (xhr, status, error) {
        console.log("Error", xhr);
      },
    });
  });
}

function wirePOCCreateButton() {

  var table_row = '<tr class="poc" poc-id="">\
        <td class="col-xs-4 poc-name" style="white-space: pre-wrap" contenteditable="true"></td>\
    <td class="col-xs-7 poc-email" style="white-space: pre-wrap" contenteditable="true"></td>\
    <td class="col-xs-1">\
        <button type="button" class="btn btn-danger delete-poc" aria-label="Delete">\
        <span class="glyphicon glyphicon-trash" aria-hidden="true"></span>\
        </button>\
        </td>\
        </tr>'

  $("button#create-poc").click(function () {
    $("tbody").append(table_row);
    wirePOCDeleteButtons();
  })
}

function wirePOCDeleteButtons() {
  var buttons = $('button.delete-poc');

  $(buttons).off("click");

  $(buttons).click(function (event) {
    console.log('delete');
    var tr = $(event.target).closest("tr");
    $(tr).remove();
  })
}
