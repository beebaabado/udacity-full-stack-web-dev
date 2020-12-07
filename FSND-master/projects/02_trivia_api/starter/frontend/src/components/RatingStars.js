import ReactStars from "react-rating-stars-component";
import React, { Component } from "react";

class RatingStars extends Component{
  constructor(props){
    super();
    this.state = {
      rating: 0
    }
   }

  componentDidMount() {
    this.setState({ rating: this.props.rating })
  }

  ratingChanged = (newRating) => {
    this.setState({ rating: newRating});
    this.props.setRating(newRating);
  }
 
  render () {
    const { rating } = this.props;
        
    return(  
        <ReactStars
                count={5}
                value={rating}
                onChange={this.ratingChanged}
                size={18}
                isHalf={false}
                emptyIcon={<i className="far fa-star"></i>}
                halfIcon={<i className="fa fa-star-half-alt"></i>}
                fullIcon={<i className="fa fa-star"></i>}
                activeColor="#ffd700"
        />
   )
  }
}
export default RatingStars;