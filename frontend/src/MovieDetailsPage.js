import React, { useEffect, useState, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import MovieCard from './MovieCard';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './MovieDetailspage.css';

const MovieDetailsPage = () => {
  let { state } = useLocation();
  const movieId = state?.movieId;

  const [movieDetails, setMovieDetails] = useState(null);
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [playlists, setPlaylists] = useState([]);
  const [isRecommendedContainerVisible, setRecommendedContainerVisible] = useState(false);

  // Ref to the recommended container
  const recommendedContainerRef = useRef(null);

  useEffect(() => {
    // Fetch movie details using Axios based on the movieId
    axios
      .get(`http://localhost:5000/movies/${movieId}`)
      .then((response) => setMovieDetails(response.data))
      .catch((error) => console.error('Error fetching movie details:', error));

    // Fetch recommended movies based on the movieId
    axios
      .get(`http://localhost:5000/recommendations/${movieId}`)
      .then((response) => {
        const recommendedMoviesData = response.data.movies;
        setRecommendedMovies(recommendedMoviesData);
      })
      .catch((error) => console.error('Error fetching recommended movies:', error));

    // Fetch playlists based on the movieId
    axios
      .get(`http://localhost:5000/playlist/${movieId}`)
      .then((response) => {
        const playlistsData = response.data.playlists;
        setPlaylists(playlistsData);
      })
      .catch((error) => console.error('Error fetching playlists:', error));

    // Add click event listener to the window to handle clicks outside of the container
    window.addEventListener('click', handleWindowClick);

    return () => {
      // Remove the event listener when the component unmounts
      window.removeEventListener('click', handleWindowClick);
    };
  }, movieId);

  const handleWindowClick = (e) => {
    if (recommendedContainerRef.current && !recommendedContainerRef.current.contains(e.target)) {
      setRecommendedContainerVisible(false);
    }
  };

  return (
    <div className="movie-details-page">
      {movieDetails && (
        <div className="movie-details__info">
          <div className="movie-details__desc">
            <h1 className="movie-details__title">{movieDetails.title}</h1>
            <p className="movie-details__description">{movieDetails.description}</p>
            <p></p>
            {movieDetails.rentPrice && (
              <button className="rent-button">
                Rent for ${movieDetails.rentPrice}
              </button>
            )}
          </div>
          <div className="poster-image">
            <img src={movieDetails.poster_link} alt={movieDetails.title} />
          </div>
        </div>
)}

      <h3>Recommended Movies:</h3>

      <div className="recommended-movie-overlay" onClick={() => setRecommendedContainerVisible(!isRecommendedContainerVisible)}>
        <div className="recommended-movie-collage" ref={recommendedContainerRef}>
          {recommendedMovies.slice(0, 4).map((movie) => (
            <img
              key={movie.id}
              src={movie.poster_link}
              alt={movie.title}
              className="recommended-movie-image"
            />
          ))}
        </div>
      </div>

      {isRecommendedContainerVisible && (
        <div className="recommended-movies-container">
          {recommendedMovies.map((movie) => (
            <div key={movie.id} className="movie">
              <Link to={`/movie/${movie.id}`} state={{ movieId: movie.id }}>
                <MovieCard infos={movie} />
              </Link>
            </div>
          ))
        }
        </div>
)}

      <h3>Playlists:</h3>
      <div className="playlists-container">
        {playlists.map((playlist) => (
          <Playlist
            key={playlist.id}
            playlist={playlist}
          />
        ))
        }
      </div>
    </div>
  );
};

export default MovieDetailsPage;

// Create a Playlist component for each playlist
function Playlist({ playlist }) {
  const [isPlaylistVisible, setIsPlaylistVisible] = useState(false);

  const handlePlaylistClick = () => {
    setIsPlaylistVisible(!isPlaylistVisible);
  };

  return (
    <div className="playlist">
       <h3 className="overlay-text">{playlist.name}</h3>
      <div className="recommended-movie-overlay" onClick={handlePlaylistClick}>
        <div className="recommended-movie-collage">
          {playlist.movies.slice(0, 4).map((movie) => (
            <img
              key={movie.id}
              src={movie.poster_link}
              alt={movie.title}
              className="recommended-movie-image"
            />
         ) )}
        </div>
       
      </div>
      {isPlaylistVisible && (
        <div className="recommended-movies-container">
          {playlist.movies.map((playlistMovie) => (
            <div key={playlistMovie.id} className="playlist-movie">
              <Link to={`/movie/${playlistMovie.id}`} state={{ movieId: playlistMovie.id }}>
                <MovieCard infos={playlistMovie} />
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
