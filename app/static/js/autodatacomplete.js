$(function() {

  var emails=[];
  var availableTutorials = [ "ActionScript", "Boostrap", "C", "C++", ];

  var myjson;
  $.getJSON("/countries", function(json){
    myjson = json;
  });
    
  console.log(myjson);

$( "#autocplt" ).autocomplete({
  source: myjson,
});


});
