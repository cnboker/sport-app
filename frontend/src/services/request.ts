import Taro from '@tarojs/taro'

// 在变量后加一个 ! 表示你保证它一定有值
const BASE_URL = process.env.BASE_URL!;

export const request = async (options: any) => {
  const token = Taro.getStorageSync('access_token')
  
  // 确保 URL 拼接正确
  const baseUrl = BASE_URL.endsWith('/') 
                  ? process.env.BASE_URL 
                  : `${process.env.BASE_URL}/`

  return Taro.request({
    ...options,
    url: `${baseUrl}${options.url}`,
    header: {
      'Authorization': token ? `Bearer ${token}` : '',
      ...options.header,
    },
  }).then(res => {
    // 自动拦截 401 (Token失效)
    if (res.statusCode === 401) {
      Taro.removeStorageSync('access_token')
      Taro.reLaunch({ url: '/pages/auth/login' })
    }
    return res
  })
}