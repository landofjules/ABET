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
        loadOutcomes(thisCourse());
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
function pushCourse() {
    selectNav.call(this.parentNode,"#courseNav");
    
    $.getJSON('dat/outcomes',{
        "semStr":thisSem(),
        "course":thisCourse()
    },
    function(data) {
        $('#outcomeNav').show();
        var here = $("#outcomeNav div.list-group");
        here.empty();
        for(var i=0;i<data.outcomes.length;i++) {
            here.append('<a class="list-group-item">'+data.outcomes[i]+'</a>');
        }
        $("#mainForm").text("Select an outcome for "+data.courseName);
        $('#outcomeNav .list-group-item').click(pushOutcome);
        $('#piNav').hide();
    })   
};

// ****************  OUTCOME NAVIGATION ***************** //

function pushOutcome() {
    selectNav.call(this,"#outcomeNav");
    if(thisPage()==='pi') {
        console.log("should load pi list");
        loadPis();
    } else if(thisPage()==='outcome') {
        console.log("should load outcome form");
        loadForm();
    }
}

function loadPis(callback) {
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
        $('#piNav .list-group-item').click(pushPi);
        if(typeof callback === 'function') callback();
    })   
};

// **************  Performance Indicator Navigation  ************* //
function pushPi() {
    selectNav.call(this,"#piNav");
    loadForm();
}

function loadForm(callback) {
    var ptext='~'
    if(thisPage()=='pi') {
        ptext = $("#piNav .active").text();
        if(ptext=="+") ptext='~';
    }
    $("#mainForm").load('form/'+thisPage() +'?'+ serialize({
        "semStr":thisSem(),
        "course":thisCourse(),
        "outcome":thisOutcome(),
        "pi":ptext
    }),
    function() {
        //$("#updateBtn").click(submitForm);
        if(typeof callback === 'function') callback();
    });
}

/*
// ************** Form Submitting ************** //

function submitPiForm() {
    var form = $('#mainForm form');
    var name = $("#piNameField").val();
    console.log("should submit");
    $.post('submit/pi',form.serialize(),function(data) {
        loadPis(function(){
            console.log("entered callback");
        });
        console.log("and does");
    });
}
    
*/
function serialize(obj) {
  var str = [];
  for(var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&");
}