# Homework 09: Notes

Clone the repository and change dir to the homework-09 folder

```bash
git clone https://github.com/jdanussi/ml-zoomcamp-2024.git
cd ml-zommcamp-2024/homework-09
```

Create a virtualenv, install the dependencies and activate the new environment 

```bash
pipenv install
pipenv shell
```

Download the trained model

```bash
wget https://github.com/alexeygrigorev/large-datasets/releases/download/hairstyle/model_2024_hairstyle.keras
```

Run ipython to convert the keras model into tensorflow lite compatible model.

```python
ipython

In [1]: import tensorflow as tf
In [2]: from tensorflow import keras
In [3]: model = keras.models.load_model('model_2024_hairstyle.keras')
In [4]: converter = tf.lite.TFLiteConverter.from_keras_model(model)
In [5]: tflite_model = converter.convert()
In [6]: with open('model_2024_hairstyle.tflite', 'wb') as f_out:
    ...:     f_out.write(tflite_model)
    ...: 
```

Export notebook.ipynb to `homework.py`, adjust the python script and make a prediction for the example image

```python
ipython

In [1]: import homework
In [2]: url = 'https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'
In [3]: homework.predict(url)
Out[3]: 0.893774151802063
```

Test the service deployed on docker
```bash
# Download the base image
docker pull agrigorev/model-2024-hairstyle:v3

# Check the size
docker image ls | grep agrigorev
agrigorev/model-2024-hairstyle                                                                   v3                             607850a2138e   5 days ago      782MB
```

Modify `homework.py` to use `tflite_runtime.interpreter` in place of `tensorflow.lite`, and to setup the model name as a parameter MODEL_NAME. 
Then build the docker image from Dockerfile, run the container and test the service

```bash

docker build -t zoomcamp-serverless-homework .

docker run -it --rm --name mlzoomcamp -p 8080:8080 zoomcamp-serverless-homework

python test.py 
{'prediction': 0.4298535883426666}

```


