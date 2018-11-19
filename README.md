# Rana Scheduler

This is a simple scheduler app made with Flask and Python 3.

## Installation

Clone the repository and cd into it.

```bash
git clone git@github.com:diggerdata/CS3733-Rana.git
cd CS3733-Rana
```

Setup a virtualenv to make it so your packages are not installed globally.

```bash
python3 -m venv .env
```

Source the newly created virtualenv to install all required pip packages.

```bash
source .enb/bin/activate
```

Install all required packages in `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Deployment

The initial deployment of the scheduler app to AWS.

```bash
zappa deploy dev
```