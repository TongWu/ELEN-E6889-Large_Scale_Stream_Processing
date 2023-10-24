import React from 'react';
import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import {HomePage} from './Components/HomePage';
import {BitcoinPage} from './Components/Bitcoin';
import {EthereumPage} from './Components/Ethereum';
import {CardanoPage} from './Components/Cardano';
import {RipplePage} from './Components/Ripple';
import {DogePage} from './Components/Doge';


function App() {
  return <BrowserRouter>
    <Routes>
      <Route path="/" element={<HomePage/>}/>
      <Route path="/bitcoin" element={<BitcoinPage/>}/>
      <Route path="/ethereum" element={<EthereumPage/>}/>
      <Route path="/cardano" element={<CardanoPage/>}/>
      <Route path="/ripple" element={<RipplePage/>}/>
      <Route path="/doge" element={<DogePage/>}/>
    </Routes>
  </BrowserRouter>
}

export default App;
