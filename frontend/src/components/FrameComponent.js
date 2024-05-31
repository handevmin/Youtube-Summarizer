import styles from "./FrameComponent.module.css";

const FrameComponent = ({ className = "" }) => {
  return (
    <div className={[styles.frameParent, className].join(" ")}>
      <div className={styles.itHasRootsInAPieceOfClaWrapper}>
        <div className={styles.itHasRoots}>
          It has roots in a piece of classical Latin literatur.
        </div>
      </div>
      <div className={styles.footerNavigationWrapper}>
        <div className={styles.footerNavigation}>
          <div className={styles.wrapperGroup48097385}>
            <img
              className={styles.wrapperGroup48097385Child}
              loading="lazy"
              alt=""
              src="/group-48097385.svg"
            />
          </div>
          <div className={styles.footerNavigationInner}>
            <div className={styles.itHasRootsInAPieceOfClaContainer}>
              <div className={styles.itHasRootsContainer}>
                <p
                  className={styles.itHasRoots1}
                >{`It has roots in a piece of classical Latin literaturIt has `}</p>
                <p className={styles.rootsInA}>
                  roots in a piece of classical Latin literatur. The first line
                </p>
                <p className={styles.ofLoremIpsum}>
                  {" "}
                  of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes
                </p>
                <p className={styles.fromALine}>
                  {" "}
                  from a line in section 1.10.32.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

FrameComponent.propTypes = {
  className: PropTypes.string,
};

export default FrameComponent;
