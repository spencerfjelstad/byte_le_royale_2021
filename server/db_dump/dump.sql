--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

-- Started on 2021-10-27 17:34:25

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'WIN874';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 17325)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 3088 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- TOC entry 239 (class 1255 OID 17402)
-- Name: fetch_latest_clients(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.fetch_latest_clients() RETURNS TABLE(team_id uuid, submission_id integer, file_text character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Select latest code files. Because of the serial nature of submissionID, we can use max(subid) to 
-- find the latest submission.
RETURN QUERY
SELECT
    sub.team_id,
    sub.submission_id,
    code_file.file_text
from
    code_file
    JOIN (
        SELECT
            submission.team_id,
            MAX(submission.submission_id) as submission_id
        FROM
            submission
        GROUP BY
            submission.team_id
    ) as sub ON sub.submission_id = code_file.submission_id;
end;
$$;


ALTER FUNCTION public.fetch_latest_clients() OWNER TO postgres;

--
-- TOC entry 247 (class 1255 OID 17578)
-- Name: get_eligible_leaderboard(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_eligible_leaderboard() RETURNS TABLE(team_name character varying, uni_name character varying, submit_time timestamp without time zone, average_score numeric, standard_deviation numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Selects all teams
RETURN QUERY
SELECT
    team.team_name,
    university.uni_name,
    submission.submit_time,
    ROUND(AVG(run.score),3) as Average_Score,
	ROUND(stddev_pop(run.score),3) as Standard_Deviation
FROM
    run
    JOIN submission ON run.submission_id = submission.submission_id
    JOIN team on submission.team_id = team.team_id
	JOIN team_type on team.team_type_id = team_type.team_type_id
    JOIN university on team.uni_id = university.uni_id
WHERE
    run.group_run_id in (
        SELECT
            MAX(group_run.group_run_id)
        FROM
            group_run
    ) AND team_type.eligible
GROUP BY team.team_name, university.uni_name, submission.submit_time
ORDER BY Average_Score DESC;
end;
$$;


ALTER FUNCTION public.get_eligible_leaderboard() OWNER TO postgres;

--
-- TOC entry 248 (class 1255 OID 17579)
-- Name: get_entire_leaderboard(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_entire_leaderboard() RETURNS TABLE(team_name character varying, uni_name character varying, submit_time timestamp without time zone, average_score numeric, standard_deviation numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Selects all teams
RETURN QUERY
SELECT
    team.team_name,
    university.uni_name,
    submission.submit_time,
    ROUND(AVG(run.score),3) as Average_Score,
	ROUND(stddev_pop(run.score),3) as Standard_Deviation
FROM
    run
    JOIN submission ON run.submission_id = submission.submission_id
    JOIN team on submission.team_id = team.team_id
	JOIN team_type on team.team_type_id = team_type.team_type_id
    JOIN university on team.uni_id = university.uni_id
WHERE
    run.group_run_id in (
        SELECT
            MAX(group_run.group_run_id)
        FROM
            group_run
    )
GROUP BY team.team_name, university.uni_name, submission.submit_time
ORDER BY Average_Score DESC;
end;
$$;


ALTER FUNCTION public.get_entire_leaderboard() OWNER TO postgres;

--
-- TOC entry 245 (class 1255 OID 17565)
-- Name: get_latest_submission(uuid); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_latest_submission(teamid uuid) RETURNS TABLE(submission_id integer, group_run_id integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Select the latest submission_id and group_run_id for a team
RETURN QUERY
SELECT
    MAX(submission.submission_id),
	MAX(run.group_run_id)
FROM
    run
    JOIN submission ON run.submission_id = submission.submission_id
WHERE submission.team_id = teamid;
--SELECT * FROM team
end;
$$;


ALTER FUNCTION public.get_latest_submission(teamid uuid) OWNER TO postgres;

--
-- TOC entry 246 (class 1255 OID 17568)
-- Name: get_stats_for_submission(integer, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_stats_for_submission(submissionid integer, groupid integer) RETURNS TABLE(group_run_id integer, run_id integer, run_time timestamp without time zone, score integer)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Select the latest submission_id and group_run_id for a team
RETURN QUERY
SELECT run.group_run_id, run.run_id, run.run_time, run.score FROM run JOIN submission ON run.submission_id = submission.submission_id
WHERE run.submission_id = submissionid AND run.group_run_id = groupid;
--SELECT * FROM team
end;
$$;


ALTER FUNCTION public.get_stats_for_submission(submissionid integer, groupid integer) OWNER TO postgres;

--
-- TOC entry 249 (class 1255 OID 17591)
-- Name: get_team_score_over_time(uuid); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_team_score_over_time(teamid uuid) RETURNS TABLE(group_run_id integer, run_time timestamp without time zone, average_score numeric, standard_deviation numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Selects all teams
RETURN QUERY
SELECT
	run.group_run_id,
	group_run.start_run as run_time,
    ROUND(AVG(run.score),3) as Average_Score,
	ROUND(stddev_pop(run.score),3) as Standard_Deviation
FROM
    run
    JOIN submission ON run.submission_id = submission.submission_id
	JOIN group_run ON run.group_run_id = group_run.group_run_id
WHERE
	submission.team_id = teamId
GROUP BY run.group_run_id, group_run.start_run
ORDER BY group_run.start_run DESC;
end;
$$;


ALTER FUNCTION public.get_team_score_over_time(teamid uuid) OWNER TO postgres;

--
-- TOC entry 243 (class 1255 OID 17545)
-- Name: get_team_types(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_team_types() RETURNS TABLE(team_type_id integer, team_type_name character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Selects all team types
RETURN QUERY
SELECT team_type.team_type_id, team_type.team_type_name FROM team_type;
end;
$$;


ALTER FUNCTION public.get_team_types() OWNER TO postgres;

--
-- TOC entry 244 (class 1255 OID 17548)
-- Name: get_teams(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_teams() RETURNS TABLE(team_name character varying, uni_name character varying, team_type_name character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Selects all teams
RETURN QUERY
SELECT team.team_name, university.uni_name, team_type.team_type_name FROM team 
JOIN university ON team.uni_id = university.uni_id 
JOIN team_type ON team.team_type_id = team_type.team_type_id;
end;
$$;


ALTER FUNCTION public.get_teams() OWNER TO postgres;

--
-- TOC entry 242 (class 1255 OID 17543)
-- Name: get_universities(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.get_universities() RETURNS TABLE(uni_id integer, uni_name character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
-- Selects all universities
RETURN QUERY
SELECT university.uni_id, university.uni_name FROM university;
end;
$$;


ALTER FUNCTION public.get_universities() OWNER TO postgres;

--
-- TOC entry 237 (class 1255 OID 17398)
-- Name: insert_group_run(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_group_run() RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE rtnid integer;
BEGIN
-- Insert into group run. both id and timestamp are default, so no parameters
    INSERT INTO group_run DEFAULT VALUES RETURNING group_run_id INTO rtnid;
	return rtnid;
end;
$$;


ALTER FUNCTION public.insert_group_run() OWNER TO postgres;

--
-- TOC entry 240 (class 1255 OID 17541)
-- Name: insert_run(integer, integer, integer); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.insert_run(sub_id integer, score integer, group_run_id integer)
    LANGUAGE plpgsql
    AS $$
begin
    -- insert run into run table
	INSERT INTO run(submission_id, score, group_run_id) VALUES (sub_id, score, group_run_id);
end;
$$;


ALTER PROCEDURE public.insert_run(sub_id integer, score integer, group_run_id integer) OWNER TO postgres;

--
-- TOC entry 241 (class 1255 OID 17540)
-- Name: insert_run(integer, integer, integer, character varying); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.insert_run(sub_id integer, score integer, group_run_id integer, err character varying)
    LANGUAGE plpgsql
    AS $$
DECLARE runid int;
begin
    -- insert run into run table
	INSERT INTO run(submission_id, score, group_run_id) 
	VALUES (sub_id, score, group_run_id) RETURNING run_id INTO runid;
	
	if err <> '' then
		INSERT INTO errors VALUES (runid, err);
	end if;
end;
$$;


ALTER PROCEDURE public.insert_run(sub_id integer, score integer, group_run_id integer, err character varying) OWNER TO postgres;

--
-- TOC entry 236 (class 1255 OID 17403)
-- Name: insert_team(integer, character varying, integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insert_team(team_type integer, team character varying, uni integer) RETURNS uuid
    LANGUAGE plpgsql
    AS $$
DECLARE tmid uuid;
BEGIN
-- Insert into team
    INSERT INTO team (team_type_id, team_name, uni_id) VALUES (team_type, team, uni)  RETURNING team_id INTO tmid;
	return tmid;
end;
$$;


ALTER FUNCTION public.insert_team(team_type integer, team character varying, uni integer) OWNER TO postgres;

--
-- TOC entry 238 (class 1255 OID 17405)
-- Name: submit_code_file(character varying, uuid); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.submit_code_file(file character varying, vid uuid)
    LANGUAGE plpgsql
    AS $$
DECLARE sub_ID int = 0;
begin
    -- insert submission into submission table
	INSERT INTO SUBMISSION (team_id) VALUES (vid) RETURNING submission_id INTO sub_ID;
	
    -- insert file into file table
	INSERT INTO code_file(submission_id, file_text) VALUES (sub_id, file);
end;
$$;


ALTER PROCEDURE public.submit_code_file(file character varying, vid uuid) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 206 (class 1259 OID 17290)
-- Name: code_file; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.code_file (
    submission_id integer,
    file_text character varying
);


ALTER TABLE public.code_file OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 17524)
-- Name: errors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.errors (
    run_id integer,
    error_text character varying
);


ALTER TABLE public.errors OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 17381)
-- Name: group_run; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.group_run (
    group_run_id integer NOT NULL,
    start_run timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.group_run OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 17379)
-- Name: group_run_group_run_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.group_run_group_run_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.group_run_group_run_id_seq OWNER TO postgres;

--
-- TOC entry 3089 (class 0 OID 0)
-- Dependencies: 212
-- Name: group_run_group_run_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.group_run_group_run_id_seq OWNED BY public.group_run.group_run_id;


--
-- TOC entry 209 (class 1259 OID 17314)
-- Name: logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs (
    run_id integer,
    log_text character varying
);


ALTER TABLE public.logs OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 17303)
-- Name: run; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.run (
    submission_id integer,
    run_id integer NOT NULL,
    score integer,
    group_run_id integer,
    run_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.run OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 17301)
-- Name: run_runid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.run_runid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.run_runid_seq OWNER TO postgres;

--
-- TOC entry 3090 (class 0 OID 0)
-- Dependencies: 207
-- Name: run_runid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.run_runid_seq OWNED BY public.run.run_id;


--
-- TOC entry 205 (class 1259 OID 17277)
-- Name: submission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submission (
    team_id uuid,
    submission_id integer NOT NULL,
    valid boolean DEFAULT false NOT NULL,
    submit_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.submission OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 17275)
-- Name: submission_submissionid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.submission_submissionid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submission_submissionid_seq OWNER TO postgres;

--
-- TOC entry 3091 (class 0 OID 0)
-- Dependencies: 204
-- Name: submission_submissionid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.submission_submissionid_seq OWNED BY public.submission.submission_id;


--
-- TOC entry 203 (class 1259 OID 17263)
-- Name: team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team (
    team_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    uni_id integer,
    team_type_id integer,
    team_name character varying(100) NOT NULL,
    CONSTRAINT team_teamname_check CHECK (((team_name)::text <> ''::text))
);


ALTER TABLE public.team OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 17339)
-- Name: team_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.team_type (
    team_type_id integer NOT NULL,
    team_type_name character varying(100) NOT NULL,
    eligible boolean,
    CONSTRAINT teamtype_teamname_check CHECK (((team_type_name)::text <> ''::text))
);


ALTER TABLE public.team_type OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 17337)
-- Name: teamtype_teamtypeid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teamtype_teamtypeid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.teamtype_teamtypeid_seq OWNER TO postgres;

--
-- TOC entry 3092 (class 0 OID 0)
-- Dependencies: 210
-- Name: teamtype_teamtypeid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teamtype_teamtypeid_seq OWNED BY public.team_type.team_type_id;


--
-- TOC entry 202 (class 1259 OID 17256)
-- Name: university; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.university (
    uni_id integer NOT NULL,
    uni_name character varying(100) NOT NULL,
    CONSTRAINT university_uniname_check CHECK (((uni_name)::text <> ''::text))
);


ALTER TABLE public.university OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 17254)
-- Name: university_uniid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.university_uniid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.university_uniid_seq OWNER TO postgres;

--
-- TOC entry 3093 (class 0 OID 0)
-- Dependencies: 201
-- Name: university_uniid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.university_uniid_seq OWNED BY public.university.uni_id;


--
-- TOC entry 2929 (class 2604 OID 17384)
-- Name: group_run group_run_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_run ALTER COLUMN group_run_id SET DEFAULT nextval('public.group_run_group_run_id_seq'::regclass);


--
-- TOC entry 2925 (class 2604 OID 17306)
-- Name: run run_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run ALTER COLUMN run_id SET DEFAULT nextval('public.run_runid_seq'::regclass);


--
-- TOC entry 2922 (class 2604 OID 17280)
-- Name: submission submission_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission ALTER COLUMN submission_id SET DEFAULT nextval('public.submission_submissionid_seq'::regclass);


--
-- TOC entry 2927 (class 2604 OID 17342)
-- Name: team_type team_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_type ALTER COLUMN team_type_id SET DEFAULT nextval('public.teamtype_teamtypeid_seq'::regclass);


--
-- TOC entry 2918 (class 2604 OID 17259)
-- Name: university uni_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.university ALTER COLUMN uni_id SET DEFAULT nextval('public.university_uniid_seq'::regclass);


--
-- TOC entry 2944 (class 2606 OID 17387)
-- Name: group_run group_run_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_run
    ADD CONSTRAINT group_run_pkey PRIMARY KEY (group_run_id);


--
-- TOC entry 2940 (class 2606 OID 17308)
-- Name: run run_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_pkey PRIMARY KEY (run_id);


--
-- TOC entry 2938 (class 2606 OID 17284)
-- Name: submission submission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (submission_id);


--
-- TOC entry 2934 (class 2606 OID 17269)
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (team_id);


--
-- TOC entry 2936 (class 2606 OID 17353)
-- Name: team team_teamname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_teamname_key UNIQUE (team_name);


--
-- TOC entry 2942 (class 2606 OID 17345)
-- Name: team_type teamtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_type
    ADD CONSTRAINT teamtype_pkey PRIMARY KEY (team_type_id);


--
-- TOC entry 2932 (class 2606 OID 17262)
-- Name: university university_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.university
    ADD CONSTRAINT university_pkey PRIMARY KEY (uni_id);


--
-- TOC entry 2948 (class 2606 OID 17296)
-- Name: code_file codefile_submissionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.code_file
    ADD CONSTRAINT codefile_submissionid_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(submission_id);


--
-- TOC entry 2952 (class 2606 OID 17530)
-- Name: errors errors_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.errors
    ADD CONSTRAINT errors_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.run(run_id);


--
-- TOC entry 2951 (class 2606 OID 17320)
-- Name: logs logs_runid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_runid_fkey FOREIGN KEY (run_id) REFERENCES public.submission(submission_id);


--
-- TOC entry 2950 (class 2606 OID 17388)
-- Name: run run_group_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_group_run_id_fkey FOREIGN KEY (group_run_id) REFERENCES public.group_run(group_run_id);


--
-- TOC entry 2949 (class 2606 OID 17309)
-- Name: run run_submissionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_submissionid_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(submission_id);


--
-- TOC entry 2947 (class 2606 OID 17285)
-- Name: submission submission_teamid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_teamid_fkey FOREIGN KEY (team_id) REFERENCES public.team(team_id);


--
-- TOC entry 2946 (class 2606 OID 17346)
-- Name: team team_teamtypeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_teamtypeid_fkey FOREIGN KEY (team_type_id) REFERENCES public.team_type(team_type_id);


--
-- TOC entry 2945 (class 2606 OID 17270)
-- Name: team team_uniid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_uniid_fkey FOREIGN KEY (uni_id) REFERENCES public.university(uni_id);


-- Completed on 2021-10-27 17:34:26

--
-- PostgreSQL database dump complete
--

