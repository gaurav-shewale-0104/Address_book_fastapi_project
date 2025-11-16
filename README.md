# Address_book_fastapi_project
#Clone the Repository
git clone https://github.com/gaurav-shewale-0104/Address_book_fastapi_project.git
cd Address_book_fastapi_project

#Create a Virtual Environment
python -m venv newvenv
cd venv\Scripts\activate

# Install reuired packages
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

