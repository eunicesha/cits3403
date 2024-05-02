function createChallenge() {
    // make a new challenge
    alert("Please login first");
}

document.addEventListener("DOMContentLoaded", function() {
    loadChallenges();
});

function loadChallenges() {
    //sample data - need to find a way to dynamically fill from db
    const challenges = [
        { id: 1, name: 'Mia' },
        { id: 2, name: 'Tashi' },
        { id: 3, name: 'Eunice' }
    ];

    const challengesContainer = document.getElementById('challenges');
    challenges.forEach(challenge => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-body">
                <p>${challenge.name} is looking for a challenger!</p>
                <button class="btn btn-primary" onclick="acceptChallenge()">Accept Challenge</button>
            </div>
        `;
        challengesContainer.appendChild(card);
    });
}


//redirects to challenge page
function acceptChallenge() {
    window.location.href = '1v1 page/challenge.html'; 
}
document.addEventListener('DOMContentLoaded', loadChallenges);

