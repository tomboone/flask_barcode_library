# flask_barcode_library

![pylint](https://github.com/tomboone/flask_barcode_library/actions/workflows/pylint.yml/badge.svg)
![flake8](https://github.com/tomboone/flask_barcode_library/actions/workflows/flake8.yml/badge.svg)
![mypy](https://github.com/tomboone/flask_barcode_library/actions/workflows/mypy.yml/badge.svg)

Scan book barcodes to add to library. Generates a list of books sorted by LC call number. Designed to sort books in a home library for shelving by subject. (No more manual sorting!)

Barcodes scanned using the [JavaScript Barcode Detection API](https://developer.mozilla.org/en-US/docs/Web/API/Barcode_Detection_API).

Book metadata and call numbers retrieved from the [Open Library API](https://openlibrary.org/developers/api).

## Local Development

### Prerequisites

- [Docker Desktop](https://docs.docker.com/get-docker/)
- [tomboone/local-dev-traefik](https://github.com/tomboone/local-dev-traefik) (reverse proxy for network routing)

### Setup

1. Clone the repository, navigate to the project directory, and copy `.env.template`.
    ```bash
    git clone git@github.com:tomboone/flask_barcode_library.git
    cd flask_barcode_library
    cp .env.template .env
    ```
2. If necessary, update the `.env` file with your host machine's `.gitconfig` and SSH key file locations:
    ```bash
    nano .env
    ``` 
   
    ```
    SSH_KEY_FILE=/path/to/ssh/key
    GITCONFIG_FILE=/path/to/gitconfig
    ```

3. Start development containers and SSH into the flask container.
    ```bash
    docker-compose up
    docker exec -i -t flask_barcode_library /bin/bash
    ```

4. Initialize the database and add a user.
    ```bash
    export SQLALCHEMY_DATABASE_URI=mariadb+mariadbconnector://user:password@flask_barcode_library_db:3306/myd
    flask initdb
    flask createuser -e <email> -p <password>
    ```

Load app: [https://barcode.jat.localhost](http://flask-barcode-library.jat.localhost)