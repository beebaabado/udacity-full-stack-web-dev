--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: show; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (1, 2, '2035-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (1, 2, '2019-08-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (1, 2, '2020-07-15 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (1, 3, '2019-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (1, 3, '2021-08-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (2, 2, '2035-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (2, 2, '2020-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (2, 3, '2035-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (3, 2, '2035-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (3, 3, '2035-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (4, 4, '2035-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (4, 2, '2035-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (5, 1, '2035-04-01 20:00:00', 'The concert of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (4, 1, '2020-10-09 15:16:47', 'The Lost Donuts glazed once again ');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (2, 7, '2020-10-10 18:00:00', 'Show description');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (2, 5, '2020-10-10 18:00:00', 'Fun Times ahead!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (5, 2, '2020-10-09 17:11:51', 'This is a longer description to see what happens when it wraps to the second line on show page.');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (2, 8, '2020-10-12 12:05:01', 'Test show description...');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (6, 8, '2020-10-12 13:55:27', 'Show description');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (6, 8, '2020-10-12 17:48:01', 'Show description');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (7, 7, '2020-10-16 20:00:00', 'Cat got your tongue?!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (6, 8, '2021-01-16 20:30:00', 'Show of the year!');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (2, 4, '2020-10-13 02:18:00', 'Show description');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (6, 8, '2020-10-12 15:50:00', 'Show description');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (7, 8, '2020-10-13 16:33:00', 'Show description');
INSERT INTO public.show (venue_id, artist_id, start_time, description) VALUES (6, 8, '2020-12-21 20:42:00', 'Show description');


--
-- PostgreSQL database dump complete
--

