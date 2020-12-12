var table;

function receiveAllCourses() { 
  jQuery.ajax({
    type: "GET",
    url: "http://localhost:5000/api/courses",
    dataType: "json",
  
    success: function(response) {
    
      buildTable(response);
    }
  });
}

function searchCourse(input) {
  var request = {
    'diverse': null,
    'guid': null,
    'number': null,
    'name': null,
    'subtitle': null,
    'keywords': null
  }

  var element = $("#element_selection")[0].value;

  console.log(request)
  for (var elem in request) {
    if (elem == element) {
      request[elem] = input
    }
  }

  jQuery.ajax({
    type: "POST",
    url: "http://localhost:5000/api/search",
    data: JSON.stringify(request),
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    async: false,
    success: function(response) {
      
      buildTable(response);
    }
  });
}

function buildTable(dataSet) {
  table ? table.destroy() : void(0);
  table = $('#table').DataTable( {
      responsive: true,
      data: dataSet,
      fixedHeader: true,
      select: true,
      "columns": [
        { title: "Guid", "data": "guid" },
        { title: "Nummer", "data": "number" },
        { title: "Name", "data": "name" },
        { title: "Untertitel", "data": "subtitle" }
    ],
    "oLanguage": { "sSearch": "Filtern"}
  } );

  // event handler for the row
  $('#table tbody').on('click', 'tr', function () {
      var data = table.row( this ).data();
      console.log( data );
      printInfo(data);
    } );
}


function printInfo(data) {
  var request = {
    'diverse': null,
    'guid': data['guid'],
    'number': null,
    'name': null,
    'subtitle': null,
    'keywords': null
  }

  jQuery.ajax({
    type: "POST",
    url: "http://localhost:5000/api/search",
    data: JSON.stringify(request),
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    async: false,
    success: function(response) {
      console.log(response)
      $('#course_info').text(`Guid: ${response[0]['guid']} Nummer: ${response[0]['number']} 
                          Name: ${response[0]['name']} Untertitel: ${response[0]['subtitle']}
                          Kategorie: ${response[0]['category']} Min. Teilnehmer: ${response[0]['min_members']} Max. Teilnehmer: ${response['max_members']}` );
    }
  });

}