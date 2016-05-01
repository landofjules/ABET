/* global $ */

$("body").load(function() {
    $("#courseNav a").click(pushCourse);
});


// highlights the link clicked
function selectNav(selector) {
    var parentId = $(selector).attr('id');
    var type = $(this).get(0).tagName;
    $('#'+parentId+' '+type).removeClass('active');
    $(this).addClass('active');
}

// these funcitons return simple information of the form for data loading
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
    if(!$(this).hasClass("active")) {
        selectNav.call(this,"#pageNav");
        $("#mainForm .outD").remove();
        var outName = thisOutcome();
        
        if( thisPage() == 'outcome') $("#piNav").hide();
        else if( thisPage() == 'pi') $("#piNav").show();
        
        if( thisCourse() != "" ) {
            pushCourse.call($("#courseNav .active a").get(0), function() {
                
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
    $("#mainForm .outD").remove();
    
    $("#mainForm form").invisible();
    $("#msg").hide();
    $("#mainForm").addClass("loading");
    
    $.getJSON("dat/courses", {
        "semStr":semStr
    },
    function(data) {
        
        var sel = $("#semSelect").detach();
        var here = $("#courseNav ul");
        here.empty()
        for(var i=0;i<data.courses.length;i++) {
            here.append("<li><a>"+ data.courses[i] +"</a></li>")
        }
        $("#msg").show();
        $("#msg").text("Select a course.");
        $('#outcomeNav .list-group').empty().append(blankListGroupHtml);
        $('#piNav .list-group').empty().append(blankListGroupHtml);
        $("#courseNav a").click(pushCourse);
        $("#mainForm").removeClass("loading");
        here.append(sel);
    })
});

// handles a selection of a course
function pushCourse(callback) {
    selectNav.call(this.parentNode,"#courseNav");
    $('#mainForm form').invisible();
    $('#msg').hide();
    $('#msg').empty();
    $('#mainForm').addClass('loading');
    
    $.getJSON('dat/outcomes',{
        "semStr":thisSem(),
        "course":thisCourse()
    },
    function(data) {
        $('#outcomeNav .list-group').visible();
        var here = $("#outcomeNav div.list-group");
        here.empty();
        $("#msg").show();
        if(data.outcomes.length == 0) {
            here.append(blankListGroupHtml);
            $("#msg").text("No outcomes for "+data.courseName+'.');
        } else {
            for(var i=0;i<data.outcomes.length;i++) {
                here.append('<a class="list-group-item">'+data.outcomes[i]+'</a>');
            }
            $('#outcomeNav .list-group-item').click(pushOutcome);
            $("#msg").text("Select an outcome for "+data.courseName+'.');
        }
        
        $('#mainForm').removeClass('loading');
        
        $('#piNav .list-group').empty().append(blankListGroupHtml);
        
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
    $("#mainForm form").invisible();
    $("#msg").hide();
    $('#mainForm').addClass('loading')
    $('#piNav list-group').empty().append(blankListGroupHtml);
  
    $.getJSON('dat/pis',{
        "semStr":thisSem(),
        "course":thisCourse(),
        "outcome":thisOutcome(),
    },
    function(data) {
        var here = $("#piNav div.list-group");
        $("#msg").show();
        here.empty();
        if(data.pis.length == 0) {
            here.append(blankListGroupHtml)
            $("#msg").text("No performance indicators. Add a new one.");
        } else {
            for(var i=0;i<data.pis.length;i++) {
                here.append('<a class="list-group-item">'+data.pis[i]+'</a>');
            }
            $("#msg").text("Select a performance indicator, or add a new one.");
        }
        here.append(addPiHtml);
        
        $("#mainForm").removeClass('loading')
        $("#mainForm").prepend('<p class="outD">Outcome '+data.outcome+': '+data.outcomeDesc+'</p>')
        $('#piNav .list-group-item:not(.disabled)').click(pushPi);
        
        if(typeof callback === 'function') callback();
    })   
};

// **************  Performance Indicator Navigation  ************* //
function pushPi(callback) {
    selectNav.call(this,"#piNav");
    loadForm(callback);
}

function loadForm(callback) {
    var ptext='~'
    if(thisPage()=='pi') {
        ptext = $("#piNav .active").text()
        if(ptext=="+") ptext='~';
    }
    
    $("#mainForm").addClass("loading");
    $("#mainForm form").invisible();
    var msg = $("#msg").hide().detach()
    var outTxt = $("#mainForm .outD");
    
    
    
    $("#mainForm").load('form/'+thisPage() +'?'+ serialize({
        "semStr":thisSem(),
        "course":thisCourse(),
        "outcome":thisOutcome(),
        "pi":ptext
    }),
    function() {
        $("#mainForm").prepend(outTxt);
        $("#mainForm").prepend(msg)
        $("#mainForm form").visible();
        $("#mainForm").removeClass("loading");
        $("#updateBtn").click(submitForm);
        $("#updateBtn").addClass('disabled');
        $("#deleteBtn").click(deletePI)
        $("#mainForm input").on("keyup",validateForm);
        $("#mainForm textarea").on("keyup",validateForm);
        if(typeof callback === 'function') callback();
    });/*.error(function (){
        $("#mainForm").removeClass("loding");
        $("#mainForm").prepend(outTxt);
        $("#mainForm").prepend(msg);
        if(thisPage()==='pi') {
            $("#msg").text('<span class="error">Server error!</span> Select new performance indicator, or try again later.')
            $("#piNav .active").removeClass('active');
        } else {
            $("#msg").text('<span class="error">Server error!</span> Select new outcome, or try again later.')
            $("#outcomeNav .active").removeClass('active');
        }
    });*/
}

// ************** Form Submitting ************** //

function submitForm(callback) {
    
    validateForm()
    var canSubmit = true;
    $("#mainForm input").each(function() {
        if( $(this).hasClass("error") ) canSubmit = false;
    })
    if( $("#updateBtn").hasClass("disabled") ) cansubmit = false;
    
    
    if(canSubmit) {
        
        var form = $('#mainForm form');
        form.invisible();
        $('#mainForm').addClass('loading')
        $.post('submit/'+thisPage(),form.serialize(),function(data) {
            if( thisPage() == 'pi' ) {
                loadPis(function() {
                    $("#piNav .list-group-item").each(function() {
                        if( $(this).text() == data['pi'] ) $(this).click();
                    })
                    
                })
                
            } else {
                $("#outcomeNav .list-group-item").each(function() {
                    if( $(this).text() == data['outcome'] ) $(this).click();
                })
                
            }
        })
    }
    
}

function deletePI() {
    var form = $('#mainForm form');
    $.post('submit/deletePI',form.serialize(),function(data) {
        loadPis();
    })
}



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
            // allow profesor to submit without weight
            weightBox.removeClass("error");
            $("#badWeightError").hide();
        }
    }
        
        
    // check all the number boxes
    $(".rubricBlock input").each(function() {
        var id = $(this).attr("name");
        var level = id.split('_')[1];
        var what = id.split('_')[2];
        
        var upper = $("input[name='r_"+level+"_upper']");
        var lower = $("input[name='r_"+level+"_lower']");
        
        // test if the value is an integer
        if($(this).val() != "" ) {
            if( isInt(this) ) {
                $(this).removeClass("error");
                if(what == 'num') $("#numNotNumError_"+level).hide();
                
                // test to make sure the ranges are proper
                if( Number(upper.val() ) < Number(lower.val() ) ) {
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
            $("#rangeDisorderError_"+level).hide();
                
        }
        
        if( !upper.hasClass('error') && !lower.hasClass('error'))
            $("#rangeNotNumError_"+level).hide();
        
        
            
    })
    
    
    // if any of the feilds are invalid, disable submission
    $("#updateBtn").removeClass("disabled");
    $("#mainForm input").each(function() {
        if( $(this).hasClass("error") ) $("#updateBtn").addClass("disabled");
    })
    
    
}

function isInt(ss) {
    return ($.isNumeric( $(ss).val() ) && Math.floor( $(ss).val() ) == $(ss).val() );
    
}


    
function serialize(obj) {
  var str = [];
  for(var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&");
}


jQuery.fn.visible = function() {
    return this.css('visibility', 'visible');
};

jQuery.fn.invisible = function() {
    return this.css('visibility', 'hidden');
};