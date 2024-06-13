import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import styles from '../styles/results.module.css';

export default function Results() {
    const router = useRouter();
    const { content } = router.query;
    const [parsedContent, setParsedContent] = useState('');

    useEffect(() => {
        if (content) {
            try {
                setParsedContent(JSON.parse(decodeURIComponent(content)));
            } catch (error) {
                setParsedContent('Failed to parse content');
            }
        }
    }, [content]);

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Test Results</h1>
            <pre className={styles.results}>{typeof parsedContent === 'string' ? parsedContent : JSON.stringify(parsedContent, null, 2)}</pre>
        </div>
    );
}
