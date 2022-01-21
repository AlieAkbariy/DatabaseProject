use DB_Project
/*
drop table FoodInterface;
drop table Food;
drop table FoodOrder;
drop table ResturantCoffeeShop;
drop table Bill;
drop table CleaningService;
drop table ReservationDetails;
drop table People;
drop table Reservation;
drop table StaffInformation;
drop table BookingStatus;
drop table Guest;
drop table Room;
drop table RoomStatus;
drop table RoomType;
*/

create table RoomType (
	id int not null identity(1,1),
	no_bed int,
	name_type nvarchar(30),
	room_image image,
	primary key(id),
);

create table RoomStatus (
	id int not null identity(1,1),
	name_status nvarchar(30),
	primary key(id),
);

create table Room (
	id int not null identity(1,1),
	rt_id int not null,
	rs_id int not null,
	price_per_night bigint,
	room_floor int,
	maximum_capacity int,
	primary key(id),
	foreign key(rt_id) references RoomType(id),
	foreign key(rs_id) references RoomStatus(id),
);

create table Guest(
	id int not null identity(1,1),
	phone_number nvarchar(20),
	guest_address nvarchar(20),
	birth_date date,
	first_name nvarchar(30),
	last_name nvarchar(30),
	national_id nvarchar(20) unique,
	g_password nvarchar(30),
	no_nights int,
	gender nvarchar(10),
	primary key(id),
);

create table BookingStatus (
	id int not null identity(1,1),
	name_status nvarchar(30),
	primary key(id),
);

create table StaffInformation(
	id int not null identity(1,1),
	first_name nvarchar(30),
	last_name nvarchar(30),
	national_id nvarchar(20) unique,
	s_password nvarchar(30),
	salary nvarchar(30),
	staff_role nvarchar(20),
	email nvarchar(30) unique,
	s_start_date date,
	gender nvarchar(10),
	primary key(id),
);

create table Reservation(
	id int not null identity(1,1),
	g_id int not null,
	bs_id int not null,
	staff_id int not null,
	checkin_date date,
	checkout_date date,
	reserve_date date,
	no_nights int,
	primary key(id),
	foreign key(g_id) references Guest(id),
	foreign key(bs_id) references BookingStatus(id),
	foreign key(staff_id) references StaffInformation(id),
);

create table People(
	id int not null identity(1,1),
	r_id int not null,
	first_name nvarchar(30),
	last_name nvarchar(30),
	national_id nvarchar(20) unique,
	gender nvarchar(10),
	primary key(id),
	foreign key(r_id) references Reservation(id),
);

create table ReservationDetails(
	id int not null identity(1,1),
	reservation_id int not null,
	room_id int not null,
	rate int ,
	extra_facilities nvarchar(150),
	foreign key(reservation_id) references Reservation(id),
	foreign key(room_id) references Room(id),
	primary key(id),

);

create table CleaningService(
	id int not null identity(1,1),
	staff_id int not null,
	rd_id int not null,
	cleaning_time datetime,
	cleaning_date date,
	cleaning_description nvarchar(150),
	foreign key(staff_id) references StaffInformation(id),
	foreign key(rd_id) references ReservationDetails(id),
	primary key(id),

);

create table Bill(
	id int not null identity(1,1),
	total_amount bigint,
	bill_status int,
	reservation_id int not null,
	foreign key(reservation_id) references Reservation(id),
	primary key(id),
);

create table ResturantCoffeeShop(
	id int not null identity(1,1),
	res_name nvarchar(100),
	res_type nvarchar(20),
	primary key(id),
);

create table FoodOrder(
	id int not null identity(1,1),
	rd_id int not null,
	flag nvarchar(20),
	foreign key(rd_id) references ReservationDetails(id),
	primary key(id),
);

create table Food(
	id int not null identity(1,1),
	resturant_id int not null,
	food_name nvarchar(50),
	food_price bigint,
	food_ingredients nvarchar(150),
	food_type nvarchar(20),
	foreign key(resturant_id) references ResturantCoffeeShop(id),
	primary key(id),
	
);

create table FoodInterface(
	id int not null identity(1,1),
	fd_id int not null,
	f_id int not null,
	foreign key(fd_id) references FoodOrder(id),
	foreign key(f_id) references Food(id),
	primary key(id)
);

insert into RoomType(no_bed,name_type) values(1,'Single')
insert into RoomType(no_bed,name_type) values(2,'Couple')

insert into RoomStatus values('Reserved')
insert into RoomStatus values('Empty')
insert into RoomStatus values('Repairing')

insert into Room (rt_id,rs_id,price_per_night,room_floor,maximum_capacity) values(1,2,500000,1,1)
insert into Room (rt_id,rs_id,price_per_night,room_floor,maximum_capacity) values(1,2,500000,1,1)
insert into Room (rt_id,rs_id,price_per_night,room_floor,maximum_capacity) values(1,2,500000,1,1)
insert into Room (rt_id,rs_id,price_per_night,room_floor,maximum_capacity) values(1,2,500000,1,1)
insert into Room (rt_id,rs_id,price_per_night,room_floor,maximum_capacity) values(2,2,1000000,1,2)
insert into Room (rt_id,rs_id,price_per_night,room_floor,maximum_capacity) values(2,2,1000000,1,2)
insert into Room (rt_id,rs_id,price_per_night,room_floor,maximum_capacity) values(2,2,1000000,1,2)

insert into BookingStatus values ('Confirm')
insert into BookingStatus values ('Not Confirm')

insert into StaffInformation (first_name,last_name,staff_role,national_id ,email) values('ali','darabi','Receptionist','2454173256','erefrefer@gmail.com')
insert into StaffInformation (first_name,last_name,staff_role,national_id ,email) values('mohammad','darabi','Receptionist','1248632574','ergergwfewrg@gmail.com')
insert into StaffInformation (first_name,last_name,staff_role,national_id ,email) values('reza','darabi','Receptionist','1547625368','urhtyfkeifh@gmail.com')
insert into StaffInformation (first_name,last_name,staff_role,national_id ,email) values('ehsan','darabi','CleaningStaff','4574152365','htyurighfnoi@gmail.com')
insert into StaffInformation (first_name,last_name,staff_role,national_id ,email) values('mohammad reza','darabi','CleaningStaff','4752135689','wfgrthrthrh@gmail.com')
insert into StaffInformation (first_name,last_name,staff_role,national_id ,email) values('mehran','darabi','CleaningStaff','5847125369','rgrthgrth@gmail.com')

insert into ResturantCoffeeShop values('Lavia','Restaurants')
insert into ResturantCoffeeShop values('Shater Abbas','Restaurants')
insert into ResturantCoffeeShop values('Coffee 57','CoffeeShop')
insert into ResturantCoffeeShop values('Barbod','Restaurants')
insert into ResturantCoffeeShop values('Atlas Coffee','CoffeeShop')


insert into Food values (1,'Hot Dog' ,50000,'cheese','Food' )
insert into Food values (1,'Soda' ,6000,'ccccccccccc','Drink' )
insert into Food values (1,'Pizza' ,50000,'mushroom,cheese','Food' )
insert into Food values (1,'Dogh' ,5000,'eeeeeeeeeeeee','Drink' )
insert into Food values (1,'Sandwich' ,35000,'Hamber,cheese','Food' )
insert into Food values (1,'Shani' ,35000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )

insert into Food values (2,'Joje Kabab' ,35000,'chicken,rice','Food' )
insert into Food values (2,'Kabab' ,30000,'rice,','Food' )
insert into Food values (2,'Soda' ,6000,'ccccccccccc','Drink' )
insert into Food values (2,'Pizza' ,50000,'mushroom,cheese','Food' )
insert into Food values (2,'Dogh' ,5000,'eeeeeeeeeeeee','Drink' )
insert into Food values (2,'Sandwich' ,35000,'Hamber,cheese','Food' )
insert into Food values (2,'Akbar Joje' ,45000,'chicken','Food' )
insert into Food values (2,'Shani' ,35000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )

insert into Food values (3,'Coffee' ,10000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )
insert into Food values (3,'Cappuccino' ,35000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )
insert into Food values (3,'Tea' ,12000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )
insert into Food values (3,'Lemonade' ,20000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )

insert into Food values (4,'Joje Kabab' ,35000,'chicken,rice','Food' )
insert into Food values (4,'Kabab' ,30000,'rice,','Food' )
insert into Food values (4,'Soda' ,6000,'ccccccccccc','Drink' )
insert into Food values (4,'Pizza' ,50000,'mushroom,cheese','Food' )
insert into Food values (4,'Dogh' ,5000,'eeeeeeeeeeeee','Drink' )
insert into Food values (4,'Sandwich' ,35000,'Hamber,cheese','Food' )
insert into Food values (4,'Akbar Joje' ,45000,'chicken','Food' )
insert into Food values (4,'Shani' ,35000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )

insert into Food values (5,'Coffee' ,10000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )
insert into Food values (5,'Cappuccino' ,35000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )
insert into Food values (5,'Tea' ,12000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )
insert into Food values (5,'Lemonade' ,20000,'hhhhhhhhhhhhhhhhhhhh','Drnk' )
