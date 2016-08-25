/* global $ */

$(document).ready(function() {
    $("#courseNav a").click(pushCourse);
});

// handles errors in ajax requests
$.ajaxSetup({
    timeout:5000,
    error:function() {
        $("#mainForm").removeClass("loading");
        $("#msg").show();
        $("#msg").html('<b class="error">Error loading!</b> Try a different item, or try again later')
    }
});

// highlights the link clicked
function selectNav(selector) {
    var parentId = $(selector).attr('id');
    var type = $(this).get(0).tagName;
    $('#'+parentId+' '+type).removeClass('active');
    $(this).addClass('active');
}

// these funcitons return simple information of the form location for data loading
function thisSem() { return $("#semSelect select").val().replace(' ','_'); }
function thisCourse() { return $("#courseNav li.active").text(); }
function thisOutcome() { return $("#outcomeNav a.active").text(); }
function thisPage() { 
    if( $("#pageNav a.active").is("#pageNavPi") ) return 'pi';
    else if( $("#pageNav a.active").is("#pageNavOut") ) return 'outcome';
}

// html strings for the special list items
var addPiHtml = '<a id="addPi" class="list-group-item">+</a>';
var blankListGroupHtml = '<a class="list-group-item disabled blank">&nbsp;</a>';

/* ******* *******   NAVIGATION   ******* ****** */

// handles a change in the page navigation
$("#pageNav a").click(function() {
    // if we're not clicking on the active page
    if(!$(this).hasClass("active")) {
        
        // select the page, remove outcome description, and record oucome name
        selectNav.call(this,"#pageNav");
        $("#mainForm .outD").remove();
        var outName = thisOutcome();
        
        // toggle performance indicator menu
        if( thisPage() == 'outcome') $("#piNav").hide();
        else if( thisPage() == 'pi') $("#piNav").show();
        
        // reload the course
        if( thisCourse() != "" ) {
            pushCourse.call($("#courseNav .active a").get(0), function() {
                
                // reload the outcome if previously selected
                if( outName != "" ) {
                    $("#outcomeNav .list-group-item").each(function() {
                        if( $(this).text() == outName ) $(this).click();
                    })
                }
                
            });
            
        }
    }
});

// handles a change in semester drop down
$('#semSelect select').change(function(e) {
    var semStr = thisSem();
    
    // make it look like it's loading
    $("#mainForm .outD").remove();
    $("#mainForm form").invisible();
    $("#msg").hide();
    $("#mainForm").addClass("loading");
    
    // create the ajax request for new courses
    $.getJSON("dat/courses", {
        "semStr":semStr
    },
    function(data) {
        
        // detach the drop-down and empty
        var sel = $("#semSelect").detach();
        var here = $("#courseNav ul");
        here.empty()
        
        // append the course list
        for(var i=0;i<data.courses.length;i++) {
            here.append("<li><a>"+ data.courses[i] +"</a></li>")
        }
        // fill the message box
        $("#msg").show();
        $("#msg").text("Select a course");
        
        // add empty list-group boxes to outcome and pi
        $('#outcomeNav .list-group').empty().append(blankListGroupHtml);
        $('#piNav .list-group').empty().append(blankListGroupHtml);
        $("#piLoadBox").hide();
        
        // assign event listeners, remove loading indicater, and append drop-down
        $("#courseNav a").click(pushCourse);
        $("#mainForm").removeClass("loading");
        here.append(sel);
    })
});

// handles a selection of a course
function pushCourse(callback) {
    
    // highlight box, hide form and message, and add loading indicator
    selectNav.call(this.parentNode,"#courseNav");
    $('#mainForm form').invisible();
    $('#msg').hide();
    $('#msg').empty();
    $('#mainForm').addClass('loading');
    
    // ajax request to get outcomes
    $.getJSON('dat/outcomes',{
        "semStr":thisSem(),
        "course":thisCourse()
    },
    function(data) {
        
        // empty outcome list and prepare message
        var here = $("#outcomeNav div.list-group");
        here.empty();
        $("#msg").show();
        
        // if there are no outcomes, add a blank box and set the appropriate message
        if(data.outcomes.length == 0) {
            here.append(blankListGroupHtml);
            $("#msg").text("No outcomes for "+data.courseName);
            
        // otherwise, add the outcomes, assign event listeners, and set the message
        } else {
            for(var i=0;i<data.outcomes.length;i++) {
                here.append('<a class="list-group-item">'+data.outcomes[i]+'</a>');
            }
            $('#outcomeNav .list-group-item').click(pushOutcome);
            $("#msg").text("Select an outcome for "+data.courseName);
        }
        
        // remove loading indicator
        $('#mainForm').removeClass('loading');
        
        // make pilist blank
        $('#piNav .list-group').empty().append(blankListGroupHtml);
        $('#piLoadBox').hide();
        
        if(typeof callback === 'function') callback();
    })   
};
$("#courseNav a").click(pushCourse);

// handles the selection of an outcome
function pushOutcome(callback) {
    selectNav.call(this,"#outcomeNav");
    $("#mainForm .outD").remove();
    
    if(thisPage()==='pi') {
        loadPis();
    } else if(thisPage()==='outcome') {
        loadForm();
    }
    if(typeof callback === 'function') callback();
}

function loadPis(callback) {
    
    // make it look like its loading
    $("#mainForm form").invisible();
    $("#msg").hide();
    $('#mainForm').addClass('loading');
    $('#piNav .list-group').empty().append(blankListGroupHtml);
    $("#piLoadBox").hide();
  
    // ajax request to load performance indicators
    $.getJSON('dat/pis',{
        "semStr":thisSem(),
        "course":thisCourse(),
        "outcome":thisOutcome(),
    },
    function(data) {
        var here = $("#piNav div.list-group");
        $("#msg").show();
        here.empty();
        
        // similar idea to outcomes ^
        if(data.pis.length == 0) {
            here.append(blankListGroupHtml)
            $("#msg").text("No performance indicators, add a new one");
        } else {
            for(var i=0;i<data.pis.length;i++) {
                here.append('<a class="list-group-item">'+data.pis[i]+'</a>');
            }
            $("#msg").text("Select a performance indicator, or add a new one");
        }
        here.append(addPiHtml);
        
        $("#mainForm").removeClass('loading')
        $("#mainForm").prepend('<p class="outD">Outcome '+data.outcome+': '+data.outcomeDesc+'</p>')
        $('#piNav .list-group-item:not(.disabled)').click(pushPi);
        
        $("#piLoadBox").show();
        $("#piLoadBox select").empty().append('<option value="--">----</option>');
        for(var i=0;i<data.piSems.length;i++) {
            $("#piLoadBox select").append('<option value="'+data.piSems[i]+'">'+data.piSems[i].capitalize()+'</option>')
        }
        $("#piLoadBox a").click(populatePis);
        
        if(typeof callback === 'function') callback();
    })   
};
function populatePis() {
    
    $("#mainForm form").invisible();
    $("#msg").hide();
    $('#mainForm').addClass('loading');
    
    $.getJSON("populatePis", {
        "semStr":thisSem(),
        "course":thisCourse(),
        "outcome":thisOutcome(),
    }, function(data) {
        
        loadPis();
    });
    
}

// **************  Performance Indicator Navigation  ************* //
function pushPi(callback) {
    selectNav.call(this,"#piNav");
    loadForm(callback);
}

// this function loads the form for the current page
function loadForm(callback) {
    var ptext='~'
    if(thisPage()=='pi') {
        ptext = $("#piNav .active").text()
        if(ptext=="+") ptext='~';
    }
    
    // prepare form for loading
    $("#mainForm").addClass("loading");
    $("#mainForm form").invisible();
    var msg = $("#msg").hide().detach()
    var outTxt = $("#mainForm .outD");
    
    // load the form 
    $("#mainForm").load('form/'+thisPage() +'?'+ serialize({
        "semStr":thisSem(),
        "course":thisCourse(),
        "outcome":thisOutcome(),
        "pi":ptext
    }),
    function() {
        // add outText and message, and make form visible
        $("#mainForm").prepend(outTxt);
        $("#mainForm").prepend(msg)
        $("#mainForm form").visible();
        $("#mainForm").removeClass("loading");
        
        // assign event listeners to buttons
        $("#updateBtn").click(submitForm);
        $("#updateBtn").addClass('disabled');
        $("#deleteBtn").click(deletePI)
        
        // assign validation functions to text feilds
        $("#mainForm input").on("keyup",validateForm);
        $("#mainForm textarea").on("keyup",validateForm);
        
        if(typeof callback === 'function') callback();
    });
}

// submits the form 
function submitForm(callback) {
    
    // test if the form should be sumbmitted
    var canSubmit = true;
    if( $("#updateBtn").hasClass("disabled") ) canSubmit = false;
    validateForm()
    $("#mainForm input").each(function() {
        if( $(this).hasClass("error") ) canSubmit = false;
    })
    
    // if it can
    if(canSubmit) {
        var form = $('#mainForm form');
        
        // remove the outcome submission
        $("#mainForm p.outD").remove();
        
        // hide the form and add loading indicator
        form.invisible();
        $('#mainForm').addClass('loading')
        
        // submit the POST request for the form
        $.post('submit/'+thisPage(),form.serialize(),function(data) {
            if( thisPage() == 'pi' ) {
                
                // if we are searching for pis, load them and click the one we submitted
                loadPis(function() {
                    $("#piNav .list-group-item").each(function() {
                        if( $(this).text() == data['pi'] ) $(this).click();
                    })
                    
                })
                
            } else {
                // if it is an outcome, click the outcome submitted
                $("#outcomeNav .list-group-item").each(function() {
                    if( $(this).text() == data['outcome'] ) $(this).click();
                })
                
            }
        })
    } else {
        // disable button after validateForm() enables it 
        $("#updateBtn").addClass("disabled");
    }
    
}

// post request to delete the pi
function deletePI() {
    $(".outD").remove()
    var form = $('#mainForm form');
    $.post('submit/deletePI',form.serialize(),function(data) {
        loadPis();
    })
}

// validates the form
function validateForm(evt) {
    
    if(thisPage()=='pi') {
        
        // the name field
        var newName = $("#mainForm input[name='newName']");
        
        // check if the name is empty
        if(newName.val() == "") {
            $("#nameEmptyError").show();
        } else $("#nameEmptyError").hide(); 
         
        //check if the name is already taken
        $("#nameUsedError").hide();
        $("#piNav .list-group-item:not(.active)").each(function() {
            if( newName.val() == $(this).text() ) $("#nameUsedError").show();
        });
        
        // turn text box red if one of the two errors apply
        if( $("#nameUsedError").is(":visible") || $("#nameEmptyError").is(":visible") ) {
            newName.addClass("error");
        } else {
            newName.removeClass("error");
        }
        
        
        // check if the weight is a floating point number between 0 and 1
        var weightBox = $("#mainForm input[name='weight']");
        if( weightBox.val() != "") {
            if( $.isNumeric(weightBox.val()) ) {
                if( Number(weightBox.val())<=1 && Number(weightBox.val())>=0 ) {
                    // good
                    weightBox.removeClass("error");
                    $("#badWeightError").hide();
                    
                } else {
                    // bad
                    weightBox.addClass("error");
                    $("#badWeightError").show();
                }
            } else {
                // bad
                weightBox.addClass("error");
                $("#badWeightError").show();
            }
        } else {
            // allow professor to submit without weight
            weightBox.removeClass("error");
            $("#badWeightError").hide();
        }
    }
        
        
    // check all the number boxes
    $(".rubricBlock input").each(function() {
        
        // get the name, the performance level, and what box it is
        var id = $(this).attr("name");
        var level = id.split('_')[1];
        var what = id.split('_')[2];
        
        // retrieve corresponding range boxes
        var upper = $("input[name='r_"+level+"_upper']");
        var lower = $("input[name='r_"+level+"_lower']");
        
        // test if the value is an integer
        if($(this).val() != "" ) {
            if( isInt(this) ) {
                $(this).removeClass("error");
                if(what == 'num') $("#numNotNumError_"+level).hide();
                
                // test to make sure the ranges are in order integers
                if( Number(upper.val()) < Number(lower.val()) ) {
                    upper.addClass("error");
                    lower.addClass("error");
                    $("#rangeDisorderError_"+level).show();
                } else {
                    $("#rangeDisorderError_"+level).hide();
                }
            } else {
                $(this).addClass("error");
                if(what == 'num') $("#numNotNumError_"+level).show();
                else  $("#rangeNotNumError_"+level).show();
            }
        } else {
            $(this).removeClass("error");
            if(what == 'num') $("#numNotNumError_"+level).hide();
            //$("#rangeDisorderError_"+level).hide();
                
        }
        
        if( !upper.hasClass('error') && !lower.hasClass('error')) {
            $("#rangeNotNumError_"+level).hide();
        }
        
    })
    
    
    // if any of the feilds are invalid, disable submission
    $("#updateBtn").removeClass("disabled");
    $("#mainForm input").each(function() {
        if( $(this).hasClass("error") ) $("#updateBtn").addClass("disabled");
    })
    
    
}

// test if an input.val() is an ingeger
function isInt(ss) {
    return ($.isNumeric( $(ss).val() ) && Math.floor( $(ss).val() ) == $(ss).val() );
    
}

// creates a url variable string out of a javasript object 
function serialize(obj) {
  var str = [];
  for(var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&");
}

// jQuery plugins to toggle visibility
jQuery.fn.visible = function() {
    return this.css('visibility', 'visible');
};
jQuery.fn.invisible = function() {
    return this.css('visibility', 'hidden');
};

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}