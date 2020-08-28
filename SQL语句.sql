# 随机选取一条记录
SELECT * FROM card_01 WHERE id >= ((SELECT MAX(id) FROM card_01)-(SELECT MIN(id) FROM card_01)) * RAND() + (SELECT MIN(id) FROM card_01)  LIMIT 1
# 插入数据
insert into card_01 (id,name,con) values(0,'001guess','voice/007guess.wav');
# 模糊查询
where name like 'guess%'
# 创建表格
create table card_guess
(
id int auto_increment,
name varchar(50) not null,
con varchar(50) default '',
ans varchar(50) not null,
res varchar(50) not null,
primary key (id)
);
update card_guess set ans='其他垃圾' where id=7;
insert into card_01 (id,name,con) values(0,'001guess','voice/007guess.wav');
insert into card_01 (name,con) values('008','/home/pi/Documents/vs_code/voice/read008.wav');