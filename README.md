To Run the applcation.

run the following commands

python -m venv .venv
pip install -r requirements.txt
uvicorn main:app


To Run the application through docker image

1. Run the below command from the root directory which would create the docker image.
   docker compose up --build (use --build only on first time)



