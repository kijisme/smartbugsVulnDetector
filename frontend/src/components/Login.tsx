import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Button, Checkbox, Form, Input } from 'antd';
import React from 'react';

import './Register.css'
import {loginAPI} from '../services/auth.ts'
const Login: React.FC = () => {

  const onFinish = async (values: any) => {
    //发送数据到后端数据库
    const res = await loginAPI(values);
    alert(res)
  };
  return (
    <Form
      name="normal_login"
      id="login-form"
      initialValues={{ remember: true }}
      // validateMessages={validateMessages}
      onFinish={onFinish}
    >
      <Form.Item
        name="username"
        rules={[{ required: true, message: 'Please input your Username!' },
                {type: 'string', min:24 ,max:24, message: 'valid Username!' }]}
      >
      <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Username" />
      </Form.Item>
      <Form.Item
        name="password"
        rules={[{ required: true, message: 'Please input your Password!' }]}
      >
        <Input
          prefix={<LockOutlined className="site-form-item-icon" />}
          type="password"
          placeholder="Password"
        />
      </Form.Item>
      <Form.Item>
        <a className="login-form-forgot" href="">
          Forgot password
        </a>
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit" className="login-form-button">
          Log in
        </Button>
      </Form.Item>
    </Form>
  );
};

export default Login;