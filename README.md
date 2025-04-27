# BlogApplication

This is a simple blog application built with Flask, featuring user authentication (sign-up and login), creating, editing, and viewing posts, as well as commenting and liking posts. The front-end is styled with Tailwind CSS for a modern design.

Features
-User Authentication: Users can sign up, log in, and maintain their sessions.

-Create Posts: Authenticated users can create new posts.

-Edit and Delete Posts: Users can edit and delete their own posts.

-Post Interactions: Users can like posts and view comments.

-Search Posts: Posts can be searched by username.

-Commenting: Users can comment on posts, and delete their own comments.

-Pagination: Posts are paginated to handle large amounts of content efficiently.

Tech Stack
-Backend: Python with Flask

-Frontend: HTML, Tailwind CSS

-Database: PostgreSQL

-Authentication: Flask-Login for session management

-ORM: SQLAlchemy for database interaction

-Frontend Framework: Tailwind CSS

*Templates
*Base Template (base.html)
This is the root template for the application. It defines the common structure like the header and footer, and all pages extend this template.

*Home Page (home.html)
The home page displays a list of posts, a search form, and a button to create a new post. Posts can be liked, and users can toggle comments.

*Post Detail (post_detail.html)
When a user clicks on a post, they are taken to this page where they can view the post, like it, and leave comments. Users can also delete or edit their comments and posts if they are the author.

*Login (login.html)
The login page allows users to log into the application with their credentials.

*Sign Up (signup.html)
Users can sign up by providing their email, username, and password.

*Create Post (create_post.html)
This page allows users to create a new post by entering the post content.

*Database Models
*User Model
The User model stores the user information, such as email, username, and password. It is used for user authentication.

*Post Model
The Post model represents a blog post, including the post's text content, author, and associated comments.

*Comment Model
The Comment model represents a comment on a post, including the comment's text content and the user who authored it.

Routes and Views
*/ - Home page that lists all posts.

*/login - Login page.

*/signup - Sign-up page.

*/create-post - Page to create a new post.

*/posts/<username> - Displays all posts by a specific user.

*/posts/<int:post_id>/edit - Edit a specific post.

*/posts/<int:post_id>/delete - Delete a specific post.

*/create-comment/<int:post_id> - Add a comment to a post.

*/delete-comment/<int:comment_id> - Delete a specific comment.