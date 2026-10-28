# Page Analyzer

[![Hexlet Checks](https://github.com/SemYakovlev/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SemYakovlev/python-project-83/actions)

**Page Analyzer** is a web application for checking websites and analyzing basic SEO-related HTML metadata.

The application checks website availability, retrieves the HTTP response status code, and extracts key HTML elements: the page title, the main heading (`h1`), and the meta description. Results are stored in a PostgreSQL database and can be viewed along with the history of previous checks.

**Live demo:** [Page Analyzer](https://python-project-83-snyq.onrender.com/)

## Features

- Add websites for analysis using their URLs.
- Validate URLs before saving them.
- Prevent duplicate websites by normalizing URLs to their scheme and domain.
- Check website availability and retrieve HTTP status codes.
- Parse HTML pages and extract:
  - Main heading (`h1`)
  - Page title (`title`)
  - Meta description
- Store websites and check results in PostgreSQL.
- View a list of websites and their latest check results.
- Browse the history of checks for each website.
- Display success and error notifications.

## Tech Stack

- **Python 3.14+**
- **Flask** — web framework
- **PostgreSQL** — relational database
- **psycopg** — PostgreSQL adapter
- **Requests** — HTTP requests
- **Beautiful Soup 4** — HTML parsing
- **Bootstrap 5** — responsive UI
- **Gunicorn** — WSGI HTTP server
- **uv** — dependency management
- **Ruff** — code linting
- **GitHub Actions** — automated checks and linting

## Requirements

Before running the application, make sure you have:

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL
- Git

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/SemYakovlev/python-project-83.git
cd python-project-83
```

Install the project dependencies:

```bash
uv sync
```

### Database configuration

Create a PostgreSQL database and configure the following environment variables:

- `DATABASE_URL` — PostgreSQL connection URL
- `SECRET_KEY` — Flask secret key used for session security

For local development, you can place these variables in a `.env` file in the project root:

```dotenv
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=your-secret-key
```

Replace the example credentials and database name with your own values.

Initialize the database schema:

```bash
psql "$DATABASE_URL" -f database.sql
```

The schema creates two tables:

- `urls` — stores websites added for analysis.
- `url_checks` — stores HTTP status codes and extracted HTML metadata for each check.

## Running the application

Start the Flask development server:

```bash
make dev
```

By default, the application is available at:

`http://127.0.0.1:5000`

To run the application using Gunicorn:

```bash
make start
```

The production server listens on port `8000` by default. You can override the port with the `PORT` environment variable.

## Code Quality

Run Ruff to check the code:

```bash
make lint
```

The repository also includes GitHub Actions workflows for automated project checks and linting.
