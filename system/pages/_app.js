import '../app/globals.css';
import {useEffect} from 'react';
import {useRouter} from 'next/router';
import Script from 'next/script';

export const GA_TRACKING_ID = ''; // complete your google analytics

const pageview = (url) => {
    if (typeof window.gtag !== 'undefined') {
        window.gtag('config', GA_TRACKING_ID, {
            page_path: url,
        });
    }
};

function MyApp({Component, pageProps}) {
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

    return (
        <>
            <Script async
                    strategy="afterInteractive"
                    src={`https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`}
            />
            <Script id="google-analytics" strategy="afterInteractive">
                {
                    ` window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${GA_TRACKING_ID}');
          `
                }
            </Script>
            <Component {...pageProps} />
        </>
    );
}

export default MyApp;
