import { Layout, Button } from 'antd';
import React, {useState} from 'react';
import Motal from '../components/Motal.tsx'
import './Welcome.css'
const { Header, Footer, Sider, Content } = Layout;

const Welcome: React.FC = () => {

    const [isDivVisible, setDivVisible] = useState(false);
    const handleButtonClick = () => {
        setDivVisible(!isDivVisible);
      };

    return(
        <Layout id='Welcome'>
            <Header>
                <Button type="primary" onClick={handleButtonClick}>注册/登录</Button>
            </Header>
            <Content>Content</Content>
            <Footer>Footer</Footer>
            {isDivVisible &&
            <div id='motal'>
                <div id='motal-bg' onClick={handleButtonClick}/>
                <div id='motal-ct'>
                    <Motal/>
                </div> 
            </div>
            
            }
        </Layout>
    )
 
};

export default Welcome;