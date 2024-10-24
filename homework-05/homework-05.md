# Homework 05: Notes

```bash
# pipenv version
pipenv --version
pipenv, version 2024.0.1

# Virtualenv creation and Install scikit-learn version 1.5.2.
pipenv install scikit-learn==1.5.2
Courtesy Notice: Pipenv found itself running within a virtual environment, so it will automatically use that environment, instead of creating its own for any project. You can set PIPENV_IGNORE_VIRTUALENVS=1 to force pipenv to ignore that environment and create its own instead. You can set PIPENV_VERBOSITY=-1 to suppress this warning.
Creating a Pipfile for this project...
Installing scikit-learn==1.5.2...
Resolving scikit-learn==1.5.2...
Added scikit-learn to Pipfile's [packages] ...
✔ Installation Succeeded
Pipfile.lock not found, creating...
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success!
Locking [dev-packages] dependencies...
Updated Pipfile.lock (dd888bf29237b1b0220d56230d97bb0c50d6abc3ae64665667d1fe2d150b43dd)!
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Installing dependencies from Pipfile.lock (0b43dd)...

# Activation of the new virtualenv
pipenv shell
Creating a virtualenv for this project...
Pipfile: /home/jdanussi/Documents/DataTalksClub/ml-zoomcamp/ml-zoomcamp-2024/homework-05/Pipfile
Using /usr/bin/python3 (3.10.12) to create virtualenv...
⠧ Creating virtual environment...created virtual environment CPython3.10.12.final.0-64 in 494ms
  creator CPython3Posix(dest=/home/jdanussi/.local/share/virtualenvs/homework-05-_0hcOUgB, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/jdanussi/.local/share/virtualenv)
    added seed packages: pip==24.2, setuptools==75.0.0, wheel==0.44.0
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

✔ Successfully created virtual environment!
Virtualenv location: /home/jdanussi/.local/share/virtualenvs/homework-05-_0hcOUgB
Launching subshell in virtual environment...
 . /home/jdanussi/.local/share/virtualenvs/homework-05-_0hcOUgB/bin/activate
(base) jdanussi@jad-xps15:~/Documents/DataTalksClub/ml-zoomcamp/ml-zoomcamp-2024/homework-05$  . /home/jdanussi/.local/share/virtualenvs/homework-05-_0hcOUgB/bin/activate

# Check the python path in the new virtualenv 
which python
/home/jdanussi/.local/share/virtualenvs/homework-05-_0hcOUgB/bin/python

# Installing dependencies for deploying the predict service
pipenv install Flask gunicorn requests

# Running the prediction service
gunicorn --bind 0.0.0.0:9696 subscript_serving:app

# Making a prediction 
python test_service_venv.py 
{
  "term_deposit": false,
  "term_deposit_probability": 0.33480703475511053
}

# Get the docker image svizor/zoomcamp-model:3.11.5-slim
docker pull svizor/zoomcamp-model:3.11.5-slim
3.11.5-slim: Pulling from svizor/zoomcamp-model
a803e7c4b030: Pull complete 
bf3336e84c8e: Pull complete 
eb76b60fbb0c: Pull complete 
a2cee97f4fbd: Pull complete 
0358d4e17ae3: Pull complete 
fb37f8d7a667: Pull complete 
4e69cd59a5af: Pull complete 
Digest: sha256:15d61790363f892dfdef55f47b78feed751cb59704d47ea911df0ef3e9300c06
Status: Downloaded newer image for svizor/zoomcamp-model:3.11.5-slim
docker.io/svizor/zoomcamp-model:3.11.5-slim

# Show the image size  
docker image ls | grep svizor
svizor/zoomcamp-model                                                                            3.11.5-slim                    975e7bdca086   5 days ago      130MB

# Running the web service from venv
python subscript_serving_venv.py 
 * Serving Flask app 'subscript'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:9696
 * Running on http://10.251.1.2:9696
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 124-661-014

# Making a prediction 
python test_service_venv.py 
{
  "subscript": false,
  "subscript_probability": 0.33480703475511053
}

# Building a custom image from Dockerfile
docker build -t subscript_predict .

# Running the container with the prediction service
docker run --rm -p 9696:9696 subscript_predict
[2024-10-23 23:46:06 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2024-10-23 23:46:06 +0000] [1] [INFO] Listening at: http://0.0.0.0:9696 (1)
[2024-10-23 23:46:06 +0000] [1] [INFO] Using worker: sync
[2024-10-23 23:46:06 +0000] [7] [INFO] Booting worker with pid: 7

# Making a prediction
python test_service_docker.py 
{
  "subscript": true,
  "subscript_probability": 0.756743795240796
}
```

