import {
    MenuFoldOutlined,
    MenuUnfoldOutlined,
    UploadOutlined,
    UserOutlined,
    VideoCameraOutlined,
  } from '@ant-design/icons';
  import { Layout, Menu } from 'antd';
  import React, { useState } from 'react';
  interface MyLayout extends React.ComponentPropsWithRef<typeof Layout> {}


  const { Header, Sider, Content } = Layout;
  
  const sitMenuData

  const MyLayout: React.FC<MyLayout> = ({ children }: any) => {
    const [collapsed, setCollapsed] = useState(false);
  
    return (
      <Layout style={{ width: '100vw', height: '100vh' }} id='components-layout-demo-custom-trigger'>
        <Sider trigger={null} collapsible collapsed={collapsed}>
          <div className="logo"/>
          <Menu
            theme="light"
            mode="inline"
            defaultOpenKeys={['']}
            defaultSelectedKeys={['1']}
            onClick={({ key }) => {
                alert(key);
            }}
            items={[
              {
                key: '1',
                icon: <UserOutlined />,
                label: 'Today',
                children:[
                    {
                        key : '11',
                        label : 'xxxxx'
                    }
                    // {TodayList}
                ]
              },
              {
                key: '2',
                icon: <VideoCameraOutlined />,
                label: 'Yesterday',
                children:[
                    {
                        key : '21',
                        label : 'xxxxx'
                    }
                    // {Yesterday}
                ]
              },
              {
                key: '3',
                icon: <UploadOutlined />,
                label: 'Preivous',
                children:[
                    {
                        key : '31',
                        label : 'xxxxx'
                    }
                    // {Preivous}
                ]
              },
            ]}
          />
        </Sider>
        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: 0 }}>
            {React.createElement(collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
              className: 'trigger',
              onClick: () => setCollapsed(!collapsed),
            })}
          </Header>
          <Content
            className="site-layout-background"
            style={{
              margin: '24px 16px',
              padding: 24,
              minHeight: 280,
            }}
          >
            {children}
          </Content>
        </Layout>
      </Layout>
    );
  };
  
  export default MyLayout;