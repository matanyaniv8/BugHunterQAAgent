import React from 'react';
import styles from '../../../styles/Index.module.css';

const ButtonBugs = ({ handleCheckboxChange, toggleSection }) => {
  return (
    <div>
      <h2 className={styles.tabTitle} onClick={() => toggleSection('buttonsSection')}>Buttons</h2>
      <div id="buttonsSection" className={styles.section} style={{ display: 'none' }}>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="submit_button_no_action"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          Submit Button Does Nothing
        </label>
        <label className={styles.label}>
          <input
            type="checkbox"
            name="bugs"
            value="empty_button"
            className={styles.inputCheckbox}
            onChange={handleCheckboxChange}
          />
          Empty Button
        </label>
      </div>
    </div>
  );
};

export default ButtonBugs;
