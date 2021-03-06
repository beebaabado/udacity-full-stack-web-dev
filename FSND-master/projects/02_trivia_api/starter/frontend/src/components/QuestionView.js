import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: {}
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, 
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
          totalCategories: result.total_categories})
          return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, 
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
          return;
      },
      error: (error) => {
        alert('Unable to load questions by category. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions`,
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }
  
  questionAction = (id) => (action, data) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, 
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
    if (action === 'RATING') {
      $.ajax({
        url: `/ratings`,
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          rating: data.rating,
          id: data.id }),        
        xhrFields: {
          withCredentials: true
        },
        crossDomain: true,
        success: (result) => {
          this.getQuestions();
        },
        error: (error) => {
          alert('Unable to save rating. Please try your request again.')
          return;
        }
      })
    }
  }
  
  render() {
    return (
       <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
                   {/* Object.key wants to return enum array of strings... {Object.keys(this.state.categories).map(category => (  */}
                {this.state.categories.map(category => (
                <li key={category.id} onClick={() => { this.getByCategory(category.id); } }>
                  <div class="category-list-holder">
                    <div class="category-list-item-left">
                        <img className="category" src={`${category.type}.svg`} alt="" 
                        onError={(event) => {
                           event.target.onerror = null
                           event.target.src = 'default_blackdot.svg'
                        }}/>
                    </div>
                    <div class="category-list-item-right">
                        {category.type}
                     </div>
                  </div>
                </li>
               
              ))} 
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              id={q.id}
              question={q.question}
              answer={q.answer}
              category={q.category_type} 
              difficulty={q.difficulty}
              rating={q.rating}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
