# Foobar

Foobar is a Python library for dealing with word pluralization.

## Installation

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