import { Layout, Menu } from 'antd';
import React, {useState} from 'react';
import type { MenuProps } from 'antd';

import Register from './Register.tsx'
import Login from './Login.tsx'

import './Motal.css'
const { Header, Content} = Layout;

const Motal: React.FC = () => {

    const items: MenuProps['items'] = [
            {label: 'register',key: 'register'},
            {label: 'login',key: 'login'}
        ]
    const [current, setCurrent] = useState('register');

    const onClick: MenuProps['onClick'] = e => {
        setCurrent(e.key);
    };
    return (
        <Layout id='Motal' style={{width:'100%', height:'100%', backgroundColor:'transparent'}}>
            <Header style={{backgroundColor:'transparent'}}>
                <Menu theme='light' onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />
            </Header>
            <Content>
                {current == 'register' && 
                <div id='register'>
                    <Register/>
                </div>}
                {current == 'login' && 
                <div id='login'>
                    <Login/>
                </div>}
            </Content>
        </Layout>
    );
};

export default Motal;