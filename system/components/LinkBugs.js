import React from 'react';
import styles from '../styles/index.module.css';

const LinkBugs = ({ handleCheckboxChange, toggleSection }) => {
  return (
    <div>
      <h2 className={styles.tabTitle} onClick={() => toggleSection('linksSection')}>Links</h2>
      <div id="linksSection" className={styles.section} style={{ display: 'none' }}>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="broken_link"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          Broken Link
        </label>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="non_visible_link"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          Non-visible Link
        </label>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="no_href_link"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          Link Without Href
        </label>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="incorrect_anchor_link"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          Incorrect Anchor Link
        </label>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="javascript_link"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          JavaScript Link
        </label>
      </div>
    </div>
  );
};

export default LinkBugs;