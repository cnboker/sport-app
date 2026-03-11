import React, { useState } from 'react';
import { View } from '@tarojs/components';
import {
    Table, Button, Input, Form, Dialog,
    Toast, Picker, Cell, Tag, Popup
} from '@nutui/nutui-react-taro';
import { Plus } from '@nutui/icons-react-taro';

// --- 类型定义 ---
type UserRole = 'CITIZEN' | 'INSPECTOR' | 'MAINTAINER' | 'ADMIN' | 'CLIENT_ADMIN';

interface UserItem {
    id: number;
    full_name: string;
    phone: string;
    role: UserRole;
}

const roleOptions = [
    [
        { text: '群众', value: 'CITIZEN' },
        { text: '巡查人员', value: 'INSPECTOR' },
        { text: '维修人员', value: 'MAINTAINER' },
        { text: '管理员', value: 'ADMIN' },
        { text: '甲方管理员', value: 'CLIENT_ADMIN' }
    ]
];

const roleMap: Record<string, string> = {
    CITIZEN: '群众',
    INSPECTOR: '巡查员',
    MAINTAINER: '维修员',
    ADMIN: '管理员',
    CLIENT_ADMIN: '甲方管理'
};

const UserManagement: React.FC = () => {
    const [userList, setUserList] = useState<UserItem[]>([]);
    const [showPopup, setShowPopup] = useState(false);
    const [showPicker, setShowPicker] = useState(false);
    const [roleText, setRoleText] = useState(''); // 用于界面展示选中的角色名

    const [form] = Form.useForm();

    // --- 表格列定义 ---
    const columns = [
        { title: '姓名', key: 'full_name' },
        { title: '手机', key: 'phone' },
        {
            title: '角色',
            key: 'role',
            render: (record: UserItem) => <Tag type="primary">{roleMap[record.role]}</Tag>
        },
        {
            title: '操作',
            key: 'id',
            render: (record: UserItem) => (
                <Button size="mini" type="danger" onClick={() => onDelete(record)}>删除</Button>
            )
        }
    ];

    // --- 逻辑处理 ---

    // 提交创建
    const onFinish = (values: any) => {
        const { password, confirmPassword } = values;

        if (password !== confirmPassword) {
            Toast.show('两次密码不一致', { type: 'fail' });
            return;
        }

        console.log('提交到 FastAPI:', values);
        // 这里执行 api.post('/users/', values)
        Toast.show('创建成功', { type: 'success' });
        setShowPopup(false);
        form.resetFields();
        setRoleText('');
    };

    // 删除确认
    const [deleteVisible, setDeleteVisible] = useState(false);
    const [targetUser, setTargetUser] = useState<UserItem | null>(null);

    // 修改删除按钮点击事件
    const onDelete = (user: UserItem) => {
        setTargetUser(user);
        setDeleteVisible(true);
    };

    // 真正执行删除的函数
    const handleConfirmDelete = async () => {
        if (targetUser) {
            console.log('执行删除 ID:', targetUser.id);
            // 这里写你的请求逻辑: await api.delete(...)
            Toast.show('已删除', { type: 'success' });
        }
        setDeleteVisible(false);
    };

    return (
        <View className="user-management" style={{ padding: '12px', background: '#f7f8fa', minHeight: '100vh' }}>
            <Dialog
                title="确认删除"
                visible={deleteVisible}
                onConfirm={handleConfirmDelete}
                onCancel={() => setDeleteVisible(false)}
            >
                <View style={{ textAlign: 'center' }}>
                    确定要删除人员：{targetUser?.full_name} 吗？
                </View>
            </Dialog>
            {/* 顶部操作区 */}
            <View style={{ marginBottom: '12px', display: 'flex', justifyContent: 'flex-end' }}>
                <Button type="primary" size="small" icon={<Plus size="14" />} onClick={() => setShowPopup(true)}>
                    新增人员
                </Button>
            </View>

            {/* 数据列表 - Taro端Table会自动处理横向滚动 */}
            <View style={{ background: '#fff', borderRadius: '8px' }}>
                <Table columns={columns} data={userList} />
            </View>

            {/* 创建用户 Popup */}
            <Popup
                visible={showPopup}
                position="bottom"
                round
                closeable
                onClose={() => setShowPopup(false)}
                style={{ height: '85%' }}
            >
                <View style={{ padding: '20px 16px' }}>
                    <View style={{ fontSize: '18px', fontWeight: 'bold', textAlign: 'center', marginBottom: '20px' }}>新增用户信息</View>

                    <Form
                        form={form}
                        onFinish={onFinish}
                        footer={
                            <View style={{ marginTop: '20px' }}>
                                <Button block type="primary" formType="submit">保存并创建</Button>
                            </View>
                        }
                    >
                        <Form.Item label="姓名" name="full_name" rules={[{ required: true, message: '姓名必填' }]}>
                            <Input placeholder="输入真实姓名" />
                        </Form.Item>

                        <Form.Item label="电话" name="phone" rules={[{ required: true, message: '手机号必填' }]}>
                            <Input type="tel" placeholder="输入手机号" />
                        </Form.Item>

                        <Form.Item label="角色" name="role" rules={[{ required: true, message: '请选择角色' }]}>
                            <Cell
                                title={roleText || '点击选择角色'}
                                onClick={() => setShowPicker(true)}
                                style={{ padding: 0 }}
                            />
                        </Form.Item>

                        <Form.Item label="密码" name="password" rules={[{ required: true, message: '请输入密码' }]}>
                            <Input type="password" placeholder="设置登录密码" />
                        </Form.Item>

                        <Form.Item label="确认密码" name="confirmPassword" rules={[{ required: true, message: '请再次输入' }]}>
                            <Input type="password" placeholder="确认登录密码" />
                        </Form.Item>
                    </Form>
                </View>
            </Popup>

            {/* 角色选择 Picker */}
            <Picker
                visible={showPicker}
                options={roleOptions}
                title="选择人员角色"
                onConfirm={(list, values) => {
                    const selected = list[0];
                    form.setFieldsValue({ role: selected.value });
                    setRoleText(selected.text as string);
                    setShowPicker(false);
                }}
                onClose={() => setShowPicker(false)}
            />

        </View>
    );
};

export default UserManagement;