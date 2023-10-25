import React from 'react'
import './projector.css'
const Projector = () => {
  return (
    <div id="projectorContainer">
    <div class="projectorLight">

    <div class="cover"></div>
    <div class="cover"></div>
  </div>
       
  <div class="projectorBody">
    <div class="lensHold"></div>
    <div class="lens"></div>
  </div>
 <div class="filmDisk" id="film1">
        <div class="fdBack">
            <div class="fdFilm"></div>
            <div class="fdBar"></div>
            <div class="fdBar2"></div>
            <div class="fdCover"></div>
        </div>
    </div>
      <div class="filmDisk" id="film2">
        <div class="fdBack">
            <div class="fdFilm"></div>
            <div class="fdBar"></div>
            <div class="fdBar2"></div>
            <div class="fdCover"></div>
        </div>
    </div>
   </div>
  )
}

export default Projector