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

function start_game(){
  accepted = [];
  rejected = [];
  end_time = get_timestamp() + server_remaining_secs;
  timer = setInterval(update_time, 500); // 0.5 secs
  document.getElementById("input").disabled = false;
}

function end_game() {
  disable_form();
  clearInterval(timer);
  var answerElem = document.getElementById("answer");
}

function update_time() {
  var remaining = end_time - get_timestamp();
  var mins = Math.floor(remaining / 60);
  var secs = remaining % 60;
  var txt = mins + ":" + pad(secs, 2);
  document.getElementById("timer").innerHTML = txt;
  if (remaining == 0) {
    end_game()
  }
}

function disable_form() {
  var inputElem = document.getElementById("input")
  inputElem.disabled = true;
  inputElem.value = "";
}

function handle_form() {
  console.log('handle');
  var input = document.getElementById("input");
  var txt = input.value;
  input.value = "";
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

  var acceptedElem = document.getElementById("accepted");
  var rejectedElem = document.getElementById("rejected");
  acceptedElem.innerHTML = accepted.join(", "); // not sanitised
  rejectedElem.innerHTML = rejected.join(", "); // not sanitised

  var scoreElem = document.getElementById("score_value");
  scoreElem.innerHTML = calculate_score();
}

function calculate_score() {
  var score = 0;
  accepted.forEach(function (word) {
    score += word.length;
  });
  return score;
}
