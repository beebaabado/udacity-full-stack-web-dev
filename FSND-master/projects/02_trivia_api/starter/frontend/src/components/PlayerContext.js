// # filename: PlayerContext.js
// # author:  modified by Connie Compos
// # date: 12/5/2020 
// # version number: n/a
// # Full Stack Web Developer Nanodegree Trivia API frontend 
// # Creates context for Player profile data to be shared by react components 
// # used by Udacity triva app - project 2
// # 
import React, { Component, createContext}  from 'react';

const PlayerContext = createContext();

class PlayerProvider extends Component {
    // Context state
    state = {
      player: {},
    }
  
    // Method to update state
    setPlayer = (player) => {
      this.setState((prevState) => ({ player }))
    }
  
    render() {
      const { children } = this.props
      const { player } = this.state
      const { setPlayer } = this
  
      return (
        <PlayerContext.Provider
          value={{
            player,
            setPlayer,
          }}
        >
          {children}
        </PlayerContext.Provider>
      )
    }
  }

export default PlayerContext;
export {PlayerProvider}