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

function thisPage() { 
    if( $("#pageNav a.active").is("#pageNavPi") ) return 'pi';
    else if( $("#pageNav a.active").is("#pageNavOut") ) return 'out';
}
function thisCourse() { return $("#courseNav li.active").attr("str");}
function thisOutcome() { 
    return $("#outcomeNav a.active").text();
}

// *************  COURSE NAVIGATION  *************** //

$('#courseNav li').click(function() {
    selectNav.call(this,"#courseNav");
    if($(this).is("#earlierCourses")){
        $("#ect").hide();
        $("#ecm").show();
        $('#ecm').on("change",function() {
            var li = $(this).parent().parent();
            li.attr("str",$(this).val());
            if(li.attr('str')!='--') loadOutcomes(li.attr("str"));
        })
    } else {
        var str = $(this).attr("str");
        loadOutcomes($(this).attr("str"));
        $("#ecm").hide();
        $("#ecm").attr("value","--")
        $("#ect").show();
    }
});
function loadOutcomes(courseName) {
    $.getJSON('dat/'+courseName,function(obj) {
        $('#outcomeNav').show();
        var here = $("#outcomeNav div.list-group");
        here.empty();
        for(var i=0;i<obj.data.length;i++) {
            here.append('<a class="list-group-item">'+obj.data[i].letter+'</a>');
        }
        $("#mainForm").text("Select an outcome for "+obj.courseName);
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
    } else if(thisPage()==='out') {
        console.log("should load outcome form");
        loadOutcomeForm(thisCourse(),thisOutcome());
    }
}

function loadPis(callback) {
    var url = 'dat/'+thisCourse()+'/'+thisOutcome();
    $.getJSON(url,function(obj) {
        $('#piNav').show()
        var here = $("#piNav div.list-group");
        var addPi = $("#addPi").detach();
        here.empty();
        for(var i=0;i<obj.data.length;i++) {
            here.append('<a class="list-group-item">'+obj.data[i].name+'</a>');
        }
        addPi.removeClass("active");
        addPi.appendTo(here);
        $("#mainForm").text("Select an performance indicator for "+obj.outcome);
        $('#piNav .list-group-item').click(pushPi);
        if(typeof callback === 'function') callback();
    })   
};

function loadOutcomeForm(course,outcome,callback) {
    var url = 'form/out/'+course+'/'+outcome;
    $("#mainForm").load(url,function(obj) {
        console.log("outcome callback")
    });
}


// **************  Performance Indicator Navigation  ************* //
function pushPi() {
    selectNav.call(this,"#piNav");
    var ptext = $(this).text();
    loadPiForm(thisCourse(),thisOutcome(),ptext);
}

function loadPiForm(course,outcome,pi,callback) {
    var url;
    if(pi=='+') url = 'form/pi/'+course+'/'+outcome+'/~'
    else url = 'form/pi/'+course+'/'+outcome+'/'+pi;
    $("#mainForm").load(url,function() {
        $("#updateBtn").click(submitPiForm);
        if(typeof callback === 'function') callback();
    });
}


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
    
