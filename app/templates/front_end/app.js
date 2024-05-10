document.addEventListener("DOMContentLoaded", function() {
    loadChallenges();
});

function loadChallenges() {
    // Fetch data from the server
    fetch('/fetch_challenges')  // Endpoint on the server to fetch challenges
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(challenges => {
        // Handle the fetched challenges
        console.log('Challenges:', challenges);
        // You can process the challenges here, e.g., update the UI
        displayChallenges(challenges); // Call another function to display challenges
    })
    .catch(error => {
        // Handle error
        console.error('Error loading challenges:', error);
    });
}

function displayChallenges(challenges) {
    const challengesContainer = document.getElementById('challenges');
    // Clear previous challenges (if any)
    challengesContainer.innerHTML = '';
    // Loop through the fetched challenges and create cards for each challenge
    challenges.forEach(challenge => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-body">
                <p class="title" style="font-size: 26px">${challenge.name} is looking for a challenger!</p>
                <button class="btn btn-primary fun" onclick="openAcceptChallengeModal(${challenge.id})">Accept Challenge</button>
            </div>
        `;
        challengesContainer.appendChild(card);
    });
}


function openAcceptChallengeModal(challengeId) {
    // Retrieve the challenge details, if needed, or directly pass challengeId if no details are needed
    console.log('Challenge ID:', challengeId); // note: use challengeId to fetch more details if needed
    const modalTitle = document.querySelector('#acceptChallengeModalLabel');
    const modalBody = document.querySelector('#acceptChallengeModal .modal-body');
    modalTitle.textContent = `Accept Challenge #${challengeId}`;
    // note: update modal content or actions based on the challengeId if needed
    const acceptModal = new bootstrap.Modal(document.getElementById('acceptChallengeModal'));
    acceptModal.show();
}

// Function to handle when a move is selected in the modal
function handleSubmitCreateGame(event) {
    event.preventDefault(); // Prevent the default form submission

    // Get the game ID and selected move from the form
    const move = document.querySelector('input[name="move"]:checked').value;
    const stake = document.querySelector('input[name="stake"]:checked').value;

    fetch('/create_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            move: move,
            stake: stake
        })
    })

    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle success response from the server
        console.log('Game successfully created:', data);
        // You can perform additional actions here if needed
    })
    .catch(error => {
        // Handle error
        console.error('Error creating game:', error);
    });
};

function loginUser(username, password) {
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Redirect to the next page after successful login
        } else {
            // Handle login failure
        }
    })
    .catch(error => {
        console.error('Error logging in:', error);
        // Handle error
    });
}

function signupUser(username, email, password) {
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Redirect to the next page after successful signup
        } else {
            // Handle signup failure
        }
    })
    .catch(error => {
        console.error('Error signing up:', error);
        // Handle error
    });
}
