import { useState } from 'react';
import axios from 'axios';
import '../public/styles.css';

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
      <h1>Select Bugs</h1>
      <div className="center-buttons">
        <button onClick={expandAll}>Expand All</button>
        <button onClick={minimizeAll}>Minimize All</button>
      </div>
      <form onSubmit={handleSubmit}>
        <div>
          <h2 className="tab-title" onClick={() => toggleSection('buttonsSection')}>Buttons</h2>
          <div id="buttonsSection" style={{ display: 'none' }}>
            <label>
              <input
                type="checkbox"
                name="bugs"
                value="submit_button_no_action"
                onChange={handleCheckboxChange}
              />
              Submit Button Does Nothing
            </label>
          </div>
        </div>

        <div>
          <h2 className="tab-title" onClick={() => toggleSection('tabsSection')}>Tabs</h2>
          <div id="tabsSection" style={{ display: 'none' }}>
            <label>
              <input
                type="checkbox"
                name="bugs"
                value="non_functional_tabs"
                onChange={handleCheckboxChange}
              />
              Non-Functional Tabs
            </label>
          </div>
        </div>

        <div>
          <h2 className="tab-title" onClick={() => toggleSection('imagesSection')}>Images</h2>
          <div id="imagesSection" style={{ display: 'none' }}>
            <label>
              <input
                type="checkbox"
                name="bugs"
                value="missing_alt"
                onChange={handleCheckboxChange}
              />
              Missing Alt Attribute
            </label>
          </div>
        </div>

        <div>
          <h2 className="tab-title" onClick={() => toggleSection('linksSection')}>Links</h2>
          <div id="linksSection" style={{ display: 'none' }}>
            <label>
              <input
                type="checkbox"
                name="bugs"
                value="broken_link"
                onChange={handleCheckboxChange}
              />
              Broken Link
            </label>
          </div>
        </div>

        <div>
          <h2 className="tab-title" onClick={() => toggleSection('doctypeSection')}>DOCTYPE</h2>
          <div id="doctypeSection" style={{ display: 'none' }}>
            <label>
              <input
                type="checkbox"
                name="bugs"
                value="missing_doctype"
                onChange={handleCheckboxChange}
              />
              Missing DOCTYPE
            </label>
          </div>
        </div>

        <button type="submit">Generate</button>
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
