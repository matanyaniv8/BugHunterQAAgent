export const reportButtonClick = (buttonId, buttonLabel) => {
    if (window.gtag) {
        window.gtag('event', `${buttonLabel} clicked`, {
            event_category: 'Button',
            event_label: buttonLabel,
            value: buttonId,
        });
    }
};
