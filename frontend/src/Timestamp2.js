import { useParams } from 'react-router-dom';
import React, { useState } from 'react';
import axios from 'axios';
import YouTube from 'react-youtube';
import ReactPlayer from 'react-player';
import './Timestamp2.css'
import SearchIcon from '@mui/icons-material/Search';
const Timestamp2 = () => {
  const { videoid } = useParams();
  const [searchQuery, setSearchQuery] = useState('');
 
  const [timestamp, setTimestamp] = useState('');
  const [resultlink,setResultlink]=useState('');
 const [showresult,setShowResult]=useState(false);
  const handleSearch = async () => {
    // Fetch data from the API using Axios
    
    const videolink = `https://www.youtube.com/watch?v=${videoid}`;
const bodydata={
videolink:videolink,
query:searchQuery
}

    try {
      const resp = await axios.post('http://localhost:5000/search', bodydata);
      setTimestamp(resp.data.timestamp);
      const temp=videolink + "&t="+resp.data.timestamp
      setShowResult(true);
      setResultlink(temp);
      console.log(temp);
  } catch (err) {
      // Handle Error Here
      console.error(err);
  }
  
  };

  return (

    <div className='timestamp-main'>
      {!showresult ?    <YouTube videoId={videoid} /> :  <></>}
   
      <div className='searchbar'>
        <input
          type="text"
          placeholder="Enter your search query"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={handleSearch}><SearchIcon/></button>
      </div>
   {showresult ? <ReactPlayer controls={true} url={resultlink} playing={true}/> : <></>}
    </div>
  );
};

export default Timestamp2;
