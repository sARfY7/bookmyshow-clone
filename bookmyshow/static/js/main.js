$(".seat").click(function(event) {
  selectedElement = $(this);
  selectedElement.toggleClass('active');
})

$(".book-now__btn").click(function(event) {
  event.preventDefault();
  selectedSeats = []
  seats = $(".seat")
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