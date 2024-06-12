import React from 'react';
import styles from '../styles/index.module.css';

const ImageBugs = ({ handleCheckboxChange, toggleSection }) => {
  return (
    <div>
      <h2 className={styles.tabTitle} onClick={() => toggleSection('imagesSection')}>Images</h2>
      <div id="imagesSection" className={styles.section} style={{ display: 'none' }}>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="missing_alt"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          Missing Alt Attribute
        </label>
      </div>
    </div>
  );
};

export default ImageBugs;