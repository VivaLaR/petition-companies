var email_txts = {};
var checkbox_count = {};

$(document).ready(function(){
  $("#email-button").click(emailOnClick);
  wireSaveEmailButtons();
  wireCheckBoxes();
});

function emailOnClick() {

  var to_send = {};
  var advertisees = $('#advertisee-list > li');
  var advertisee, advertisers;
  var i, j;
  for (i=0; i < advertisees.length; i++) {
    advertisee = advertisees[i];
    to_send[advertisee.id] = [];
    advertisers = $(advertisee).find("li");
    for (j=0; j < advertisers.length; j++) {
      if ($(advertisers[j]).find("input").is(":checked")) {
        to_send[advertisee.id].push(advertisers[j].id)
      }
    }
  }

  postDataToEmail(to_send, true);
}

function postDataToEmail(data) {

  data['emails'] = email_txts;

  $.ajax({
    type: 'POST',
    url: url_email,
    data: JSON.stringify(data),
    contentType: "application/json",
    dataType: 'json',
    success: function(data, status, xhr){
      console.log('Success');
    },
    error: function(xhr, status, error){
      if (xhr['status'] == 401) {
        window.location.replace(url_email);
      } else {
        console.log('Failure');
      }
    },
  });
}

function wireSaveEmailButtons() {
  $('.email-modal').click(function (event) {
    var email_txt = $(event.target).closest('.modal-content').find('div.modal-body > div').html();
    var advertisee_id = $(event.target).closest('.modal').attr('eid');

    email_txts[advertisee_id] = email_txt;
  })
}

function wireCheckBoxes() {

  var top_list_str = 'ul#advertisee-list > li';
  var bottom_list_str = 'ul#advertiser-list > li > input';

  $(top_list_str).each(
      function (i, elem) {
        checkbox_count[elem.id] = $(elem).find(bottom_list_str + ':checked').length;
      }
  );

  $(top_list_str).children('input').click(function (event) {
    var elem = event.target;

    var top_li = $(elem).closest('li');

    if ($(elem).is(':checked')) {
      top_li.find(bottom_list_str + ':not(:checked)').prop('checked', true);
      checkbox_count[top_li[0].id] = top_li.find('li').length;
    } else {
      top_li.find(bottom_list_str + ':checked').prop('checked', false);
      checkbox_count[top_li[0].id] = 0;
    }
  });

  $(top_list_str).find(bottom_list_str).click(function (event) {
    var elem = event.target;
    var delta = ($(elem).is(':checked')) ? 1 : -1;
    var top_li = elem.closest(top_list_str);
    checkbox_count[top_li.id] += delta;

    if (checkbox_count[top_li.id] == 0) {
      $(top_li).children('input').prop('checked', false)
    } else if (checkbox_count[top_li.id] == 1 && delta == 1) {
      $(top_li).children('input').prop('checked', true);
    }
  })
}
