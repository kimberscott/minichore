# Minichore

This is a Django site for allocating chores among household members using a simple, brute-force minimax algorithm. Each household member gets to say how much each chore is "worth" to him or her, and then we minimize the total work done by each person according to their own weightings. 

For instance, maybe Bob thinks laundry is 60% of the work and 
dishes are 40% of the work, and Joe thinks that dishes are 60% while laundry is 40%. Clearly, Bob should do the dishes and Joe should do the laundry - they'll each feel like they're getting the better deal! But as the number of chores and/or household members grows, it gets trickier to optimize without a lot of horse-trading. That's where minichore comes in.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- Install pyenv (see https://github.com/yyuu/pyenv)

- Install virtualenv
  `[sudo] pip install virtualenv`

- Install python 3.6.4 or higher via pyenv, e.g.:
  `pyenv install 3.6.4`

### Installing

1. Clone this repo. (You can fork it to keep track of your own changes on github if you want, and submit PRs back here.)
2. Create a virtual environment (from the main minichore directory, or wherever else is convenient for you):
  `virtualenv -p ~/.pyenv/versions/3.6.4/bin/python3.6 venv`
3. Enter the virtual environment
   `source venv/bin/activate`
4. Install requirements:
  `pip install -r requirements.txt`
5. Now you should be able to run it locally using manage.py!
  ```
      python manage.py makemigrations
      python manage.py migrate
      python manage.py runserver
   ```
6. After installation, you can run the server just by entering the virtual environment and using `manage.py runserver`.

## Running the tests

There are no tests yet! Sorry. 

## Deployment

Notes on how to deploy once that happens once!

## Contributing

Contributions are welcome! 
