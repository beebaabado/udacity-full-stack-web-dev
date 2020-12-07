// # filename: PlayerLogin.js
// # author:  modified by Connie Compos
// # date: 12/5/2020 
// # version number: n/a
// # Full Stack Web Developer Nanodegree Trivia API frontend 
// # Creates view for user to login to Udacity trivia app to retreive scores
// # and to allow new quiz scores
// # to be saved in the Udacity triva app database - project 2
// # 
import React, { Component, useContext } from 'react';
import '../stylesheets/FormView.css';

class PlayerLogin extends Component {
  constructor(){
    super();
    this.state  = {
      name: '',
      id: 0,
      error: ''
    }
}
  
  componentDidMount() {
    
  }

  shouldComponentUpdate(nextState){
    return (this.state.name!==nextState.name);
  }

  dismissError = () => {
    this.setState({ error: '' });
  }

  handlePlayerNameChange = (event) => {
      this.setState({
        name:  event.target.value
      });
  }
  
  handleSubmit = (event) => {
    event.preventDefault();
    if (!this.state.name) {
      return this.setState({ error: 'Player name is required' });
    }
     
    this.setState({ error: '' })
    console.log(this.state.name);
    return(this.props.playerAction(this.state.name));
  }
 
  render() {  
    return (
      <div className="Player-holder">
        <form className="form-view" id="add-form" onSubmit={this.handleSubmit}>
          {
            this.state.error &&
            <h3 data-test="error" onClick={this.dismissError}>
              <button onClick={this.dismissError}>✖</button>
              {this.state.error}
            </h3>
          }
          <label>Enter player name</label>
          <input
            type="text"
            data-test="name"
            value={this.state.name}
            onChange={ this.handlePlayerNameChange}  
          />
          <input type="submit" id="profile" data-test="submit" value="Get Profile" className="button"/>
        </form>
      </div>
    );
  }
}

export default PlayerLogin;
