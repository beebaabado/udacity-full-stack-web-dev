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
-- Data for Name: venue; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (1, 'The Musical Hop', 'San Francisco', 'CA', '233 Cheery Street', '123-33-1234', 'Country, Rock & Roll, Classical', 'www.themusicalhop.com', '/static/img/DefaultVenueImage.jpeg', 'https://www.facebook.com/TheMusicalHop', false, 'Come play here!');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (2, 'The Dueling Pianos Bar', 'New York', 'NY', '335 Delancey Street', '914-003-1132', 'Country, Hip Hop, Classical', 'www.theduelingpianosbar.com', '/static/img/DefaultVenueImage.jpeg', 'https://www.facebook.com/theduelingpianos', true, 'Come play here!');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (3, 'Park Square Live Music & Coffee', 'San Francisco', 'CA', '34 Whiskey Moore Ave', '415-000-1234', 'Rock & Roll, Hip Hop, Punk', 'www.theparksqure.com', '/static/img/DefaultVenueImage.jpeg', 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', true, 'Come play here!');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (4, 'Salted Toast', 'Boulder', 'UT', '4056 Hipster Lane', '123-33-1234', 'Alternative, Other', 'www.saltedtoast.com', '/static/img/DefaultVenueImage.jpeg', 'https://www.facebook.com/Therainbows', true, 'Come play here!');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (6, '1ST BANK Center', 'Broomfield', 'CO', '11450 Broomfield Lane', '303-410-0700', 'Alternative, Folk, Jazz, Blues', 'http://www.1stbankcenter.com/', '/static/img/DefaultVenueImage.jpeg', 'http://www.facebook.com', true, 'Looking for new talent.');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (7, 'The Late Night Bar & Grill', 'Boulder', 'CO', '23 Pearl St', '303-567-4320', 'Jazz, R&B', 'http://www.latetnightbarandgrill.com/', '/static/img/DefaultVenueImage.jpeg', 'http://www.facebook.com', true, 'Quaint late night scene with small stage.  Open from 8pm to 1am.  Come check us out.');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (8, 'The Crystal Palace', 'Charlotte', 'NC', '56 North Main Avenue', '111-333-1111', 'Alternative, Classical, Instrumental, Other', 'http://www.crystalpalace.com/', '/static/img/DefaultArtistImage.jpeg', 'http://www.facebook.com/crystalpalace', true, 'Vintage is in.');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (5, 'The Rainbows', 'Boulder', 'CO', '14 Folsom Avenue', '123-33-1234', 'Alternative, Classical, Folk', 'www.therainbows.com', '/static/img/DefaultVenueImage.jpeg', 'https://www.facebook.com/Therainbows', true, 'Come play here!');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (57, 'Beer''s on the House', 'Broomfield', 'CO', '36 Garden Center', '111-333-1111', 'Blues, Classical, Country', 'www.americanastro.com', '/static/img/DefaultArtistImage.jpeg', 'http://', false, 'New Venue with eclectic, art inspired atmosphere. Looking for local talent.');
INSERT INTO public.venue (id, name, city, state, address, phone, genres, website, image_link, facebook_link, seeking_talent, seeking_description) VALUES (58, 'The dog, and cat cafe', 'Minneapolis', 'MN', 'P.O. Box 9189', '3034992876', 'Classical', 'http://www.myfakewebsite.com/', '/static/img/DefaultArtistImage.jpeg', 'http://', true, 'Looking for new talent.');


--
-- Name: venue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.venue_id_seq', 58, true);


--
-- PostgreSQL database dump complete
--

