-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;

-- GRANT ALL ON SCHEMA public TO postgres;
-- GRANT ALL ON SCHEMA public TO public;
truncate setup_users, setup_tags, setup_posts, setup_comments, setup_votes, setup_badges, setup_post_history, setup_post_links;

\copy setup_users from '/home/himanshukumargupta/webdev/syntax_error/Data/Users.csv' with (FORMAT csv,HEADER true);
\copy setup_tags from '/home/himanshukumargupta/webdev/syntax_error/Data/Tags.csv' with (FORMAT csv,HEADER true);
\copy setup_comments from '/home/himanshukumargupta/webdev/syntax_error/Data/Comments.csv' with (FORMAT csv,HEADER true);
\copy setup_posts from '/home/himanshukumargupta/webdev/syntax_error/Data/Posts.csv' with (FORMAT csv,HEADER true,delimiter ',');
\copy setup_post_links from '/home/himanshukumargupta/webdev/syntax_error/Data/PostLinks.csv' with (FORMAT csv,HEADER true);
\copy setup_post_history from '/home/himanshukumargupta/webdev/syntax_error/Data/PostHistory.csv' with (FORMAT csv,HEADER true);
\copy setup_votes from '/home/himanshukumargupta/webdev/syntax_error/Data/Votes.csv' with (FORMAT csv,HEADER true);
\copy setup_badges from '/home/himanshukumargupta/webdev/syntax_error/Data/Badges.csv' with (FORMAT csv,HEADER true);
