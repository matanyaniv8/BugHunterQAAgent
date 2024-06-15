import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import styles from '../styles/results.module.css';

export default function Results() {
    const router = useRouter();
    const [parsedContent, setParsedContent] = useState(null);

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

    const calculatePassedTests = (category, categoryName) => {
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
        return `${passedTests}/${totalTests} tests passed in ${categoryName}`;
    };

    const calculateValidElements = (category, categoryName) => {
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
        return `${validElements}/${totalElements} valid ${categoryName}`;
    };

    const formatResult = (result) => {
        if (typeof result !== 'string') {
            return JSON.stringify(result);
        }
        const parts = result.split('-');
        const formattedParts = parts.map((part, index) => {
            part = part.trim();
            if (part.toLowerCase() === 'passed') {
                return <span key={index} className={styles.passed}>{part.toUpperCase()}</span>;
            } else if (part.toLowerCase() === 'failed') {
                return <span key={index} className={styles.failed}>{part.toUpperCase()}</span>;
            }
            return part;
        });
        return formattedParts.reduce((prev, curr, index) => <>{prev}{index > 0 ? ' - ' : ''}{curr}</>);
    };

    const titleCase = (text) => {
        return text.replace(
            /\w\S*/g,
            (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
        );
    };

    return (
        <div className={styles.container}>
            <div className={styles.overlay}></div>
            <div className={styles.content}>
                <h1 className={styles.title}>Test Results</h1>
                {typeof parsedContent === 'string' ? (
                    <pre className={styles.results}>{formatResult(parsedContent)}</pre>
                ) : (
                    <>
                        {parsedContent && Object.keys(parsedContent).map(categoryName => (
                            <div key={categoryName} className={styles.category}>
                                <h2>{titleCase(categoryName)}</h2>
                                <h3 className={styles.subtitle}>
                                    <span className={styles.summary}>
                                        {calculateValidElements(parsedContent[categoryName], categoryName)}
                                    </span>
                                </h3>
                                <h3 className={styles.subtitle}>
                                    {calculatePassedTests(parsedContent[categoryName], categoryName)}
                                </h3>
                                <ul className={styles.list}>
                                    {Object.keys(parsedContent[categoryName]).map((item) => (
                                        <li key={item} className={styles.listItem}>
                                            <strong>{titleCase(item)}</strong>
                                            <ul className={styles.list}>
                                                {Object.entries(parsedContent[categoryName][item]).map(([test, result]) => (
                                                    <li key={test} className={styles.listItem}>
                                                        {titleCase(test)}: {formatResult(result)}
                                                    </li>
                                                ))}
                                            </ul>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </>
                )}
                <button onClick={handleHomeClick} className={styles.homeButton}>Home</button>
            </div>
        </div>
    );
}
