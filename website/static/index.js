// Function to handle the like action for a post
function like(postId) {
  // Get the HTML element that displays the like count for the post
  const likeCount = document.getElementById(`likes-count-${postId}`);
  // Get the HTML element for the like button of the post
  const likeButton = document.getElementById(`like-button-${postId}`);

  // Make a POST request to the server to like/unlike the post
  fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json())  // Parse the JSON response from the server
    .then((data) => {
      // Update the like count displayed on the page
      likeCount.innerHTML = data["likes"];
      
      // Change the button style based on whether the post is liked or not
      if (data["liked"] === true) {
        likeButton.className = "fas fa-thumbs-up";  // Liked state: filled thumbs-up
      } else {
        likeButton.className = "far fa-thumbs-up";  // Unliked state: outline thumbs-up
      }
    })
    .catch((e) => alert("Could not like post."));  // If an error occurs, show an alert
}
