document.getElementById('createChallengeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const challengeName = document.getElementById('challengeName').value;
    // Assuming the username is fetched from the session or a placeholder for now
    const username = 'PlaceholderUser'; // This will eventually come from the user's session

    // Post the new challenge to the server or local storage
    console.log(`New Challenge Created by ${username}: ${challengeName}`);
    
    // Redirect back to the main page or update UI directly
    window.location.href = 'indexx.html'; // Redirect user back to the main page
});
