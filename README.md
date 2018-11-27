# Rana Scheduler

This is a simple scheduler app made with Flask and Python 3.

## Installation

Clone the repository and cd into it.

```bash
git clone git@github.com:diggerdata/CS3733-Rana.git
cd CS3733-Rana
```

### Linux/Mac
Setup a virtualenv to make it so your packages are not installed globally.

```bash
virtualenv .env
```

Source the newly created virtualenv to install all required pip packages.

```bash
source .enb/bin/activate
```

### Windows

First, you will need to change your PowerShell execution policty to run the script. Open PowerShell as an `Administrator` and run the following.
```bash
Set-ExecutionPolicy Unrestricted
```

Enter `A` and press `Enter`.

Now cd into the project directory and run the following in in a normal, non-administrator PowerShell.
```bash
.\.env\Scripts\activate
```

This will launch the virtual enviroment for the project. Within this environment you can install all the required packages without them being installed globally.

Install all required packages in `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Deployment

The initial deployment of the scheduler app to AWS.

```bash
zappa deploy dev
```