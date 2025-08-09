// Page2.js – Dynamic land cycle selector interface
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import cyclesData from '../Data/cycles';
import './Pages.css';



const COLUMN_IDS = {
    include: 'Definitely include these',
    consider: 'Consider these',
    exclude: 'Never include these'
};

const RANK_IDS = {
    fetchable: 'Fetchable Taplands',
    nonFetchable: 'Nonfetchable Taplands'
}

const Page2 = () => {


    //routing
    const navigate = useNavigate();
    const location = useLocation();

    //data handling
    const data = location.state?.data;


    //state setting for toggles
    const [minBasics, setMinBasics] = useState(0)
    const [minIndividualBasics, setMinIndividualBasics] = useState(0)
    const [allowOffColorFetches, setAllowOffColorFetches] = useState(false)
    const [viewedCycle, setViewedCycle] = useState(null)

    const [filters, setFilters] = useState({
        tappedNonfetch: false,
        tappedFetchable: false,
        maxPrice: '',
        currency: 'USD',
    });

    const [columns, setColumns] = useState(() => {
        const autoIncluded = [];
        const consider = [];
        const autoincludeList = ["Shock Lands", "Fetch Lands"];


        data.forEach((cycle) => {
            console.log(autoincludeList.includes(cycle.displayName))

            if (autoincludeList.includes( cycle.displayName )){
                autoIncluded.push(cycle);
                cycle.suggestAutoInclude = true
            }
            else {
                consider.push(cycle);
                cycle.suggestAutoInclude = false
            }


            console.log(autoIncluded)
            console.log(consider)
        });

        return {
            include: autoIncluded,
            consider: consider,
            exclude: []
        };
    });

    const [rankings, setRankings] = useState(() => {
        const untypedTaps = []
        const typedTaps = []


        cyclesData.forEach((cycle) => {
            if (cycle.alwaysTapped) {
                if (cycle.fetchable) typedTaps.push(cycle);
                else untypedTaps.push(cycle);
            }
        });

        return {
            fetchable: typedTaps,
            nonFetchable: untypedTaps,
        };
    });

    //listeners

    useEffect(() => {
        applyFilters();
    }, [filters.tappedNonfetch, filters.tappedFetchable, filters.maxPrice, filters.currency]);


    //handle data from Page 1 (OLD VERSION - has to after react hooks)
    /*const data = location.state?.data;
    if (!data) {
        return <p>No data received. Please go back to Page 1.</p>;
    }
    console.log(data)*/

    //behaviour definition for drag and drop columns

    const onDragEnd = result => {
        if (!result.destination) return;
        const { source, destination } = result;

        if (source.droppableId === destination.droppableId) return;

        const srcList = Array.from(columns[source.droppableId]);
        const [movedItem] = srcList.splice(source.index, 1);
        const destList = Array.from(columns[destination.droppableId]);
        destList.splice(destination.index, 0, movedItem);

        const newColumns = {
            ...columns,
            [source.droppableId]: srcList,
            [destination.droppableId]: destList
        };


        // Uncheck filters if cycle was manually moved
        setFilters(prev => {
            let updated = { ...prev };
            if (destination.droppableId !== 'exclude') {
                if (cycleMatchesFilter(movedItem, prev)) {
                    updated = { ...prev, tappedNonfetch: false, tappedFetchable: false };
                }
            }
            return updated;
        });

        setColumns(newColumns);
    };

    const onReorder = result => {
        if (!result.destination) return;
        const { source, destination } = result;

        if (source.index === destination.index) return;
        if (source.droppableId !== destination.droppableId) return;


        const newList = Array.from(rankings[source.droppableId]);
        //throw new Error("This has been a test of your emergency broadcasting system")
        const [movedItem] = newList.splice(source.index, 1);
        newList.splice(destination.index, 0, movedItem)

        setRankings({...rankings,
            [source.droppableId]: newList
        })


    }


    

    const cycleMatchesFilter = (cycle, filters) => {
        const { alwaysTapped, fetchable } = cycle;
        const { tappedNonfetch, tappedFetchable, maxPrice, currency } = filters;

        if (tappedNonfetch && alwaysTapped && !fetchable) return true;
        if (tappedFetchable && alwaysTapped && fetchable) return true;
        if (
            maxPrice &&
            cycle[`maxPriceIn${currency}`] > parseFloat(maxPrice)
        )
            return true;
        return false;
    };

    const applyFilters = () => {
        const remaining = [
            ...columns.include,
            ...columns.consider,
            ...columns.exclude
        ];

        const newExclude = remaining.filter(cycle => cycleMatchesFilter(cycle, filters));
        const newInclude = remaining.filter(
            cycle => cycle.suggestAutoInclude && !cycleMatchesFilter(cycle, filters)
        );
        const newConsider = remaining.filter(
            cycle =>
                !cycle.suggestAutoInclude &&
                !cycleMatchesFilter(cycle, filters)
        );
        setColumns({ include: newInclude, consider: newConsider, exclude: newExclude });
    };

    const handleFilterChange = e => {
        const { name, value, type, checked } = e.target;
        const val = type === 'checkbox' ? checked : value;
        setFilters(prev => ({ ...prev, [name]: val }));
    };




    return (
        <div className="page2">
        <div className="main-content">
            <div className="admin">
                <h1>Land Cycle Preferences</h1>

                <div className="faq-row">
                    <FAQ label="How will this optimize my manabase?" content="OPTIMIZATON EXPLANATION HERE"/>
                    <FAQ label="How Long Will optimization take?" content="OPTIMIZATION TIME ESTIMATE HERE"/>
                </div>

                <div className="preferences">
                    <div className="filters">
                        <h3>Remove from consideration:</h3>
                        <label>
                            <input type="checkbox" name="tappedNonfetch" checked={filters.tappedNonfetch} onChange={handleFilterChange} />
                            All lands that are always tapped and aren’t fetchable (eg, GuildGates)
                        </label>
                        <label>
                            <input type="checkbox" name="tappedFetchable" checked={filters.tappedFetchable} onChange={handleFilterChange} />
                            All lands that are always tapped even if they're fetchable (eg, Surveil Lands)
                        </label>
                        <label>
                            All lands that cost more than
                            <input
                                type="number"
                                name="maxPrice"
                                value={filters.maxPrice}
                                onChange={handleFilterChange}
                                placeholder="Amount"
                            />
                            <select name="currency" value={filters.currency} onChange={handleFilterChange}>
                                <option value="USD">USD</option>
                                <option value="Euros">Euros</option>
                                <option value="GBP">GBP</option>
                            </select>
                        </label>
                    </div>

                    <div className = "preciseSpecs">
                        <label>
                            <input type="checkbox" name="OffColorFetches" checked={allowOffColorFetches} onChange={setAllowOffColorFetches} />
                            Allow Off-Color Fetches
                        </label>

                        <label>
                            Include at least
                            <input
                                type="number"
                                name="minBasics"
                                value={minBasics}
                                onChange={setMinBasics}
                                /*placeholder="Amount"*/
                            /> basic lands.
                        </label>

                        <label>
                            Include at least
                            <input
                                type="number"
                                name="minIndividualBasics"
                                value={minIndividualBasics}
                                onChange={setMinIndividualBasics}
                                /*placeholder="Amount"*/
                            /> of every basic land in the deck's colours.
                        </label>
                    </div>
                </div>

            </div>

            <DragDropContext onDragEnd={onDragEnd}>
                <div className="columns">
                    {Object.entries(COLUMN_IDS).map(([key, label]) => (
                        <div>
                        <h3>{label}</h3>
                        <Droppable droppableId={key} key={key}>
                            {(dropProvided) => (
                                <div
                                    className="column"
                                    ref={dropProvided.innerRef}
                                    {...dropProvided.droppableProps}
                                >
                                    {columns[key]?.map((cycle, index) => (<CyclePanel
                                        cycle={cycle}
                                        index={index}
                                        setViewedCycle={setViewedCycle}/>)
                                    )}
                                    {dropProvided.placeholder}
                                </div>
                            )}
                        </Droppable></div>
                    ))}


                </div>
            </DragDropContext>


            <div className="prioritization">
                <h3>
                    Rank Equivalent Lands
                </h3>
                <DragDropContext onDragEnd={onReorder}>
                    <div className="columns">
                        {Object.entries(RANK_IDS).map(([key, label]) => (
                            <div>
                                <h3>{label}</h3>
                                <Droppable droppableId={key} key={key}>
                                    {(dropProvided) => (
                                        <div
                                            className="ranking"
                                            ref={dropProvided.innerRef}
                                            {...dropProvided.droppableProps}
                                        >
                                            {rankings[key]?.map((cycle, index) => (<CyclePanel
                                                cycle={cycle}
                                                index={index}
                                                setViewedCycle={setViewedCycle}/>)
                                            )}
                                            {dropProvided.placeholder}
                                        </div>
                                    )}
                                </Droppable></div>
                        ))}

                    </div>
                </DragDropContext>
            </div>
        </div>

        <div className="side-panel">
            <CycleInfoPanel cycle={viewedCycle}/>

            <div className="nav-buttons">
                <button onClick={() => navigate('/page1')}>⬅ Back</button>
                <button onClick={() => navigate('/page3')}>Run Optimizer</button>
            </div>
        </div>
        </div>
    );
};

const FAQ = ({ label, content }) => {
    const [open, setOpen] = useState(false);
    return (
        <div className="faq" onClick={() => setOpen(!open)}>
            <strong>{label}</strong>
            {open && <div className="faq-content">{content}</div>}
        </div>
    );
};

const InfoIcon = ({ cycle }) => {

    return(<span className="info-icon" title={cycle.description}>❔</span>)
}

const CycleInfoPanel = ({ cycle }) => {
    if (cycle === null) return <div className="card-info-panel">sploop</div>

    return (

    <div className="card-info-panel">
        <img src={cycle.image} alt={cycle.description} />
        <div className="card-text-info">
            <p>Name: {cycle.displayName}</p>
            <p>Lands: [listed by price]</p>
        </div>

    </div>);
};

const CyclePanel = ({ cycle, index, setViewedCycle }) => (
    <Draggable
        key={cycle.displayName}
        draggableId={cycle.displayName}
        index={index}
    >
        {(dragProvided) => (
            <div
                className="cycle-card"
                ref={dragProvided.innerRef}
                {...dragProvided.draggableProps}
                {...dragProvided.dragHandleProps}
                onMouseOver={() => setViewedCycle(cycle)}
            >
                <span>{cycle.displayName}</span>
            </div>
        )}
    </Draggable>
);

export default Page2;
