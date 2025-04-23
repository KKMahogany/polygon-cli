# polygon-cli
Fork of command-line tool for [polygon](https://polygon.codeforces.com/)

This fork aims to improve the overall code quality and 

## Requirements

* diff and diff3 available in path

## Supported features

* Download files and solutions from polygon.
* Uploading them back to polygon.
* Automatic merging with conflicts.

## Installation

Python package installation can become a huge headache if you do so recklessly.
If this is your first time doing this, I would highly recommend reading [this](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments) section of the Python Packaging User Guide.

Creating a virtual environment to install this CLI is optional, but highly recommended.

### Prework

You will need to install [pip](https://pip.pypa.io/en/stable/installation/) (this is already installed if you're using a virtual environment).

You will also need to install [setuptools](https://pypi.org/project/setuptools/) (this *may* already be installed by default, depending on your Python version and choice of virtual environment).

### From PyPI

(You cannot install this fork from PyPI)

### From the source code

1. Checkout the repo (e.g. with `git clone https://github.com/kunyavskiy/polygon-cli.git`)
1. Run `python -m pip install path/to/downloaded/repo`
      * On Linux, it will put the executable polygon-cli in /usr/local/bin
      * On Windows, it will put the executable polygon-cli in Scripts directory of your Python3 installation. It should be added to the path variable for easier usage.

## Running and authentication

Run `polygon-cli -h` for useful help text.

Usually the usage starts with (use problem short name or problem id instead of `aplusb`):

```bash
# Initialise the working directory
polygon-cli init aplusb # or use the numeric problem ID if you prefer

# Pull a copy of all files from polygon
polygon-cli update 
```

On the first usage, you will be prompted to provide:

- `login`: your polygon username.
- `password`: your polygon password. Recommend you leave this blank, as it will be saved in plaintext.
  You will be prompted interactively if it is needed.
- `api_key` and `api_secret`: You can get this from your settings in polygon.

Most methods don't use the `login` / `password`, so you can just provide a dummy login and blank password.
Just the API key/secret are needed.
