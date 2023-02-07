-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;

-- GRANT ALL ON SCHEMA public TO postgres;
-- GRANT ALL ON SCHEMA public TO public;
truncate setup_users, setup_tags, setup_posts, setup_comments, setup_votes, setup_badges, setup_post_history, setup_post_links;

\copy setup_users from '/home/charanubuntu/DBMS/DBMS-2/A2/Data/Users.csv' with (FORMAT csv,HEADER true);
\copy setup_tags from '/home/charanubuntu/DBMS/DBMS-2/A2/Data/Tags.csv' with (FORMAT csv,HEADER true);
\copy setup_comments from '/home/charanubuntu/DBMS/DBMS-2/A2/Data/Comments.csv' with (FORMAT csv,HEADER true);
\copy setup_posts from '/home/charanubuntu/DBMS/DBMS-2/A2/Data/Posts.csv' with (FORMAT csv,HEADER true);
\copy setup_post_links from '/home/charanubuntu/DBMS/DBMS-2/A2/Data/PostLinks.csv' with (FORMAT csv,HEADER true);
\copy setup_post_history from '/home/charanubuntu/DBMS/DBMS-2/A2/Data/PostHistory.csv' with (FORMAT csv,HEADER true);
\copy setup_votes from '/home/charanubuntu/DBMS/DBMS-2/A2/Data/Votes.csv' with (FORMAT csv,HEADER true);
\copy setup_badges from '/home/charanubuntu/DBMS/DBMS-2/A2/Data/Badges.csv' with (FORMAT csv,HEADER true);
