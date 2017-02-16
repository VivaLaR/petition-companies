$(document).ready(function(){
  wireSaveButton();
  wireCloseButton();
  wireDeleteButton();

  wireDeleteAdvertiserButtons();
  wireAddAdvertiserButton();
});

function wireCloseButton() {
  $("#close-advertisee").click(function () {
    window.location.href = url_index;
  });
}

function wireSaveButton() {
  $("#save-advertisee").click(function () {
    var user_data = {};
    user_data['name'] = $("#advertisee-name").html();
    user_data['description'] = $("#advertisee-description").html();
    user_data['email'] = $("#advertisee-email").html();

    console.log(user_data);

    $.ajax({
      type: 'POST',
      url: url_advertisee,
      data: JSON.stringify(user_data),
      contentType: "application/json",
      dataType: 'json',
      success: function(data, status, xhr){
        window.location.href = url_index;
      },
      error: function(xhr, status, error){
        console.log("Error", xhr);
      },
    });
  });
}

function wireDeleteButton() {
  $("#delete-advertisee").click(function () {
    $.ajax({
      type: 'DELETE',
      url: url_advertisee,
      contentType: "application/json",
      dataType: 'json',
      success: function (data, status, xhr) {
        window.location.href = url_index;
      },
      error: function (xhr, status, error) {
        console.log("Error", xhr);
      },
    });
  });
}

function wireDeleteAdvertiserButtons() {
  $("button.delete-advertiser").click(function (e) {

    var data = {};
    data['method'] = 'delete';
    data['advertisee_id'] = advertisee_key;
    data['advertiser_id'] = $(e.target).closest("tr").attr('value');

    $.ajax({
          type: 'POST',
          url: url_delete_advertiser,
          data: JSON.stringify(data),
          contentType: "application/json",
          dataType: 'json',
          success: function(data, status, xhr){
            window.location.reload();
          },
          error: function(xhr, status, error){
            console.log("Error", xhr);
          }
        }
    )
  })
}

function wireAddAdvertiserButton() {
  $("button#add-advertiser").click(function () {

    var data = {};
    data['method'] = 'post';
    data['advertisee_id'] = advertisee_key;
    data['advertiser_id'] = $('select.advertiser').find(':selected').val();
    console.log($('select').find(':selected'));

    $.ajax({
          type: 'POST',
          url: url_delete_advertiser,
          data: JSON.stringify(data),
          contentType: "application/json",
          dataType: 'json',
          success: function(data, status, xhr){
            window.location.reload();
          },
          error: function(xhr, status, error){
            console.log("Error", xhr);
          }
        }
    )
  })
}
