CREATE TABLE public.Audit_Trail
(
	Id UUID NOT NULL,
	Sequence_Id BIGSERIAL NOT NULL,
	Execution_Id TEXT NOT NULL,
	Date TIMESTAMP WITH TIME ZONE NOT NULL,
	Class_Name TEXT NOT NULL, -- the class/table name of the updated/created object
	User_Name TEXT,
	Email TEXT,
	Object_Id UUID NOT NULL, -- the Id value of the object
	After json NULL, --
	Identity_Id UUID NOT NULL, -- the identity that performed the action
	Action_Type TEXT not null default 'Insert',
  Instance_Version INTEGER not null default 0, -- the _resulting_ version value of the change
  CONSTRAINT PK_AuditTrail PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Audit_Trail
  OWNER TO postgres;
CREATE INDEX Idx_AuditTrail_ActionDate ON Audit_Trail(Date);
CREATE INDEX Idx_AuditTrail_ObjectId ON Audit_Trail(Object_Id);

CREATE TABLE public.Ifr_Activity
(
	Id UUID NOT NULL,
	Creation_Date TIMESTAMP WITH TIME ZONE,
  Activity_Type TEXT NOT NULL,
  Specification_Key TEXT NOT NULL,
  Origin TEXT NOT NULL,
  Origin_Filing_Id TEXT NOT NULL,
	Origin_Filing_Date TIMESTAMP WITH TIME ZONE NOT NULL,
  Agency_Id TEXT,
  Filer_Id TEXT,
  Filer_Name TEXT,
  Apply_To_Filing_Id TEXT,
  Body jsonb,
  CONSTRAINT Pk_Ifr_Activity PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Ifr_Activity OWNER TO postgres;
CREATE INDEX Idx_Ifr_Activity_Activity_Type ON Ifr_Activity(Activity_Type);
CREATE INDEX Idx_Ifr_Activity_Specification_Key ON Ifr_Activity(Specification_Key);
CREATE INDEX Idx_Ifr_Activity_Origin ON Ifr_Activity(Origin);
CREATE INDEX Idx_Ifr_Activity_Origin_Filing_Id ON Ifr_Activity(Origin_Filing_Id);
CREATE INDEX Idx_Ifr_Activity_Origin_Filing_Date ON Ifr_Activity(Origin_Filing_Date);
CREATE INDEX Idx_Ifr_Activity_Agency_Id ON Ifr_Activity(Agency_Id);
CREATE INDEX Idx_Ifr_Activity_Filer_Id ON Ifr_Activity(Filer_Id);
CREATE INDEX Idx_Ifr_Activity_Apply_To_Filing_Id ON Ifr_Activity(Apply_To_Filing_Id);

CREATE TABLE public.Flare_Activity
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
  CONSTRAINT Pk_Flare_Activity PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Flare_Activity OWNER TO postgres;
CREATE INDEX Idx_Flare_Activity_Filing_Sequence ON Flare_Activity(Publish_Sequence);
CREATE INDEX Idx_Flare_Activity_Origin ON Flare_Activity(Origin);
CREATE INDEX Idx_Flare_Activity_Filing_Specification_Key ON Flare_Activity(Filing_Specification_Key);
CREATE INDEX Idx_Flare_Activity_Activity_Type ON Flare_Activity(Activity_Type);

CREATE TABLE public.Flare_Element
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
  CONSTRAINT Pk_Flare_Element PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Flare_Element OWNER TO postgres;
CREATE INDEX Idx_Flare_Element_Activity_Id ON Flare_Element(Activity_Id);
CREATE INDEX Idx_Flare_Element_Element_Specification ON Flare_Element(Element_Specification);

CREATE TABLE public.Flare_Publish_Sequence
(
	Publish_Sequence BIGSERIAL NOT NULL,
	Creation_Date TIMESTAMP WITH TIME ZONE,
  Flare_Activity_Id UUID NOT NULL,
  CONSTRAINT Pk_Flare_Publish_Sequence PRIMARY KEY (Publish_Sequence)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Flare_Publish_Sequence OWNER TO postgres;
CREATE INDEX Idx_Flare_Publish_Sequence_Flare_Activity_Id ON Flare_Publish_Sequence(Flare_Activity_Id);