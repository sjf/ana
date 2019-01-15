'use strict';

var end_time;
var timer;
var accepted;
var rejected;
var socket;

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

function end_game() {
  disable_form();
  clearInterval(timer);
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

function disable_form() {
  $("#input").disabled = true;
  $("#input").val("");
}

$(document).ready(function() {
  socket = io.connect('http://' + document.domain + ':' + location.port + '/');//, {query: game_id});
  $("form").on("submit", handle_form);

  end_time = get_timestamp() + server_remaining_secs;
  timer = setInterval(update_time, 500); // 0.5 secs
  // Update fields from server values
  update_ui(); 
  $("#input").disable = false;
});


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
  // Send complete client state to the server.
  var data = JSON.stringify({'game_id':game_id, 'accepted':accepted, 'rejected':rejected})
  socket.emit('submit', data)
  console.log('Submitted ' + data)
  update_ui()

  return false;
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
}

function calculate_score() {
  var score = 0;
  accepted.forEach(function (word) {
    score += word.length;
  });
  return score * 10;
}
