import { useState } from 'react';
import axios from 'axios';
import styles from '../styles/index.module.css';

import ButtonBugs from '../components/ButtonBugs';
import LinkBugs from '../components/LinkBugs';
import ImageBugs from '../components/ImageBugs';
import TabBugs from '../components/TabBugs';
import FormBugs from '../components/FormBugs';

export default function Home() {
  const [selectedBugs, setSelectedBugs] = useState([]);
  const [generatedUrl, setGeneratedUrl] = useState('');
  const [inputUrl, setInputUrl] = useState('');

  const handleCheckboxChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelectedBugs((prev) => [...prev, value]);
    } else {
      setSelectedBugs((prev) => prev.filter((bug) => bug !== value));
    }
  };

  const handleInputChange = (event) => {
    setInputUrl(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (inputUrl) {
      setGeneratedUrl(inputUrl);
    } else {
      const response = await axios.post('http://127.0.0.1:8000/generate', {
        bugs: selectedBugs,
      });
      setGeneratedUrl(response.data.url);
    }
  };

  const toggleSection = (section) => {
    const content = document.getElementById(section);
    if (content.style.display === 'none' || !content.style.display) {
      content.style.display = 'block';
    } else {
      content.style.display = 'none';
    }
  };

    const expandAll = () => {
    const sections = ['buttonsSection', 'tabsSection', 'imagesSection', 'linksSection', 'doctypeSection'];
    sections.forEach((section) => {
      const element = document.getElementById(section);
      if (element) {
        element.style.display = 'block';
      }
    });
  };

  const minimizeAll = () => {
    const sections = ['buttonsSection', 'tabsSection', 'imagesSection', 'linksSection', 'doctypeSection'];
    sections.forEach((section) => {
      const element = document.getElementById(section);
      if (element) {
        element.style.display = 'none';
      }
    });
  };


  return (
    <div>
      <h1 className={styles.title}>Select Bugs or Enter URL</h1>
      <div className={styles.centerButtons}>
        <button className={styles.button} onClick={expandAll}>Expand All</button>
        <button className={styles.button} onClick={minimizeAll}>Minimize All</button>
      </div>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.inputGroup}>
          <label htmlFor="urlInput">Enter URL (optional):</label>
          <input
            type="text"
            id="urlInput"
            value={inputUrl}
            onChange={handleInputChange}
            placeholder="Enter URL if you want to use an existing webpage"
            className={styles.input}
          />
        </div>
        <ButtonBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
        <TabBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
        <ImageBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
        <LinkBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
        <FormBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection} />
        <button type="submit" className={styles.button}>Generate or Use URL</button>
      </form>
      {generatedUrl && (
        <div>
          <h2>Generated HTML or Entered URL:</h2>
          <a href={generatedUrl} target="_blank" rel="noopener noreferrer">{generatedUrl}</a>
        </div>
      )}
    </div>
  );
}
