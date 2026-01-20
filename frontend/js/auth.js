const Auth = {
    user: null,

    async init() {
        this.renderUserSection();
        await this.checkAuth();
    },

    async checkAuth() {
        if (API.isLoggedIn()) {
            const res = await API.getMe();
            if (res.success) {
                this.user = res.data;
                this.renderUserSection();
            } else {
                this.logout();
            }
        }
    },

    async login(email, password) {
        const res = await API.login(email, password);
        if (res.success) {
            this.user = res.data.user;
            this.renderUserSection();
            this.closeModal();
            alert(`Xin chào ${this.user.name}!`);

            // Reload to sync history if needed, or just let them play
            window.location.reload();
            return true;
        } else {
            alert('Đăng nhập thất bại: ' + (res.data?.detail || res.error));
            return false;
        }
    },

    async register(name, email, password) {
        const res = await API.register(name, email, password);
        if (res.success) {
            this.user = res.data.user;
            this.renderUserSection();
            this.closeModal();
            alert('Đăng ký thành công!');
            window.location.reload();
            return true;
        } else {
            alert('Đăng ký thất bại: ' + (res.data?.detail || res.error));
            return false;
        }
    },

    logout() {
        API.clearToken();
        this.user = null;
        this.renderUserSection();
        window.location.reload();
    },

    renderUserSection() {
        const container = document.getElementById('user-section');
        if (!container) return;

        if (this.user) {
            container.innerHTML = `
                <div class="flex items-center space-x-3 bg-white py-1 px-3 rounded-xl border border-gray-100 shadow-sm cursor-pointer" onclick="Auth.showProfile()">
                    <div class="flex flex-col text-right hidden sm:flex">
                        <span class="font-bold text-gray-800 text-sm">${this.user.name}</span>
                        <div class="flex items-center justify-end text-xs text-primary-pink font-bold">
                            <i class="fa-solid fa-star text-yellow-500 mr-1"></i> ${this.user.total_stars}
                        </div>
                    </div>
                    <div class="h-9 w-9 rounded-full bg-gradient-to-br from-primary-pink to-primary-orange flex items-center justify-center text-white font-bold text-lg shadow-sm">
                        ${this.user.name.charAt(0).toUpperCase()}
                    </div>
                </div>
            `;
        } else {
            container.innerHTML = `
                <button onclick="Auth.openModal()" class="fun-btn bg-white text-primary-pink border-2 border-primary-pink px-4 py-2 rounded-xl text-sm hover:bg-primary-pink hover:text-white transition-colors shadow-sm font-bold">
                    <i class="fa-solid fa-user mr-2"></i> Đăng nhập
                </button>
            `;
        }
    },

    showProfile() {
        // Simple profile view via alert/confirm for now
        if (confirm(`Tài khoản: ${this.user.email}\nTên: ${this.user.name}\nSao: ${this.user.total_stars}\n\nBạn có muốn đăng xuất?`)) {
            this.logout();
        }
    },

    openModal(mode = 'login') {
        const modal = document.getElementById('auth-modal');
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');
        const modalTitle = document.getElementById('auth-modal-title');

        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');

            if (mode === 'login') {
                loginForm.classList.remove('hidden');
                registerForm.classList.add('hidden');
                modalTitle.textContent = 'Đăng Nhập';
            } else {
                loginForm.classList.add('hidden');
                registerForm.classList.remove('hidden');
                modalTitle.textContent = 'Đăng Ký Tài Khoản';
            }
        }
    },

    closeModal() {
        const modal = document.getElementById('auth-modal');
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    },

    switchMode(mode) {
        this.openModal(mode);
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    Auth.init();
});

// Expose handle functions for forms
function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const pass = document.getElementById('login-password').value;
    Auth.login(email, pass);
}

function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const pass = document.getElementById('reg-password').value;
    Auth.register(name, email, pass);
}
