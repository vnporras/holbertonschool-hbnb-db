# HBNB Solution Part 1

This solution successfully implements the repository pattern.
It passes the tests provided in the `/hbnb/part1/tests` directory.

## Some things to note

- Doesn't implement the place_amenities `endpoints` yet.
- The repositories impletented are `FileRepository` and `MemoryRepository`, and also has a placeholder for a `DBRepository`.
- The `MemoryRepository` doesn't persists the data between runs.
- The `FileRepository` persists the data in a JSON file by default called `data.json`.
- It was designed at first to work with memory just to test the tests.

## What you need to know about the solution?

- The repositories has a base class called Repository that has the methods that the repositories should implement. The class itself is an abstract class, and all the methods are abstract methods.
- - The methods are: `get`, `get_all`, `reload`, `save`, `update`, `delete`.
- The models has a base class called Base which is an abstract class, it contains three types of methods:
- - @abstractmethods - methods that the class that inherits from Base should implement. The methods are: `to_dict`
- - @classmethods - This methods are: `get`, `get_all`, `delete`. The logic for these methods is the same for all the models, so it was implemented in the Base class.
- - @staticabstractmethods - methods that the class that inherits from Base should implement, but are static methods. The methods are: `create`, `update`.

It has no documentation yet. ***And this nothing here was created with ChatGPT***. Sorry if something here is not clear enough 😅. Feel free to contact me if you don't understand something, I'm *Ignacio Peralta* find me on Slack.

> [!TIP]
> You can preload the persistence layer selected via the `reload` method in the `Repository` class.
> This method is called in the `__init__` method of the `Repository` class.

---

> [!IMPORTANT]
> The tests won't pass if there isn't a dummy country created, for example `MemoryRepository` on the reload function creates a dummy `UY` country via the `reload` method which also calls the `populate_db` function in the `utils/populate.py` file.

## MVC

The solution is divided into four main parts: `Models`, `Controllers`, and `Persistence`, but not uses Views because it is just a REST API.

- In the `controllers` package you will find the logic for the API endpoints.
- In the `models` package you will find the classes that represent the data.
- In the `routes` package you will find the routes for the API, which are routes that call the controllers.
- In the `persistence` package you will find the repositories that handle the data.

## How the solution works?

The application is built using the factory pattern. The `create_app` function in the `src/__init__.py` file creates the application and returns it. The function accepts a `config` object which is used to configure the application. It registers the routes, the error handlers, cors, and then returns the application.

To run the application you can simply run the app object returned by the `create_app` function just like the `hbnb.py` file does. Or you can run the `manage.py` file, which uses the `Flask CLI`, with `python manage.py run` to run the application.

The routes are divided into `Blueprints` and are registered in the `create_app` function mentioned above. The routes are located in the `src/routes` directory.

The routes defined in the files use the controllers to handle the requests. The controllers are in the `src/controllers` directory.

Then the controllers queries the models to retrieve or save the data. The models are in the `src/models` directory.

And the models use the current selected repository to handle the data. The repositories are in the `src/persistence` directory. The `src/persistence/__init__.py` exports a `db` object that is the current selected repository.

So, the flow is like this:

```text
Request -> Route -> Controller -> Model -> Repository
(then all the way back)
Response <- Route <- Controller <- Model <- Repository
```

You can choose the repository you want to use by setting the `REPOSITORY_TYPE` environment variable to `memory`, `file`, or `db`. The default is `memory`.

---
Just to mention, there is a `utils` package that for now contains only two files, `constants.py` and `populate.py`. The `constants.py` file contains the constants used in the application, and the `populate.py` file contains the logic to populate the database with some data.

You can change the constants arbitrarily.

## How to run

To run the solution first install the requirements with `pip install -r requirements.txt`. Then there is a few ways to run it:

- Run the `manage.py` file with the command `python manage.py run` and specify flags like `--port {port} --host {host}` if you want to run it in a different port or host.
- Run the `hbnb.py`. This file calls a function before running the app that will populate the database with some data.
- Build and run the Dockerfile.
