



function getUsername() {
    //get usernames of users
    return ['User1', 'User2'];
}

window.onload = function() {
    const usernames = getUsername();
    document.getElementById('usernames').textContent = usernames.join(' vs ');
};

function submitAnswer() {
    const answer = document.getElementById('answerInput').value;
    console.log("Submitted answer:", answer);
  //finish later to sort out submitted answers
}
