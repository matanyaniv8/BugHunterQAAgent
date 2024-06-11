import { useState } from 'react';
import axios from 'axios';
import styles from '../../styles/Index.module.css';

import ButtonBugs from './components/ButtonBugs';
import LinkBugs from './components/LinkBugs';
import ImageBugs from './components/ImageBugs';
import TabBugs from './components/TabBugs';

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
        <ButtonBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
        <TabBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
        <ImageBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
        <LinkBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
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
