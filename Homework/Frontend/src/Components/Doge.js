import { Button, Image } from 'react-bootstrap';
import React, { useState, useEffect } from 'react';
import smile from './smile.png';
import day1 from './DOGE/Prediction_1days.png';
import day3 from './DOGE/Prediction_3days.png';
import day5 from './DOGE/Prediction_5days.png';

export const DogePage = () => {
  const [textFromFile1, setTextFromFile1] = useState('');
  const [textFromFile3, setTextFromFile3] = useState('');
  const [textFromFile5, setTextFromFile5] = useState('');
  const [showText1, setShowText1] = useState(false);
  const [showText3, setShowText3] = useState(false);
  const [showText5, setShowText5] = useState(false);

  useEffect(() => {
    fetch('results/DOGE/Prediction_1days.txt')
      .then((response) => {
        if (response.ok) {
          return response.text();
        } else {
          throw new Error('Error fetching text file');
        }
      })
      .then((data) => setTextFromFile1(data))
      .catch((error) => console.error('Error:', error));
  }, []);

  useEffect(() => {
    fetch('results/DOGE/Prediction_3days.txt')
      .then((response) => {
        if (response.ok) {
          return response.text();
        } else {
          throw new Error('Error fetching text file');
        }
      })
      .then((data) => setTextFromFile3(data))
      .catch((error) => console.error('Error:', error));
  }, []);

  useEffect(() => {
    fetch('results/DOGE/Prediction_5days.txt')
      .then((response) => {
        if (response.ok) {
          return response.text();
        } else {
          throw new Error('Error fetching text file');
        }
      })
      .then((data) => setTextFromFile5(data))
      .catch((error) => console.error('Error:', error));
  }, []);

  const clickToHomePage = async (e) => {
    e.preventDefault();
    window.location.href = '/';
  };

  function oneDayPrediction() {
    var image = document.getElementById('predictionImage');
    image.src = day1;
    setShowText1(true);
    setShowText3(false);
    setShowText5(false);
  }

  function threeDayPrediction() {
    var image = document.getElementById('predictionImage');
    image.src = day3;
    setShowText1(false);
    setShowText3(true);
    setShowText5(false);
  }

  function fiveDayPrediction() {
    var image = document.getElementById('predictionImage');
    image.src = day5;
    setShowText1(false);
    setShowText3(false);
    setShowText5(true);
  }

  return (
    <>
      <header>
        DOGE <Button onClick={clickToHomePage}>Back to Homepage</Button>
      </header>
      <p></p>
      {showText1 && <p>{textFromFile1}</p>}
      {showText3 && <p>{textFromFile3}</p>}
      {showText5 && <p>{textFromFile5}</p>}
      <p></p>
      <div>
        <Image src={smile} id="predictionImage" width="500" height="400" />
        <p></p>
        Please select days you want to predict:
        <p></p>
        <Button onClick={oneDayPrediction}>Next day</Button>
        <Button onClick={threeDayPrediction}>Next 3 days</Button>
        <Button onClick={fiveDayPrediction}>Next 5 days</Button>
        <p></p>
      </div>
    </>
  );
};
