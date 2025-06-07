import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/aboutPage.module.css';
import devsImg from '../assets/pictures/devs.jpg'
import ideaImg from '../assets/pictures/idea.jpg'
import chooseUsImg from '../assets/pictures/chooseUs.png'

export default function AboutPage() {
  return (
    <div className={styles.container}>
      <h1 className='mainTitle'>About Us</h1>
      <div className={styles.columns}>
        <div className={styles.column}>
          <h2>Our Team</h2>
          <p>
            We are young yet passionate developers who totally should get 100% from this project ;)
          </p>
          <img src={devsImg} alt="Developers" className={styles.image} />
        </div>
        <div className={styles.column}>
          <h2>Our Vision</h2>
          <p>
            Rail Rave is our answer to a very popular problem: how to be a responsible adult and have fun at the same time? 
            It is simple: throw a party while moving towards a conference in another city or some professional training 
            (even if it's secretly an affair – well, if it’s an affair, you can throw an even better party).
          </p>
          <img src={ideaImg} alt="Party Train" className={styles.image} />
        </div>
        <div className={styles.column}>
          <h2>Our Product</h2>
          <p>
            So what? Are you tired of meaningless hours wasted in a train? <Link to="/">Book</Link> a carriage or even a whole train and get those old bones moving!
          </p>
          <img src={chooseUsImg} alt="Train Booking" className={styles.image} />
        </div>
      </div>
    </div>
  );
}