-- Customer Details

INSERT INTO special_customer (id, plate, first_name, surname, local_authority, local_consultancy)
VALUES (1, "AA11 AAA", "Bob" , "Jenkins", 1, 0);

INSERT INTO special_customer (id, plate, first_name, surname, local_authority, local_consultancy)
VALUES (2, "BB22 BBB", "Joe", "Kennedy", 0, 1);


-- Manager Logins

INSERT INTO manager_login (id, username, password, first_name, surname)
VALUES (1, "user1", "sha256$n1ahn0HfsURc5XNC$20808a045adf0f1cc91f643fe8817aa268add6cf360cc3671936580162c3854d", "John", "Stewart");

INSERT INTO manager_login (id, username, password, first_name, surname)
VALUES (2, "user2", "sha256$MjqBW0r4z3pfnPR0$c86def9243b2f4eb768d3cee89661b086376852f8c2f8fb69ebd17cf0e006f70", "Mason", "Jarvis");

INSERT INTO manager_login (id, username, password, first_name, surname)
VALUES (3, "user3", "sha256$5qMgcgjoCvNTDZ0k$f00156082d387791ca2bd4dd4dc88e0fa00d819c03bec26728d41a48a7cbfed6", "Adam", "Brady");

