import { useState } from 'react';
import axios from 'axios';
import styles from '../../styles/Index.module.css';

export default function Home() {
  const [selectedBugs, setSelectedBugs] = useState([]);
  const [generatedUrl, setGeneratedUrl] = useState('');

  const handleCheckboxChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelectedBugs((prev) => [...prev, value]);
    } else {
      setSelectedBugs((prev) => prev.filter((bug) => bug !== value));
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await axios.post('http://127.0.0.1:8000/generate', {
      bugs: selectedBugs,
    });
    setGeneratedUrl(response.data.url);
  };

  const toggleSection = (section) => {
    const content = document.getElementById(section);
    if (content.style.display === "none" || !content.style.display) {
      content.style.display = "block";
    } else {
      content.style.display = "none";
    }
  };

  const expandAll = () => {
    const sections = ['buttonsSection', 'tabsSection', 'imagesSection', 'linksSection', 'doctypeSection'];
    sections.forEach(section => {
      document.getElementById(section).style.display = "block";
    });
  };

  const minimizeAll = () => {
    const sections = ['buttonsSection', 'tabsSection', 'imagesSection', 'linksSection', 'doctypeSection'];
    sections.forEach(section => {
      document.getElementById(section).style.display = "none";
    });
  };

  return (
    <div>
      <h1 className={styles.title}>Select Bugs</h1>
      <div className={styles.centerButtons}>
        <button className={styles.button} onClick={expandAll}>Expand All</button>
        <button className={styles.button} onClick={minimizeAll}>Minimize All</button>
      </div>
      <form onSubmit={handleSubmit} className={styles.form}>
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
          </div>
        </div>

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
          </div>
        </div>

        <div>
          <h2 className={styles.tabTitle} onClick={() => toggleSection('doctypeSection')}>DOCTYPE</h2>
          <div id="doctypeSection" className={styles.section} style={{ display: 'none' }}>
            <label className={styles.label}>
              <input
                type="checkbox"
                name="bugs"
                value="missing_doctype"
                className={styles.inputCheckbox}
                onChange={handleCheckboxChange}
              />
              Missing DOCTYPE
            </label>
          </div>
        </div>

        <button type="submit" className={styles.button}>Generate</button>
      </form>
      {generatedUrl && (
        <div>
          <h2>Generated HTML:</h2>
          <a href={generatedUrl} target="_blank" rel="noopener noreferrer">{generatedUrl}</a>
        </div>
      )}
    </div>
  );
}
