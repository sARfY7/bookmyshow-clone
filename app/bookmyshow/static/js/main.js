$(".seat").click(function(event) {
  const selectedElement = $(this);
  selectedElement.toggleClass('active');
})

$(".book-now__btn").click(function(event) {
  event.preventDefault();
  const selectedSeats = []
  const seats = $(".seat")
  for(seat of seats) {
    if (seat.classList.contains("active")) {
      selectedSeats.push({row: seat.dataset.row, column: seat.dataset.column})
    }
  }
  sendSeatData(selectedSeats);
})

function sendSeatData(seatData) {
  $("#seats-data").val(JSON.stringify(seatData));
  $('#seat-form').submit();
}

$('.pay-now__btn').click(function(event) {
  event.preventDefault();
  $('#booking-form').submit();
});

$('#search-inp').on("input", function(event) {
  const autocompleteResultsElement = $(".autocomplete__results")
  const searchQuery = event.target.value;
  if (searchQuery == "") {
    autocompleteResultsElement.css({ opacity: 0, 'pointer-events': 'none' });
    return
  }
  const endpointUrl = `/movies/search?q=${searchQuery}`
  $.get(endpointUrl, function(data) {
    autocompleteResultsElement.css({"opacity": 1, "pointer-events": "all"})
    autocompleteResultsElement.html(data);
  })
})

$("#download__btn").click(function() {
  const endpointUrl = "/user/data";
  $.post(endpointUrl, function(data) {
    checkTaskStatus(data.location)
  })
})

function checkTaskStatus(taskCompletionUrl) {
  timerId = setInterval(function() {
    $.get(taskCompletionUrl, function(data) {
      parsedData = JSON.parse(data)
      if (parsedData.status == 'SUCCESS') {
        downloadUserData();
        clearInterval(timerId);
      }
    })
    .fail(function () {
      clearInterval(timerId);
    })
  }, 1000)
}

function downloadUserData() {
  const endpointUrl = "/user/data/download"
  window.location = endpointUrl;
}