import { request } from './request'

/**
 * 用户相关 API 服务
 */

// 1. 获取所有用户
export const fetchAllUsers = () => {
  return request({
    url: 'users/',
    method: 'GET'
  })
}

// 2. 创建用户 (注册)
export const createUser = (userData: any) => {
  return request({
    url: 'users/create',
    method: 'POST',
    data: userData
  })
}

// 3. 登录逻辑
// 注意：后端使用了 Form(...) 接收，所以这里必须用 form-urlencoded
export const login = (id: string, password: string) => {
  return request({
    url: 'users/token',
    method: 'POST',
    header: {
      'content-type': 'application/x-www-form-urlencoded'
    },
    data: {
      id: id,
      password: password
    }
  })
}

// 4. 分配角色 (修改角色)
export const assignUserRole = (userId: number, newRole: string) => {
  return request({
    url: `users/${userId}/role`,
    method: 'PATCH',
    // FastAPI 获取路径参数或查询参数
    data: {
      new_role: newRole
    }
  })
}

// 5. 禁用/启用用户
export const toggleUserStatus = (userId: number, isDisabled: boolean) => {
  return request({
    url: `users/${userId}/status`,
    method: 'PATCH',
    data: {
      is_disabled: isDisabled
    }
  })
}

// 6. 删除用户 (物理删除)
export const deleteUser = (userId: number) => {
  return request({
    url: `users/${userId}`,
    method: 'DELETE'
  })
}