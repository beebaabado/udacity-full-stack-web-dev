import React, { Component } from 'react';
import $ from 'jquery';
import PlayerContext from './PlayerContext';
import '../stylesheets/QuizView.css';

const questionsPerPlay = 5; 

class QuizView extends Component {
  constructor(props){
    super();
    this.state = {
        quizCategory: null,
        previousQuestions: [], 
        showAnswer: false,
        categories: [],
        numCorrect: 0,
        currentQuestion: {},
        guess: '',
        forceEnd: false
    }
  }

  // context for sharing player profile info
  static contextType = PlayerContext;
    
  componentDidMount(){
    
    // store current player id and name
    const search = window.location.search;
    const params = new URLSearchParams(search);
    const { player, setPlayer } = this.context;
    const currPlayer = { id: params.get('player_id'), name: params.get('player_name') }
    setPlayer(currPlayer);
 
    // get available quiz categories 
    $.ajax({
      url: '/categories',
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }

  // NOTE:  state in React: updating a React component’s state is asynchronous. 
  // It does not happen immediately.  To solve this specific React issue, 
  // we can use the setState function’s 
  // callback. Whatever we pass into setState’s second argument executes 
  // after the setState function updates.
  selectCategory = (type, id=0) => {
    if (id == 0) {type = "All"}
    this.setState({quizCategory: {id: id, type: type} }, this.getNextQuestion)
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  getNextQuestion = () => {
    const previousQuestions =[...this.state.previousQuestions] // why use spread operator?
    if (this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }
    
    $.ajax({      
      url: '/quizzes',   
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory 
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => { 
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question[0],  // backend returns an array...grab first element
          guess: '',
          forceEnd: result.question[0] ? false : true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  submitGuess = (event) => {
    event.preventDefault(); 
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    })
  }

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [], 
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    })
  }

  renderPrePlay(){
      return (
          <div className="quiz-play-holder">
              <div className="choose-header">Choose Category</div>
              <div className="category-holder">
                  <div className="play-category" onClick={this.selectCategory}>ALL</div>
                  {this.state.categories.map(category => {
                  return (
                    <div
                      key={category.id}
                      value={category.id}
                      className="play-category"
                      onClick= {() => this.selectCategory(category.type, category.id)} >
                      {category.type}
                    </div>
                  )
                })}
              </div>
          </div>
      )
  }
  

  saveUserScore = () => {   
    const { player, setPlayer} = this.context;
    if (player.name === null)
      return;  // no player id, cannot save scores
     
    $.ajax({
        url: '/score',
        type: "POST",
        dataType: 'json',  
        contentType: 'application/json',
        data: JSON.stringify({
          player_id: parseInt(player.id),
          category_id: this.state.quizCategory.id,
          value: this.state.numCorrect
         }),
        xhrFields: {
          withCredentials: true
        },
        crossDomain: true,
         success: (result) => {
          return;
        },
        error: (error) => {
          //console.log("Error saving quiz score.")  
          return;
        }
    })
  }   

  renderFinalScore(){
    this.saveUserScore();
    return(
      <div className="quiz-play-holder">
        <div className="final-header"> Your Final Score is {this.state.numCorrect}</div>
        <div className="play-again button" onClick={this.restartGame}> Play Again? </div>
      </div>
      
    )
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase().split(' ')
    const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ')
    return formatGuess.every(item => answerArray.includes(item));
  }

  renderCorrectAnswer(){
    let evaluate =  this.evaluateAnswer()
    return(
      <div className="quiz-play-holder">
        <div className="quiz-question">{this.state.currentQuestion.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">{this.state.currentQuestion.answer}</div>
        <div className="next-question button" onClick={this.getNextQuestion}> Next Question </div>
      </div>
    )
  }

  renderPlay(){   
    return this.state.previousQuestions.length >= questionsPerPlay || this.state.forceEnd
      ? this.renderFinalScore()
      : this.state.showAnswer 
        ? this.renderCorrectAnswer()
        : (
          <div className="quiz-play-holder">
            <div 
              value={this.state.currentQuestion.id}
              className="quiz-question">
              {this.state.currentQuestion.question}
            </div>
            <form onSubmit={this.submitGuess}>
              <input type="text" name="guess" onChange={this.handleChange}/>
              <input className="submit-guess button" type="submit" value="Submit Answer" />
            </form>
          </div>
        )
     
  }

  render() {
    return this.state.quizCategory             
        ? this.renderPlay()
        : this.renderPrePlay()
  }
}

export default QuizView;
