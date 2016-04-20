// link highlighting
function selectNav(selector) {
    var parentId = $(selector).attr('id');
    var type = $(this).get(0).tagName;
    $('#'+parentId+' '+type).removeClass('active');
    $(this).addClass('active');
}

$("#pageNav a").click(function() {
    if(!$(this).hasClass("active")) {
        selectNav.call(this,"#pageNav");
        var outName = thisOutcome()
        
        if( thisCourse() != "" ) {
            pushCourse.call($("#courseNav .active a").get(0), function() {
                
                if( outName != "" ) {
                    $("#outcomeNav .list-group-item").each(function() {
                        if( $(this).text() == outName ) $(this).click();
                    })
                }
                
            })
            
        }
    }
})


$('#semSelect select').change(function(e) {
    // TODO make the main page have a loading icon
    var semStr = thisSem();
    console.log(semStr);
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
        $('#outcomeNav .list-group').invisible();
        $("#courseNav a").click(pushCourse);
        here.append(sel);
    })
});


function thisSem() { return $("#semSelect select").val().replace(' ','_'); }
function thisCourse() { return $("#courseNav li.active").text(); }
function thisOutcome() { return $("#outcomeNav a.active").text(); }
function thisPage() { 
    if( $("#pageNav a.active").is("#pageNavPi") ) return 'pi';
    else if( $("#pageNav a.active").is("#pageNavOut") ) return 'outcome';
}

// *************  COURSE NAVIGATION  *************** //

$("#courseNav a").click(pushCourse);

function pushCourse(callback) {
    selectNav.call(this.parentNode,"#courseNav");
    $('#mainForm').empty();
    $('#mainForm').addClass('loading');
    
    $.getJSON('dat/outcomes',{
        "semStr":thisSem(),
        "course":thisCourse()
    },
    function(data) {
        $('#outcomeNav .list-group').visible();
        var here = $("#outcomeNav div.list-group");
        here.empty();
        for(var i=0;i<data.outcomes.length;i++) {
            here.append('<a class="list-group-item">'+data.outcomes[i]+'</a>');
        }
        $("#mainForm").text("Select an outcome for "+data.courseName);
        $('#mainForm').removeClass('loading');
        $('#outcomeNav .list-group-item').click(pushOutcome);
        $('#piNav').hide();
        if(typeof callback === 'function') callback();
    })   
};

// ****************  OUTCOME NAVIGATION ***************** //

function pushOutcome(callback) {
    selectNav.call(this,"#outcomeNav");
    if(thisPage()==='pi') {
        console.log("should load pi list");
        loadPis();
    } else if(thisPage()==='outcome') {
        console.log("should load outcome form");
        loadForm();
    }
    if(typeof callback === 'function') callback();
}

function loadPis(callback) {
    var txt = $('#mainForm').text();
    $('#mainForm').addClass('loading')
    $.getJSON('dat/pis',{
        "semStr":thisSem(),
        "course":thisCourse(),
        "outcome":thisOutcome(),
    },
    function(data) {
        $('#piNav').show()
        var here = $("#piNav div.list-group");
        var addPi = $("#addPi").detach();
        here.empty();
        for(var i=0;i<data.pis.length;i++) {
            here.append('<a class="list-group-item">'+data.pis[i]+'</a>');
        }
        addPi.removeClass("active");
        here.append(addPi);
        $("#mainForm").text("Select an performance indicator for "+data.outcome);
        $("#mainForm").removeClass('loading')
        $('#piNav .list-group').visible()
        $('#piNav .list-group-item').click(pushPi);
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
    $("#mainForm").children().invisible();
    $("#mainForm").load('form/'+thisPage() +'?'+ serialize({
        "semStr":thisSem(),
        "course":thisCourse(),
        "outcome":thisOutcome(),
        "pi":ptext
    }),
    function() {
        $("#mainForm form").visible();
        $("#mainForm").removeClass("loading");
        $("#updateBtn").click(submitForm);
        $("#updateBtn").addClass('disabled');
        $("#deleteBtn").click(deletePI)
        $("#mainForm input, #mainForm textarea").change(changeInput);
        if(typeof callback === 'function') callback();
    });
}

// ************** Form Submitting ************** //

function submitForm(callback) {
    if( !$('#updateBtn').hasClass('disabled') ) {
        var form = $('#mainForm form');
        console.log("should submit");
        form.invisible();
        $('#mainForm').addClass('loading')
        $.post('submit/'+thisPage(),form.serialize(),function(data) {
            console.log(data);
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
        console.log(data);
        loadPis();
    })
}

function changeInput() {
    $("#updateBtn").removeClass("disabled");
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