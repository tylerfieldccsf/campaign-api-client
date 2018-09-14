CREATE TABLE public.Filing_Activity
(
	Id UUID NOT NULL,
	Version INTEGER NOT NULL,
	Creation_Date TIMESTAMP WITH TIME ZONE,
  Last_Update TIMESTAMP WITH TIME ZONE,
  Activity_Type TEXT NOT NULL,
  Filing_Specification_Key TEXT NOT NULL,
  Origin TEXT NOT NULL,
  Origin_Filing_Id TEXT NOT NULL,
  Agency_Id TEXT,
  Apply_To_Filing_Id TEXT,
	Publish_Sequence BIGINT,
  CONSTRAINT Pk_Filing_Activity PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Filing_Activity OWNER TO postgres;
CREATE INDEX Idx_Filing_Activity_Filing_Sequence ON Filing_Activity(Publish_Sequence);
CREATE INDEX Idx_Filing_Activity_Origin ON Filing_Activity(Origin);
CREATE INDEX Idx_Filing_Activity_Filing_Specification_Key ON Filing_Activity(Filing_Specification_Key);
CREATE INDEX Idx_Filing_Activity_Activity_Type ON Filing_Activity(Activity_Type);

CREATE TABLE public.Filing_Element
(
	Id UUID NOT NULL,
	Creation_Date TIMESTAMP WITH TIME ZONE,
  Activity_Id UUID NOT NULL,
  Activity_Type TEXT NOT NULL,
  Element_Specification TEXT NOT NULL,
  Origin TEXT NOT NULL,
  Origin_Filing_Id TEXT NOT NULL,
  Agency_Id TEXT,
  Apply_To_Filing_Id TEXT,
  Publish_Sequence BIGINT,
  Element_Index TEXT NOT NULL,
  Model_Json jsonb,
  Filing_Specification TEXT,
  CONSTRAINT Pk_Filing_Element PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Filing_Element OWNER TO postgres;
CREATE INDEX Idx_Filing_Element_Activity_Id ON Filing_Element(Activity_Id);
CREATE INDEX Idx_Filing_Element_Element_Specification ON Filing_Element(Element_Specification);

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