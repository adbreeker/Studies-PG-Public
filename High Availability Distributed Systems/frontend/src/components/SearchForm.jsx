import React, { useState, useEffect, useRef } from 'react';
import styles from '../styles/homePage.module.css';
import townsData from '../assets/kod90.json';
import prescrapedJson from '../assets/PrescrappedResults.json';

const trainScraperApi = '/api/train-scraper'

export default function SearchForm({ setResults, from, setFrom, to, setTo, date, setDate, time, setTime }) {
  const [townNames, setTownNames] = useState([]);
  const [fromSuggestions, setFromSuggestions] = useState([]);
  const [toSuggestions, setToSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fromError, setFromError] = useState(false);
  const [toError, setToError] = useState(false);
  const [isSelecting, setIsSelecting] = useState(false);

  const fromInputRef = useRef(null);
  const toInputRef = useRef(null);

  useEffect(() => {
    if (date === '') {
      const currentDate = new Date().toLocaleDateString('en-CA'); // Format: YYYY-MM-DD
      setDate(currentDate);
    }
  }, [date, setDate]);

  useEffect(() => {
    if (time === '') {
      const currentTime = new Date().toLocaleTimeString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
      }); // Format: HH:MM
      setTime(currentTime);
    }
  }, [time, setTime]);

  useEffect(() => {
    setTownNames(Object.keys(townsData));
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        fromInputRef.current &&
        !fromInputRef.current.contains(event.target)
      ) {
        setFromSuggestions([]);
      }
      if (toInputRef.current && !toInputRef.current.contains(event.target)) {
        setToSuggestions([]);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, []);

  const handleInputChange = (value, setSuggestions, setValue, setError) => {
    setValue(value);
    setError(false);

    if (value.length > 0) {
      const filteredSuggestions = townNames.filter((town) =>
        town.toLowerCase().startsWith(value.toLowerCase())
      );

      setSuggestions(filteredSuggestions);
    } else {
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (suggestion, setValue, setSuggestions, setError) => {
    setIsSelecting(true);
    setValue(suggestion);
    setSuggestions([]);
    setError(false);
    setIsSelecting(false);
  };

  const handleFocus = (setValue) => {
    if (!isSelecting) {
      setValue('');
    }
    setIsSelecting(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResults(null);

    const fromCode = townsData[from];
    const toCode = townsData[to];

    const isFromValid = !!fromCode;
    const isToValid = !!toCode;

    setFromError(!isFromValid);
    setToError(!isToValid);

    if (!isFromValid || !isToValid) {
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`${trainScraperApi}/commands/scrap?from=${fromCode}&to=${toCode}`, { method: 'POST' });
      if (!res.ok) throw new Error(`Failed to trigger scraping: ${res.statusText}`);

      const scrapingId = await res.text();
      console.log('Scraping ID:', scrapingId);

      await new Promise((resolve) => setTimeout(resolve, 1000));

      let status = 'STARTED';
      let data = null;
      const startTime = Date.now();
      const SCRAPER_TIMEOUT_MS = Number(import.meta.env.VITE_SCRAPER_TIMEOUT_MS) || 5000;

      while (status !== 'COMPLETED') {
        if (Date.now() - startTime > SCRAPER_TIMEOUT_MS) break;

        const queryRes = await fetch(`${trainScraperApi}/queries/scraping/${scrapingId}`);
        const queryData = await queryRes.json();
        status = queryData.status;

        if (queryRes.status === 404) {
          data = [];
          break;
        }

        if (status === 'COMPLETED') {
          data = queryData.results;
          if (data && data.length > 0) break;
        }
      }

      setResults(Array.isArray(data) ? data : [], { from, to, date, time }); // <-- pass query
    } catch (error) {
      console.error('Error fetching train data:', error);

      await new Promise((resolve) => setTimeout(resolve, 1000));

      const fallbackData = prescrapedJson.results || []; // Use the imported JSON directly as fallback
      setResults(Array.isArray(fallbackData) ? fallbackData : [], { from, to, date, time }); // <-- pass query
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form className={styles.card} onSubmit={handleSubmit}>
        <div className={styles.searchRow}>
          <div className={styles.searchColumn}>
            <label>Departure station:</label>
            <div className={styles.searchBox} ref={fromInputRef}>
              <input
                type="text"
                className={styles.searchInput}
                value={from}
                onFocus={() => handleFocus(setFrom)}
                onChange={(e) => handleInputChange(e.target.value, setFromSuggestions, setFrom, setFromError)}
                placeholder="Enter departure station"
                style={{ borderColor: fromError ? 'red' : '' }}
                required
              />
              {fromSuggestions.length > 0 && (
                <ul className={styles.suggestions}>
                  {fromSuggestions.map((suggestion) => (
                    <li
                      key={suggestion}
                      className={styles.suggestionItem}
                      onMouseDown={() => handleSuggestionClick(suggestion, setFrom, setFromSuggestions, setFromError)}
                    >
                      {suggestion}
                    </li>
                  ))}
                </ul>
              )}
            </div>
            {fromError && <p className="errorMessage">Invalid departure station</p>}

            <label>Arrival station:</label>
            <div className={styles.searchBox} ref={toInputRef}>
              <input
                type="text"
                className={styles.searchInput}
                value={to}
                onFocus={() => handleFocus(setTo)}
                onChange={(e) => handleInputChange(e.target.value, setToSuggestions, setTo, setToError)}
                placeholder="Enter arrival station"
                style={{ borderColor: toError ? 'red' : '' }}
                required
              />
              {toSuggestions.length > 0 && (
                <ul className={styles.suggestions}>
                  {toSuggestions.map((suggestion) => (
                    <li
                      key={suggestion}
                      className={styles.suggestionItem}
                      onMouseDown={() => handleSuggestionClick(suggestion, setTo, setToSuggestions, setToError)}
                    >
                      {suggestion}
                    </li>
                  ))}
                </ul>
              )}
            </div>
            {toError && <p className="errorMessage">Invalid arrival station</p>}
          </div>

          <div className={styles.dateColumn}>
            <label>Date:</label>
            <div className={styles.searchBox}>
              <input
                type="date"
                className={styles.searchInput}
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
              />
            </div>
            <label>Time:</label>
            <div className={styles.searchBox}>
              <input
                type="time"
                className={styles.searchInput}
                value={time}
                onChange={(e) => setTime(e.target.value)}
                required
              />
            </div>
          </div>
        </div>

        <button type="submit" className="primary" disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {loading && (
        <div className="loader">
          <div className="spinner"></div>
        </div>
      )}
    </div>
  );
}
