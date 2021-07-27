# hotel-reservations-api
Simple WebAPI to manage hotel reservations.

## Technologies used
- Python 3.9.6+ (Python 3.9 is required to run code)
- Django 3.2.5+
- Django REST Framework 3.12.4+
- SQLite database (default Django configuration)

## API features
1.  Manage rooms (list, add, modify, delete)
    
    Note: Each room has class assigned which determines room's price for one day. Room class' management is not exposed by API. To manage room classes, one has to operate directly on the database.

2.  Manage reservations (list/search, add, modify, delete)

## Documentation

API documentation is stored in OpenAPI format in `docs/openapi.yaml`.

Generated according to [official docs](https://www.django-rest-framework.org/api-guide/schemas/#generating-an-openapi-schema) and updated.

API supports also [browseable api](https://www.django-rest-framework.org/topics/browsable-api/) format.

## Requirements and assumptions
*   Room classes are created manually directly on the DB. API comes with four predefined room classes:
    * class: A, price: 200
    * class: B, price: 150
    * class: C, price: 100
    * class: D, price: 50
    
    Predefined classes are created using [database migrations](https://docs.djangoproject.com/en/3.2/topics/migrations/#data-migrations).
*   Room has to be assigned to room class.
*   Deleting a room class deletes all rooms of this class.
*   Each room can be assigned to many reservations (but not to different reservations at the same or conflicting date range).
*   Room cannot be deleted if it has an assignment to some reservation (could be past reservation).
*   Reservations can be made for multiple rooms (if rooms are available for reserving at given date range). At least one room number is required.
*   Reservation starting date has to be in the future.
*   Reservation end date has to be after start date.
*   Reservations can be searched for using following query params:
    *  `room_number`
        Reservations with room number reserved. Can be given multiple times to include more rooms booked together.
    *  `name`
        Reservations for given name. Name search parameter can be partial.
    *  `date`
        Reservations active at given date. Date is between start and end date (both inclusive).
    *  `date_from`
        Reservations starting at given date.
    *  `date_to`
        Reservations ending at given date.
    *  `duration`
        Reservations lasting given number of days.

    Search parameters can be combined together to narrow down results.

## Running

Run application as usual DRF API:
```bash
cd hra
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Docker

Reservation API is dockerized.

Docker image file location: `docker/Dockerfile`. Note that docker image uses github repository instead of current directory to build a clean version without the need to remove unnecessary files from working directory in the machine where it's built.

### Building docker image
```bash
docker build -f docker/Dockerfile -t hotel-api .
```
### Running docker image
```bash
docker run -d -p 8000:8000 hotel-api
```

API should now be visible under http://localhost:8000. Thanks to browseable API, it can be interacted with using web browser.

## Things to improve
- [ ] Add users, authentication and security
- [ ] Use real, separate DB, not default embedded SQLite
- [ ] Turn off `DEBUG` in `hra/settings.py`
- [ ] Search using [django-filter](https://django-filter.readthedocs.io/en/latest/index.html) library
- [ ] Descriptive and full error messages (e.g from all validations)

## Useful links
