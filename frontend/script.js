/**
 * SMS Dashboard - Frontend JavaScript
 * จัดการการส่ง SMS, ดูประวัติ, และสถิติ
 */

const API_BASE = window.location.origin + '/api';

// ===== DOM Elements =====
const smsForm = document.getElementById('smsForm');
const recipientInput = document.getElementById('recipient');
const messageInput = document.getElementById('message');
const totalSmsEl = document.getElementById('total-sms');
const lastSentEl = document.getElementById('last-sent');
const smsTableBody = document.querySelector('.sent-sms-list tbody');
const historySection = document.querySelector('.history-section');

// ===== Notification System =====
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background:none;border:none;color:inherit;font-size:18px;cursor:pointer;margin-left:10px;">&times;</button>
    `;
    document.body.prepend(notification);

    setTimeout(() => {
        if (notification.parentElement) notification.remove();
    }, 5000);
}

// ===== Send SMS =====
async function sendSMS(event) {
    event.preventDefault();

    const recipient = recipientInput.value.trim();
    const message = messageInput.value.trim();

    if (!recipient || !message) {
        showNotification('Please fill in all fields', 'error');
        return;
    }

    const submitBtn = smsForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/sms/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipient, message })
        });

        const data = await response.json();

        if (data.success) {
            showNotification('SMS sent successfully!', 'success');
            smsForm.reset();
            loadHistory();
            loadStats();
        } else {
            showNotification(data.message || 'Failed to send SMS', 'error');
        }
    } catch (error) {
        showNotification('Network error. Please try again.', 'error');
        console.error('Send SMS error:', error);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

// ===== Load SMS History =====
async function loadHistory(page = 1) {
    try {
        const response = await fetch(`${API_BASE}/sms/history?page=${page}&per_page=10`);
        const data = await response.json();

        if (data.success) {
            renderSMSTable(data.data);
            renderPagination(data.pagination);
        }
    } catch (error) {
        console.error('Load history error:', error);
        renderSMSTable([]);
    }
}

// ===== Render SMS Table =====
function renderSMSTable(smsList) {
    if (!smsTableBody) return;

    if (smsList.length === 0) {
        smsTableBody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align:center;color:#888;padding:20px;">
                    No SMS messages yet. Send your first SMS!
                </td>
            </tr>
        `;
        return;
    }

    smsTableBody.innerHTML = smsList.map(sms => `
        <tr>
            <td>${escapeHtml(sms.recipient)}</td>
            <td>${escapeHtml(sms.message.length > 50 ? sms.message.substring(0, 50) + '...' : sms.message)}</td>
            <td><span class="status-badge status-${sms.status}">${sms.status}</span></td>
            <td>${formatDate(sms.created_at)}</td>
            <td>
                <button class="btn-delete" onclick="deleteSMS(${sms.id})" title="Delete">
                    &#128465;
                </button>
            </td>
        </tr>
    `).join('');
}

// ===== Render Pagination =====
function renderPagination(pagination) {
    if (!historySection) return;

    let paginationEl = historySection.querySelector('.pagination');
    if (!paginationEl) {
        paginationEl = document.createElement('div');
        paginationEl.className = 'pagination';
        historySection.appendChild(paginationEl);
    }

    if (pagination.pages <= 1) {
        paginationEl.innerHTML = '';
        return;
    }

    let html = '';
    if (pagination.has_prev) {
        html += `<button onclick="loadHistory(${pagination.page - 1})">&laquo; Prev</button>`;
    }
    html += `<span class="page-info">Page ${pagination.page} of ${pagination.pages} (${pagination.total} total)</span>`;
    if (pagination.has_next) {
        html += `<button onclick="loadHistory(${pagination.page + 1})">Next &raquo;</button>`;
    }
    paginationEl.innerHTML = html;
}

// ===== Load Statistics =====
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/sms/stats`);
        const data = await response.json();

        if (data.success) {
            const stats = data.data;
            if (totalSmsEl) totalSmsEl.textContent = stats.total || 0;
            if (lastSentEl) {
                lastSentEl.textContent = stats.last_sms
                    ? `To ${stats.last_sms.recipient} at ${formatDate(stats.last_sms.created_at)}`
                    : 'N/A';
            }

            // Update statistics panel if exists
            renderStatsPanel(stats);
        }
    } catch (error) {
        console.error('Load stats error:', error);
    }
}

// ===== Render Stats Panel =====
function renderStatsPanel(stats) {
    const statsPanel = document.querySelector('.statistics-panel');
    if (!statsPanel) return;

    statsPanel.innerHTML = `
        <h2>Statistics</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">${stats.total}</div>
                <div class="stat-label">Total SMS</div>
            </div>
            <div class="stat-card stat-success">
                <div class="stat-number">${stats.sent}</div>
                <div class="stat-label">Sent</div>
            </div>
            <div class="stat-card stat-danger">
                <div class="stat-number">${stats.failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card stat-warning">
                <div class="stat-number">${stats.pending}</div>
                <div class="stat-label">Pending</div>
            </div>
        </div>
        <p style="margin-top:10px;">Last Sent: <strong>${
            stats.last_sms
                ? `To ${stats.last_sms.recipient} at ${formatDate(stats.last_sms.created_at)}`
                : 'N/A'
        }</strong></p>
    `;
}

// ===== Delete SMS =====
async function deleteSMS(id) {
    if (!confirm('Are you sure you want to delete this SMS?')) return;

    try {
        const response = await fetch(`${API_BASE}/sms/${id}`, {
            method: 'DELETE'
        });
        const data = await response.json();

        if (data.success) {
            showNotification('SMS deleted successfully', 'success');
            loadHistory();
            loadStats();
        } else {
            showNotification('Failed to delete SMS', 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
        console.error('Delete SMS error:', error);
    }
}

// ===== Utility Functions =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleString('th-TH', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    // Attach form submit handler
    if (smsForm) {
        smsForm.addEventListener('submit', sendSMS);
    }

    // Load initial data
    loadHistory();
    loadStats();

    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadHistory();
        loadStats();
    }, 30000);
});
