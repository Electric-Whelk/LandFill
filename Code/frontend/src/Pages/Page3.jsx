import React, {useEffect, useState} from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useDeck } from '../DeckContext'
import './Pages.css';
import cardsData from '../Data/cards';
import page2 from "./Page2";

const Page3 = () => {

    const navigate = useNavigate();
    const location = useLocation();

    const { currency } = useDeck()


    //REMEMBER TO READD THE STUFF THAT ALLOWS RANKING BY PERFORMANCE
    /*const [outputLands, setOutputLands] = useState(() => {
        cardsData.sort((a, b) => b.performance - a.performance);
        return (cardsData);
    });*/

    const [landsString, setLandsString] = useState('')
    const [nonLandsString, setNonLandsString] = useState('')
    const [viewedCard, setViewedCard] = useState(null)
    const [includeNonLands, setIncludeNonLands] = useState(false)
    const [outputStyle, setOutputStyle] = useState({});
    const [textContents, setTextContents] = useState('')


    function cardListToString(cardList){
        let output = cardList[0].name
        let len = cardList.length
        for (let i = 1; i < len; i++){
            output = output + "\n"
            output = output + cardList[i].name
        }
        return output
    }


    const [fullContents, setFullContents] = useState(() => {
        const data = location.state?.data
        const output = {moxbox:{}, archidekt:{}, tappedout:{}}
        output.moxbox.cards = data.moxbox
        output.moxbox.lands = data.moxboxLands
        output.archidekt.cards = data.archidekt
        output.archidekt.lands = data.archidektLands
        output.tappedout.cards = data.tappedout
        output.tappedout.lands = data.tappedoutLands
        setOutputStyle(output.moxbox)
        return output
    })

    const [landContents, setLandContents] = useState(() => {
        const data = location.state?.data
        const output = {}
        output.moxbox = data.moxboxLands
        output.archidekt = data.archidektLands
        output.tappedout = data.tappedoutLands
        return output
    })



    const [lands, setLands] = useState(() => {

        const data = location.state?.data
        const innerLands = data.lands;
        setLandsString(cardListToString(innerLands))
        return innerLands.sort((a, b) => b.proportions - a.proportions)
    });

    const [nonLands, setNonLands] = useState(() => {

        const data = location.state?.data
        const innerCards = data.nonLands;
        setNonLandsString(cardListToString(innerCards))
        return innerCards
    });


    const [deckScore, setDeckScore] = useState(() => {
        const data = location.state?.data
        return data.proportions
    });





    //Effect Hooks
    //set the default text string on creation not sur why this isn't handled by our setLands useState but w/e
    function formatLandsOrCards(input){
        switch(outputStyle){
            case "moxbox":
                setTextContents(input.moxbox)
                break;
            case "archidekt":
                setTextContents(input.archidekt)
                break;
            case "tappedout":
                setTextContents(input.tappedout)
                break;
        }
    }

    //sort out the contents of the textbox
    //set it on loading the page
    useEffect(() => {
        setTextContents(outputStyle.lands)
    }, [fullContents])

    useEffect(() => {
        if(includeNonLands){
            setTextContents(outputStyle.cards)
        }else{
            setTextContents(outputStyle.lands)
        }
    }, [outputStyle])

    const handleFormatChange = (e) => {
        switch(e.target.value){
            case "moxbox":
                setOutputStyle(fullContents.moxbox);
                break;
            case "archidekt":
                setOutputStyle(fullContents.archidekt);
                break;
            case "tappedout":
                setOutputStyle(fullContents.tappedout);
                break;
        }
    }

    const handleIncludeNonLandTick = (e) => {
        setIncludeNonLands(e.target.value)
        if(e.target.checked){
            setTextContents(outputStyle.cards)
        }else{
            setTextContents(outputStyle.lands)
        }
    }

    const CardInfoPanel = ({ card }) => {

        if (card === null) return <div className="card-info-panel">sploop</div>

        return (

            <div className="card-info-panel">
                <img src={card.image} />
                <div className="card-text-info">
                    <p>Name: {card.name}</p>
                    <p>Performance: {card.proportions}</p>
                    <p>Price: {card[currency]} ({currency})</p>
                </div>

            </div>);
    }

    return(
        <div className="page3">


            <div className = "main-content" id="page3-main">
            <div className="card-outputs">
                <h3>Lands We've Added (ranked by performance)</h3>
                <i>HINT: If you don't like some of these, remove them and hit "re-run optimizer"</i>

                {lands.map((land, index) => (
                    <CardRankPanel land={land}
                                   index={index}
                                   setViewedCard={setViewedCard}
                                   key={land.displayName || index}
                    />
                ))}
            </div>



            <div className="admin-outputs">


            <div>
                <h3>Metrics</h3>
                <p>Percentage of wasteless games: {deckScore}</p>
                <p>Total manabase price: {lands.reduce((total, land) => total + land[currency], 0).toFixed(2)}</p>

            </div>

            <div>
                <h3>Format Output</h3>
                <textarea cols="40"
                          rows="20"
                          value={textContents}
                ></textarea>
            </div>

                <div>
                    <label htmlFor="outputStyle">Output Style:</label>
                    <select name="outputStyle" id="outputStyle" onChange={e => handleFormatChange(e)}>
                        <option value="moxbox">Moxfield/Deckbox</option>
                        <option value="tappedout">TappedOut</option>
                        <option value="archidekt">Archidekt</option>
                    </select>
                </div>
                <div>
                    <input type="checkbox" id="includeNonLands" name="includeNonLands"
                            onChange={(e) => handleIncludeNonLandTick(e)} />
                    <label htmlFor="includeNonLands"> Include nonlands</label>
                </div>



            </div>

        </div>
        <div className = "side-panel">
            <CardInfoPanel card={viewedCard}/>

            <div className="nav-buttons">
                <button onClick={() => navigate('/page2')}>⬅ Back to Cycles</button>
                <button onClick={() => navigate('/page3')}>Re-Run Optimizer</button>
            </div>
        </div>
        </div>
    );
}

const CardRankPanel = ({ land, index, setViewedCard }) => {
    return (

        <div
            className = "cycle-card"
            land={land}
            index={index}
            onMouseOver={() => setViewedCard(land)}>
            <Remover hey={"hey"}/>
            {land.name} ({land.proportions})
        </div>
    );
};

const Remover = ({ hey }) => {
    return(
        <span> X </span>
    )
}


export default Page3;