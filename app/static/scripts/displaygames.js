document.addEventListener("DOMContentLoaded", function() {
    loadPosts();
});

function loadPosts() {
    fetch('/fetch_challenges') 
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(posts => {
        console.log('Posts:', posts);
      // will add ui stuff here
        displayPosts(posts);
    })
    .catch(error => {
        // Handle error
        console.error('Error loading posts:', error);
    });
}

function displayPosts(posts) {
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = '';
  // will check if posts have been responded to
    posts.forEach(post => {
        const postElement = document.createElement('div');
        postElement.innerHTML = `
            <div>
                <p>${post.author.username} says: <b>${post.body}</b></p>
            </div>
        `;
        postContainer.appendChild(postElement);
    });
}
