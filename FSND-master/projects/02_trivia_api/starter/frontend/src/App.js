import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

import { PlayerProvider } from './components/PlayerContext';
// import logo from './logo.svg';
import './stylesheets/App.css';
import PlayerView from './components/PlayerView';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';

let playerProfileInfo = {  //default data for Player context
  id: 0,
  name: '',
}

class App extends Component {
  render(){
    return (
    <PlayerProvider value={playerProfileInfo}>
    <div className="App">
      <Header path />
      <Router>
        <Switch>
          <Route path="/" exact component={PlayerView} />
          <Route path="/list" component ={QuestionView} />
          <Route path="/add" component={FormView} />
          <Route path="/play" component={QuizView} />
          <Route component={QuestionView} />
        </Switch>
      </Router>
    </div>
    </PlayerProvider> 
  );

  }
}

export default App;
