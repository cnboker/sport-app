-- 切换到你的数据库
\c mysport;

-- 批量插入区域数据
INSERT INTO dictionary (dict_code, dict_value) VALUES 
('region', '福田区'),
('region', '罗湖区'),
('region', '龙岗区'),
('region', '龙华区'),
('region', '坪山区'),
('region', '宝安区');