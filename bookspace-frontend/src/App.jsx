import { useState } from 'react'
import styles from './style'

import {
  Navbar,
  Header,
  Hero,
  CardDeal,
  LatestBooks,
  NewsSection,
  Stats,
  Footer,
} from './components'

const App = () => {
  return (
    <div className="w-full font-bree text-white bg-slate-100 overflow-hidden">
      <div className={`${styles.paddingX} ${styles.flexCenter}`}>
        <div className={`${styles.boxWidth}`}>
          <Navbar />
        </div>
      </div>

      <div className={`${styles.paddingX} ${styles.flexCenter}`}>
        <div className={`${styles.boxWidth}`}>
          <Header />
        </div>
      </div>

      <div className={`${styles.paddingX} ${styles.flexStart}`}>
        <div className={`${styles.boxWidth}`}>
          <Hero />
        </div>
      </div>

      <div
        className={` ${styles.paddingX} ${styles.flexCenter} flex flex-wrap mt-8`}
      >
        <div className={`${styles.boxWidth} sm:w-2/3 bg-teal-200 p-`}>
          <LatestBooks />
        </div>
        <div className={`${styles.boxWidth} sm:w-1/3 bg-cyan-200 pl-2`}>
          <NewsSection />
        </div>
      </div>

      <div className={` ${styles.paddingX} ${styles.flexCenter}`}>
        <div className={`${styles.boxWidth}`}>
          <CardDeal />
          <Stats />
          <Footer />
        </div>
      </div>
    </div>
  )
}

export default App
