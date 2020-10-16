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
-- Data for Name: artist; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (5, 'Streamers', 'Boulder', 'CO', '123-444-5656', 'Blues, Jazz', 'http://www.deadbeats.com', '/static/img/DefaultArtistImage.jpeg', 'www.facebook.com/deadbeats', true, 'New local band looking for shows in Boulder/Denver area.', '2020-10-15 21:30:00', '2020-11-21 21:30:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (7, 'Meow Cat!', 'New York', 'NY', '667-333-6789', 'Classical, Musical Theatre', 'http://www.meowcat.com/', '/static/img/DefaultArtistImage.jpeg', 'http://', true, 'Meows the word with this new band looking to play the local scene in the Village.', '2020-10-15 21:30:00', '2020-11-21 21:30:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (9, 'Chocolate Waters', 'Boulder', 'CO', '303-856-4019', 'Country', 'http://www.myfackwebsite.com/', '/static/img/DefaultArtistImage.jpeg', 'http://', true, 'Looking for new talent.', '2020-10-15 21:30:00', '2020-11-21 21:30:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (3, 'The Lost Donuts', 'San Francisco', 'CA', '123-444-5656', 'Hip Hop, Blues', 'http://www.deadbeats.com', '/static/img/DefaultArtistImage.jpeg', 'www.facebook.com/deadbeats', true, 'New local band looking for shows in Boulder/Denver area.', '2020-10-15 21:30:00', '2020-11-21 21:30:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (1, 'Bean Le Bean the 3rd gets another name', 'Austin', 'TX', '879-444-5555', 'Alternative, Other', 'http://www.BeanLeBeanwebsite.com/', '/static/img/DefaultArtistImage.jpeg', '', true, 'Love to play a few ukulele tunes at your venue.', '2020-10-15 21:30:00', '2020-11-21 21:30:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (2, 'Milano', 'Boulder', 'CO', '720-840-5678', 'Classical, Instrumental', 'http://www.myfakewebsite.com/', '/static/img/DefaultArtistImage.jpeg', 'www.facebook.com/milano', true, 'Would like to find small venue to shwowcase my talent for the theremin.', '2020-12-01 21:30:00', '2021-01-31 21:30:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (8, 'American Astronaut', 'Portland', 'OR', '555-66-7777', 'Alternative, Heavy Metal, Rock n Roll', 'www.americanastro.com', '/static/img/DefaultArtistImage.jpeg', 'http://www.facebook.com/americanastro', true, 'Spaced out group of people who like to play instruments from far off places.', '2020-12-01 21:30:00', '2021-01-31 21:30:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (4, 'Billy Eilish', 'New York', 'NY', '123-444-5656', 'Blues, Alternative, Classical', 'http://www.deadbeats.com', '/static/img/DefaultArtistImage.jpeg', 'www.facebook.com/deadbeats', true, 'New local band looking for shows in Boulder/Denver area.', '2020-12-01 21:30:00', '2021-01-31 21:30:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (12, 'Magnificent Bumble Bees', 'Minneapolis', 'MN', '303-499-2876', 'Alternative, Instrumental, Other', 'www.magbees.com', '/static/img/DefaultArtistImage.jpeg', 'http://', false, 'Looking for quiet small space to perform with small band.', '2020-10-31 20:00:00', '2020-12-31 20:00:00');
INSERT INTO public.artist (id, name, city, state, phone, genres, website, image_link, facebook_link, seeking_venue, seeking_description, time_available_start, time_available_stop) VALUES (11, 'Mousey Mouse', 'Cheesetown', 'PA', '111-333-1111', 'Classical, Country, Musical Theatre, Pop', 'http://www.1stbankcenter.com/', '/static/img/DefaultArtistImage.jpeg', 'http://', false, 'Looking for quiet small space to perform with my theremin.', '2020-10-31 20:00:00', '2020-12-31 20:00:00');


--
-- Name: artist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.artist_id_seq', 12, true);


--
-- PostgreSQL database dump complete
--

