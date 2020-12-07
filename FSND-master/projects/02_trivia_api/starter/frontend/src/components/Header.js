
import React, { Component } from 'react';
import logo from '../logo.svg';
import '../stylesheets/Header.css';
import PlayerContext from './PlayerContext';

class Header extends Component {
  constructor(){
    super();
    this.state = {
       playerName: '', 
       playerId: 0 
    }
  }  
  
  static contextType = PlayerContext;

  // Temp code for testing...set mock data...for displaying player name in header 
  componentDidMount(){

    // store current player id and name
    const search = window.location.search;
    const params = new URLSearchParams(search);
    const { player, setPlayer } = this.context;
    const currPlayer = { id: params.get('player_id'), name: params.get('player_name') }
    setPlayer(currPlayer);
    this.setState({ playerName: player.name, playerId: player.id});
    
  }

  navTo(uri, name, id){
    const {player} = this.context;
    window.location.href =window.location.origin + uri + "?player_id=" + player.id + "&player_name=" + player.name;
  }   
  
  
  render() {
    const {player} = this.context
    return (
      <div className="App-header">
         
          <div className="header-player-info">
              <div><button onClick={() => {this.navTo('', player.name, player.id)}}>Player: {player.name}</button></div>
          </div>
          <div className="header-menu">
            <img id="logo" src={logo} alt="" />  {/*CC added logo to prevent warnings  */}
            <h1 onClick={() => {this.navTo('')}}>Udacitrivia</h1>
            <h2 onClick={() => {this.navTo('/list')}}>List</h2>
            <h2 onClick={() => {this.navTo('/add')}}>Add</h2>
            <h2 onClick={() => {this.navTo('/play')}}>Play</h2>
          </div>
      </div>
    );
  }
}

export default Header;
