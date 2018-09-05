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

CREATE TABLE public.Immutable_Filing
(
	Id UUID NOT NULL,
	Version INTEGER NOT NULL,
	Filing_Sequence BIGSERIAL NOT NULL,
	Creation_Date TIMESTAMP WITH TIME ZONE,
  Last_Update TIMESTAMP WITH TIME ZONE,
  Origin TEXT NOT NULL,
  Origin_Filing_Id TEXT NOT NULL,
  Specification_Key TEXT NOT NULL,
  Body jsonb,
  CONSTRAINT PK_Immutable_Filing PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Immutable_Filing OWNER TO postgres;
CREATE INDEX Idx_Immutable_Filing_Sequence_Id ON Immutable_Filing(Filing_Sequence);
CREATE INDEX Idx_Immutable_Filing_Origin ON Immutable_Filing(Origin);
CREATE INDEX Idx_Immutable_Filing_Origin_Filing_Id ON Immutable_Filing(Origin);
CREATE INDEX Idx_Immutable_Filing_Specification_Key ON Immutable_Filing(Specification_Key);

CREATE TABLE public.Filing_Activity
(
	Id UUID NOT NULL,
	Version INTEGER NOT NULL,
	Filing_Sequence BIGSERIAL NOT NULL,
	Creation_Date TIMESTAMP WITH TIME ZONE,
  Last_Update TIMESTAMP WITH TIME ZONE,
  Origin TEXT NOT NULL,
  Origin_Filing_Id TEXT NOT NULL,
  Specification_Key TEXT NOT NULL,
  Activity_Type TEXT NOT NULL,
  Body jsonb,
  CONSTRAINT PK_Filing_Activity PRIMARY KEY (Id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.Filing_Activity OWNER TO postgres;
CREATE INDEX Idx_Filing_Activity_Filing_Sequence ON Filing_Activity(Filing_Sequence);
CREATE INDEX Idx_Filing_Activity_Origin ON Filing_Activity(Origin);
CREATE INDEX Idx_Filing_Activity_Origin_Filing_Id ON Filing_Activity(Origin);
CREATE INDEX Idx_Filing_Activity_Specification_Key ON Filing_Activity(Specification_Key);
CREATE INDEX Idx_Filing_Activity_Activity_Type ON Filing_Activity(Activity_Type);