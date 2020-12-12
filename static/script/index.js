var table;
var request = {
  'guid': null,
  'number': null,
  'name': null,
  'subtitle': null
}

function receiveAllCourses() { 
  jQuery.ajax({
    type: "GET",
    url: "http://localhost:5000/api/courses",
    dataType: "json",
  
    success: function(response) {
    
      buildTableAll(response);
    }
  });
}

function searchCourse(input) {
  //var request = buildRequest()
  var element = $("#element_selection")[0].value;
  //var data = e.value;
  console.log(request)
  for (var elem in request) {
    if (elem == element) {
      request[elem] = input
    }
  } 
  console.log(request)

  jQuery.ajax({
    type: "POST",
    url: "http://localhost:5000/api/search",
    data: JSON.stringify(request),
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    async: false,
    success: function(response) {
      buildTableAll(response);
    }
  });
}

function buildTableAll(dataSet) {
  console.log(dataSet)
  table ? table.destroy() : void(0);
  table = $('#table').DataTable( {
      data: dataSet,
      "columns": [
        { "data": "guid" },
        { "data": "number" },
        { "data": "name" },
        { "data": "subtitle" }
    ],
    "oLanguage": { "sSearch": "Filtern"}
  } );
}
