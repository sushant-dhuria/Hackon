import React from 'react';
import './Rent.css';
import StarIcon from '@mui/icons-material/Star';
import StarHalfIcon from '@mui/icons-material/StarHalf';

const RentCard = (props) => {
  const { title, price, rating, imageUrl } = props;

  // Function to generate star icons based on the rating value
  const renderStars = (rating) => {
    const maxStars = 5;
    const fullStars = Math.floor(rating);
    const halfStars = Math.ceil(rating - fullStars);
    const emptyStars = maxStars - fullStars - halfStars;
  
    const stars = [];
    for (let i = 0; i < fullStars; i++) {
      stars.push(<StarIcon key={i} />);
    }
    for (let i = 0; i < halfStars; i++) {
      stars.push(<StarHalfIcon key={i + fullStars} />);
    }
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<StarIcon key={i + fullStars + halfStars} color="disabled" />);
    }
  
    return stars;
  };
  return (
    <div className="movie-rent-card">
      <div className="movie-image">
        <img src={imageUrl} alt={title} />
      </div>
      <div className="movie-details">
        <h2 className="movie-title">{title}</h2>
        <div className="movie-rating">
          <div className="rating-stars">{renderStars(rating)}</div>
        </div>
        <div className="movie-price">
          <span>Rent for </span><button className="rental-button">${price}</button> / 30days
        </div>
      </div>
    </div>
  );
};

export default RentCard;
