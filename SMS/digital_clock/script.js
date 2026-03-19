/**
 * Digital Clock - Multi-timezone support
 * Features: Real-time clock, multiple timezones, 12/24 hour toggle
 */

let timezones = ['Asia/Bangkok', 'UTC'];
let is24Hour = true;

// Default timezones to show on load
const DEFAULT_TIMEZONES = ['Asia/Bangkok', 'UTC'];

function updateClock() {
    const clockDiv = document.getElementById('clock');
    if (!clockDiv) return;

    const utcDate = new Date();
    let html = '';

    if (timezones.length === 0) {
        html = '<div class="timezone" style="color:#888;">No timezones added. Add one below!</div>';
    } else {
        timezones.forEach(tz => {
            try {
                const options = {
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: !is24Hour,
                    timeZone: tz
                };
                const timeStr = utcDate.toLocaleTimeString('en-US', options);
                const dateStr = utcDate.toLocaleDateString('en-US', {
                    weekday: 'short',
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    timeZone: tz
                });
                html += `
                    <div class="timezone">
                        <strong>${tz}</strong>
                        <div style="font-size:2em;font-family:monospace;">${timeStr}</div>
                        <div style="font-size:0.9em;color:#666;">${dateStr}</div>
                    </div>
                `;
            } catch (e) {
                html += `<div class="timezone"><strong>${tz}</strong>: Invalid timezone</div>`;
            }
        });
    }

    clockDiv.innerHTML = html;
}

function addTimezone() {
    const input = document.getElementById('timezone_input');
    if (!input) return;

    const timezone = input.value.trim();
    if (!timezone) {
        alert('Please enter a timezone (e.g., Asia/Bangkok, US/Eastern, Europe/London)');
        return;
    }

    if (timezones.includes(timezone)) {
        alert('Timezone already added!');
        return;
    }

    // Validate timezone
    try {
        new Date().toLocaleString('en-US', { timeZone: timezone });
        timezones.push(timezone);
        input.value = '';
        updateClock();
        renderTimezoneList();
    } catch (e) {
        alert('Invalid timezone: ' + timezone + '\nTry: Asia/Bangkok, US/Eastern, Europe/London, etc.');
    }
}

function removeTimezone(tz) {
    timezones = timezones.filter(t => t !== tz);
    updateClock();
    renderTimezoneList();
}

function toggleFormat() {
    is24Hour = !is24Hour;
    const btn = document.getElementById('toggle_format');
    if (btn) {
        btn.textContent = is24Hour ? 'Switch to 12-Hour' : 'Switch to 24-Hour';
    }
    updateClock();
}

function renderTimezoneList() {
    const tzDiv = document.getElementById('timezones');
    if (!tzDiv) return;

    if (timezones.length === 0) {
        tzDiv.innerHTML = '<p style="color:#888;">No timezones added.</p>';
        return;
    }

    tzDiv.innerHTML = '<strong>Active Timezones:</strong><br>' +
        timezones.map(tz =>
            `<span style="display:inline-block;margin:5px;padding:5px 12px;background:#e8f4fd;border-radius:15px;font-size:0.9em;">
                ${tz}
                <button onclick="removeTimezone('${tz}')" style="background:none;border:none;color:#e74c3c;cursor:pointer;font-weight:bold;margin-left:5px;">&times;</button>
            </span>`
        ).join('');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add_timezone');
    const removeBtn = document.getElementById('remove_timezone');
    const toggleBtn = document.getElementById('toggle_format');
    const input = document.getElementById('timezone_input');

    if (addBtn) addBtn.onclick = addTimezone;
    if (removeBtn) removeBtn.onclick = () => {
        const tz = input ? input.value.trim() : '';
        if (tz) removeTimezone(tz);
        if (input) input.value = '';
    };
    if (toggleBtn) toggleBtn.onclick = toggleFormat;

    // Enter key support
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') addTimezone();
        });
    }

    // Initialize with defaults
    timezones = [...DEFAULT_TIMEZONES];
    updateClock();
    renderTimezoneList();

    // Update every second
    setInterval(updateClock, 1000);
});
