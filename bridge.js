window.Telegram = {
    WebApp: {
        initData: "__INIT_DATA__",
        ready: () => { console.log("Aether: WebApp Ready"); },
        expand: () => { console.log("Aether: WebApp Expanded"); }
    }
};

// Авто-разметка DOM для Агента
setInterval(() => {
    document.querySelectorAll('button, a, input, [role="button"]').forEach((el, i) => {
        if (!el.getAttribute('data-agent-id')) {
            el.setAttribute('data-agent-id', 'element_' + i);
        }
    });
}, 500);
