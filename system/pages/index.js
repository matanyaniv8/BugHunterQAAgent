import {useEffect, useState} from 'react';
import axios from 'axios';
import {useRouter} from 'next/router';
import styles from '../styles/index.module.css';
import ButtonBugs from '../components/ButtonBugs';
import LinkBugs from '../components/LinkBugs';
import TabBugs from '../components/TabBugs';
import FormBugs from '../components/FormBugs';

export default function Home() {
    const [selectedBugs, setSelectedBugs] = useState([]);
    const [generatedUrl, setGeneratedUrl] = useState('');
    const [inputUrl, setInputUrl] = useState('');
    const [loading, setLoading] = useState(false); // Loading state
    const router = useRouter();

    useEffect(() => {
        const handleRouteChange = (url) => {
            pageview(url);
        };
        router.events.on('routeChangeComplete', handleRouteChange);
        return () => {
            router.events.off('routeChangeComplete', handleRouteChange);
        };
    }, [router.events]);

    const handleCheckboxChange = (event) => {
        const {value, checked} = event.target;
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
        try {
            if (inputUrl) {
                setGeneratedUrl(inputUrl);
            } else {
                const response = await axios.post('http://127.0.0.1:8000/generate', {
                    bugs: selectedBugs,
                });
                if (response.data.url) {
                    setGeneratedUrl(response.data.url);
                } else {
                    alert('Failed to generate HTML. No URL returned.');
                }
            }
        } catch (error) {
            console.error('Failed to generate HTML:', error);
            alert('Failed to generate HTML. Please check the server and try again.');
        }
    };

    const openResultsPage = (content) => {
        sessionStorage.setItem('testResults', JSON.stringify(content));
        router.push('/results');
    };

    const handleTestHTML = async () => {
        const htmlFilePath = 'generated_html/buggy_website.html'; // Use the dynamically set file path
        if (htmlFilePath) {
            try {
                setLoading(true); // Set loading state
                const response = await axios.post('http://127.0.0.1:8000/test_html', {
                    file_path: htmlFilePath,
                });
                setLoading(false); // Reset loading state
                if (response.data.error) {
                    openResultsPage({error: response.data.error});
                } else {
                    openResultsPage(response.data); // Display the test results
                }
            } catch (error) {
                setLoading(false); // Reset loading state
                console.error('Failed to fetch results:', error);
                openResultsPage({error: error.response ? error.response.data.detail : ''});
            }
        } else {
            alert('No HTML file generated yet.');
        }
    };

    const handleTestURL = async () => {
        if (inputUrl) {
            try {
                setLoading(true); // Set loading state
                const response = await axios.post('http://127.0.0.1:8000/test_url', {
                    url: inputUrl, // This key needs to match your FastAPI model
                });
                setLoading(false); // Reset loading state
                if (response.data.error) {
                    openResultsPage({error: response.data.error});
                } else {
                    openResultsPage(response.data.results); // Display the test results
                }
            } catch (error) {
                setLoading(false); // Reset loading state
                console.error('Failed to fetch results:', error);
                openResultsPage({error: error.response ? error.response.data.detail : ''});
            }
        } else {
            alert('Please enter a URL.');
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
        const sections = ['buttonsSection', 'tabsSection', 'linksSection', 'doctypeSection'];
        sections.forEach((section) => {
            const element = document.getElementById(section);
            if (element) {
                element.style.display = 'block';
            }
        });
    };

    const minimizeAll = () => {
        const sections = ['buttonsSection', 'tabsSection', 'linksSection', 'doctypeSection'];
        sections.forEach((section) => {
            const element = document.getElementById(section);
            if (element) {
                element.style.display = 'none';
            }
        });
    };

    return (
        <div>
            {loading ? (
                <div className={styles.loadingContainer}>
                    <img src="/loading.gif" alt="Loading..." className={styles.loadingGif}/>
                </div>
            ) : (
                <>
                    <h1 className={styles.title}>Bug Hunter</h1>
                    <p className={styles.subtitle}>Your Ultimate Bug Detection Tool</p>
                    <form onSubmit={handleSubmit} className={styles.form}>
                        <div className={styles.inputGroup}>
                            <label htmlFor="urlInput" className={styles.inputLabel}>Enter URL (optional):</label>
                            <input
                                type="text"
                                id="urlInput"
                                value={inputUrl}
                                onChange={handleInputChange}
                                placeholder="Enter URL if you want to use an existing webpage"
                                className={styles.input}
                            />
                        </div>
                        <div id="menuButtons" className={styles.menuButtons}>
                            <button className={styles.button} type="button" onClick={expandAll}>Expand All</button>
                            <button className={styles.button} type="button" onClick={minimizeAll}>Minimize All</button>
                        </div>
                        <ButtonBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection}/>
                        <TabBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection}/>
                        <LinkBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection}/>
                        <FormBugs handleCheckboxChange={handleCheckboxChange} toggleSection={toggleSection}/>
                        <button type="submit" className={styles.button}>Generate HTML</button>
                    </form>
                    {generatedUrl && (
                        <div className={styles.generatedHTML}>
                            <a href={generatedUrl} id="generatedUrl" target="_blank"
                               rel="noopener noreferrer">{generatedUrl}</a>
                        </div>
                    )}
                    <div id="testButtons" className={styles.testButtons}>
                        <button className={styles.button} type="button" onClick={handleTestHTML}>Test HTML</button>
                        <button className={styles.button} type="button" onClick={handleTestURL}>Test URL</button>
                    </div>
                </>
            )}
        </div>
    );
}
