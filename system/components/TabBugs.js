import React from 'react';
import styles from '../styles/index.module.css';

const TabBugs = ({ handleCheckboxChange, toggleSection }) => {
  return (
    <div>
      <h2 className={styles.tabTitle} onClick={() => toggleSection('tabsSection')}>Tabs</h2>
      <div id="tabsSection" className={styles.section} style={{ display: 'none' }}>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="non_functional_tabs"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          Non-Functional Tabs
        </label>
      </div>
    </div>
  );
};

export default TabBugs;