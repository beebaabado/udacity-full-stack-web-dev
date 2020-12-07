***
# **<center>Documentation for Trivia App API </center>**

The Trivia App API allows developers to access a database of questions and question categories.  You can obtain all questions, questions by category, single questions by category for quiz.  Each question has question text, difficulty level, rating, and category.  Additionally,  you can search for specific questions, add new questions, and delete questions. 

This is a REST API that returns encoded JSON responses and uses standard HTTP response codes (success and error codes) and verbs (GET, POST, and DELETE).  You may create, retrieve, and delete API objects through this simple interface.  
>Note:  Update of API objects is not currently supported.

This documentation will take you through each end point providing the following information:  

- Endpoint description
- A sample curl statement to call the endpoint with necessary parameters
- Returned encoded JSON response  
&nbsp;  
&nbsp;  


## **<center>General Information</center>**
&nbsp;

## Base URL
***
This project has not been deployed and is not hosted at a base URL.  The backend is hosted locally at the following default address:

<http://localhost:5000>

<http://127.0.0.1:5000>  
&nbsp;  
&nbsp;  
  
## Authentication
***
This API does not currently implement authentication.  
&nbsp;  
&nbsp;  
&nbsp;

## Error handling - HTTP error codes
***

HTTP status/error codes and messages.   This API returns the following status codes.  Supported status and error handling includes 200 for successful requests and 4xx error codes for malformed requests to resource not available events.

Attributes 
- success:  Boolean.  Returns False for all error codes.
- error:    HTTP status code
- message:  Human readable message with details about the error


### Status and Error codes

- 200 "OK": request was succesful.
    - response: varies, see documentation for specific endpoint


- 422 "unprocessable":  request was not valid or server could not process the request
    - response
    ```json           
    {
        "success": False, 
        "error": 422,
        "message": "unprocessable"
    }
    ```

- 404 "resource not found":  request was valid but the resouce was not found
     - response
     ```json
     {
        "success": False, 
        "error": 404,
        "message": "resource not found"
     }
     ```
- 400 "bad request":  request was not formatted correctly
    - response  
     ```json
     {
        "success": False, 
        "error": 400,
        "message": "bad request"
     }
     ```

- 405 "method not allowed":  request specified unsupported method for request
    - response  
     ```json
     {
        "success": False, 
        "error": 405,
        "message": "method not all0wed"
     }
     ```
- 500 "Internal Server Error":  The server encountered an unexpected condition
  which prevented it from fulfilling the request.
    - response  
     ```json
     {
        "success": False, 
        "error": 500,
        "message": "internal server error"
     }
     ```
&nbsp;  
&nbsp;  

## **<center>Endpoints</center>**
***

### Trivia Data Types
The following datatypes are used in request arguments and responses for the Trivia endpoints. Throughout the rest of this document the following notation will be used to represent a list of questions  [{question 1}....{question n}] and list of categories [{category 1}...{category n}]  

- Question object represents a trivia question and is respresented as follows in JSON format with key/value pairs:
  
  ```json
   "question": {
      "id": <integer>, 
      "question": <string>,
      "answer": <string>, 
      "category": <integer>, 
      "category_type": <string>, 
      "difficulty": <integer>, 
      "rating": <integer>
   }
  ```
  >NOTE: category_type is not present with response returned by endpoint `/quizzes`
  >and not included when adding a new question 
  &nbsp;  
- Category object represents a trivia category and is represented as follows in JSON format with key/value pairs:
  ```json
    "category": {
      "id": <integer>,
      "type": <string>
      }
  ```
   &nbsp; 
- Player object represent the user playing trivia game.  If a player is active then quiz scores are store automatically in the trivia database.  If player does not enter a name then scores are not saved. 
  ```json
      "player": {
        'id': <integer>,
        'name': <string>
      }
  ```
  >NOTE: Player name is optional to play the trivia game.
  &nbsp;
- Score object represents scores associated with players.  Multiple scores can exist for each player.
  ```json
     "score": {
        'id': <integer>,
        'value': <integer>,
        'category_id': <integer>,
        'playerId': <integer>   
     }
  ```
  &nbsp;
  &nbsp;

### **Pagination**
Question objects are returned in batches using pagination. Each page displays 10 questions.  This display value cannot be configured at this time.  You can specify a query parameter page=<page_number> where page_number is an integer value when retrieving a list of questions. By default page_number=1.  If page_number is not valid then an error will be returned specifying the resource could not be found.

- curl to interact with the API over HTTP
```
  curl -X GET http://127.0.0.1:5000/questions?page=2
```
- Response 
```json
  {
    "categories": [
      {
        "id": 2, 
        "type": "Art"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 1, 
        "type": "Science"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }
    ], 
    "current_category": {
      "id": 2, 
      "type": "Art"
    }, 
    "questions": [
      {
        "answer": "Escher", 
        "category": 2, 
        "category_type": "Art", 
        "difficulty": 1, 
        "id": 16, 
        "question": "Which Dutch graphic artist with initials M C was a creator of optical illusions?"
      }, 
      {
        "answer": "Mona Lisa", 
        "category": 2, 
        "category_type": "Art", 
        "difficulty": 3, 
        "id": 17, 
        "question": "La Giaconda is better known as what?"
      }, 
      {
        "answer": "One", 
        "category": 2, 
        "category_type": "Art", 
        "difficulty": 4, 
        "id": 18, 
        "question": "How many paintings did Van Gogh sell in his lifetime?"
      }, 
      {
        "answer": "Jackson Pollock", 
        "category": 2, 
        "category_type": "Art", 
        "difficulty": 2, 
        "id": 19, 
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
      }, 
      {
        "answer": "The Liver", 
        "category": 1, 
        "category_type": "Science", 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
      }, 
      {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "category_type": "Science", 
        "difficulty": 3, 
        "id": 21, 
        "question": "Who discovered penicillin?"
      }, 
      {
        "answer": "Blood", 
        "category": 1, 
        "category_type": "Science", 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
      }, 
      {
        "answer": "Scarab", 
        "category": 4, 
        "category_type": "History", 
        "difficulty": 4, 
        "id": 23, 
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
      }, 
      {
        "answer": "The Palace of Versailles", 
        "category": 3, 
        "category_type": "Geography", 
        "difficulty": 3, 
        "id": 63, 
        "question": "In which royal palace would you find the Hall of Mirrors?"
      }
    ], 
    "success": true, 
    "total_questions": 19
  }
```

### GET `/categories`
Retrieves a listing of all categories

- Request Arguments: None
- method: HTTP request method is GET (by default)
- Returns: dictionary of category objects as 'categories': [{category 1}...{category n}],  success status as 'success': <boolean>, and total number of categories as 'total_categories':<integer>.  Category Ids will not necessarily be consecutive numbers in database (ids are not reused if a category is deleted and a new one is created.)

- Response Attributes
  - categories:  list of categories
  - success: true if request was successful
  - total_categories: number of categories currently in trivia database

- curl to interact with the API over HTTP
```
  curl -X GET http://127.0.0.1:5000/categories
```
- Response
```json
  {
    "categories": [
      {
        "id": 2, 
        "type": "Art"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 1, 
        "type": "Science"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }
    ], 
    "success": true, 
    "total_categories": 6
  }
```

### GET `/questions`
Retrieves questions and returns a subset using pagination (see description of pagination). Returns paginated page=1 by default.  Also returns total question count, all current_categories, and current category (defaulted to category id=1).

- Request Arguments:  as query paramenter as  page=<int>
- method: HTTP request method is GET (by default)
- Returns: a dictionary with Category objects, dictionary paginagted Question objects, current category and total number of questions in database.

- Response Attributes
  - questions:  list of paginated questions
  - success: true if request was successful
  - total_questions: number of questions currently in trivia database
  - categories: list of categories 
  - current_category: current category 

- curl to interact with the API over HTTP

Returns paginated page=1 by default.
```
  curl -X GET http://127.0.0.1:5000/questions       
``` 
Returns paginated result for page=2.
```
  curl -X GET http://127.0.0.1:5000/questions?page=2
```

- Response
```json
  {
    "categories": [
      {
        "id": 2, 
        "type": "Art"
      }, 
      {
        "id": 5, 
        "type": "Entertainment"
      }, 
      {
        "id": 3, 
        "type": "Geography"
      }, 
      {
        "id": 4, 
        "type": "History"
      }, 
      {
        "id": 1, 
        "type": "Science"
      }, 
      {
        "id": 6, 
        "type": "Sports"
      }
    ], 
    "current_category": {
      "id": 2, 
      "type": "Art"
    }, 
    "questions": [
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "category_type": "History", 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "category_type": "History", 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
      {
        "answer": "Apollo 13", 
        "category": 5, 
        "category_type": "Entertainment", 
        "difficulty": 4, 
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      }, 
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "category_type": "Entertainment", 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "category_type": "Entertainment", 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "category_type": "Sports", 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "category_type": "Sports", 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "category_type": "History", 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "category_type": "Geography", 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "Agra", 
        "category": 3, 
        "category_type": "Geography", 
        "difficulty": 2, 
        "id": 15, 
        "question": "The Taj Mahal is located in which Indian city?"
      }
    ], 
    "success": true, 
    "total_questions": 19
  }
```

### Create POST `/categories`
Create a new category

- Request Arguments: 
  ```json
  data = {
      "category_type": <string>,     
    }
  ```
  Example:  
  ```json
  data = {
      "category_type": "Music",         
    }
  ```  
- method: HTTP request method is POST
- Returns: "success": <Boolean>,  "created": <integer>
     ```
      {
       "success": <Boolean>,
       "created": <integer>
      }
     ```
- Response Attributes
  - success: true if request was successful
  - created: the new category id

- curl to interact with the API over HTTP

 ```
  curl -X POST -H "Content-Type: application/json" -d '{ "category_type": "Music"}' http://127.0.0.1:5000/categories
 ```

- Response
  ```json
    {
      "created": 7, 
      "success": true
    } 
  ```   

### DELETE `/categories/<int:category_id>`
Delete category with specified id.

- Request Arguments: category_id as integer
- method: HTTP request method is DELETE
- Returns:  "success":<Boolean>, "deleted": <integer>

- Response Attributes
   - success: true if request was successful
   - deleted: id of category that was deleted successfully

- curl to interact with the API over HTTP

Deletes category with id=7
```
  curl  -X DELETE http://127.0.0.1:5000/categories/7 
```
- Response
```json
  {
    "deleted": 7, 
    "success": true
  }
```  
### GET `/categories/<int:category_id>/questions`
Retrieve a list of questions based upon category id.

- Request Arguments: category_id as integer
- method: HTTP request method is GET (by default)
- Returns:  "success":<Boolean>, "total_quesions": <integer>, dictionary paginagted Question objects, total questions and current category.

- Response Attributes
  - questions:  list of paginated questions
  - success: true if request was successful
  - total_questions: number of questions currently in trivia database
  - current_category: current category 

- curl to interact with the API over HTTP
```
  curl -X GET http://127.0.0.1:5000/categories/<int:category_id>/questions
```

- Response
```json
  {
    "current_category": {
      "id": 6, 
      "type": "Sports"
    }, 
    "questions": [
      {
        "answer": "Brazil", 
        "category": 6, 
        "category_type": "Sports", 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "category_type": "Sports", 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }
    ], 
    "success": true, 
    "total_questions": 2
  }
```

### Create POST `/questions`
Create a new question

- Request Arguments: 
  ```json
  data = {
      "question": <string>,     
      "answer": <string>,       
      "category": <integer>,    - IDs of category may not necessarily be consecutive in the database
      "difficulty": <integer>   - Value between 1 and 5
    }
  ```
  Example:  
  ```json
  data = {
      "question": "who was the first programmer?",        
      "answer": "Ada Lovelace",       
      "category": 4,      
      "difficulty": 3     
    }
  ```  
- method: HTTP request method is POST
- Returns: "success": <Boolean>,  "created": <integer>, "total_questions": <integer>, dictionary paginagted question objects as 'questions' with key/value pairs:
     ```
      {
      "answer": <string>, 
      "category": <int>, 
      "category_type": <string>, 
      "difficulty": <int>, 
      "id": <int>, 
      "question": <string>
      }
     ```
- Response Attributes
  - questions:  list of paginated question for page=1
  - success: true if request was successful
  - total_questions: number of questions currently in trivia database
  - created: the new question id

- curl to interact with the API over HTTP

 ```
  curl -X POST -H "Content-Type: application/json" -d '{"question": "Who was the first programmer", "answer": "Ada Lovelace", "category": 4,  "difficulty": 3}' http://127.0.0.1:5000/questions 
 ```

- Response
```json
  {
    "created": 70, 
    "questions": [
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
      }, 
      {
        "answer": "Apollo 13", 
        "category": 5, 
        "difficulty": 4, 
        "id": 2, 
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
      }, 
      {
        "answer": "Tom Cruise", 
        "category": 5, 
        "difficulty": 4, 
        "id": 4, 
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }, 
      {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
      }, 
      {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
      }, 
      {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
      }, 
      {
        "answer": "Lake Victoria", 
        "category": 3, 
        "difficulty": 2, 
        "id": 13, 
        "question": "What is the largest lake in Africa?"
      }, 
      {
        "answer": "Agra", 
        "category": 3, 
        "difficulty": 2, 
        "id": 15, 
        "question": "The Taj Mahal is located in which Indian city?"
      }
    ], 
    "success": true, 
    "total_questions": 20
  }
```

### DELETE `/questions/<int:question_id>`
Delete question with specified id.

- Request Arguments: question_id as integer
- method: HTTP request method is DELETE
- Returns:  "success":<Boolean>, "deleted": <integer>

- Response Attributes
   - success: true if request was successful
   - deleted: id of question that was deleted successfully

- curl to interact with the API over HTTP

Deletes question with id=69 
```
  curl  -X DELETE http://127.0.0.1:5000/questions/69 
```
- Response
```json
  {
    "deleted": 69, 
    "success": true
  }
```

### Search POST `/questions`
Search for questions that contain specific search term.

- Request Arguments: 
  ```json
  data = {
       "searchTerm": <string>
    }
  ```
  Example:
  ```json
  data = {
       "searchTerm": "title"
    }
  ```

- method: HTTP request method is POST
- Returns: "success": <Boolean>, "total_questions": <integer>, "questions": list of paginagted <Question> objects:
  ```
      {
       "success": <boolean>,
       "questions": [{Question}...{Question}],
       "total_questions": <integer>
      }
  ```
- Response Attributes
  - questions:  list of paginated questions for page=1 that match search term
  - success: true if request was successful
  - total_questions: number of questions currently in trivia database

- curl to interact with the API over HTTP

 ```
  curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questions 
 ```

- Response
```json
  {
    "questions": [
      {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
      }, 
      {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      }
    ], 
    "success": true, 
    "total_questions": 2
  }
```

### POST `/quizzes`
Retrieve a random quiz question from specifiec category of questions.  Category can be "All" to retrieve question from all questions in the database.  
      
- Request Arguments: 
  ```json 
  data = {
      "previous_questions": [<integer>],     -list of question ids
      "quiz_category": <integer>
    }
  ```

  Example:  
  ```json
  data = {
         "previous_questions": [
            {
              "id": 5,
              "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
              "answer": "Maya Angelou",
              "category": 4,
              "difficulty": 2,
              "rating": 3
              }, 
              {
               "id": 9,
               "question": "What boxer's original name is Cassius Clay?",
               "answer": "Muhammad Ali",
               "category": 4,
               "difficulty": 1,
               "rating": 3
          }],
          "quiz_category": 4
  }
  ``` 
- method: HTTP request method is POST
- Returns:  "success":<Boolean>, "question": <Question>

- Response Attributes
   - success: true if request was successful
   - question: randomly chosen question from questions in category but not found in previous questions list

- curl to interact with the API over HTTP
```
  curl -X POST -H "Content-Type: application/json" -d '{
    "previous_questions": [{
                "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "rating": 3
                }, 
                {
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?",
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "rating": 3
                }],
    "quiz_category": {"id": 4, "type": "History"}
        }' http://127.0.0.1:5000/quizzes
```
- Response
```json
  {
    "success": true,
    "question": [{
                    "id": 12, 
                    "question": "Who invented Peanut Butter?", 
                    "answer": "George Washington Carver", 
                    "category": 4, 
                    "difficulty": 2,
                    "rating": 3
                }]
  }
```
### Create POST `/score`
Create a new score for player

- Request Arguments: 
  ```json
  data = {
      "value": <integer>,
      "category_id": <integer>,    
      "player_id": <integer> 
    }
  ```
  Example:  
  ```json
  data = {
      "value": 4,
      "category_id": 4,    
      "player_id": 59 
    }
  ```  
- method: HTTP request method is POST
- Returns: "success": <Boolean>,  "created": <integer>:
  ```  
      {
      "created": <integer>, 
      "success": <Boolean>
      }
  ```   
- Response Attributes
  - success: true if request was successful
  - created: the new score id

- curl to interact with the API over HTTP

 ```
  curl -X POST -H "Content-Type: application/json" -d '{ "player_id": 9, "value":4, "category_id": 1}' http://127.0.0.1:5000/score

 ```

- Response
```json
  {
  "created": 57, 
  "success": true
  }
```

### Create POST `/players`
Create a new player

- Request Arguments: 
  ```json
  data = {
      "name": <string>,     
    }
  ```
  Example:  
  ```json
  data = {
      "name": "Ariana",         
    }
  ```  
- method: HTTP request method is POST
- Returns: "success": <Boolean>,  "created": <integer>
     ```
      {
       "success": <Boolean>,
       "created": <integer>
      }
     ```
- Response Attributes
  - success: true if request was successful
  - created: the new player id

- curl to interact with the API over HTTP

 ```
  curl -X POST -H "Content-Type: application/json" -d '{ "name": "Ariana"}' http://127.0.0.1:5000/players
 ```

- Response
  ```json
    {
      "created": 61, 
      "success": true
    } 
  ```   

### GET `/players/<string:player_name>`
Retrieve player profile using player name.

- Request Arguments: player_name as string
- method: HTTP request method is GET (by default)
- Returns:  "success":<Boolean>, "player": <Player>, "scores": list of <Score> objects, "scoreCount":<Integer>:
  ```   
      {
      "success": <Boolean>,
      "player": <Player>,
      "scores": [{<Score>}...{Score}],
      "scoreCount": <integer>
      }
  ```
- Response Attributes
  - success: true if request was successful
  - player: player objected with name and id
  - scores:  score ojects associated with player
  - scoreCount:  number of score objects 

- curl to interact with the API over HTTP
```
  curl -X GET http://127.0.0.1:5000/players/Bean
```

- Response
```json
{
  "player": {
    "id": 1, 
    "name": "Bean"
  }, 
  "scoreCount": 1, 
  "scores": [
    {
      "category_id": 1, 
      "category_type": "Science", 
      "id": 1, 
      "playerId": 1, 
      "value": 2
    }
  ], 
  "success": true
}

```

### DELETE `/players/<int:player_id>`
Delete player and associated scores with specified player id.

- Request Arguments: player_id as integer
- method: HTTP request method is DELETE
- Returns:  "success":<Boolean>, "deleted": <integer>

- Response Attributes
   - success: true if request was successful
   - deleted: id of player that was deleted successfully

- curl to interact with the API over HTTP

Deletes player with id=61
```
  curl  -X DELETE http://127.0.0.1:5000/players/61
```
- Response
```json
  {
    "deleted": 61, 
    "success": true
  }
```

### Update POST `/ratings`
Update rating for question with specified id

- Request Arguments: 
  ```json
  data = {
      "id": <integer>,
      "rating": <integer>
    }
  ```
  Example:  
  ```json
  data = {
      "id": 5,
      "rating": 1,         
    }
  ```  
- method: HTTP request method is POST
- Returns: "success": <Boolean>,  "modified": <integer>
     ```
      {
       "success": <Boolean>,
       "modified": <integer>
      }
     ```
- Response Attributes
  - success: true if request was successful
  - modified: the modified question id

- curl to interact with the API over HTTP

 ```
  curl -X POST -H "Content-Type: application/json" -d '{ "id": 5, "rating": 1}' http://127.0.0.1:5000/ratings
 ```

- Response
  ```json
    {
      "modified": 1, 
      "success": true
    } 
  ```   

## Deployment  N/A
Not applicable.  This is a practice project for Full Stack Web Developer nanodegree program.

## Authors
Written by Connie Compos  
Last modified: 12/05/2020

## Acknowledgments
UDACITY FULL STACK WEB DEVELOPER Nanodegree team