export interface DictItem {
  id?: number;          // 后端主键
  dictCode: string;     // 字典编码，如 "FAULT_TYPE"
  itemKey: string;      // 键，如 "01"
  itemValue: string;    // 值，如 "器材破损"
  sortOrder: number;    // 排序
  isSystem: boolean;    // 是否系统内置（不可删除）
}

// 模拟 API 返回结构
export interface ApiResponse<T> {
  code: number;
  data: T;
  message: string;
}