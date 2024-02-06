// 服务器地址
export const serverUrl = 'http://localhost:8000';

//token设置
export const setToken = (token: string) => sessionStorage.setItem('Bearer', token);
export const getToken = () => sessionStorage.getItem('Bearer');
