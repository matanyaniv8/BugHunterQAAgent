// utils/analytics.js
export const reportButtonClick = (buttonId, buttonLabel) => {
    if (window.gtag) {
        window.gtag('event', `Button Click ${buttonLabel}`, {
            event_category: 'Button',
            event_label: buttonLabel,
            value: buttonId,
        });
    }
};