'use strict';

var client_id;
var game_id;
var end_time;
var timer;
var accepted;
var rejected;
var others;
var socket;

$(document).ready(function() {
  socket = io.connect('http://' + document.domain + ':' + location.port + '/');//, {query: game_id});
  $("form").on("submit", handle_form);

  end_time = get_timestamp() + server_remaining_secs;
  timer = setInterval(timer_loop, 500); // 0.5 secs
  // Update fields from server values
  update_ui(); 
  $("#input").disable = false;
});

function timer_loop() {
  update_time();
  submit_state();
}

function end_game() {
  disable_form();
  clearInterval(timer);
}

function handle_form() {
  event.preventDefault();

  // Read and clear input field
  var txt = $("input").val();
  $("input").val("")
  var words = txt.toLowerCase().split(/, /);

  // Process input
  words.forEach(function (word) {
    if (subs.includes(word)) {
      if (!accepted.includes(word)) {
        accepted.push(word);
      }
    } else if (is_lowercase_ascii(word) && !rejected.includes(word)) {
        rejected.push(word);
    }
  });
  submit_state();
  update_ui();

  return false;
}

function submit_state() {
  // Send complete client state to the server.
  var data = JSON.stringify({'game_id':game_id, 'accepted':accepted, 'rejected':rejected})
  socket.emit('submit', data)
  console.log('Submitted ' + data)  
}

function update_ui() {
  var atxt = accepted.join(", ");
  var rtxt = rejected.join(", ");
  // Only display lower case ascii plus comma and
  if (is_text(atxt)) {
    $("#accepted").html(atxt); 
  } 
  if (is_text(rtxt)) {
    $("#rejected").html(rtxt);
  }
  $("#score_value").html(calculate_score());
  var otherstxt = "";
  others.forEach(function (other) {
    otherstxt += other['client_id'] + ': ' + other['score'] + "<br>"
  })
  $("#others").html(otherstxt)
}

function update_time() {
  var remaining = Math.max(end_time - get_timestamp(), 0);
  var mins = Math.floor(remaining / 60);
  var secs = remaining % 60;
  var txt = mins + ":" + pad(secs, 2);
  $("#timer").html(txt);

  if (remaining <= 0) {
    end_game()
  }
}

function calculate_score() {
  var score = 0;
  accepted.forEach(function (word) {
    score += word.length;
  });
  return score * 10;
}

function disable_form() {
  $("#input").disabled = true;
  $("#input").val("");
}

/** 
 * Return the current time in seconds since the epoch.
 */
function get_timestamp() {
  return Math.floor(new Date().getTime() / 1000);
}

/** 
 * Pad a number with leading zeros.
 */
function pad(num, len) {
  var str = num.toString();
  if (str.length >= len) {
    return str;
  }
  return "0".repeat(len - str.length) + str 
}

function is_lowercase_ascii(w) {
  return /[a-z]/.test(w);
}

function is_text(w) {
  return /[a-z, ]/.test(w);
}


