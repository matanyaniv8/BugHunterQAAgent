import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import styles from '../styles/results.module.css';

export default function Results() {
    const router = useRouter();
    const [parsedContent, setParsedContent] = useState(null);
    const [selectedFamily, setSelectedFamily] = useState(null);
    const [selectedTest, setSelectedTest] = useState(null);
    const [description, setDescription] = useState('');

    useEffect(() => {
        const content = sessionStorage.getItem('testResults');
        if (content) {
            try {
                setParsedContent(JSON.parse(content));
            } catch (error) {
                setParsedContent('Failed to parse content');
            }
        }
    }, []);

    const handleHomeClick = () => {
        router.push('/');
    };

    const calculatePassedTests = (category) => {
        let totalTests = 0;
        let passedTests = 0;
        Object.values(category).forEach(test => {
            Object.values(test).forEach(result => {
                totalTests++;
                if (typeof result === 'string' && result.toLowerCase().includes('passed')) {
                    passedTests++;
                }
            });
        });
        return `${passedTests}/${totalTests} tests passed`;
    };

    const calculateValidElements = (category) => {
        let totalElements = 0;
        let validElements = 0;
        Object.values(category).forEach(tests => {
            totalElements++;
            let allPassed = true;
            Object.values(tests).forEach(result => {
                if (typeof result === 'string' && !result.toLowerCase().includes('passed')) {
                    allPassed = false;
                }
            });
            if (allPassed) {
                validElements++;
            }
        });
        return `${validElements}/${totalElements} valid elements`;
    };

    const formatResult = (result, showDetails = false) => {
        if (typeof result !== 'string') {
            return { main: JSON.stringify(result), description: '' };
        }
        const parts = result.split('-');
        const mainResult = parts[0].trim();
        const description = parts.slice(1).join('-').trim();

        const formattedMainResult = mainResult.toLowerCase() === 'passed'
            ? <span className={styles.passed}>{mainResult.toUpperCase()}</span>
            : <span className={styles.failed}>{mainResult.toUpperCase()}</span>;

        return {
            main: formattedMainResult,
            description: showDetails ? description : ''
        };
    };

    const titleCase = (text) => {
        return text.replace(
            /\w\S*/g,
            (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
        );
    };

    const handleFamilyClick = (family) => {
        setSelectedFamily(family);
        setSelectedTest(null);
    };

    const handleTestClick = (categoryName, item, test) => {
        const result = parsedContent[categoryName][item][test];
        const formattedResult = formatResult(result, true);
        setSelectedTest({
            category: categoryName,
            item,
            test,
            result: formattedResult.main
        });
        setDescription(formattedResult.description);
    };

    const handleSuggestFix = () => {
        // Implement suggestion fix logic here
        alert('Suggest Fix button clicked for ' + selectedTest.test);
    };

    const handleMinimizeClick = () => {
        setSelectedFamily(null);
    };

    return (
        <div className={styles.container}>
            <div className={styles.overlay}></div>
            <div className={styles.content}>
                <h1 className={styles.title}>Test Results</h1>
                {typeof parsedContent === 'string' ? (
                    <pre className={styles.results}>{formatResult(parsedContent).main}</pre>
                ) : (
                    <div className={styles.familyContainer}>
                        {['links', 'buttons', 'forms'].map(family => (
                            <div key={family} className={styles.familySquare} onClick={() => handleFamilyClick(family)}>
                                <h2>{titleCase(family)}</h2>
                                {parsedContent && parsedContent[family] && (
                                    <>
                                        <p>{calculateValidElements(parsedContent[family])}</p>
                                        <p>{calculatePassedTests(parsedContent[family])}</p>
                                    </>
                                )}
                            </div>
                        ))}
                    </div>
                )}
                {selectedFamily && parsedContent && parsedContent[selectedFamily] && (
                    <div className={styles.details}>
                        <button onClick={handleMinimizeClick} className={styles.minimizeButton}>Minimize</button>
                        <h2>{titleCase(selectedFamily)}</h2>
                        <ul className={styles.list}>
                            {Object.keys(parsedContent[selectedFamily]).map((item) => (
                                <li key={item} className={styles.listItem}>
                                    <strong>{titleCase(item)}</strong>
                                    <ul className={styles.list}>
                                        {Object.entries(parsedContent[selectedFamily][item]).map(([test, result]) => (
                                            <li key={test} className={styles.listItem} onClick={() => handleTestClick(selectedFamily, item, test)}>
                                                {titleCase(test)}: {formatResult(result, false).main}
                                            </li>
                                        ))}
                                    </ul>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
                <button onClick={handleHomeClick} className={styles.homeButton}>Home</button>

                {selectedTest && (
                    <div className={styles.testDetails}>
                        <h2>Test Details</h2>
                        <p><strong>Category:</strong> {selectedTest.category}</p>
                        <p><strong>Item:</strong> {selectedTest.item}</p>
                        <p><strong>Test:</strong> {selectedTest.test}</p>
                        <p><strong>Result:</strong> {selectedTest.result}</p>
                        {description && (
                            <p><strong>Description:</strong> {description}</p>
                        )}
                        {typeof selectedTest.result === 'string' && selectedTest.result.toLowerCase().includes('failed') && (
                            <button onClick={handleSuggestFix} className={styles.suggestFixButton}>Suggest Fix</button>
                        )}
                        <button onClick={() => setSelectedTest(null)} className={styles.closeButton}>Close</button>
                    </div>
                )}
            </div>
        </div>
    );
}
