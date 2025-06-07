import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import SearchForm from '../components/SearchForm';
import TrainList from '../components/TrainList';
import TrainDetails from '../components/TrainDetails';
import styles from '../styles/homePage.module.css';

export default function HomePage() {
  const [results, setResults] = useState(null);
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [searchedQuery, setSearchedQuery] = useState({ from: '', to: '', date: '', time: '' });
  const [searchParams, setSearchParams] = useSearchParams();

  const selectedTrainId = searchParams.get('trainId');
  const selectedTrain = results?.find((train) => train.trainId === selectedTrainId);

  const handleSelectTrain = (train) => {
    setSearchParams({ trainId: train.trainId });
  };

  const handleGoBack = () => {
    setSearchParams({});
  };

  return (
    <div className={styles.container}>
      <h1 className='mainTitle'>Rail Rave</h1>
      {!selectedTrain && (
        <h3 style={{ marginTop: '-2rem' }}>Your party train booking site 🎉</h3>
      )}
      {!selectedTrain && (
        <>
          <SearchForm
            setResults={(res) => {
              setResults(res);
              setSearchedQuery({ from, to, date, time }); // freeze whole query at search
            }}
            from={from}
            setFrom={setFrom}
            to={to}
            setTo={setTo}
            date={date}
            setDate={setDate}
            time={time}
            setTime={setTime}
          />
          <TrainList results={results} searchQuery={searchedQuery} onSelect={handleSelectTrain} />
        </>
      )}
      {selectedTrain && (
        <TrainDetails train={selectedTrain} searchQuery={searchedQuery} goBack={handleGoBack} />
      )}
    </div>
  );
}