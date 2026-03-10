import React, { useState } from 'react'
import { Button, ConfigProvider, TextArea, Dialog } from '@nutui/nutui-react-taro'
import enUS from '@nutui/nutui-react-taro/dist/locales/en-US'
import zhCN from '@nutui/nutui-react-taro/dist/locales/zh-CN'
import { View, Navigator } from '@tarojs/components'

import './index.css'
function Index() {
  const [locale, setLocale] = useState(zhCN)
  const localeKey = locale === zhCN ? 'zhCN' : 'enUS'
  const [visible, setVisible] = useState(false)
  const [translated] = useState({
    zhCN: {
      welcome: '欢迎使用  React 开发 Taro 项目。',
      button: '使用英文',
      open: '点击打开',
    },
    enUS: {
      welcome: 'Welcome to use NutUI React to develop Taro multi-terminal projects.',
      button: 'Use Chinese',
      open: 'Click Me',
    },
  })
  const handleSwitchLocale = () => {
    setLocale(locale === zhCN ? enUS : zhCN)
  }
  return (
    <ConfigProvider locale={locale}>
      <View className='nutui-react-demo'>
        <View>{translated[localeKey].welcome}</View>
        <Navigator url='/pages/dict/index' className='nav-link'>
          打开数据字典
        </Navigator>
      </View>
    </ConfigProvider>
  )
}

export default Index
