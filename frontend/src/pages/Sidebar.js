import styles from "./Sidebar.module.css";

const Sidebar = () => {
  return (
    <div className={styles.sidebar}>
      <div className={styles.sidebarChild} />
      <header className={styles.sidebarInner}>
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
      <main className={styles.parent}>
        <img className={styles.icon} alt="" src="/-1.svg" />
        <div className={styles.aiIsAnalyzingParent}>
          <h2 className={styles.aiIsAnalyzing}>AI is analyzing...</h2>
          <div className={styles.instanceWrapper}>
            <img
              className={styles.frameChild}
              loading="lazy"
              alt=""
              src="/group-3.svg"
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Sidebar;
