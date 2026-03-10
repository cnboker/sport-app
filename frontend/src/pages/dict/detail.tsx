import React, { useState, useEffect } from 'react';
import { View } from '@tarojs/components';
import { Cell, CellGroup, Button, Dialog, Input, Toast } from '@nutui/nutui-react-taro';
import { DictItem } from './types';

const DictionaryAdmin: React.FC = () => {
  const [list, setList] = useState<DictItem[]>([]);
  const [visible, setVisible] = useState(false);
  const [currentItem, setCurrentItem] = useState<Partial<DictItem>>({});

  useEffect(() => {
    fetchDictList();
  }, []);

  const fetchDictList = () => {
    const mockData: DictItem[] = [
      { id: 1, dictCode: 'FAULT', itemKey: '01', itemValue: '踏板松动', sortOrder: 1, isSystem: true },
      { id: 2, dictCode: 'FAULT', itemKey: '02', itemValue: '显示屏黑屏', sortOrder: 2, isSystem: false },
    ];
    setList(mockData);
  };

  const handleSave = () => {
    if (!currentItem.itemValue) {
      Toast.show('内容不能为空');
      return;
    }
    // 这里执行保存逻辑...
    Toast.show('保存成功');
    setVisible(false);
  };

  return (
    <View style={{ background: '#f7f8fa', minHeight: '100vh', paddingBottom: '20px' }}>
      <CellGroup 
        title="故障类型管理" 
        extra={<Button size="small" type="primary" onClick={() => { setCurrentItem({}); setVisible(true); }}>新增</Button>}
      >
        {list.map(item => (
          <Cell
            key={item.id}
            title={item.itemValue}
            description={`编码: ${item.itemKey}`}
            extra={
              <View style={{ display: 'flex', gap: '10px' }}>
                <Button size="mini" fill="outline" type="primary" onClick={() => { setCurrentItem(item); setVisible(true); }}>编辑</Button>
                {!item.isSystem && (
                  <Button size="mini" fill="outline" type="danger" onClick={() => {
                    setList(list.filter(i => i.id !== item.id));
                  }}>删除</Button>
                )}
              </View>
            }
          />
        ))}
      </CellGroup>

      {/* NutUI 标准对话框 */}
      <Dialog
        title={currentItem.id ? "编辑项" : "新增项"}
        visible={visible}
        onConfirm={handleSave}
        onCancel={() => setVisible(false)}
      >
        <View style={{ marginTop: '10px' }}>
          <Input
            label="名称"
            placeholder="请输入字典项内容"
            value={currentItem.itemValue}
            onChange={(val) => setCurrentItem({ ...currentItem, itemValue: val })}
          />
          <Input
            label="编码"
            placeholder="请输入编码"
            value={currentItem.itemKey}
            onChange={(val) => setCurrentItem({ ...currentItem, itemKey: val })}
          />
        </View>
      </Dialog>
    </View>
  );
};

export default DictionaryAdmin;