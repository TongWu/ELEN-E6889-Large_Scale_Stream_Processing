import {Button} from 'react-bootstrap';

export const HomePage = () => {

    const clickToBTC = async (e) => {
        e.preventDefault();
        window.location.href="/bitcoin"
    };

    const clickToETH = async (e) => {
        e.preventDefault();
        window.location.href="/ethereum"
    };

    const clickToADA = async (e) => {
        e.preventDefault();
        window.location.href="/cardano"
    };

    const clickToXRP = async (e) => {
        e.preventDefault();
        window.location.href="/ripple"
    };

    const clickToDOGE = async (e) => {
        e.preventDefault();
        window.location.href="/doge"
    };

    return <>
        <header>
            Welcome to the Cryptocurrency Trend Prediction Website!
        </header>
        <p></p>

        <div>
            Please choose a cryptocurrency
        </div>
        <p></p>

        <Button onClick={clickToBTC}>BTC (Bitcoin)</Button>
        <p></p>

        <Button onClick={clickToETH}>ETH (Ethereum)</Button>
        <p></p>

        <Button onClick={clickToADA}>ADA (Cardano)</Button>
        <p></p>

        <Button onClick={clickToXRP}>XRP (Ripple)</Button>
        <p></p>

        <Button onClick={clickToDOGE}>DOGE (Doge)</Button>
        <p></p>
    </>
}