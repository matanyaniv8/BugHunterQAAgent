// utils/analytics.js
export const reportButtonClick = (buttonId, buttonLabel) => {
    if (window.gtag) {
        window.gtag('event', `${buttonLabel} clicked`, {
            event_category: 'Button',
            event_label: buttonLabel,
            value: buttonId,
        });
    }
};
// export const trackEvent = (action, category, label, value) => {
//   if (window.gtag) {
//     window.gtag('event', action, {
//       event_category: category,
//       event_label: label,
//       value: value,
//     });
//   }
// };