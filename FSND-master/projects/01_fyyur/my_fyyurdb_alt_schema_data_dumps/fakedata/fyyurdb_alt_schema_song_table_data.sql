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
-- Data for Name: song; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.song (id, name, album_id) VALUES (1, 'Corona', 14);
INSERT INTO public.song (id, name, album_id) VALUES (2, 'Dark and Cloudy', 14);
INSERT INTO public.song (id, name, album_id) VALUES (3, 'Recluse', 14);
INSERT INTO public.song (id, name, album_id) VALUES (4, 'End Times', 14);
INSERT INTO public.song (id, name, album_id) VALUES (5, 'Flowers in the Wind', 13);
INSERT INTO public.song (id, name, album_id) VALUES (6, 'Buzz Kill', 13);
INSERT INTO public.song (id, name, album_id) VALUES (7, 'Yellow Sunflowers', 13);
INSERT INTO public.song (id, name, album_id) VALUES (8, 'Dusted', 12);
INSERT INTO public.song (id, name, album_id) VALUES (9, 'Queen Bee', 12);
INSERT INTO public.song (id, name, album_id) VALUES (10, 'Cheese Plz', 11);
INSERT INTO public.song (id, name, album_id) VALUES (11, 'Scaredy Cats', 11);
INSERT INTO public.song (id, name, album_id) VALUES (12, 'Sqeeeeek!', 11);
INSERT INTO public.song (id, name, album_id) VALUES (13, 'Purrrrrfect', 10);
INSERT INTO public.song (id, name, album_id) VALUES (14, 'Sleeping in', 10);
INSERT INTO public.song (id, name, album_id) VALUES (15, 'My life as a dog', 10);
INSERT INTO public.song (id, name, album_id) VALUES (16, 'Space is Cold', 9);
INSERT INTO public.song (id, name, album_id) VALUES (17, 'Floating', 9);
INSERT INTO public.song (id, name, album_id) VALUES (18, 'alone', 9);
INSERT INTO public.song (id, name, album_id) VALUES (19, 'Earth, abandoned', 9);
INSERT INTO public.song (id, name, album_id) VALUES (20, 'Red', 8);
INSERT INTO public.song (id, name, album_id) VALUES (21, '3..2..1..', 8);
INSERT INTO public.song (id, name, album_id) VALUES (22, 'Not Earth', 8);
INSERT INTO public.song (id, name, album_id) VALUES (23, 'Static', 8);
INSERT INTO public.song (id, name, album_id) VALUES (24, 'Lost in Space', 7);
INSERT INTO public.song (id, name, album_id) VALUES (25, 'Beyond the Universe', 7);
INSERT INTO public.song (id, name, album_id) VALUES (26, 'TV the last stand', 6);
INSERT INTO public.song (id, name, album_id) VALUES (27, 'N* drain', 6);
INSERT INTO public.song (id, name, album_id) VALUES (28, 'Honey glazed', 4);
INSERT INTO public.song (id, name, album_id) VALUES (29, 'Sprinkles', 4);
INSERT INTO public.song (id, name, album_id) VALUES (30, 'One more cup', 3);
INSERT INTO public.song (id, name, album_id) VALUES (31, 'Sugar buzz', 3);
INSERT INTO public.song (id, name, album_id) VALUES (33, 'Why dogs are cool', 2);
INSERT INTO public.song (id, name, album_id) VALUES (34, 'Dogs are better than cats', 2);
INSERT INTO public.song (id, name, album_id) VALUES (35, 'Leashed', 2);
INSERT INTO public.song (id, name, album_id) VALUES (36, 'Unleashed', 2);


--
-- Name: song_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.song_id_seq', 36, true);


--
-- PostgreSQL database dump complete
--

