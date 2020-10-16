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
-- Data for Name: album; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.album (id, name, artist_id) VALUES (2, 'BlockHead', 1);
INSERT INTO public.album (id, name, artist_id) VALUES (3, 'Sweet Coffee', 3);
INSERT INTO public.album (id, name, artist_id) VALUES (4, 'Dunk It', 3);
INSERT INTO public.album (id, name, artist_id) VALUES (6, 'Binge', 5);
INSERT INTO public.album (id, name, artist_id) VALUES (7, 'The Last Frontier', 8);
INSERT INTO public.album (id, name, artist_id) VALUES (8, 'Mars Bound', 8);
INSERT INTO public.album (id, name, artist_id) VALUES (9, 'American Astronaut', 8);
INSERT INTO public.album (id, name, artist_id) VALUES (10, 'Wow, Meow!', 7);
INSERT INTO public.album (id, name, artist_id) VALUES (11, 'Le Chat Noir', 11);
INSERT INTO public.album (id, name, artist_id) VALUES (12, 'Pollinate This', 12);
INSERT INTO public.album (id, name, artist_id) VALUES (13, 'Spring 2020', 12);
INSERT INTO public.album (id, name, artist_id) VALUES (14, 'Corona', 1);


--
-- Name: album_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.album_id_seq', 14, true);


--
-- PostgreSQL database dump complete
--

