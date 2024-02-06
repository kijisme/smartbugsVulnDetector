import { post } from '../utils/request.ts';

type LoginData = {
  userName: string;
  password: string;
};

export const loginAPI = (data: LoginData) => post('/login', data);