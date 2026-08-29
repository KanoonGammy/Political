from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class EntityType(str, Enum):
    PERSON = "PERSON"
    PARTY = "PARTY"
    INSTITUTION = "INSTITUTION"
    EVENT = "EVENT"
    POLICY = "POLICY"

class RelationType(str, Enum):
    ALLIANCE = "ALLIANCE"                 # Coalition, endorsement, cooperation
    OPPOSITION = "OPPOSITION"             # Opposition, rival, competing faction
    CRITICISM = "CRITICISM"               # Public rebuke, political attack, debate
    LEGAL_ACTION = "LEGAL_ACTION"         # Lawsuit, court petition, impeachment, dissolution probe
    MEMBER_OF = "MEMBER_OF"               # Party membership, cabinet post, affiliation
    POLICY_STANCE = "POLICY_STANCE"       # Policy sponsorship, opposition, proposal
    INVESTIGATION = "INVESTIGATION"       # NACC / ECT / Police / Court probe

class EntityNode(BaseModel):
    id: str
    name: str
    type: EntityType
    party: Optional[str] = None
    role: Optional[str] = None
    coalition: Optional[str] = None       # "Government", "Opposition", "Independent", "Judicial"
    aliases: List[str] = Field(default_factory=list)
    mention_count: int = 1
    wiki_link: Optional[str] = None
    image_url: Optional[str] = None
    party_logo_url: Optional[str] = None
    party_symbol: Optional[str] = None

class RelationEdge(BaseModel):
    id: str
    source: str                           # Node ID
    target: str                           # Node ID
    relation_type: RelationType
    description: str
    sentiment: float = 0.0                # -1.0 (hostile/conflict) to +1.0 (strong alliance/support)
    date: str                             # YYYY-MM-DD
    evidence: str
    source_url: str
    weight: int = 1

class PoliticalGraph(BaseModel):
    nodes: List[EntityNode] = Field(default_factory=list)
    edges: List[RelationEdge] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
