-- Customer Details

INSERT INTO special_customer (id, plate, first_name, surname, local_authority, local_consultancy)
VALUES (1, "AA11 AAA", "Bob" , "Jenkins", 1, 0);

INSERT INTO special_customer (id, plate, first_name, surname, local_authority, local_consultancy)
VALUES (2, "BB22 BBB", "Joe", "Kennedy", 0, 1);


-- Manager Logins

INSERT INTO manager_login (id, username, password, first_name, surname)
VALUES (1, "user1", "pass1", "John", "Stewart");

INSERT INTO manager_login (id, username, password, first_name, surname)
VALUES (2, "user2", "pass2", "Mason", "Jarvis");

INSERT INTO manager_login (id, username, password, first_name, surname)
VALUES (3, "user3", "pass3", "Adam", "Brady");


