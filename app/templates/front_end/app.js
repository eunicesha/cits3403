document.addEventListener("DOMContentLoaded", function() {
    loadChallenges();
});

function loadChallenges() {
    // Sample data - for actual use, this should be fetched from a database or server
    const challenges = [
        { id: 1, name: 'Mia' },
        { id: 2, name: 'Tashi' },
        { id: 3, name: 'Eunice' },
        { id: 3, name: 'Davin' },
    ];

    const challengesContainer = document.getElementById('challenges');
    challenges.forEach(challenge => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-body">
                <p class = "title" style = "font-size: 26px">${challenge.name} is looking for a challenger!</p>
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
