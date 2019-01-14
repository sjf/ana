'use strict';

var end_time;
var timer;
var accepted;
var rejected;

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
  $("form").on("submit", handle_form);

  accepted = [];
  rejected = [];
  end_time = get_timestamp() + server_remaining_secs;
  timer = setInterval(update_time, 500); // 0.5 secs
  $("#input").disable = false;
});


function handle_form() {
  event.preventDefault();
  console.log('handle');

  var txt = $("input").val();
  $("input").val("")
  rejected = [];
  var words = txt.split(/, /);
  words.forEach(function (word) {
    if (subs.includes(word)) {
      if (!accepted.includes(word)) {
        accepted.push(word);
      }
    } else if (!rejected.includes(word)) {
        rejected.push(word);
    }
  });

  $("#accepted").html(accepted.join(", ")); // not sanitised
  $("#rejected").html(rejected.join(", ")); // not sanitised
  $("#score_value").html(calculate_score()); 
}

function calculate_score() {
  var score = 0;
  accepted.forEach(function (word) {
    score += word.length;
  });
  return score;
}
