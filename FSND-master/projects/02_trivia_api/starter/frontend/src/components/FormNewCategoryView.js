import React, { Component } from 'react';
import $ from 'jquery';
import '../stylesheets/FormView.css';

class FormNewCategoryView extends Component {
  constructor(props){
    super();
    this.state = {
      category_id: 0,
      category_type: ""
    }
  }

  componentDidMount(){
  }


  submitAddCategory = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/categories', 
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        category_type: this.state.category_type,
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-category-form").reset();
        this.setState ({
          category_id: result.created,  
          visibility: true
        }) 
        return;
      },
      error: (error) => {
        alert('Unable to add category. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value,
      visibility: false
    })

  }
  
  flipVisibility() {
    this.setState({visibility: !this.state.visibility});
  }

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Category</h2>
        <form className="form-view" id="add-category-form" onSubmit={this.submitAddCategory}>
          <label>Category</label>
          <input type="text" name="category_type" onChange={this.handleChange}/>      
          <input type="submit" className="button" value="Submit" />
          <div className="message">
            <span style={{"visibility": this.state.visibility ? 'visible' : 'hidden'}}>Category was added successfully.</span>
          </div>
        </form>
      </div>
    );
  }
}

export default FormNewCategoryView;