CREATE TABLE `orders` (
    id int not null auto_increment,
    `status` tinyint not null default 0,
    primary key(`id`)
) comment '订单表';

CREATE TABLE `order_payment` (
    id int not null auto_increment,
    `status` tinyint not null default 0,
    primary key(`id`)
) comment '订单支付表';

CREATE TABLE `order_local_messages` (
    id int not null auto_increment,
    tid varchar(100) not null default '' comment '事务id',
    message_name varchar(100) not null default '' comment '',
    param json not null default '{}' comment '消息参数',
    `status` tinyint not null default 0 comment '状态：0-未完成；1-已完成',
    primary key(`id`)
) comment '本地消息表';


