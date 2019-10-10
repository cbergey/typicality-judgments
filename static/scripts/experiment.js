var my_node_id;
var trial = 0;
var adj = ""
var noun = ""
var numtrials = 20

var get_info = function() {
  // Get info for node
  if (trial == numtrials) {
    noun = "attentioncheck"
    adj = ""
    $("#question").html("Select \"Often\".");
    $("#stimulus").show();
    $("#response-form").hide();
    $("#submit-response").show();
  } else {
  
    dallinger.getReceivedInfos(my_node_id)
      .done(function (resp) {
        var stims = resp.infos[0].contents;
        stims = stims.replace(/[\.-\/#!$%\^&\*;:{}=\-_`~()@\+\?><\[\]\+]/g, '')
        var words = stims.split(",")
        adj = words[trial*3]
        noun = words[trial*3 + 1]
        if (words[trial*3 + 2] == "NA") {
          var article = ""
        } else {
          var article = words[trial*3 + 2] + " "
        } 
        adj.trim()
        $("#question").html("How common is it for " + article + "<b>" + noun + "</b> to be " + article + "<b>" + adj + " " + noun + "</b>?");
        $("#stimulus").show();
        $("#response-form").hide();
        $("#submit-response").show();
      })
      .fail(function (rejection) {
        console.log(rejection);
        $('body').html(rejection.html);
      });
  }
};

var create_agent = function() {
  $('#finish-reading').prop('disabled', true);
  dallinger.createAgent()
    .done(function (resp) {
      $('#finish-reading').prop('disabled', false);
      my_node_id = resp.node.id;
      get_info();
    })
    .fail(function (rejection) {
      // A 403 is our signal that it's time to go to the questionnaire
      if (rejection.status === 403) {
        dallinger.allowExit();
        dallinger.goToPage('questionnaire');
      } else {
        dallinger.error(rejection);
      }
    });
};

submit_response = function(choice) {
  $("#stimulus").hide();
  dallinger.createInfo(my_node_id, {
    contents: choice,
    property1: adj,
    property2: noun,
    info_type: 'Info'
  }).done(function (resp) {
    trial = trial + 1;
    if (trial == 0 || trial == (numtrials + 1)) {
      create_agent();
    } else {
      get_info();
    }
  });
};

$(document).ready(function() {

  $("#submit-response").click(function() {
    $("#submit-response").addClass('disabled');
    $("#submit-response").html('Sending...');


    dallinger.createInfo(my_node_id, {
      contents: response,
      property3: response,
      info_type: 'Info'
    }).done(function (resp) {
      if (trial == 0 || trial == (numtrials + 1)) {
        create_agent();
      } else {
        get_info();
      }
    });
  });

});
