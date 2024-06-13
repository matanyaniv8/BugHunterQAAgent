import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import styles from '../styles/results.module.css';

export default function Results() {
    const [parsedContent, setParsedContent] = useState('');

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

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Test Results</h1>
            <pre className={styles.results}>{typeof parsedContent === 'string' ? parsedContent : JSON.stringify(parsedContent, null, 2)}</pre>
        </div>
    );
}
