# disk-io-parser

This Python script (short summary)

## Overview

How it works...

## Features

* **Feature 1:** Explaination.

## Usage

1.  **Installation:** (instruction)
2.  **Running the script:** (instruction)

    **Example:** (instruction)

    ```bash
    python main.py
    ```

3.  **Output:** (what does it do?)

## Example Output

# Setup

## Initial repo setup

 1. Install the dependencies with uv (given uv is in the path):
    ```bash
    uv lock
    uv sync --group dev
    ```
 2. Create the repository on GitHub
 3. Add the remote:
    ```bash
    git init
    git add .
    git commit -m "first commit"
    git switch --create main
    git remote add origin https://github.com/innovmetric/(repo).git  # <- Replace by your repo
    git push -U origin main
    ```

## Setup the release keys

 1. Go to ``minio.innovmetric.com:42721``
 2. Log in with the `equipekastor` username
 3. Create a new `Access Key`. Take note of the `Access Key id` and the `Secret Key`
 4. When the key is created, edit it and add the following `Policy`:
  ```
{
 "Version": "2012-10-17",
 "Statement": [
  {
   "Effect": "Allow",
   "Action": [
    "s3:PutObject"
   ],
   "Resource": [
    "arn:aws:s3:::im-tools/project_name-slug/*"  <- Replace this with your project name.
   ]
  }
 ]
}
 ```
 5. In your repository in GitHub, add new repository variables:
  ```dotenv
  AWS_ACCESS_KEY_ID=(The Access Key Id)  # Make sure there are no newline at the end
  AWS_ENDPOINT_URL=https://minio.innovmetric.com:9000
  IM_S3_BUCKET_NAME=im-tools
  ```
 6. Add a new repository secret:
  ```dotenv
  AWS_SECRET_ACCESS_KEY=(The Secret Access Key)
  ```

## Release the app

 * Create a new release in GitHub. It will make your app available using the url `"https://minio.innovmetric.com:9000/im-tools/$(project_name-slug)/$(version)/$(project_name-slug).exe"`.
 * The tag used must start with a lowercase v. For example: `v0.0.1`. It must respect [SemVer](https://semver.org/).

## Other tools

  * **Run tests using pytest:** ``pytest``
  * **Check types using mypy:** ``mypy .``
  * **Format code with ruff:** ``ruff format``
  * **Lint and fix code using ruff:** ``ruff check --fix``
