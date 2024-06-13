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

        return `${passedTests}/${totalTests}`;
    };

    return (
        <div className={styles.container}>
            <div className={styles.overlay}></div>
            <div className={styles.content}>
                <h1 className={styles.title}>Test Results</h1>
                {typeof parsedContent === 'string' ? (
                    <pre className={styles.results}>{parsedContent}</pre>
                ) : (
                    <>
                        {parsedContent && ['links', 'buttons', 'forms'].map((category) => (
                            <div key={category} className={styles.category}>
                                <h2>{category.charAt(0).toUpperCase() + category.slice(1)}</h2>
                                <h3 className={styles.subtitle}>
                                    {calculatePassedTests(parsedContent[category])} tests passed
                                </h3>
                                <ul className={styles.list}>
                                    {Object.keys(parsedContent[category]).map((item) => (
                                        <li key={item} className={styles.listItem}>
                                            <strong>{item}</strong>
                                            <ul className={styles.list}>
                                                {Object.entries(parsedContent[category][item]).map(([test, result]) => (
                                                    <li key={test} className={styles.listItem}>
                                                        {test}: {typeof result === 'string' ? result : JSON.stringify(result)}
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
