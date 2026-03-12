import { View } from '@tarojs/components'
import Taro, { useDidShow } from '@tarojs/taro'
import { Grid, Toast, Badge } from '@nutui/nutui-react-taro'
import {
  Find, Edit, List,
  Invoice, Target,
  Notice, Tips, Clock,
  Category, People, Scan
} from '@nutui/icons-react-taro'
import './index.css'

const Index = () => {
  // 统一路由跳转处理
  const navTo = (url: string) => {
    Taro.navigateTo({ url })
  }

  useDidShow(() => {
    const token = Taro.getStorageSync('token');
    const currPages = Taro.getCurrentPages();
    const currRoute = currPages[currPages.length - 1].route;

    // 只有当前不在登录页，且没有 Token 时才跳转
    if (!token && currRoute !== 'pages/auth/login') {
      Taro.reLaunch({ url: '/pages/auth/login' });
    }
  });

  // 扫码功能处理
  const handleScan = () => {
    Taro.scanCode({
      success: (res) => {
        // 扫码后跳转到器材详情或报修页，携带设备编号
        navTo(`/pages/device/detail?sn=${res.result}`)
      },
      fail: () => {
        Toast.show('取消扫码', { type: 'warn' })
      }
    })
  }

  const handleFunctionClick = (type: string) => {
    switch (type) {
      // --- 业务功能 ---
      case 'repair_create':
        navTo('/pages/repair/create')
        break
      case 'inspect':
        navTo('/pages/inspect/list')
        break
      case 'repair_list':
        navTo('/pages/repair/list')
        break

      // --- 运营统计 ---
      case 'stat_completion':
        navTo('/pages/stats/completion')
        break
      case 'stat_efficiency':
        navTo('/pages/stats/efficiency')
        break
      case 'stat_loss':
        navTo('/pages/stats/loss')
        break

      // --- 实时通知 ---
      case 'notice_task':
        navTo('/pages/message/list?type=task')
        break
      case 'notice_urgent':
        navTo('/pages/message/list?type=urgent')
        break
      case 'notice_timeout':
        navTo('/pages/message/list?type=timeout')
        break

      // --- 基础数据 ---
      case 'base_location':
        navTo('/pages/base/location') // 街道/社区/场地
        break
      case 'base_device':
        navTo('/pages/base/device') // 器材维护
        break
      case 'base_user':
        navTo('/pages/base/user/index') // 用户管理
        break
      case 'base_dict':
        navTo('/pages/base/dict') // 数据字典
        break

      default:
        Toast.show('功能开发中', { type: 'warn' })
    }
  }

  return (
    <View className='home-container'>
      <Toast id='home-toast' />

      {/* 业务功能 */}
      <View className='section-card'>
        <View className='section-header'>业务功能</View>
        <Grid columns={3}>
          <Grid.Item text='创建维修单' onClick={() => handleFunctionClick('repair_create')}>
            <Edit size={28} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='巡查单' onClick={() => handleFunctionClick('inspect')}>
            <Find size={28} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='维修单' onClick={() => handleFunctionClick('repair_list')}>
            <List size={28} color='#3b82f6' />
          </Grid.Item>
        </Grid>

        {/* 运营统计 */}
        <View className='card-header'>运营统计</View>
        <Grid columns={3}>
          <Grid.Item text='完成率统计' onClick={() => handleFunctionClick('stat_completion')}>
            <Invoice size={24} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='效率统计' onClick={() => handleFunctionClick('stat_efficiency')}>
            <Invoice size={24} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='损耗统计' onClick={() => handleFunctionClick('stat_loss')}>
            <Invoice size={24} color='#3b82f6' />
          </Grid.Item>
        </Grid>
      </View>

      {/* 实时通知 */}
      <View className='section-card'>
        <View className='card-header'>实时通知</View>
        <Grid columns={3}>
          <Grid.Item text='任务通知' onClick={() => handleFunctionClick('notice_task')}>
            <Badge value={3}><Notice size={24} color='#f59e0b' /></Badge>
          </Grid.Item>
          <Grid.Item text='加急指令' onClick={() => handleFunctionClick('notice_urgent')}>
            <Badge dot><Tips size={24} color='#ef4444' /></Badge>
          </Grid.Item>
          <Grid.Item text='超时预警' onClick={() => handleFunctionClick('notice_timeout')}>
            <Badge value="2"><Clock size={24} color='#6b7280' /></Badge>
          </Grid.Item>
        </Grid>
      </View>

      {/* 基础数据管理 */}
      <View className='section-card'>
        <View className='card-header'>基础数据</View>
        <Grid columns={3}>
          <Grid.Item text='街道/社区' onClick={() => handleFunctionClick('base_location')}>
            <Target size={24} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='场地' onClick={() => handleFunctionClick('base_location')}>
            <Target size={24} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='器材' onClick={() => handleFunctionClick('base_device')}>
            <Target size={24} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='用户管理' onClick={() => handleFunctionClick('base_user')}>
            <People size={24} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='数据字典' onClick={() => handleFunctionClick('base_dict')}>
            <Category size={24} color='#3b82f6' />
          </Grid.Item>
          <Grid.Item text='扫码录入' onClick={handleScan}>
            <Scan size={24} color='#10b981' />
          </Grid.Item>
        </Grid>
      </View>
    </View>
  )
}

export default Index