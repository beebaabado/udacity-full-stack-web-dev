import React, { Component } from 'react'

import '../stylesheets/player.css';
import PlayerLogin from './PlayerLogin';
import Search from './Search';
import $, { event } from 'jquery';
import PlayerContext from './PlayerContext';

class PlayerView extends Component {
  constructor(){
    super();
    this.state = {
       currentPlayerId: 0,
       name: '',
       scores: [],
       scoreCount: 0,
       visiblePlayer: false
    }
  }
  
  static contextType = PlayerContext;

  componentDidMount() {

   // store current player id and name
    const search = window.location.search;
    const params = new URLSearchParams(search);
    const { player, setPlayer } = this.context;
    const currPlayer = { id: params.get('player_id'), name: params.get('player_name') }
    setPlayer(currPlayer);
    this.getPlayer(currPlayer.name);
  }
  
  shouldComponentUpdate(nextProps, nextState){
    if (nextState.visiblePlayer === true){
      return true;
    }
    else {
       return false; 
      }
  }
 
  flipVisibility(state) {
      this.setState({ visibilePlayer: state });
    }

  createNewPlayer = (playerName) => {
    $.ajax({
      url: `/players`,
      type: "POST",
      dataType: 'json',  
      contentType: 'application/json',
      data: JSON.stringify({name: playerName}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
       success: (result) => {
        this.setState({
          currentPlayerId: result.created,
          name: playerName,
          scores: [],  // no scores for new user
          scoreCount: 0,
          visiblePlayer: true
        })
        this.setPlayerContextData();
        return;
      },
      error: (error) => {
        if (error.statusCode === 422)
          alert('That player name already exists.  Please enter a new name.');
        else
          alert('Unable to create new player profile. Please try your request again');
        return;
      }
    })
  } 

  setPlayerContextData = () => {
    const { player, setPlayer } = this.context;
    const newPlayer = {id: this.state.currentPlayerId, name: this.state.name};
    setPlayer(newPlayer);
    return;  
  }

  getPlayer = (playerName) => {
      $.ajax({
          url: `/players/${playerName}`, 
          type: "GET",
          success: (result) => {
            this.setState({
              currentPlayerId: result.player.id,
              name: result.player.name,
              scores: result.scores,
              scoreCount: result.scoreCount,
              visiblePlayer: true
            })
            this.setPlayerContextData();
            return;
          },
          error: (error) => {
            this.setState({
              visibilePlayer: false,
            })
            
            const msg = "Unable to load Player profile for " + playerName + ". " + "Create new profile?"
            if (window.confirm(msg)){
              this.createNewPlayer(playerName);
            }  
            else
              alert("Please enter valid player name.");
            return;
          }
      })
  }

  playerAction = (playerName) => {
    this.getPlayer(playerName);
    return;
  }
  
  navTo(uri){
    const player = this.context.player
    window.location.href = window.location.origin + uri + "?player_id=" + player.id + "&player_name=" + player.name
  }

  render() {
    return (
      <div className="center-item">
        <div className="player-info">
        <h2>Welcome to Udacitrivia!</h2>
        {(<PlayerLogin
            playerAction={this.playerAction}
          />)}
          <span className="center-item" style={{"visibility": this.state.visiblePlayer ? 'visible' : 'hidden'}}>
            <div className="player"><br></br></div>
                <div className="name">Hello {this.state.name}!</div>
                    <div>
                      <div className="score-container"> Your past scores:</div>
                        <ul>  
                           {`${this.state.scoreCount === 0 ? 'No scores yet.' : ''}`}
                            {this.state.scores.map(score => (
                              <li>{score.category_type}: {score.value}</li> 
                            ))} 
                        </ul>  
                  </div>  
                  <input type="button" data-test="play" value="Let's Play!" className="button" onClick={() => {this.navTo('/play')}}/>
          </span>
         </div>  
    </div>
    )
  }
}

export default PlayerView
