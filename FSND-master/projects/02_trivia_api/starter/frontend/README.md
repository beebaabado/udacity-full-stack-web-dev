# Full Stack Trivia API  Frontend

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Modifications to front end
1. Added react components to allow player to enter name (PlayerLogin, PlayerView).  Player name and scores are retrieved from database and displaye   Player name is displayed in upper right hand corner of header.  If player does not exist then player is prompted to allow new player to be added to the database.  
2. After playing a quiz, if player specified a name then score is saved to the database.
3. Added react component PlayerContext to store player information in order to understand how context object works in react.
4. Added ability to add questions and categories to the database.  Currently cannot add new image for the category.  New category image will be default image:  default_blackdot.svg.
5. Added ratings stars to questions.  Player can set ratings and they will be stored in the database.  
   

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Request Formatting

The frontend should be fairly straightforward and disgestible. You'll primarily work within the ```components``` folder in order to edit the endpoints utilized by the components. While working on your backend request handling and response formatting, you can reference the frontend to view how it parses the responses. 

After you complete your endpoints, ensure you return to and update the frontend to make request and handle responses appropriately: 
- Correct endpoints
- Update response body handling 

## Optional: Styling

In addition, you may want to customize and style the frontend by editing the CSS in the ```stylesheets``` folder. 

## Optional: Game Play Mechanics

Currently, when a user plays the game they play up to five questions of the chosen category. If there are fewer than five questions in a category, the game will end when there are no more questions in that category. 

You can optionally update this game play to increase the number of questions or whatever other game mechanics you decide. Make sure to specify the new mechanics of the game in the README of the repo you submit so the reviewers are aware that the behavior is correct. 

## Acknowledgements
https://www.npmjs.com/package/react-rating-stars-component  for Rating Stars
https://www.digitalocean.com/community/tutorials/how-to-share-state-across-react-components-with-context  for sharing context between REACT components.