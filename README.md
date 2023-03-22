# Pokemon Checklist
## Description
This project is a web server that allows users to keep track of which Pokemon that have caught in the Pokemon games. The server uses data scraped from [Serebii.net](https://serebii.net) to display information about all the Pokemon in the National Pokedex, and allows users to mark each Pokemon as "caught" or "not caught."

## Preview
![Preview](/checklist/static/img/sample.png)

## Installation
To install and run this project, you will need to have Python 3.x, Django, requests, bs4, pandas, pillow, and lxml installed on your computer. Once you have these dependencies installed, follow these steps:

1. Clone or download the project code from this repository.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the command `python manage.py runserver`.
4. Open a web browser and go to `http://localhost:8000` to view the home page.

## Usage
The home page of the web server displays a list of all the Pokemon in the National Pokedex, along with their names, numbers, and images. Each Pokemon is displayed in a container with a checkbox next to it.

To mark a Pokemon as "caught," simply click on the checkbox next to the Pokemon's name. The container for the Pokemon will turn gray to indicate that it has been caught. To mark the Pokemon as "not caught," simply uncheck the checkbox.

To view a list of all the Pokemon you have caught, click on the "Checklist" link in the navigation bar. This will take you to a page that displays only the Pokemon you have caught, along with their names, numbers, and images.

To log in to the web server and save your progress, click on the "Sign in" button in the navigation bar. You can log in with an existing account, or create a new account if you do not have one. Once you are logged in, your progress will be saved to the database, and you can view your progress from any device by logging in with the same account.

## Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request.

## Acknowledgements
Special thanks to [Serebii.net](https://serebii.net) for providing the data used in this project, and to [Living Pokedex Tracker](https://pokedexapp.net/) for inspiring the UI layout."
