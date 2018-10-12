CREATE TABLE public.Filing_Activity
(
	Filing_Activity_Nid UUID NOT NULL,
  Api_Version TEXT NOT NULL,
	Creation_Date TIMESTAMP WITH TIME ZONE,
  Last_Update TIMESTAMP WITH TIME ZONE,
  Activity_Type TEXT NOT NULL,
	Publish_Sequence BIGINT,
  Filing_Nid UUID NOT NULL,
  Root_Filing_Nid UUID NOT NULL,
  Legal_Origin TEXT NOT NULL,
  Legal_Filing_Id TEXT NOT NULL,
  Specification_Key TEXT NOT NULL,
  Form_Id Text,
  Legal_Filing_Date TIMESTAMP WITH TIME ZONE NOT NULL,
  Start_Date TIMESTAMP WITH TIME ZONE,
  End_Date TIMESTAMP WITH TIME ZONE,
  Report_Number TEXT,
  Apply_To_Filing_Id TEXT,
  String_Id TEXT,
  Common_Name TEXT,
  Systemized_Name TEXT,
  Status TEXT,
  Aid TEXT,
  Client_Dataspace_Id TEXT,
  Application_Dataspace_Id TEXT,
  CONSTRAINT Pk_Filing_Activity PRIMARY KEY (Filing_Activity_Nid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Filing_Activity OWNER TO postgres;
CREATE INDEX Idx_Filing_Activity_Filing_Sequence ON Filing_Activity(Publish_Sequence);
CREATE INDEX Idx_Filing_Activity_Legal_Origin ON Filing_Activity(Legal_Origin);
CREATE INDEX Idx_Filing_Activity_Filing_Specification_Key ON Filing_Activity(Specification_Key);
CREATE INDEX Idx_Filing_Activity_Activity_Type ON Filing_Activity(Activity_Type);

CREATE TABLE public.Element_Activity
(
	Element_Activity_Nid UUID NOT NULL,
  Api_Version TEXT NOT NULL,
	Creation_Date TIMESTAMP WITH TIME ZONE,
  Filing_Activity_Nid UUID NOT NULL,
  Activity_Type TEXT NOT NULL,
  Publish_Sequence BIGINT,
  Element_Nid UUID NOT NULL,
  Root_Element_Nid UUID NOT NULL,
  Filing_Nid UUID NOT NULL,
  Root_Filing_Nid UUID NOT NULL,
  Specification_Key TEXT NOT NULL,
  Element_Classification TEXT NOT NULL,
  Element_Type TEXT NOT NULL,
  Element_Index TEXT NOT NULL,
  Element_Model jsonb,
  CONSTRAINT Pk_Element_Activity PRIMARY KEY (Element_Activity_Nid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Element_Activity OWNER TO postgres;
CREATE INDEX Idx_Element_Activity_Activity_Id ON Element_Activity(Element_Activity_Nid);
CREATE INDEX Idx_Element_Activity_Element_Type ON Element_Activity(Element_Type);

CREATE TABLE public.Sync_Subscription
(
    Id UUID NOT NULL,
    Version INTEGER NOT NULL,
    Identity_Id UUID,
    Feed_Id UUID,
    Name TEXT,
    Auto_Complete boolean DEFAULT false ,
    status TEXT,
    CONSTRAINT Pk_Sync_Subscription PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Sync_Subscription OWNER TO postgres;