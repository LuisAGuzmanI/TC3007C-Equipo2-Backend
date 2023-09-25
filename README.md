# TC3007C-Equipo2-Backend

## How to Run

### Setting up a Local Environment

1. **Clone the Repository**
```
git clone https://github.com/LuisAGuzmanI/TC3007C-Equipo2-Backend.git
```

2. **Create a Virtual Environment** (Optional but recommended)
```
python -m venv venv
source venv/bin/activate # On Windows, use: venv\Scripts\activate
```

3. **Install Requirements**
```
pip install -r requirements.txt
```


4. **Set Environment Variables**

Create a `.env` file in the project root and set your environment variables. Example:
```
MONGO_URI="mongodb+srv://..."
```


### Running the Project

Use `uvicorn` to run the FastAPI application:
```
uvicorn main:app --reload
```

The `--reload` flag enables auto-reloading of the server when code changes are detected.

Access the API at `http://localhost:8000` in your web browser or via an API client.

## Project Structure

- `main.py`: The main script containing the FastAPI application setup.
- `app/`: This directory may contain additional modules or packages related to your application.
- `requirements.txt`: Contains a list of Python dependencies. Install them using `pip install -r requirements.txt`.

## Environment Variables

- `MONGO_URI`: URI for MongoDB database.
