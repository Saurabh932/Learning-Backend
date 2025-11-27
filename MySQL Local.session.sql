CREATE DATABASE practice_sql;
USE practice_sql;


CREATE TABLE departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50)
);


CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    department_id INT,
    salary INT,
    join_date DATE,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);


CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    city VARCHAR(50)
);


CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    amount INT,
    status VARCHAR(20),
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);


CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    price INT,
    category VARCHAR(50)
);


CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);


INSERT INTO departments (name) VALUES
('IT'),
('HR'),
('Finance'),
('Marketing');


INSERT INTO employees (name, department_id, salary, join_date) VALUES
('Rahul', 1, 55000, '2020-01-02'),
('Saurabh', 2, 45000, '2021-02-12'),
('Aisha', 1, 60000, '2022-05-20'),
('Rohit', 3, 70000, '2023-04-10'),
('Simran', 4, 50000, '2022-11-15');


INSERT INTO customers (name, city) VALUES
('Rahul', 'Pune'),
('Aisha', 'Delhi'),
('Saurabh', 'Nagpur'),
('Rita', 'Pune'),
('Vikas', 'Nagpur');


INSERT INTO orders (customer_id, amount, status, order_date) VALUES
(1, 300, 'Completed', '2023-01-03'),
(1, 800, 'Completed', '2023-03-29'),
(2, 450, 'Pending', '2023-02-10'),
(3, 350, 'Completed', '2023-03-22'),
(4, 600, 'Cancelled', '2023-04-01');


INSERT INTO products (name, price, category) VALUES
('Laptop', 60000, 'Electronics'),
('Mouse', 500, 'Electronics'),
('Keyboard', 1500, 'Electronics'),
('Chair', 4000, 'Furniture'),
('Desk', 8000, 'Furniture');


INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 2, 2),
(1, 3, 1),
(2, 1, 1),
(3, 2, 1),
(4, 4, 1);


SELECT * from customers;
SELECT * from departments;
SELECT * from employees;
SELECT * from order_items;
SELECT * from orders;
SELECT * from products;



-- Q1: Select all employee names and salaries from the employees table.
select name, salary from employees;



-- Q2: Get all customers who live in the city 'Nagpur'.
select * from customers
where city="Nagpur";


-- Q3: Retrieve all orders where the status is 'Completed'
select * from orders
where status="Completed";



-- Q4: Show all employees sorted by salary in descending order.
select * from employees
order by salary desc;


-- Q5: Get all employees who joined after January 1st, 2021.
select * from employees
where join_date > '2021-01-01';


-- Q6: Show the total number of customers in each city.
select city, count(*) as total_customers from customers
group by city;


-- Q7: Find the total money spent by each customer.
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id;


-- Q8: List all employees along with their department name.

select e.name as E_name, d.name as D_name from employees e
right join departments d 
on e.department_id = d.id;


-- Find customers who have placed more than 1 order.
select c.name, count(o.id) as o_count from customers c
inner join orders o on c.id = o.customer_id
group by c.id
having o_count > 1;


-- Q10: Get the products whose price is between 500 and 1500.
select p.name from products p
where p.price between 500 and 1500;


-- Q11: Select all employees and their department names
select e.name, d.name from employees e
inner join departments d on e.department_id = d.id;


-- Q12: Show all customers and the orders they have placed.
select c.name, o.amount from customers c
inner join orders o on c.id = o.customer_id;


-- Q13: Show all employees, even those who do not belong to any department
select e.name, d.name from employees e
left join departments d on e.department_id = d.id;


-- Q14: Show all departments and the employees who belong to them
