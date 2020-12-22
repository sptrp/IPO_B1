var table, data, client_id;

/**
 * Function to receive all courses
 */
function receiveAllCourses() { 
  jQuery.ajax({
    type: "GET",
    url: "http://localhost:5000/api/courses",
    dataType: "json",
  
    success: function(response) {
      buildTable(response);
      
      // event handler for the row selection / deselection
      $('#table tbody').on('click', 'tr', function () {
        if ( $(this).hasClass('selected') ) { // deselect if selected 
          $(this).removeClass('selected');
          data = undefined;
          $('#course_info').text("");

        } else { // select if deselected
          table.$('tr.selected').removeClass('selected');
          $(this).addClass('selected');
          data = table.row( this ).data();
          $('#course_info_modal').modal('show');
          showCourseInfo();
        }
      } );
    }
  });
}

/**
 * Function to find courses
 */
function searchCourse(dataSet) {
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
      request[elem] = dataSet
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
      
      data = undefined;
      $('#course_info').text("");

      buildTable(response);

      // event handler for the row selection / deselection
      $('#table tbody').on('click', 'tr', function () {
        if ( $(this).hasClass('selected') ) { // deselect if selected 
          $(this).removeClass('selected');
          data = undefined;
          $('#course_info').text("");

        } else { // select if deselected
          table.$('tr.selected').removeClass('selected');
          $(this).addClass('selected');
          data = table.row( this ).data();
          $('#course_info_modal').modal('show');
          showCourseInfo();
        }
      } );
    }
  });
}

/**
 * Function to book courses
 */
function bookCourse() {
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
    url: "http://localhost:5000/api/book",
    data: JSON.stringify(request),
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    async: false,
    success: function(response) { console.log(response) } 
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
}


function showCourseInfo() {
    $('.info-guid').text(`Guid: ${data['guid']}`);
    $('.info-number').text(`Nummer: ${data['number']}`);
    $('.info-name').text(`Name: ${data['name']}`);
    $('.info-subtitle').text(`Untertitel: ${data['subtitle']}`);
    $('.info-category').text(`Kategorie: ${data['category']}`);
    $('.info-minmembers').text(`Min. Teilnehmer: ${data['min_members']}`);
    $('.info-maxmembers').text(`Max. Teilnehmer: ${data['max_members']}`);
    $('.info-keywords').text(`Schlagwörter: ${data['keywords']}`);
    console.log(data['keywords'])
}

function sendLoginRequest() {

  var request = {
    'type': 'login',
    'username': document.getElementById("login_username").value,
    'password': document.getElementById("login_password").value
  } 

  jQuery.ajax({
    type: "POST",
    url: "http://localhost:5000/api/login",
    data: JSON.stringify(request),
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    async: false,
    success: function(response) { 
      $('#login_modal').modal('hide');
      client_id = response['id'];
     }
  });
}

function sendLogoutRequest() {

  var request = {
    'type': 'logout',
    'username': null,
    'password': null
  } 

  jQuery.ajax({
    type: "POST",
    url: "http://localhost:5000/api/login",
    data: JSON.stringify(request),
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    async: false,
    success: function(response) { 
      console.log(response)
      $('#login_modal').modal('hide')
     }
  });
}

function sendRegisterRequest() {

  passwordHash = CryptoJS.SHA256(document.getElementById("register_password").value);

  var request = {
    'username': document.getElementById("register_username").value,
    'name': document.getElementById("register_name").value,
    'surname': document.getElementById("register_surname").value,
    'street': document.getElementById("register_street").value,
    'postcode': document.getElementById("register_postcode").value,
    'city': document.getElementById("register_city").value,
    'country': document.getElementById("register_country").value,
    'email': document.getElementById("register_email").value,
    'password': passwordHash.toString(CryptoJS.enc.Hex)
  } 
  console.log(request)
  jQuery.ajax({
    type: "POST",
    url: "http://localhost:5000/api/register",
    data: JSON.stringify(request),
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    async: false,
    success: function(response) { 
      console.log(response)
      $('#register_modal').modal('hide')
     }
  });
}

function openRegister() {
  $('#login_modal').modal('hide'); 
  $('#register_modal').modal('show');
}

function openLogin() {
  $('#register_modal').modal('hide');
  $('#login_modal').modal('show');
}


