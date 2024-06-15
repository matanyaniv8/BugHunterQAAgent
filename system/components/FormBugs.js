import React from 'react';
import styles from '../styles/index.module.css';
const FormBugs = ({handleCheckboxChange, toggleSection}) => {
    return (
        <div>
            <h2 className={styles.tabTitle} onClick={() => toggleSection('formSection')}>Form Bugs</h2>
            <div id="formSection" className={styles.section} style={{display: 'none'}}>
                <label className={styles.label}>
                    <input
                        type="checkbox"
                        name="bugs"
                        value="Drop-Down list selection validation"
                        className={styles.inputCheckbox}
                        onChange={handleCheckboxChange}
                    />
                    Drop-Down List Validation Issue
                </label>
                <label className={styles.label}>
                    <input
                        type="checkbox"
                        name="bugs"
                        value="inputs buttons"
                        className={styles.inputCheckbox}
                        onChange={handleCheckboxChange}
                    />
                    Inputs and Buttons
                </label>
                <label className={styles.label}>
                    <input
                        type="checkbox"
                        name="bugs"
                        value="combined"
                        className={styles.inputCheckbox}
                        onChange={handleCheckboxChange}
                    />
                    Combined Form Issues
                </label>
            </div>
        </div>
    );
};

export default FormBugs;










