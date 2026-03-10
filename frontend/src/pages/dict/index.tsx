import React from 'react';
import { View } from '@tarojs/components';
import { Cell, CellGroup, ConfigProvider } from '@nutui/nutui-react-taro';

const Dictionary = () => {
  const dictData = [
    { label: 'gu', value: '跑步' },
    { label: '强度等级', value: '高' },
    { label: '更新时间', value: '2026-03-10' }
  ];

  return (
    <ConfigProvider>
      <View style={{ padding: '10px', background: '#f7f8fa', minHeight: '100vh' }}>
        <CellGroup title="基础数据字典">
          {dictData.map((item, index) => (
            <Cell 
              key={index} 
              title={item.label} 
              extra={item.value} 
              align="center"
            />
          ))}
        </CellGroup>
      </View>
    </ConfigProvider>
  );
};

export default Dictionary;