# FastAPI Chat Application

This is a simple FastAPI application with a single endpoint `/chat` that uses `StreamingResponse` to stream chat messages in real-time.

## Project Structure

- `.gitignore`: Specifies files and directories to be ignored by Git.
- `README.md`: Provides an overview of the project.
- `requirements.txt`: Lists the required Python packages and their versions.
- `app/`: Contains the application code.
  - `main.py`: Initializes the FastAPI application.
  - `models.py`: Defines the data models used in the application.
  - `routes.py`: Defines the API routes and their corresponding functions.
  - `utils.py`: Contains utility functions used in the application.