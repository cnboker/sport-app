import React from 'react'
import { NavBar } from '@nutui/nutui-react-taro'
import { ArrowLeft, Home } from '@nutui/icons-react-taro'
import Taro from '@tarojs/taro'

interface AppNavBarProps {
    title: string
    showHome?: boolean // 是否强制显示首页图标
}

const AppNavBar: React.FC<AppNavBarProps> = ({ title, showHome = false }) => {

    const handleBack = () => {
        const pages = Taro.getCurrentPages()

        // 如果页面栈大于1，正常返回；否则回首页
        if (pages.length > 1 && !showHome) {
            Taro.navigateBack()
        } else {
            Taro.reLaunch({ url: '/pages/index/index' })
        }
    }

    // 根据页面栈深度决定图标：1层显示Home，多层显示Left
    const renderIcon = () => {
        const pages = Taro.getCurrentPages()
        return pages.length > 1 && !showHome ? <ArrowLeft size={16} /> : <Home size={16} />
    }

    return (
        <NavBar
            back={renderIcon()}
            onBackClick={handleBack}
            fixed
            // 这里的 style 是为了适配自定义导航栏时的置顶
            style={{ position: 'sticky', top: 0, zIndex: 100, width: '100%' }}
        >{title}</NavBar>
    )
}

export default AppNavBar