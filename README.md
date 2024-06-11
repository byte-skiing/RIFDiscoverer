# RIFDiscoverer

## Manual install

Make sure you have Python 3.8.10 or above installed in your machine, and that `python3` is your OS path. To run the testing application is necessary to have `python3-tk` and Android Debug Bridge (adb).

```
sudo apt-get install python3-tk
sudo apt-get install adb
```

With the previous packages installed, you can:

### 1. Create your virtual environment

```
python3 -m venv .venv
```

### 2. Activate your virtual environment

```
source .venv/bin/activate
```

### 3. Install required packages

```
pip install -r requirements.txt
```

### Running the application

After doing the installation steps, everytime you want to use the application, make sure the virtual environment is activated by running the following command.

```
source .venv/bin/activate
```

Then, you can execute the python script that will launch the application in your browser


```
python3 main.py
```

When you're finished, type `deactivate` in your terminal to make sure you're out of the virtual environment.


### Demonstration Video

A demonstation video showing how to use the tool is available on [Youtube](https://youtu.be/oz39ME5KDas).
