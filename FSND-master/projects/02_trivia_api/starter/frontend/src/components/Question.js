import React, { Component } from 'react';
import '../stylesheets/Question.css';
import RatingStars from './RatingStars'

class Question extends Component {
  constructor(props){
    super();
    this.state = {
      visibleAnswer: false
    }
  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }
  
  setRating = (newRating) => {
    const { id, rating } = this.props;
    return (
       this.props.questionAction('RATING', { rating: newRating, id: id })
    )
  }

  render() {
    const { question, answer, category, difficulty, rating } = this.props;
    return (
      <div className="Question-holder">
        <div className="Question">{question}</div>
        <div className="Question-status">
          <img className="category" src={`${category}.svg`} alt=""
          onError={(event) => {
            event.target.onerror = null
            event.target.src = 'default_blackdot.svg'
         }}/>
          <div className="difficulty">Difficulty: {difficulty}</div>
          <img src="delete.png" alt="Delete" className="delete" onClick={() => this.props.questionAction('DELETE', '')}/>
        </div>
        <div className="show-answer button"
            onClick={() => this.flipVisibility()}>
            {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
          </div>
        <div className="answer-holder">
          <span style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
        </div>
        <div>Rate this question: 
          {<RatingStars 
             rating = { rating } 
             setRating = {this.setRating}
           />}
        </div>
      </div>
    );
  }
}

export default Question;
