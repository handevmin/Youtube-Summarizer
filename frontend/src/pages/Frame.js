import { useLocation } from "react-router-dom";
import styles from "./Frame.module.css";

const Frame = () => {
  const location = useLocation();
  const sttResult = location.state?.sttResult;

  return (
    <div className={styles.div}>
      <div className={styles.child} />
      <div className={styles.wrapper}>
        <img className={styles.icon} alt="" src="/-.svg" />
      </div>
      <header className={styles.inner}>
        <div className={styles.linkHomeSvgParent}>
          <img
            className={styles.linkHomeSvg}
            loading="lazy"
            alt=""
            src="/link--home--svg.svg"
          />
          <nav className={styles.frameWrapper}>
            <nav className={styles.linkHomeParent}>
              <a className={styles.linkHome}>Home</a>
              <a className={styles.linkFeatures}>Features</a>
              <a className={styles.linkPricing}>Pricing</a>
            </nav>
          </nav>
        </div>
      </header>
      <div className={styles.rectangleParent}>
        <div className={styles.frameChild} />
        <div className={styles.frameContainer}>
          <button className={styles.rectangleGroup}>
            <div className={styles.frameItem} />
            <b className={styles.heading1}>Result</b>
          </button>
        </div>
        <div className={styles.frameDiv}>
          <div className={styles.contraryToPopularBeliefLoParent}>
            {sttResult ? (
              <>
                <h2 className={styles.contraryToPopular}>STT Result</h2>
                <div className={styles.itHasRoots}>
                  {sttResult.slice(0, 100)}
                  {sttResult.length > 100 && "..."}
                </div>
              </>
            ) : (
              <>
                <h2 className={styles.contraryToPopular}>
                  Contrary to popular belief, Lorem is not simply random text.
                </h2>
                <div className={styles.itHasRoots}>
                  It has roots in a piece of classical Latin literature from 45
                  BC, making it over 2000 years old. Richard McClintock, a Latin
                  professor at Hampden-Sydney College in Virginia, looked up one
                  of the more obscure Latin words, consectetur, from a Lorem
                  Ipsum passage, and going through the cites of the word in
                  classical literature, discovered the undoubtable source. Lorem
                  Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus
                  Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero,
                  written in 45 BC. This book is a treatise on the theory of
                  ethics, very popular during the Renaissance. The first line of
                  Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line
                  in section 1.10.32.
                </div>
              </>
            )}
          </div>
        </div>
        <div className={styles.frameParent}>
          <button className={styles.rectangleContainer}>
            <div className={styles.frameInner} />
            <div className={styles.askAQuestion}>Ask a question to AI</div>
          </button>
          <div className={styles.rectangleParent1}>
            <div className={styles.rectangleDiv} />
            <input
              className={styles.pleaseEnterWhat}
              placeholder="Please enter what you want to ask"
              type="text"
            />
            <div className={styles.frameFrame}>
              <img className={styles.frameIcon} alt="" src="/frame.svg" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Frame;