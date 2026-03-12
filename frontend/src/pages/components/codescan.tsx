import { Toast } from "@nutui/nutui-react-taro"
import { View } from "@tarojs/components"
import Taro from "@tarojs/taro"
import { Scan } from '@nutui/icons-react-taro' // 引入图标

const Index = () => {
    // 扫码识别设备逻辑
    const handleScan = () => {
        Taro.scanCode({
            success: (res) => {
                // 扫码成功后跳转到创建页，并携带设备ID
                Taro.navigateTo({
                    url: `/pages/repair/create?sn=${res.result}`
                })
            },
            fail: () => {
                Toast.show('取消扫码', { type: 'warn' })
            }
        })
    }

    return
    <View className='home-container'>
        {/* 补充：扫码直达快捷键（大按钮） */}
        <View className='scan-box' onClick={handleScan}>
            <Scan size={40} color='#fff' />
            <View className='scan-text'>扫码报修/巡检</View>
        </View>
    </View>
}

export default Index