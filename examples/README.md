# Quick Start
For testing purposes, the ```examples``` project can be deployed as follows: 

1. Download the zip of the repo and place the examples folder somewhere in your machine.

2.  Install apiDoc.
```shell
sudo npm install -g apidoc
```
- The apiDoc framework will enable you to document services using **<span style="color:#adc03a"> froggy's:frog:</span>** custom apiDoc wrapper.

3. Execute the following set of commands to create a python3 virtual environment and install the requirements:

```shell
cd examples
python3 -m venv cookbook/venv
source cookbook/venv/bin/activate
pip3 install -r requirements.txt
```

4. Run the application:
```shell
$ export FLASK_APP=cookbook
$ flask run
```

And... you are done! :smile: The documentation can now be accessed on the following URL ```http://localhost:5000```
