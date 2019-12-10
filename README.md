Get Device List
===============


## Installation 

Create a virtualenv with python3.6 and activate 

```bash
$ virtualenv -p python3.6 env
$ source env/bin/activate
```

## Configuration 

Edit `~/.bashrc` file and add the following environment variables 


```bash 
export API_USERNAME=username
export API_PASSWORD=password
```

Run the the script


```bash
(env) $ source ~/.bashrc
(env) $ python3 get_device_list.py
``` 

