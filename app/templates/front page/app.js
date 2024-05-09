

document.addEventListener("DOMContentLoaded", function() {
    loadChallenges();
    updateUserWagerLimits();
});


function updateUserWagerLimits() {
    // assuming a function fetchUserPoints() that returns a promise with the points
    fetchUserPoints().then(points => {
        document.getElementById('createWager').placeholder = `Your points: ${points}`;
        document.getElementById('createWager').max = points;

        document.getElementById('acceptWager').placeholder = `Your points: ${points}`;
        document.getElementById('acceptWager').max = points;
    });
}

function fetchUserPoints() {
    // placeholder for fetching user points; replace with actual API call
    return Promise.resolve(100); // eg: User has 100 points
}

function loadChallenges() {
    const challenges = [
        { id: 1, name: 'Mia', points: 50 },
        { id: 2, name: 'Tashi', points: 30 },
        { id: 3, name: 'Eunice', points: 20 },
        { id: 4, name: 'Davin', points: 40 },
        { id: 5, name: 'Bob', points: 69 },
    ];

    const challengesContainer = document.getElementById('challenges');
    challenges.forEach(challenge => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-body">
                <p class="title" style="font-size: 26px">${challenge.name} is looking for a challenger!<p>
                <p class ="title" style:margin-botton 10px >Wager: ${challenge.points} points</p>
                <button class="btn btn-primary fun" onclick="openAcceptChallengeModal(${challenge.id}, ${challenge.points})">Accept Challenge</button>
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
