

#### roles

> CREATE DEFINER=`root`@`localhost` TRIGGER `roles_AFTER_DELETE` AFTER DELETE ON `roles` FOR EACH ROW BEGIN
>	DELETE FROM users
>			WHERE users.role_id = old.id;
>	END




#### users


> CREATE DEFINER=`root`@`localhost` TRIGGER `users_AFTER_DELETE` AFTER DELETE ON `users` FOR EACH ROW BEGIN
>	IF(OLD.role_id=2) THEN
>		DELETE FROM books
>			WHERE books.author_id = old.id;
>	END IF;
>END