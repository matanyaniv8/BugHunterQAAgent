import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import styles from '../styles/results.module.css';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const tooltipTexts = {
    'W3C Validation Report': 'Validates adherence to W3C web standards, ensuring your site is accessible and works well across different browsers and devices.',
    'links': 'Checks links for reachability (status 200), valid format (http, https, mailto, or internal), responsiveness, and absence of 404 errors.',
    'buttons': 'Tests buttons for visibility, interactivity, and click functionality, ensuring they perform expected actions.',
    'forms': 'Evaluates input fields for valid data entry, correct input types, and successful form submission.'
};

export default function Results() {
    const router = useRouter();
    const [parsedContent, setParsedContent] = useState(null);
    const [selectedFamily, setSelectedFamily] = useState(null);
    const [selectedTest, setSelectedTest] = useState(null);
    const [description, setDescription] = useState('');
    const [sortOption, setSortOption] = useState('all');
    const [suggestion, setSuggestion] = useState('');
    const [loadingSuggestion, setLoadingSuggestion] = useState(false);
    const [codeSnippetVisible, setCodeSnippetVisible] = useState(false); // Add this state

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

    const handleSortChange = (e) => {
        setSortOption(e.target.value);
    };

    const filterResults = (results) => {
        if (sortOption === 'passed') {
            return Object.keys(results).reduce((filtered, item) => {
                const tests = results[item];
                const allPassed = Object.entries(tests).every(([key, result]) =>
                    key === 'code_snippet' || result.toLowerCase().includes('passed')
                );
                if (allPassed) {
                    filtered[item] = tests;
                }
                return filtered;
            }, {});
        } else if (sortOption === 'failed') {
            return Object.keys(results).reduce((filtered, item) => {
                const tests = results[item];
                const anyFailed = Object.entries(tests).some(([key, result]) => key !== 'code_snippet' && result.toLowerCase().includes('failed'));
                if (anyFailed) {
                    filtered[item] = tests;
                }
                return filtered;
            }, {});
        }
        return results;
    };

    const calculatePassedTests = (category) => {
        let totalTests = 0;
        let passedTests = 0;
        Object.values(category).forEach(test => {
            Object.entries(test).forEach(([key, result]) => {
                if (typeof result === 'string' && key !== 'code_snippet') {
                    totalTests++;
                    if (result.toLowerCase().includes('passed')) {
                        passedTests++;
                    }
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
            Object.entries(tests).forEach(([key, result]) => {
                if (typeof result === 'string' && key !== 'code_snippet' && !result.toLowerCase().includes('passed')) {
                    allPassed = false;
                }
            });
            if (allPassed) {
                validElements++;
            }
        });
        return `${validElements}/${totalElements} valid elements`;
    };

    const calculateScore = (category) => {
        let totalTests = 0;
        let passedTests = 0;
        Object.values(category).forEach(test => {
            Object.entries(test).forEach(([key, result]) => {
                if (typeof result === 'string' && key !== 'code_snippet') {
                    totalTests++;
                    if (result.toLowerCase().includes('passed')) {
                        passedTests++;
                    }
                }
            });
        });
        return Math.round((passedTests / totalTests) * 100);
    };

    const getColor = (score) => {
        if (score < 30) {
            return 'red';
        } else if (score < 60) {
            return 'orange';
        } else if (score < 80) {
            return 'yellow';
        } else if (score < 90) {
            return 'lightgreen';
        } else {
            return 'green';
        }
    };

    const renderScore = (category) => {
        const score = calculateScore(category);
        return (
            <div className={styles.scoreContainer}>
                <CircularProgressbar
                    value={score}
                    text={`${score}%`}
                    styles={buildStyles({
                        textColor: getColor(score),
                        pathColor: getColor(score),
                    })}
                />
            </div>
        );
    };

    const formatResult = (result, showDetails = false) => {
        if (typeof result !== 'string') {
            return {main: JSON.stringify(result), description: ''};
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
        const testData = parsedContent[categoryName][item][test];
        const formattedResult = formatResult(testData, true);
        setSelectedTest({
            category: categoryName,
            item,
            test,
            result: formattedResult.main,
            description: formattedResult.description,
            codeSnippet: parsedContent[categoryName][item]['code_snippet']
        });
        setDescription(formattedResult.description);
        setSuggestion('');
        setCodeSnippetVisible(false);
    };

    const handleSuggestFix = async () => {
        setLoadingSuggestion(true);
        setSuggestion('Generating fix...');

        const testData = {
            category: selectedTest.category,
            description : selectedTest.description,
            item: selectedTest.item,
            test: selectedTest.test,
            code_snippet: selectedTest.codeSnippet
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/suggest_fix', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(testData)
            });

            const data = await response.json();
            setLoadingSuggestion(false);

            if (data.suggestion) {
                // Remove the "Suggested Fix:" label from the suggestion
                const formattedSuggestion = data.suggestion.replace(/^Suggested Fix:\s*/i, '');
                setSuggestion(formattedSuggestion);
            } else {
                setSuggestion('No specific fix suggestion available.');
            }
        } catch (error) {
            setLoadingSuggestion(false);
            setSuggestion('Error generating fix suggestion');
            console.error('Error during suggestion generation:', error);
        }
    };

    const handleMinimizeClick = () => {
        setSelectedFamily(null);
    };

    return (
        <div className={styles.container}>
            <div className={styles.overlay}></div>
            <div className={styles.content}>
                <h1 className={styles.title}>Test Results</h1>
                <div className={styles.sortContainer}>
                    <label htmlFor="sortOptions">Sort by: </label>
                    <select id="sortOptions" onChange={handleSortChange} value={sortOption}>
                        <option value="all">All</option>
                        <option value="passed">Passed</option>
                        <option value="failed">Failed</option>
                    </select>
                </div>
                {typeof parsedContent === 'string' ? (
                    <pre className={styles.results}>{formatResult(parsedContent).main}</pre>
                ) : (
                    <div className={styles.familyContainer}>
                        {['links', 'buttons', 'forms', 'W3C Validation Report'].map(family => (
                            <div key={family} className={styles.familySquare} onClick={() => handleFamilyClick(family)}>
                                {parsedContent && parsedContent[family] && renderScore(parsedContent[family])}
                                <div className={styles.titleContainer}>
                                    <h2>{titleCase(family)}</h2>
                                    <div className={styles.tooltip}>
                                        <img src="/info.jpg" alt="Info" className={styles.infoImage} />
                                        <span className={styles.tooltipText}>{tooltipTexts[family]}</span>
                                    </div>
                                </div>
                                {parsedContent && parsedContent[family] && (
                                    <>
                                        <p className={styles.subtitle}>{calculateValidElements(parsedContent[family])}</p>
                                        <p className={styles.subtitle}>{calculatePassedTests(parsedContent[family])}</p>
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
                            {Object.keys(filterResults(parsedContent[selectedFamily])).map((item) => (
                                <li key={item} className={styles.listItem}>
                                    <strong>{titleCase(item)}</strong>
                                    <ul className={styles.list}>
                                        {Object.entries(parsedContent[selectedFamily][item]).map(([test, result]) => (
                                            test !== 'code_snippet' && (
                                                <li key={test} className={styles.listItem}
                                                    onClick={() => handleTestClick(selectedFamily, item, test)}>
                                                    {titleCase(test)}: {formatResult(result, false).main}
                                                </li>
                                            )
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
                        {selectedTest.codeSnippet && (
                            <div className={styles.codeSnippetContainer}>
                                <div className={styles.codeSnippetTitle} onClick={() => setCodeSnippetVisible(!codeSnippetVisible)}>
                                    Code Snippet &gt;
                                </div>
                                {codeSnippetVisible && (
                                    <pre className={styles.codeSnippet}>
                                        <div>{selectedTest.codeSnippet}</div>
                                    </pre>
                                )}
                            </div>
                        )}
                        {(suggestion || loadingSuggestion) && (
                            <p className={styles.suggestion} style={{backgroundColor: 'lightblue'}}>
                                <strong>Fix Suggestion:</strong><br/>
                                <span
                                    dangerouslySetInnerHTML={{__html: suggestion.trim().replace(/\n/g, '<br />')}}/>
                            </p>
                        )}
                        {selectedTest.result.props.children === 'FAILED' && !loadingSuggestion && (
                            <button onClick={handleSuggestFix} className={styles.suggestFixButton}>Suggest Fix</button>
                        )}
                        <button onClick={() => setSelectedTest(null)} className={styles.closeButton}>Close</button>
                    </div>
                )}
            </div>
        </div>
    );
}
