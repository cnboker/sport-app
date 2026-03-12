import { useState } from 'react'
import { View } from '@tarojs/components'
import Taro from '@tarojs/taro'
import { Form, Input, Button, Toast, Divider } from '@nutui/nutui-react-taro'
import { People, Lock } from '@nutui/icons-react-taro'
import './index.scss'
import { login } from '../../services/user' // 引入你刚才写的服务

const Login = () => {
    const [loading, setLoading] = useState(false)

    // 远程登录 API 调用
    const handleRemoteLogin = async (values: any) => {
        setLoading(true)
        try {
            const res = await login(values.id, values.password)
      
            if (res.statusCode === 200) {
                // 存储 Token (假设返回数据里有 access_token)
                Taro.setStorageSync('token', res.data.access_token)
                Taro.showToast({ title: '登录成功', icon: 'success' })
                // 登录成功后跳转首页
                Taro.reLaunch({ url: '/pages/index/index' })
            } else {
                Taro.showToast({ title: res.data.detail||'登录失败', icon: 'error' })
            }
        } catch (err) {
            Taro.showToast({ title: '网络错误，请稍后再试', icon: 'error' })
        } finally {
            setLoading(false)

        }
    }

    return (
        <View className='login-page'>
            <Toast id="test" />
            <View className='login-header'>
                <View className='title'>用户登录</View>
            </View>
            <Form
                onFinish={handleRemoteLogin}
                footer={
                    // 提交按钮放在 Form 的 footer 中，会自动触发表单提交
                    <Button block type='primary' formType='submit' loading={loading}>
                        立即登录
                    </Button>
                }
            >
                <Form.Item
                    label={<People size={18} />}
                    name='id'
                    rules={[{ required: true, message: '请输入用户名' }]}
                >
                    <Input placeholder='请输入用户名' />
                </Form.Item>

                <Form.Item
                    label={<Lock size={18} />}
                    name='password'
                    rules={[{ required: true, message: '请输入密码' }]}
                >
                    <Input placeholder='请输入密码' type='password' />
                </Form.Item>
            </Form>

            {/* 角色快捷入口 */}
            <Divider contentPosition='center' style={{ marginTop: '40px' }}>快捷切换</Divider>
            <View className='role-grid'>
                {['群众', '巡查人员', '维修人员', '管理员', '甲方人员'].map(role => (
                    <Button
                        key={role}
                        size='small'
                        fill='outline'
                        onClick={() => handleRemoteLogin({ username: role, password: 'nopassword' })}
                    >
                        {role}登录
                    </Button>
                ))}
            </View>
        </View>
    )
}

export default Login