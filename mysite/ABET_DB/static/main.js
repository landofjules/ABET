$("#outcomeNav, #piNav").hide();   


// when a course is selected, load the outcomes
function loadOutcomes() {
    selectNav.call(this);
    var ctext = $(this).text();
    $.getJSON('dat/'+ctext,function(obj) {
        $('#outcomeNav').show()
        var here = $("#outcomeNav div.list-group");
        here.empty();
        for(var i=0;i<obj.data.length;i++) {
            here.append('<a class="list-group-item" href="#">'+obj.data[i].letter+'</a>');
        }
        $("#mainForm").text("Select an outcome for "+obj.courseName);
        $('#outcomeNav .list-group-item').click(loadPis);
    })   
};
$('#courseNav li').click(loadOutcomes);


// when an outcome is selected, load the Preformance indicators
function loadPis() {
    var ctext = $("#courseNav li.active").text();
    var otext = $(this).text();
    $.getJSON('dat/'+ctext+'/'+otext,function(obj) {
        $('#piNav').show()
        var here = $("#piNav div.list-group");
        here.empty();
        for(var i=0;i<obj.data.length;i++) {
            here.append('<a class="list-group-item" href="#">'+obj.data[i].level+'</a>');
        }
        $("addPi").detach().appendTo(here);
        $("#mainForm").text("Select an performance indicator for "+obj.outcome);
        $('#piNav .list-group-item').click(selectNav);
        selectNav.call(this);
    })   
};
$('#outcomeNav a').click(loadPis);

//when a preformance indicator is selected, load the main form
function loadPiForm() {
    selectNav.call(this);   
    var ctext = $("#courseNav li.active").text();
    var otext = $("#outcomeNav a.active").text();
    var ptext = $(this).text();
    
    //load the view
    var url = 'form/'+ctext+'/'+otext+'/'+ptext;
    $("#mainForm").load(url)
}


// link highlighting
$('.list-group-item').click(selectNav);
function selectNav() {
    var parentId = $(this).parent().parent().attr('id');
    var type = $(this).get(0).tagName;
    $('#'+parentId+' '+type).removeClass('active');
    $(this).addClass('active');
}

