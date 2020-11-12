import React, { Component } from 'react';
import $ from 'jquery';

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

  componentDidMount(){
    $.ajax({
      url: '/categories', //TODO: update request URL
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

  // NOTE TO SELF:  Here’s something extremely important to know about 
  // state in React: updating a React component’s state is asynchronous. 
  // It does not happen immediately.
  // To solve this specific React issue, we can use the setState function’s 
  // callback. Whatever we pass into setState’s second argument executes 
  // after the setState function updates.
  selectCategory = (type, id=0) => {
    if (id == 0) {type = "All"}
    this.setState({quizCategory: {id: id, type: type} }, this.getNextQuestion)
  }

  handleChange = (event) => {
    console.log("handleChange...................")
    console.log(event.target.value)
    this.setState({[event.target.name]: event.target.value})
    console.log(this.state.guess)
  }

  getNextQuestion = () => {
    const previousQuestions =[...this.state.previousQuestions] // why use spread operator?
    //const previousQuestions = this.state.previousQuestions
    if (this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }
  
    console.log("GetNExtQuestion quizCategory;  " )
    console.log(this.state.quizCategory)
    console.log(this.state.currentQuestion.id)
    console.log(previousQuestions)

    $.ajax({      
      url: '/quizzes', //TODO: update request URL     
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
        // console.log("In getNextQuestion sucessfully got next question:  print result")
        // console.log(result) 
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question[0],  // backend returns an array...grab first element
          guess: '',
          forceEnd: result.question[0] ? false : true
        })
        // console.log("GetNExtQuestion currentQuestion;  " )
        // console.log(this.state.currentQuestion.question)  
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  submitGuess = (event) => {
    event.preventDefault();  /* what action is being prevented? */
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
    // console.log("renderPrePlay....")
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

  renderFinalScore(){
    return(
      <div className="quiz-play-holder">
        <div className="final-header"> Your Final Score is {this.state.numCorrect}</div>
        <div className="play-again button" onClick={this.restartGame}> Play Again? </div>
      </div>
    )
  }

  evaluateAnswer = () => {
    console.log("GUESS................................. ")
    console.log(this.state.guess)
    console.log(this.state.currentQuestion.answer)
  
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase().split(' ')
    const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ')
    console.log(formatGuess)
    console.log(answerArray)
    return formatGuess.every(item => answerArray.includes(item));
    //return answerArray.includes(formatGuess)
  }

  renderCorrectAnswer(){
    //const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
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
    console.log("renderPlay....")
    console.log(this.state.previousQuestions.length)
    console.log(this.state.numCorrect)
    return this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd
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
          
            {/* use mapping if need to iterate through array  */}
            {/* {this.state.currentQuestion.map(current_question => {
            return (
              <div 
                key={current_question.id} v
                value={current_question.id}
                className="quiz-question">
                {current_question.question}
              </div>
              )
            })} */}
            
            <form onSubmit={this.submitGuess}>
              <input type="text" name="guess" onChange={this.handleChange}/>
              <input className="submit-guess button" type="submit" value="Submit Answer" />
            </form>
          </div>
        )
     
  }


  render() {
    // console.log("render...")
    // console.log(this.state)

    return this.state.quizCategory             
        ? this.renderPlay()
        : this.renderPrePlay()
  }
}

export default QuizView;
