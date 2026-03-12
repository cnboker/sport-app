import type { UserConfigExport } from "@tarojs/cli";
export default {
  env: {
    // 注意：值必须用双引号包裹，因为它会被直接替换为字符串
    BASE_URL: '"http://127.0.0.1:8000/api/v1/"' 
  },
  mini: {},
  h5: {}
} satisfies UserConfigExport<'vite'>
