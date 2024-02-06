import React from 'react'
import ReactDOM from 'react-dom/client'
import 'antd/dist/antd.compact.css' //紧凑主题
import { ConfigProvider } from 'antd'
import zhCN from 'antd/es/locale/zh_CN'; //引入中文
import {HashRouter as Router} from 'react-router-dom'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Router>
    <ConfigProvider locale={zhCN}>
      <App />
    </ConfigProvider>
  </Router>
)
