import { createContext, useContext, useState } from 'react';

const DeckContext = createContext();

export const DeckProvider = ({ children }) => {
    //Page 1 Details
    const [deckList, setDeckList] = useState('');
    const [commander, setCommander] = useState('');
    const [partner, setPartner] = useState('');
    const [currency, setCurrency] = useState("GBP")

    //page2 Details
    const [cycles, setCycles] = useState([]);

    const [excludeArrays, setExcludeArrays] = useState({
        belowMaxPrice: [],
        uncheckedByPlayer: [],
        offColorFetch: [],
        cycleMovedToExclude: [],
        addedBecauseNotTappedButFetchable: [],
        addedBecauseNotTappedAndNotFetchable: []
    });

    const [positiveArrays, setPositiveArrays] = useState({
        include: [],
        consider: []
    });

    const [filters, setFilters] = useState({
        tappedNonfetch: false,
        tappedFetchable: false,
        maxPrice: ''
    });

    const [minBasics, setMinBasics] = useState(0);
    const [minIndividualBasics, setMinIndividualBasics] = useState(0);
    const [allowOffColorFetches, setAllowOffColorFetches] = useState(true);

    return (
        <DeckContext.Provider value={{
            deckList, setDeckList,
            commander, setCommander,
            partner, setPartner,
            currency, setCurrency,
            cycles, setCycles,
            excludeArrays, setExcludeArrays,
            positiveArrays, setPositiveArrays,
            filters, setFilters,
            minBasics, setMinBasics,
            minIndividualBasics, setMinIndividualBasics,
            allowOffColorFetches, setAllowOffColorFetches

        }}>
            {children}
        </DeckContext.Provider>
    );
};

export const useDeck = () => useContext(DeckContext);
