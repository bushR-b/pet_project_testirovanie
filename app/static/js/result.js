function refreshToken() {
    return fetch('/auth/refresh', {
        method: 'POST',
    })
        .then((res) => {
            if (res.status === 200) {
                const tokenData = res.json();
                
                return Promise.resolve();
            }
            return Promise.reject();
        });
}
const hasToken = document.cookie.includes('my_access_token') ||
                    localStorage.getItem('my_access_token');
const hasRefreshToken = document.cookie.includes('my_refresh_token') ||
                    localStorage.getItem('my_refresh_token');

if (!hasToken){
    if (hasRefreshToken){
        refreshToken()
    }
}
