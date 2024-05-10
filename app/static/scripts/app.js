function createChallenge() {
    // make a new challenge
    alert("Please login first");
}

document.addEventListener("DOMContentLoaded", function() {
    loadChallenges();
});


function loadChallenges() {
    //example data
    const challenges = [
        {
            id: 1, text: "Mia is looking for a challenger!", status: "Open", 
        },
        {
            id: 2, text: "Tashi is looking for a challenger!", status: "Open"
        },
        {
            id: 3, text: "Eunice is looking for a challenger!", status: "Open"
        }
    ];

    const challengesContainer = document.getElementById('challenges');
    challenges.forEach(challenge => {
        const cardHtml = `
            <div class="col-sm-6 col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${challenge.text}</h5>
                        <p class="card-text">Status: ${challenge.status}</p>
                        <button class="btn btn-primary challenge-btn" onclick="acceptChallenge(${challenge.id})">Accept Challenge</button>
                    </div>
                </div>
            </div>
        `;
        challengesContainer.innerHTML += cardHtml;
    });
}

function acceptChallenge(challengeId) {
    // what happens after accepting challenge
    console.log("Challenge accepted:", challengeId);
    alert(`Challenge ${challengeId} accepted!`);
}

