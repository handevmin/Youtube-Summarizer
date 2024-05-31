import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Desktop.module.css";

const Desktop = () => {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // 서버 응답을 기다리는 동안 Sidebar 페이지로 이동
      navigate("/sidebar");
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: youtubeUrl }),
      });
      const data = await response.json();
      console.log(data);
      // 서버 응답이 오면 STT 결과와 함께 / 페이지로 이동
      navigate("/", { state: { sttResult: data.text } });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className={styles.desktop}>
      <div className={styles.desktopChild} />
      <header className={styles.desktopInner}>
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
      <footer className={styles.parent}>
        <img className={styles.icon} alt="" src="/-1.svg" />
        <div className={styles.frameParent}>
          <div className={styles.frameGroup}>
            <div className={styles.frameContainer}>
              <div className={styles.frameDiv}>
                <div className={styles.wrapperUnionParent}>
                  <div className={styles.wrapperUnion}>
                    <img
                      className={styles.unionIcon}
                      loading="lazy"
                      alt=""
                      src="/union.svg"
                    />
                  </div>
                  <b className={styles.heading1}>with A.I</b>
                </div>
              </div>
              <h1 className={styles.heading1Container}>
                <p className={styles.revolutionize}>Revolutionize</p>
                <p className={styles.yourApproach}>{`Your Approach `}</p>
              </h1>
            </div>
            <div className={styles.rizeIsAnAiProductivityCoaWrapper}>
              <div className={styles.rizeIsAnContainer}>
                <p className={styles.rizeIsAn}>
                  Rize is an AI productivity coach that uses time tracking to
                </p>
                <p className={styles.improveYourFocus}>
                  improve your focus and build better work habits.
                </p>
              </div>
            </div>
          </div>
          <div className={styles.frameWrapper1}>
            <form onSubmit={handleSubmit} className={styles.frameParent1}>
              <div className={styles.rectangleParent}>
                <div className={styles.frameChild} />
                <input
                  className={styles.youtubeUrl}
                  placeholder="YOUTUBE url"
                  type="text"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                />
              </div>
              <button type="submit" className={styles.rectangleGroup}>
                <div className={styles.frameItem} />
                <div className={styles.getAudio}>Get audio</div>
              </button>
            </form>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Desktop;