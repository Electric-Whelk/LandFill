// Page2.js – Dynamic land cycle selector interface
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import cyclesData from '../Data/cycles';
import './Page2.css';

const COLUMN_IDS = {
    include: 'Definitely include these',
    consider: 'Consider these',
    exclude: 'Never include these'
};

const Page2 = () => {
    console.log("📦 Rendering Page2 — cyclesData:", cyclesData);

    const navigate = useNavigate();

    /*const [columns, setColumns] = useState({
        include: [],
        consider: [],
        exclude: []
    });*/

    const [filters, setFilters] = useState({
        tappedNonfetch: false,
        tappedFetchable: false,
        maxPrice: '',
        currency: 'USD',
        allowOffColorFetches: false
    });

    /*seEffect(() => {
        console.log("🚀 cyclesData:", JSON.stringify(cyclesData, null, 2));

        const autoIncluded = [];
        const consider = [];

        cyclesData.forEach(cycle => {
            if (cycle.suggestAutoInclude) autoIncluded.push(cycle);
            else consider.push(cycle);
        });

        const newCols = { include: autoIncluded, consider, exclude: [] };
        console.log("🧪 Setting columns to:", newCols);

        setColumns(newCols);
    }, []);

    useEffect(() => {
        console.log("🔁 [columns] useEffect triggered");
        console.log("✅ Updated columns state:", JSON.stringify(columns, null, 2));
    }, [columns]);*/

    const [columns, setColumns] = useState(() => {
        const autoIncluded = [];
        const consider = [];

        cyclesData.forEach((cycle) => {
            if (cycle.suggestAutoInclude) autoIncluded.push(cycle);
            else consider.push(cycle);
        });

        return {
            include: autoIncluded,
            consider: consider,
            exclude: []
        };
    });

    const onDragEnd = result => {
        if (!result.destination) return;
        const { source, destination } = result;

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

    useEffect(() => {
        applyFilters();
    }, [filters.tappedNonfetch, filters.tappedFetchable, filters.maxPrice, filters.currency]);

    return (
        <div className="page2">
            <button onClick={() => navigate('/')}>⬅ Back</button>
            <h1>Land Cycle Preferences</h1>

            <div className="faq-row">
                <FAQ label="How will this optimize my manabase?" content="OPTIMIZATON EXPLANATION HERE" />
                <FAQ label="How Long Will optimization take?" content="OPTIMIZATION TIME ESTIMATE HERE" />
            </div>

            <DragDropContext onDragEnd={onDragEnd}>
                <div className="columns">
                    {Object.entries(COLUMN_IDS).map(([key, label]) => (
                        <Droppable droppableId={key} key={key}>
                            {(dropProvided) => (
                                <div
                                    className="column"
                                    ref={dropProvided.innerRef}
                                    {...dropProvided.droppableProps}
                                >
                                    <h3>{label}</h3>
                                    {columns[key]?.map((cycle, index) => (
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
                                                >
                                                    <span>{cycle.displayName}</span>
                                                    <InfoIcon info={cycle.description}/>
                                                </div>
                                            )}
                                        </Draggable>)
                                    )}
                                    {dropProvided.placeholder}
                                </div>
                            )}
                        </Droppable>
                    ))}


                </div>
            </DragDropContext>

            <div className="filters">
                <h3>Remove from consideration:</h3>
                <label>
                    <input type="checkbox" name="tappedNonfetch" checked={filters.tappedNonfetch} onChange={handleFilterChange} />
                    All lands that are always tapped and aren’t fetchable (eg, GuildGates)
                </label>
                <label>
                    <input type="checkbox" name="tappedFetchable" checked={filters.tappedFetchable} onChange={handleFilterChange} />
                    All lands that are always tapped but are fetchable (eg, Surveil Lands)
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
                <label>
                    <input type="checkbox" name="allowOffColorFetches" checked={filters.allowOffColorFetches} onChange={handleFilterChange} />
                    Allow Off-Color Fetches
                </label>
            </div>

            <div className="prioritization">
                <h3>
                    Land Prioritization <InfoIcon info="LandFill can only judge lands by how good they are at producing mana..." />
                </h3>
                {/* Typed and Untyped Tapland Prioritization blocks would go here */}
                <div>(Placeholder for ranking lists of taplands with drag-to-rank behavior)</div>
            </div>

            <button onClick={() => navigate('/advanced')}>Advanced Prioritization Settings</button>
            <button onClick={() => navigate('/results')}>Run Optimizer</button>
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

const InfoIcon = ({ info }) => (
    <span className="info-icon" title={info}>❔</span>
);

export default Page2;
