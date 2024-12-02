list of intruction

# create a new environment with python 3.10
conda create -n learning python=3.10

# list all the environments that have been created
conda env list   

# activate the environment that has been created
conda activate learning 

# install all the packages in the requirements.txt file
pip install -r requirements.txt

# start the crawler by running the following command
uvicorn blog.main:app --reload
# fast_api
