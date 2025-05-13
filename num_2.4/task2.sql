create table if not exists drink(
id integer primary key,
name char(26) not null,
alcohol_percentage float(3) not null,
price_for_litre float(2) not null
);

create table if not exists ingredient(
id integer primary key,
name char(26) not null
);

create table if not exists cocktails(
id integer primary key,
name char(26) not null,
alcohol_percentage float(2) not null,
price float(2) not null
);

create table if not exists ingredients(
id integer primary key,
cocktail int references cocktails(id),
ingredient int references ingredient(id),
volume float(3) not null
);

create table if not exists drinks(
id integer primary key,
cocktail int references cocktails(id),
drink int references drink(id),
volume float(3) not null
);

create table if not exists supply_ingredient(
id integer primary key,
supply_date date not null,
ingredient int references ingredient(id),
volume float(3) not null,
quantity int not null,
price float(2) not null
);

create table if not exists supply_drink(
id integer primary key,
supply_date date not null,
drink int references drinks(id),
volume float(3) not null,
quantity int not null,
price float(2) not null
);

create table if not exists sells_drink(
id integer primary key,
sell_date date not null,
cocktail int references cocktails(id),
volume float(3) not null,
quantity int not null,
price float(2) not null
);

create table if not exists sells_cocktail(
id integer primary key,
sell_date date not null,
cocktail int references cocktails(id),
volume float(3) not null,
quantity int not null,
price float(2) not null
);