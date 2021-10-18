--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

-- Started on 2021-10-18 10:30:42

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
-- TOC entry 2 (class 3079 OID 17325)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 3096 (class 0 OID 0)
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
	INSERT INTO SUBMISSION (team_id) VALUES (v_id) RETURNING submission_id INTO sub_ID;
	
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
-- TOC entry 3097 (class 0 OID 0)
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
    group_run_id integer
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
-- TOC entry 3098 (class 0 OID 0)
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
-- TOC entry 3099 (class 0 OID 0)
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
-- TOC entry 3100 (class 0 OID 0)
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
-- TOC entry 3101 (class 0 OID 0)
-- Dependencies: 201
-- Name: university_uniid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.university_uniid_seq OWNED BY public.university.uni_id;


--
-- TOC entry 2923 (class 2604 OID 17384)
-- Name: group_run group_run_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_run ALTER COLUMN group_run_id SET DEFAULT nextval('public.group_run_group_run_id_seq'::regclass);


--
-- TOC entry 2920 (class 2604 OID 17306)
-- Name: run run_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run ALTER COLUMN run_id SET DEFAULT nextval('public.run_runid_seq'::regclass);


--
-- TOC entry 2917 (class 2604 OID 17280)
-- Name: submission submission_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission ALTER COLUMN submission_id SET DEFAULT nextval('public.submission_submissionid_seq'::regclass);


--
-- TOC entry 2921 (class 2604 OID 17342)
-- Name: team_type team_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_type ALTER COLUMN team_type_id SET DEFAULT nextval('public.teamtype_teamtypeid_seq'::regclass);


--
-- TOC entry 2913 (class 2604 OID 17259)
-- Name: university uni_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.university ALTER COLUMN uni_id SET DEFAULT nextval('public.university_uniid_seq'::regclass);


--
-- TOC entry 3082 (class 0 OID 17290)
-- Dependencies: 206
-- Data for Name: code_file; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.code_file (submission_id, file_text) FROM stdin;
4	Wow what an awesome and large code file
5	from game.client.user_client import UserClient\nfrom game.common.enums import *\n\n\nclass Client(UserClient):\n    # Variables and info you want to save between turns go here\n    def __init__(self):\n        super().__init__()\n        self.turn = 0\n\n    def team_name(self):\n        """\n        Allows the team to set a team name.\n        :return: Your team name\n        """\n        return 'Team Name'\n\n    # This is where your AI will decide what to do\n    def take_turn(self, turn, actions, world, truck, time):\n        """\n        This is where your AI will decide what to do.\n        :param turn:        The current turn of the game.\n        :param actions:     This is the actions object that you will add effort allocations or decrees to.\n        :param world:       Generic world information\n        """\n        self.turn += 1\n\n        chosen_upgrade = self.select_upgrade(actions, truck)\n        # If there is not an active contract get one\n        if(truck.active_contract is None):\n            #print("Select")\n            chosen_contract = self.select_new_contract(actions, truck)\n            actions.set_action(ActionType.select_contract, chosen_contract)\n        # Buy gas if below 20% and there is enough money to fill tank to full at max gas price\n        elif (truck.speed != 100):\n            actions.set_action(ActionType.set_speed, 100)\n            print('speed')\n        elif(truck.body.current_gas < 1 and truck.money > 100*truck.active_contract.game_map.current_node.gas_price):\n            print("Gas")\n            actions.set_action(ActionType.buy_gas)\n        # If health is below max and have enough money to fully repair do so\n        elif truck.health < 100 and truck.money > 1000:\n            #print("Heal")\n            actions.set_action(ActionType.repair)\n        elif chosen_upgrade is not None:\n            #print("Upgrade")\n            actions.set_action(ActionType.upgrade, chosen_upgrade)\n        elif(truck.active_contract.game_map.current_node.next_node is not None):\n            # Move to next node\n            # Road can be selected by passing the index or road object\n            #print("Move")\n            road = self.select_new_route(actions, truck)\n            actions.set_action(ActionType.select_route, road)\n\n        if self.turn == 69 or self.turn == 420:\n            print("Funny Number! " + truck.__str__())\n        \n        pass\n\n    # These methods are not necessary, so feel free to modify or replace\n    def select_new_contract(self, actions, truck):\n        selected_contract = truck.contract_list[0]\n        for contract in truck.contract_list:\n            if contract.difficulty == ContractDifficulty.easy:\n                selected_contract = contract\n        return selected_contract\n\n    # Contract can be selected by passing the index or contract object\n    def select_upgrade(self, actions, truck):\n        target_body_upgrade = ObjectType.tank\n        target_addons_upgrade = ObjectType.rabbitFoot\n        if truck.body.level < 3 and truck.get_cost_of_upgrade(target_body_upgrade) < truck.money:\n            chosen_upgrade = target_body_upgrade\n        elif truck.addons.level < 3 and truck.get_cost_of_upgrade(target_addons_upgrade) < truck.money:\n            chosen_upgrade = target_addons_upgrade\n        else:\n            chosen_upgrade = None\n        return chosen_upgrade\n    \n    # Road can be selected by passing the index or road object\n    def select_new_route(self, actions, truck):\n        roads = truck.active_contract.game_map.current_node.roads\n        return roads[0]\n
6	from game.client.user_client import UserClient\nfrom game.common.enums import *\n\n\nclass Client(UserClient):\n    # Variables and info you want to save between turns go here\n    def __init__(self):\n        super().__init__()\n        self.turn = 0\n\n    def team_name(self):\n        """\n        Allows the team to set a team name.\n        :return: Your team name\n        """\n        return 'Team Name'\n\n    # This is where your AI will decide what to do\n    def take_turn(self, turn, actions, world, truck, time):\n        """\n        This is where your AI will decide what to do.\n        :param turn:        The current turn of the game.\n        :param actions:     This is the actions object that you will add effort allocations or decrees to.\n        :param world:       Generic world information\n        """\n        self.turn += 1\n\n        chosen_upgrade = self.select_upgrade(actions, truck)\n        # If there is not an active contract get one\n        if(truck.active_contract is None):\n            #print("Select")\n            chosen_contract = self.select_new_contract(actions, truck)\n            actions.set_action(ActionType.select_contract, chosen_contract)\n        # Buy gas if below 20% and there is enough money to fill tank to full at max gas price\n        elif (truck.speed != 100):\n            actions.set_action(ActionType.set_speed, 100)\n            print('speed')\n        elif(truck.body.current_gas < 1 and truck.money > 100*truck.active_contract.game_map.current_node.gas_price):\n            print("Gas")\n            actions.set_action(ActionType.buy_gas)\n        # If health is below max and have enough money to fully repair do so\n        elif truck.health < 100 and truck.money > 1000:\n            #print("Heal")\n            actions.set_action(ActionType.repair)\n        elif chosen_upgrade is not None:\n            #print("Upgrade")\n            actions.set_action(ActionType.upgrade, chosen_upgrade)\n        elif(truck.active_contract.game_map.current_node.next_node is not None):\n            # Move to next node\n            # Road can be selected by passing the index or road object\n            #print("Move")\n            road = self.select_new_route(actions, truck)\n            actions.set_action(ActionType.select_route, road)\n\n        if self.turn == 69 or self.turn == 420:\n            print("Funny Number! " + truck.__str__())\n        \n        pass\n\n    # These methods are not necessary, so feel free to modify or replace\n    def select_new_contract(self, actions, truck):\n        selected_contract = truck.contract_list[0]\n        for contract in truck.contract_list:\n            if contract.difficulty == ContractDifficulty.easy:\n                selected_contract = contract\n        return selected_contract\n\n    # Contract can be selected by passing the index or contract object\n    def select_upgrade(self, actions, truck):\n        target_body_upgrade = ObjectType.tank\n        target_addons_upgrade = ObjectType.rabbitFoot\n        if truck.body.level < 3 and truck.get_cost_of_upgrade(target_body_upgrade) < truck.money:\n            chosen_upgrade = target_body_upgrade\n        elif truck.addons.level < 3 and truck.get_cost_of_upgrade(target_addons_upgrade) < truck.money:\n            chosen_upgrade = target_addons_upgrade\n        else:\n            chosen_upgrade = None\n        return chosen_upgrade\n    \n    # Road can be selected by passing the index or road object\n    def select_new_route(self, actions, truck):\n        roads = truck.active_contract.game_map.current_node.roads\n        return roads[0]\n
7	from game.client.user_client import UserClient\nfrom game.common.enums import *\n\n\nclass Client(UserClient):\n    # Variables and info you want to save between turns go here\n    def __init__(self):\n        super().__init__()\n        self.turn = 0\n        self.queue = []\n        self.low = 800\n        self.high = 1500\n        self.low_speed = 100\n        self.high_speed = 100\n\n    def team_name(self):\n        """\n        Allows the team to set a team name.\n        :return: Your team name\n        """\n        return 'Team Name'\n\n    def getMPG(self, speed):\n        return (-0.002649444*(speed**2))+(.2520296*speed)+.22752\n\n    def calculateLength(self,map):\n        currNode = map.head\n        totLen = 0\n        while(currNode != None):\n            shortest = 10000\n            for x in currNode.roads:\n               shortest = min(shortest, x.length)\n            totLen += shortest\n            currNode = currNode.next_node\n        return totLen\n\n    def canIMakeIt(self, truck):\n        dist = self.chooseBestRoad(truck.active_contract.game_map.current_node.roads)\n        return True if (dist.length/self.getMPG(truck.speed))/(truck.body.max_gas*100) - (dist.length * 1.11) > 0 else False\n\n    def handleUpgrades(self, truck, bodyEnum, addonEnum):\n        if truck.body.level < truck.addons.level:\n            if truck.body.level < 3:\n                return bodyEnum\n        else:\n            if truck.addons.level < 3:\n                return addonEnum\n\n\n    def chooseBestContract(self, truck, contractList):\n        bestIndex = -1\n        prevBest = -1\n        score = 0\n        for index in range(len(contractList)):\n            if truck.money < 10000:\n                score = contractList[index].money_reward / self.calculateLength(contractList[index].game_map)\n            else:\n                score = contractList[index].renown_reward / self.calculateLength(contractList[index].game_map) \n            if score > prevBest:\n                prevBest = score\n                bestIndex = index\n        #print(bestIndex)\n        return bestIndex\n    \n    def chooseBestContract2(self, truck, contractList):\n        bestIndex = -1\n        if self.turn < 10:\n            bestIndex = 0\n        else:\n            bestIndex = 1\n        #print(bestIndex)\n        return bestIndex\n\n    def chooseBestContract2(self, truck, contractList):\n        bestIndex = -1\n        for index in range(len(contractList)):\n            if self.turn < self.low and contractList[index].difficulty == ContractDifficulty.easy:\n                bestIndex = index\n            elif self.turn < self.high and contractList[index].difficulty == ContractDifficulty.medium:\n                bestIndex = index\n            elif self.turn > self.high and contractList[index].difficulty == ContractDifficulty.hard:\n                bestIndex = index\n        #print(contractList[bestIndex]['contract'].difficulty == ContractDifficulty.easy)\n        return bestIndex\n    \n\n    def chooseBestContract2(self, truck, contractList):\n        bestIndex = -1\n        for index in range(len(contractList)):\n            if self.turn < self.low and contractList[index].difficulty == ContractDifficulty.easy:\n                bestIndex = index\n            elif self.turn < self.high and contractList[index].difficulty == ContractDifficulty.medium:\n                bestIndex = index\n            elif self.turn > self.high and contractList[index].difficulty == ContractDifficulty.hard:\n                bestIndex = index\n        #print(contractList[bestIndex]['contract'].difficulty == ContractDifficulty.easy)\n        return bestIndex\n\n    def chooseShortestRoad(self,roads):\n        shortest = 10000\n        index = roads[0]\n        for x in range(len(roads)):\n               if(shortest > roads[x].length and roads[x].road_type != RoadType.city_road):\n                   index = roads[x]\n        #print("move index: " + str(index))\n        return index\n\n    def chooseBestRoad(self,roads):\n        bestScore = -1\n        index = -1\n        for x in range(len(roads)):\n            score = roads[x].length\n            if roads[x].road_type is RoadType.city_road or RoadType.mountain_road:\n                score = (score * 1.4)  \n            if bestScore > score:\n                index = x \n        #print("move index: " + str(index))\n        return roads[index]\n\n    # This is where your AI will decide what to do\n    def take_turn(self, turn, actions, world, truck, time):\n        """\n        This is where your AI will decide what to do.\n        :param turn:        The current turn of the game.\n        :param actions:     This is the actions object that you will add effort allocations or decrees to.\n        :param world:       Generic world information\n        """\n        self.turn += 1\n        if(truck.active_contract is None):\n            # Select contractCont\n            ind = self.chooseBestContract2(truck, truck.contract_list)\n            actions.set_action(ActionType.select_contract, ind)\n            #print("Selecting index " + str(ind))\n        elif ActionType.set_speed not in self.queue and (truck.speed != self.low_speed and self.turn < self.high) or (truck.speed != self.high_speed and self.turn > self.high):\n            actions.set_action(ActionType.set_speed, self.low_speed) if self.turn < self.high else actions.set_action(ActionType.set_speed, self.high_speed)\n            print('speed')\n        elif ActionType.buy_gas not in self.queue and (( truck.active_contract.game_map.current_node.next_node is not None and truck.active_contract.game_map.current_node.gas_price > truck.active_contract.game_map.current_node.next_node.gas_price and self.canIMakeIt(truck)) or not self.canIMakeIt(truck)):\n                # Buy gas\n                #print("Gas")\n                actions.set_action(ActionType.buy_gas)\n        elif ActionType.repair != self.queue[0] and truck.health < 75:\n            actions.set_action(ActionType.repair)\n            #print("Heal")\n        elif ActionType.upgrade not in self.queue and truck.money > 1000 and (truck.tires != TireType.tire_normal and self.turn < self.high) or (truck.tires != TireType.monster_truck and self.turn > self.high):\n            actions.set_action(ObjectType.tires, TireType.tire_normal) if self.turn < self.high else actions.set_action(ObjectType.tires, TireType.monster_truck)\n        elif  (truck.body.level < 3 and (10000 * 1.2 * (truck.body.level + 1)) < truck.money) and ActionType.upgrade not in self.queue:\n            #print("upgrade")\n            actions.set_action(ActionType.upgrade, self.handleUpgrades(truck, ObjectType.tank, ObjectType.GPS))\n        else:\n            # Move to next node\n            #print("move")\n            actions.set_action(ActionType.select_route, self.chooseBestRoad(truck.active_contract.game_map.current_node.roads))\n        if len(self.queue) > 2:\n            self.queue.pop(-1)\n        self.queue.insert(0, actions._chosen_action)\n             \n        pass\n\n\n\n\n\n\n
8	from game.client.user_client import UserClient\nfrom game.common.enums import *\n\n\nclass Client(UserClient):\n    # Variables and info you want to save between turns go here\n    def __init__(self):\n        super().__init__()\n        self.turn = 0\n\n    def team_name(self):\n        """\n        Allows the team to set a team name.\n        :return: Your team name\n        """\n        return 'Team Name'\n\n    # This is where your AI will decide what to do\n    def take_turn(self, turn, actions, world, truck, time):\n        """\n        This is where your AI will decide what to do.\n        :param turn:        The current turn of the game.\n        :param actions:     This is the actions object that you will add effort allocations or decrees to.\n        :param world:       Generic world information\n        """\n        self.turn += 1\n\n        chosen_upgrade = self.select_upgrade(actions, truck)\n        # If there is not an active contract get one\n        if(truck.active_contract is None):\n            #print("Select")\n            chosen_contract = self.select_new_contract(actions, truck)\n            actions.set_action(ActionType.select_contract, chosen_contract)\n        # Buy gas if below 20% and there is enough money to fill tank to full at max gas price\n        elif(truck.body.current_gas < .20 and truck.money > 100*truck.active_contract.game_map.current_node.gas_price):\n            #print("Gas")\n            actions.set_action(ActionType.buy_gas)\n        # If health is below max and have enough money to fully repair do so\n        elif truck.health < 100 and truck.money > 1000:\n            #print("Heal")\n            actions.set_action(ActionType.repair)\n        elif chosen_upgrade is not None:\n            #print("Upgrade")\n            actions.set_action(ActionType.upgrade, chosen_upgrade)\n        elif(truck.active_contract.game_map.current_node.next_node is not None):\n            # Move to next node\n            # Road can be selected by passing the index or road object\n            #print("Move")\n            road = self.select_new_route(actions, truck)\n            actions.set_action(ActionType.select_route, road)\n\n        if self.turn == 69 or self.turn == 420:\n            print("Funny Number!")\n        \n        pass\n\n    # These methods are not necessary, so feel free to modify or replace\n    def select_new_contract(self, actions, truck):\n        selected_contract = truck.contract_list[0]\n        for contract in truck.contract_list:\n            if contract.difficulty == ContractDifficulty.easy:\n                selected_contract = contract\n        return selected_contract\n\n    # Contract can be selected by passing the index or contract object\n    def select_upgrade(self, actions, truck):\n        target_body_upgrade = ObjectType.tank\n        target_addons_upgrade = ObjectType.rabbitFoot\n        if truck.body.level < 3 and truck.get_cost_of_upgrade(target_body_upgrade) < truck.money:\n            chosen_upgrade = target_body_upgrade\n        elif truck.addons.level < 3 and truck.get_cost_of_upgrade(target_addons_upgrade) < truck.money:\n            chosen_upgrade = target_addons_upgrade\n        else:\n            chosen_upgrade = None\n        return chosen_upgrade\n    \n    # Road can be selected by passing the index or road object\n    def select_new_route(self, actions, truck):\n        roads = truck.active_contract.game_map.current_node.roads\n        return roads[0]\n
\.


--
-- TOC entry 3090 (class 0 OID 17524)
-- Dependencies: 214
-- Data for Name: errors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.errors (run_id, error_text) FROM stdin;
\.


--
-- TOC entry 3089 (class 0 OID 17381)
-- Dependencies: 213
-- Data for Name: group_run; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.group_run (group_run_id, start_run) FROM stdin;
13	2021-10-16 22:25:34.366244
14	2021-10-16 22:26:03.308529
15	2021-10-16 22:26:19.242999
16	2021-10-16 22:27:22.186907
17	2021-10-16 22:28:53.416485
18	2021-10-16 22:29:49.331011
19	2021-10-16 22:30:05.589721
20	2021-10-16 22:31:25.007863
21	2021-10-16 22:31:49.448154
22	2021-10-16 22:32:25.406779
23	2021-10-16 22:33:22.449278
24	2021-10-16 22:34:42.668431
25	2021-10-16 22:35:17.42183
26	2021-10-17 17:17:02.037264
27	2021-10-17 17:20:23.412447
28	2021-10-17 17:21:06.02744
29	2021-10-17 17:21:17.525289
30	2021-10-17 17:22:05.444534
31	2021-10-17 17:29:53.560351
32	2021-10-17 17:32:25.527278
33	2021-10-17 17:41:58.922025
34	2021-10-17 17:48:43.442115
35	2021-10-17 17:48:56.11967
36	2021-10-17 17:50:37.346587
37	2021-10-17 17:52:40.78962
38	2021-10-17 17:53:40.985377
39	2021-10-17 17:54:36.430039
40	2021-10-17 17:58:09.323835
41	2021-10-17 17:58:29.93884
42	2021-10-17 17:59:22.94764
43	2021-10-17 18:00:05.720334
44	2021-10-17 18:00:44.161125
45	2021-10-17 18:03:09.124433
46	2021-10-17 18:04:09.594017
47	2021-10-17 18:05:17.536257
48	2021-10-17 18:05:50.249955
49	2021-10-17 18:08:58.595352
50	2021-10-17 18:10:27.284389
51	2021-10-17 18:11:15.230096
52	2021-10-17 18:11:41.269721
53	2021-10-17 18:15:39.217131
54	2021-10-17 20:15:57.057842
55	2021-10-17 20:16:18.763087
56	2021-10-17 20:16:39.840657
57	2021-10-17 20:17:38.090281
58	2021-10-17 20:18:18.158171
59	2021-10-17 20:19:08.044993
60	2021-10-17 20:20:47.724226
61	2021-10-17 20:21:10.567139
62	2021-10-17 20:21:37.763148
63	2021-10-17 20:21:59.888558
64	2021-10-17 20:25:21.941708
\.


--
-- TOC entry 3085 (class 0 OID 17314)
-- Dependencies: 209
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs (run_id, log_text) FROM stdin;
\.


--
-- TOC entry 3084 (class 0 OID 17303)
-- Dependencies: 208
-- Data for Name: run; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.run (submission_id, run_id, score, group_run_id) FROM stdin;
4	1	0	29
4	2	0	30
6	3	0	30
4	4	0	31
6	5	0	31
4	6	0	32
6	7	0	32
4	8	0	33
6	9	0	33
7	10	0	33
4	11	0	34
4	12	0	35
6	13	0	35
7	14	0	35
4	15	0	36
6	16	0	36
7	17	0	36
4	18	0	37
6	19	0	37
7	20	0	37
4	21	0	38
6	22	0	38
7	23	0	38
4	24	0	39
6	25	0	39
7	26	0	39
4	27	0	40
4	28	0	41
6	29	0	41
7	30	0	41
4	31	0	42
6	32	0	42
7	33	0	42
4	34	0	43
6	35	0	43
7	36	0	43
4	37	0	44
6	38	0	44
7	39	0	44
4	40	0	45
6	41	0	45
7	42	0	45
4	43	0	46
6	44	0	46
7	45	0	46
4	46	0	47
6	47	0	47
7	48	0	47
4	49	0	48
6	50	0	48
7	51	0	48
4	52	0	49
6	53	0	49
7	54	0	49
4	55	0	52
6	56	0	52
7	57	0	52
4	58	0	52
6	59	0	52
7	60	0	52
4	61	0	52
6	62	0	52
7	63	0	52
4	64	0	52
6	65	0	52
7	66	0	52
4	67	0	52
6	68	0	52
7	69	0	52
4	70	0	53
6	71	0	53
8	72	40	53
4	73	0	53
6	74	0	53
8	75	30	53
4	76	0	53
6	77	0	53
8	78	36	53
4	79	0	53
6	80	0	53
8	81	112	53
4	82	0	53
6	83	0	53
8	84	30	53
4	85	0	60
4	86	0	61
4	87	0	62
4	88	0	63
6	89	0	63
8	90	356	63
4	91	0	63
6	92	0	63
8	93	878	63
4	94	0	63
6	95	0	63
8	96	30	63
4	97	0	63
6	98	0	63
8	99	0	63
4	100	0	63
6	101	0	63
8	102	16	63
4	103	0	64
6	104	0	64
8	105	60	64
\.


--
-- TOC entry 3081 (class 0 OID 17277)
-- Dependencies: 205
-- Data for Name: submission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.submission (team_id, submission_id, valid, submit_time) FROM stdin;
9f50ba24-5f23-47ad-850d-b9e85fca1a98	4	f	2021-10-12 14:57:55.42256
70fa0d49-fea3-409d-8c25-cde394621c1b	5	f	2021-10-12 18:28:57.325778
70fa0d49-fea3-409d-8c25-cde394621c1b	6	f	2021-10-16 16:58:00.632921
69b5d2a3-a383-48b1-a27c-a82e75429595	7	f	2021-10-17 17:41:33.735318
69b5d2a3-a383-48b1-a27c-a82e75429595	8	f	2021-10-17 18:15:26.884064
\.


--
-- TOC entry 3079 (class 0 OID 17263)
-- Dependencies: 203
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.team (team_id, uni_id, team_type_id, team_name) FROM stdin;
9f50ba24-5f23-47ad-850d-b9e85fca1a98	1	1	seeeeeeeean
1d800cd0-2608-42d3-9702-ba64b8338c27	1	1	mitchell
70fa0d49-fea3-409d-8c25-cde394621c1b	1	1	l
69b5d2a3-a383-48b1-a27c-a82e75429595	2	2	test_team
5436ccb7-ebf4-491a-b0ba-8e649f3a7a7b	1	2	seantest
dac0c008-082b-42d9-a35d-65598efe9b53	3	2	pp
\.


--
-- TOC entry 3087 (class 0 OID 17339)
-- Dependencies: 211
-- Data for Name: team_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.team_type (team_type_id, team_type_name) FROM stdin;
1	Graduate
2	Under Graduate
3	Alumni
\.


--
-- TOC entry 3078 (class 0 OID 17256)
-- Dependencies: 202
-- Data for Name: university; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.university (uni_id, uni_name) FROM stdin;
1	NDSU
2	UND
3	MSUM
\.


--
-- TOC entry 3102 (class 0 OID 0)
-- Dependencies: 212
-- Name: group_run_group_run_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.group_run_group_run_id_seq', 64, true);


--
-- TOC entry 3103 (class 0 OID 0)
-- Dependencies: 207
-- Name: run_runid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.run_runid_seq', 105, true);


--
-- TOC entry 3104 (class 0 OID 0)
-- Dependencies: 204
-- Name: submission_submissionid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.submission_submissionid_seq', 8, true);


--
-- TOC entry 3105 (class 0 OID 0)
-- Dependencies: 210
-- Name: teamtype_teamtypeid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teamtype_teamtypeid_seq', 3, true);


--
-- TOC entry 3106 (class 0 OID 0)
-- Dependencies: 201
-- Name: university_uniid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.university_uniid_seq', 3, true);


--
-- TOC entry 2938 (class 2606 OID 17387)
-- Name: group_run group_run_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_run
    ADD CONSTRAINT group_run_pkey PRIMARY KEY (group_run_id);


--
-- TOC entry 2934 (class 2606 OID 17308)
-- Name: run run_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_pkey PRIMARY KEY (run_id);


--
-- TOC entry 2932 (class 2606 OID 17284)
-- Name: submission submission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (submission_id);


--
-- TOC entry 2928 (class 2606 OID 17269)
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (team_id);


--
-- TOC entry 2930 (class 2606 OID 17353)
-- Name: team team_teamname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_teamname_key UNIQUE (team_name);


--
-- TOC entry 2936 (class 2606 OID 17345)
-- Name: team_type teamtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team_type
    ADD CONSTRAINT teamtype_pkey PRIMARY KEY (team_type_id);


--
-- TOC entry 2926 (class 2606 OID 17262)
-- Name: university university_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.university
    ADD CONSTRAINT university_pkey PRIMARY KEY (uni_id);


--
-- TOC entry 2942 (class 2606 OID 17296)
-- Name: code_file codefile_submissionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.code_file
    ADD CONSTRAINT codefile_submissionid_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(submission_id);


--
-- TOC entry 2946 (class 2606 OID 17530)
-- Name: errors errors_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.errors
    ADD CONSTRAINT errors_run_id_fkey FOREIGN KEY (run_id) REFERENCES public.run(run_id);


--
-- TOC entry 2945 (class 2606 OID 17320)
-- Name: logs logs_runid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_runid_fkey FOREIGN KEY (run_id) REFERENCES public.submission(submission_id);


--
-- TOC entry 2944 (class 2606 OID 17388)
-- Name: run run_group_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_group_run_id_fkey FOREIGN KEY (group_run_id) REFERENCES public.group_run(group_run_id);


--
-- TOC entry 2943 (class 2606 OID 17309)
-- Name: run run_submissionid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.run
    ADD CONSTRAINT run_submissionid_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(submission_id);


--
-- TOC entry 2941 (class 2606 OID 17285)
-- Name: submission submission_teamid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_teamid_fkey FOREIGN KEY (team_id) REFERENCES public.team(team_id);


--
-- TOC entry 2940 (class 2606 OID 17346)
-- Name: team team_teamtypeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_teamtypeid_fkey FOREIGN KEY (team_type_id) REFERENCES public.team_type(team_type_id);


--
-- TOC entry 2939 (class 2606 OID 17270)
-- Name: team team_uniid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_uniid_fkey FOREIGN KEY (uni_id) REFERENCES public.university(uni_id);


-- Completed on 2021-10-18 10:30:43

--
-- PostgreSQL database dump complete
--

