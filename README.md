# Guide to start project
1. Clone the repository.
2. Add following in environment variables or .env file
    ```txt
    SECRET_KEY=
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_STORAGE_BUCKET_NAME=
    AWS_S3_REGION_NAME=
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=
    RAZORPAY_KEY_ID=
    RAZORPAY_KEY_SECRET=
    DOMAIN=
    ```
3. Run the following commands
    ```sh
    $ docker compose build
    $ docker compose up
    # or
    $ docker compose up --build
    ```
4. You have to run migrations for the first time
    ```sh
    $ docker exec -it fullstack_backend python manage.py makemigrations
    $ docker exec -it fullstack_backend python manage.py migrate
    ```