# Import the create_app function from the website module
from website import create_app

# Check if the script is being run directly (not imported)
if __name__ == "__main__":
    app = create_app()  # Create the Flask app instance using the create_app function
    app.run(debug=True)  # Run the app in debug mode for development (auto-reload, better error messages)
