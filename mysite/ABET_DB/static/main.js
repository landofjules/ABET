

// when a course is selected, load the outcomes
function loadOutcomes(courseName) {
    selectNav.call(this);
    $.getJSON('dat/'+courseName,function(obj) {
        $('#outcomeNav').show()
        var here = $("#outcomeNav div.list-group");
        here.empty();
        for(var i=0;i<obj.data.length;i++) {
            here.append('<a class="list-group-item" href="#">'+obj.data[i].letter+'</a>');
        }
        $("#mainForm").text("Select an outcome for "+obj.courseName);
        $('#outcomeNav .list-group-item').click(loadPis);
        $('#piNav').hide();
    })   
};
$('#courseNav li').click(function() {
    if($(this).is("#earlierCourses")){
        selectNav.call(this);
        $("#ect").hide();
        $("#ecm").show();
    } else {
        selectNav.call(this);
        loadOutcomes($(this).text());
        $("#ecm").hide();
        $("#ect").show();
    }
});


// when an outcome is selected, load the Preformance indicators
function loadPis() {
    selectNav.call(this);
    var ctext = $("#courseNav li.active").text();
    var otext = $(this).text();
    $.getJSON('dat/'+ctext+'/'+otext,function(obj) {
        $('#piNav').show()
        var here = $("#piNav div.list-group");
        var addPi = $("#addPi").detach();
        here.empty();
        for(var i=0;i<obj.data.length;i++) {
            here.append('<a class="list-group-item" href="#">'+obj.data[i].name+'</a>');
        }
        addPi.appendTo(here);
        $("#mainForm").text("Select an performance indicator for "+obj.outcome);
        $('#piNav .list-group-item').click(pushPi);
    })   
};
$('#outcomeNav a').click(loadPis);

function pushPi() {
    selectNav.call(this);   
    var ctext = $("#courseNav li.active").text();
    var otext = $("#outcomeNav a.active").text();
    var ptext = $(this).text();
    loadPiForm(ctext,otext,ptext);
}
//when a preformance indicator is selected, load the main form
function loadPiForm(course,outcome,pi) {
    var url = 'form/'+course+'/'+outcome+'/'+pi;
    $("#mainForm").load(url);
}


// link highlighting
$('.list-group-item').click(selectNav);
function selectNav() {
    var parentId = $(this).parent().parent().attr('id');
    var type = $(this).get(0).tagName;
    $('#'+parentId+' '+type).removeClass('active');
    $(this).addClass('active');
    //$("#mainForm").css("min-width",$("#container").width() - $("#outcomeNav").width() - $("#piNav").width())
}

    
