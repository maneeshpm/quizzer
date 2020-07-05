## QUIZ API USING DJANGO

### Running the server
Install the dependencies from requirements.txt and run the command
```
$ python3 manage.py makemigrations 
$ python3 manage.py migrate
$ python3 manage.py runserver
```
### Endpoints and usage
The user attributes and methods are completely implemented by the `userAccounts` app and quiz is handled by the `quiz` app separately.

- `/api/users/register/`   `["POST"]`  Register a new user.<br>
Format
```
{
    "username":"t2",
    "email":"t2@t.com",
    "password":"testing321"
}
```
- `/api/users/login/`   `["POST"]`  Returns an API token for authenticated endpoints.<br>
Format
```
{
    "username":"t2",
    "password":"testing321"
}
```

- `/api/quizzes/`   `["GET"]`  Returns a list of all quizzes(past, live, scheduled) with muted details.<br>
Response JSON
```
[
    {
        "id": 1,
        "title": "Football Quiz",
        "begin": "2020-07-05T11:18:10Z",
        "end": "2020-07-13T11:18:13Z",
        "isLive": true,
        "questionCount": 2
    },
    {
        "id": 2,
        "title": "Phineas And Ferb Quiz",
        "begin": "2020-07-05T17:21:10Z",
        "end": "2020-07-22T17:21:16Z",
        "isLive": true,
        "questionCount": 2
    }
]
```

- `/api/quizzes/<int:pk>/`   `["GET"]`   `authentication required`  Where pk is the id of the quiz. Returns the entire quiz body after hiding the `isCorrect` attribute of choices/text.<br>
Response JSON
```
{
    "id": 2,
    "question_set": [
        {
            "id": 3,
            "text": "Hey Phineas! ____?",
            "image": "rm2.png",
            "questionType": "mcq",
            "choices_set": [
                {
                    "id": 6,
                    "label": "Watcha eating"
                },
                {
                    "id": 7,
                    "label": "Watcha watching"
                },
                {
                    "id": 8,
                    "label": "Watcha doin"
                },
                {
                    "id": 9,
                    "label": "Howza"
                }
            ]
        },
        {
            "id": 4,
            "text": "Name the platypus",
            "image": null,
            "questionType": "text",
            "choices_set": null
        }
    ],
    "begin": "2020-07-05T17:21:10Z",
    "end": "2020-07-22T17:21:16Z",
    "title": "Phineas And Ferb Quiz",
    "isLive": true
}
```

- `/api/quizzes/save/`   `["POST"]`  `authentication required`  Used to save a user response. Checks are in place to see if the quiz is live and the quiz is not already submitted.<br>
Format
```
{
    "quiz" : <int:quizID>,
    "question" : <int:questionID>,
    "label" : <string:userResponse>
}
```

- `/api/quizzes/submit/`   `["POST"]`   `authentication required`   Used to sumbit a quiz and write the evaluation to the PointTable in database.<br>
Format
```
{
    "quiz" : <int:quizID>,
}
```

